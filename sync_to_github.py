import os
import requests
import base64
import subprocess
import json
import re
import urllib3
from datetime import datetime
from pathlib import Path

# 禁用安全请求警告（因为在公司代理环境下使用了 verify=False）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- 配置区 ---
PROXY = "http://10.200.86.85:8080"
VERIFY_SSL = False  # 公司环境通常需要关闭

# 从环境变量获取 Token
TOKEN = os.getenv("GITHUB_TOKEN")

def run_git_command(args):
    """封装 git 命令调用，强制使用 UTF-8 解码并处理 core.quotepath"""
    # 加入 -c core.quotepath=false 确保中文不被转义
    cmd = ["git", "-c", "core.quotepath=false"] + args
    try:
        # 显式指定 encoding='utf-8' 解决 Windows GBK 报错
        return subprocess.check_output(cmd, text=True, encoding='utf-8').strip()
    except UnicodeDecodeError:
        # 如果 utf-8 失败，尝试 gbk (极端情况兼容)
        return subprocess.check_output(cmd, text=True, encoding='gbk').strip()

def get_github_remote_info():
    """自动寻找指向 github.com 的 Remote 配置 (支持 HTTPS 和 SSH)"""
    try:
        output = run_git_command(["remote", "-v"])
        lines = output.splitlines()
        
        for line in lines:
            parts = line.split()
            if len(parts) < 2: continue
            remote_name, url = parts[0], parts[1]
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
        head = run_git_command(["symbolic-ref", f"refs/remotes/{remote_name}/HEAD"])
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
    """获取本地相对于远端追踪分支的差异 (支持中文路径)"""
    try:
        # 1. 检查已跟踪文件的差异
        output = run_git_command(["diff", f"{remote_name}/{remote_branch}", "--name-status"])
        output_lines = output.splitlines() if output else []
        
        # 2. 检查未跟踪的文件
        untracked = run_git_command(["ls-files", "--others", "--exclude-standard"])
        untracked_lines = untracked.splitlines() if untracked else []
        
        change_map = {}
        for line in output_lines:
            parts = line.split(None, 1)
            if len(parts) < 2: continue
            status, path = parts
            st_text = "Modified" if status.startswith('M') else "Added"
            change_map[path.strip()] = st_text
        
        for path in untracked_lines:
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

    # 1. 自动探测
    remote_name, owner, repo = get_github_remote_info()
    if not remote_name:
        print("❌ 错误: 未能在本地配置中识别到 GitHub 仓库地址。")
        return

    target_branch = get_remote_branch_name(session, remote_name, owner, repo)
    curr_branch = run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])

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

    # --- 提交日志编写 ---
    default_msg = f"Sync from local - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    print(f"\n💬 请输入提交日志 (直接回车将使用默认: '{default_msg}'):")
    user_msg = input("> ").strip()
    commit_msg = user_msg if user_msg else default_msg

    # --- 交互确认 ---
    confirm = input(f"\n❓ 确认以该日志同步到 GitHub 的 {target_branch} 分支? (y/n): ").lower()
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
            if not os.path.isfile(f_path): 
                print(f"⚠️ 跳过无效文件: {f_path}")
                continue
            
            print(f"正在上传: {f_path} ...")
            sha = upload_blob(session, owner, repo, f_path)
            if sha:
                tree_items.append({"path": f_path.replace("\\", "/"), "mode": "100644", "type": "blob", "sha": sha})
        
        if not tree_items:
            print("❌ 没有成功上传任何文件，退出。")
            return

        print("\n✅ 文件上传完成。正在创建提交...")
        new_tree_sha = session.post(f"https://api.github.com/repos/{owner}/{repo}/git/trees", 
                                   json={"base_tree": base_tree_sha, "tree": tree_items}).json()["sha"]
        
        new_commit_sha = session.post(f"https://api.github.com/repos/{owner}/{repo}/git/commits", 
                                     json={"message": commit_msg, "tree": new_tree_sha, "parents": [last_commit_sha]}).json()["sha"]

        # 更新远端分支 (Push)
        resp = session.patch(f"https://api.github.com/repos/{owner}/{repo}/git/refs/heads/{target_branch}", json={"sha": new_commit_sha})
        
        if resp.status_code == 200:
            print(f"\n✨ 同步成功！远程 Commit: {new_commit_sha[:7]}")
            
            # --- 第三阶段: 本地同步 ---
            print("🔄 正在自动同步本地 Git 记录以避免冲突...")
            subprocess.run(["git", "update-ref", f"refs/remotes/{remote_name}/{target_branch}", new_commit_sha])
            subprocess.run(["git", "reset", "--mixed", new_commit_sha], stdout=subprocess.DEVNULL)
            print("✅ 本地记录已更新。")
        else:
            print(f"\n❌ 远程更新失败: {resp.text}")

    except Exception as e:
        print(f"\n💥 错误: {e}")

if __name__ == "__main__":
    main()
