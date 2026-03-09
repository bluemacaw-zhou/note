import os
import requests
import base64
import subprocess
import json
import re
import urllib3
from pathlib import Path

# 禁用安全请求警告（因为在公司代理环境下使用了 verify=False）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- 配置区 ---
PROXY = "http://10.200.86.85:8080"
VERIFY_SSL = False  # 公司环境通常需要关闭

# 从环境变量获取 Token
TOKEN = os.getenv("GITHUB_TOKEN")

def get_github_remote_info():
    """自动寻找指向 github.com 的 Remote 配置 (支持 HTTPS 和 SSH)"""
    try:
        output = subprocess.check_output(["git", "remote", "-v"], text=True).strip()
        lines = output.splitlines()
        
        for line in lines:
            parts = line.split()
            if len(parts) < 2: continue
            
            remote_name, url = parts[0], parts[1]
            
            # 正则解释:
            # github\.com          匹配域名
            # [:/]                 匹配 SSH 的冒号或 HTTPS 的斜杠
            # ([^/]+)              匹配 owner (直到下一个斜杠)
            # /                    匹配分隔斜杠
            # ([^/.]+?)            匹配 repo (直到点或斜杠)
            # (?:\.git)?           可选的 .git 后缀
            # (?:$|/|\s)           结尾或是斜杠/空格
            match = re.search(r"github\.com[:/]([^/]+)/([^/.]+?)(?:\.git)?(?:$|/|\s)", url)
            
            if match:
                owner = match.group(1)
                repo = match.group(2)
                return remote_name, owner, repo
                
    except Exception as e:
        print(f"探测 GitHub Remote 失败: {e}")
    return None, None, None

def get_remote_branch_name(session, remote_name, owner, repo):
    """获取远端默认分支名"""
    try:
        head = subprocess.check_output(
            ["git", "symbolic-ref", f"refs/remotes/{remote_name}/HEAD"], 
            text=True, stderr=subprocess.DEVNULL
        ).strip()
        return head.split("/")[-1]
    except:
        pass

    try:
        url = f"https://api.github.com/repos/{owner}/{repo}"
        resp = session.get(url)
        resp.raise_for_status()
        return resp.json().get("default_branch", "master")
    except:
        return "master"

def get_git_changes(remote_name, remote_branch):
    """获取本地相对于远端追踪分支的差异"""
    try:
        output = subprocess.check_output(
            ["git", "diff", f"{remote_name}/{remote_branch}", "--name-status"], 
            text=True
        ).splitlines()
        
        untracked = subprocess.check_output(
            ["git", "ls-files", "--others", "--exclude-standard"],
            text=True
        ).splitlines()
        
        change_map = {}
        for line in output:
            parts = line.split(None, 1)
            if len(parts) < 2: continue
            status, path = parts
            # 状态码处理 (M: 修改, A: 新增, R: 重命名)
            st_text = "Modified" if status.startswith('M') else "Added"
            change_map[path.strip()] = st_text
        
        for path in untracked:
            p = path.strip()
            if p != "sync_to_github.py":
                change_map[p] = "Untracked (New)"
                
        return change_map
    except Exception as e:
        print(f"获取 Git 差异失败: {e}")
        return {}

def upload_blob(session, owner, repo, file_path):
    """通过 API 上传文件"""
    try:
        with open(file_path, "rb") as f:
            content = f.read()
        b64_content = base64.b64encode(content).decode("utf-8")
        url = f"https://api.github.com/repos/{owner}/{repo}/git/blobs"
        resp = session.post(url, json={"content": b64_content, "encoding": "base64"})
        resp.raise_for_status()
        return resp.json()["sha"]
    except Exception as e:
        print(f"上传 {file_path} 失败: {e}")
        return None

def main():
    if not TOKEN:
        print("❌ 错误: 未检测到环境变量 GITHUB_TOKEN")
        return

    session = requests.Session()
    if PROXY:
        session.proxies = {"http": PROXY, "https": PROXY}
    session.verify = VERIFY_SSL
    session.headers.update({
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    })

    # 1. 自动探测 (支持 SSH/HTTPS)
    remote_name, owner, repo = get_github_remote_info()
    if not remote_name:
        print("❌ 错误: 未能在本地配置中识别到 GitHub 仓库地址。")
        return

    target_branch = get_remote_branch_name(session, remote_name, owner, repo)
    curr_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()

    print(f"✅ 已匹配 GitHub: '{remote_name}' -> {owner}/{repo}")
    print(f"🔍 比对范围: 本地工作区({curr_branch}) vs 远端({remote_name}/{target_branch})")
    
    # --- 第一阶段: 扫描 ---
    changes = get_git_changes(remote_name, target_branch)
    if not changes:
        print("✅ 没有检测到任何需要同步的改动。")
        return

    print("\n--- 待同步文件 ---")
    for path, status in changes.items():
        print(f"[{status}] {path}")

    # --- 交互 ---
    confirm = input(f"\n❓ 确认通过 API 同步到 GitHub 的 {target_branch} 分支? (y/n): ").lower()
    if confirm != 'y': return

    # --- 第二阶段: 提交 ---
    try:
        # 获取基准 SHA
        ref_data = session.get(f"https://api.github.com/repos/{owner}/{repo}/git/refs/heads/{target_branch}").json()
        last_commit_sha = ref_data["object"]["sha"]
        base_tree_sha = session.get(f"https://api.github.com/repos/{owner}/{repo}/git/commits/{last_commit_sha}").json()["tree"]["sha"]

        # 上传文件
        tree_items = []
        for f_path in changes.keys():
            if not os.path.isfile(f_path): continue
            print(f"正在上传: {f_path} ...", end="\r")
            sha = upload_blob(session, owner, repo, f_path)
            if sha:
                tree_items.append({"path": f_path.replace("\\", "/"), "mode": "100644", "type": "blob", "sha": sha})
        
        # 创建 Tree/Commit
        new_tree_sha = session.post(f"https://api.github.com/repos/{owner}/{repo}/git/trees", 
                                   json={"base_tree": base_tree_sha, "tree": tree_items}).json()["sha"]
        
        new_commit_sha = session.post(f"https://api.github.com/repos/{owner}/{repo}/git/commits", 
                                     json={"message": "Sync via Gemini API tool", "tree": new_tree_sha, "parents": [last_commit_sha]}).json()["sha"]

        # 更新分支 (Push)
        resp = session.patch(f"https://api.github.com/repos/{owner}/{repo}/git/refs/heads/{target_branch}", json={"sha": new_commit_sha})
        
        if resp.status_code == 200:
            print(f"\n✨ 同步成功！Commit: {new_commit_sha[:7]}")
        else:
            print(f"\n❌ 更新失败: {resp.text}")

    except Exception as e:
        print(f"\n💥 错误: {e}")

if __name__ == "__main__":
    main()
