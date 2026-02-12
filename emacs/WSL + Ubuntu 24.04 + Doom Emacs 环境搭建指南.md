# WSL + Ubuntu 24.04 + Doom Emacs 环境搭建指南

## 项目目标

在 Windows 环境下通过 WSL 2 搭建 Doom Emacs 开发环境，支持离线迁移到内网机器。主要解决 Windows 原生 Emacs 终端体验不佳、无法正常启动 Claude Code 等问题。

## 环境要求

### 外网机器（用于环境搭建）
- Windows 11（推荐）或 Windows 10 版本 1903+ (Build 18362+)
- 支持虚拟化（BIOS 中启用 VT-x/AMD-V）
- 足够的磁盘空间（建议 20GB+）

### 内网机器（迁移目标）
- Windows 10 版本 1903+ (Build 18362+)
- WSL 2 已安装（通过 `wsl --status` 验证）
- 支持 WSLg（通过 `wsl --version` 确认 WSLg 版本号）

## 兼容性说明

- **Windows 11 → Windows 10 迁移**：完全兼容，WSL 2 架构一致
- **WSL 导出的 .tar 文件**：本质是 Linux 文件系统镜像，与宿主 Windows 版本无关
- **WSLg GUI 支持**：Windows 10 Build 19045+ 完整支持 GUI 应用

---

## 第一阶段：外网机器环境搭建

### 1. 验证 WSL 安装状态

```powershell
# 检查 WSL 是否已安装
wsl --status

# 查看 WSL 版本信息
wsl --version
```

**目的**：
- 确认 WSL 2 已安装并设为默认版本
- 验证 WSLg（GUI 支持）是否可用

**预期输出**：
```
默认版本: 2
WSLg 版本: 1.0.xx
```

### 2. 安装 Ubuntu 24.04

```powershell
# 查看可用的 Linux 发行版
wsl --list --online

# 安装 Ubuntu 24.04
wsl --install -d Ubuntu-24.04
```

**目的**：
- 选择 Ubuntu 24.04 LTS 确保长期支持和稳定性
- 首次安装会要求创建用户名和密码（记住这些信息）

**注意**：
- 安装过程需要联网下载
- 创建的用户将是 WSL 中的默认用户

### 3. 更新系统并安装基础工具

```bash
# 进入 WSL
wsl -d Ubuntu-24.04

# 更新软件包列表
sudo apt update

# 升级已安装的软件包
sudo apt upgrade -y

# 安装基础开发工具
sudo apt install -y build-essential git curl wget
```

**目的**：
- 获取最新的安全更新和软件包
- 安装编译工具链（Doom Emacs 某些包需要编译）
- 安装 Git（Doom Emacs 通过 Git 管理）

### 4. 安装 Emacs

```bash
# 安装 Emacs（包含 GUI 支持）
sudo apt install -y emacs

# 验证安装
emacs --version
```

**目的**：
- 安装 Emacs GUI 版本，支持在 Windows 桌面显示独立窗口
- Ubuntu 24.04 仓库中的 Emacs 版本通常 >= 28，满足 Doom Emacs 要求

**测试 GUI**：
```bash
# 测试 GUI 模式（应弹出独立窗口）
emacs &

# 测试终端模式
emacs -nw
```

### 5. 安装 Doom Emacs

```bash
# 克隆 Doom Emacs 到 ~/.emacs.d
git clone --depth 1 https://github.com/doomemacs/doomemacs ~/.emacs.d

# 运行安装脚本
~/.emacs.d/bin/doom install
```

**目的**：
- `--depth 1`：浅克隆，减少下载量
- `doom install`：初始化配置，下载核心包，设置环境

**安装过程**：
- 会询问是否生成配置文件（选择 Yes）
- 会下载大量 Emacs 包（需要时间，确保网络稳定）

### 6. 配置环境变量

```bash
# 编辑 ~/.bashrc 或 ~/.zshrc
echo 'export PATH="$HOME/.emacs.d/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**目的**：
- 将 Doom 命令行工具添加到 PATH
- 可以直接使用 `doom sync`、`doom upgrade` 等命令

### 7. 同步并验证 Doom Emacs

```bash
# 同步配置，下载所有包
doom sync

# 检查环境
doom doctor
```

**目的**：
- `doom sync`：根据配置文件下载所有必需的 Emacs 包
- `doom doctor`：诊断环境问题，检查依赖是否满足

**重要**：
- 仔细查看 `doom doctor` 的输出
- 修复所有 WARNING 和 ERROR
- 这一步确保环境完整，适合离线迁移

### 8. 安装 Claude Code（可选）

```bash
# 根据 Claude Code 官方文档安装
# 示例（具体命令以官方为准）：
npm install -g @anthropic-ai/claude-code
# 或
pip install claude-code
```

**目的**：
- 安装 Claude Code CLI 工具
- 验证在 Doom Emacs 终端中能否正常启动

**测试**：
```bash
# 在 WSL 中测试
claude-code --version

# 在 Emacs 中测试
emacs
M-x shell
claude-code
```

### 9. 离线测试（关键步骤）

```bash
# 模拟断网环境
sudo systemctl stop systemd-resolved
# 或通过其他方式断网

# 测试 Emacs 启动
emacs &

# 测试 Doom 命令
doom doctor

# 测试 Claude Code
claude-code --help

# 恢复网络
sudo systemctl start systemd-resolved
```

**目的**：
- **验证环境在完全离线状态下是否可用**
- 这是决定迁移方案可行性的关键测试
- 确保所有依赖已完整下载，不需要额外联网

**检查清单**：
- [ ] Emacs 能正常启动（GUI 和终端模式）
- [ ] Doom Emacs 所有功能正常
- [ ] Claude Code 能启动（如果需要 API key，确认离线可用性）
- [ ] 没有报错提示需要下载包或更新

### 10. 导出 WSL 发行版

```powershell
# 退出 WSL，在 Windows PowerShell 中执行

# 查看发行版名称
wsl -l -v

# 导出为 tar 文件
wsl --export Ubuntu-24.04 D:\ubuntu-doom-emacs.tar

# 可选：压缩以减少体积
# 使用 7-Zip 等工具压缩为 .tar.gz
```

**目的**：
- 将整个 WSL 文件系统导出为单个文件
- 包含所有已安装的软件、配置、下载的包
- 这个文件是**完全离线的环境快照**

**注意**：
- 导出文件可能很大（5-10GB+）
- 确保有足够的磁盘空间
- 导出过程可能需要几分钟

---

## 第二阶段：内网机器环境迁移

### 1. 验证内网机器 WSL 状态

```powershell
# 检查 WSL 是否已安装
wsl --status

# 查看详细版本信息
wsl --version
```

**目的**：
- 确认 WSL 2 已安装（应显示"默认版本: 2"）
- 确认 WSLg 已安装（应显示 WSLg 版本号）

**如果未安装**：
```powershell
# 需要联网安装（如果内网无网络，需提前准备）
wsl --install
```

### 2. 复制 tar 文件到内网机器

**方式选择**：
- U 盘传输
- 网络共享（如果内网允许）
- 其他符合公司安全策略的方式

**建议位置**：
```
D:\WSL-Backup\ubuntu-doom-emacs.tar
```

### 3. 导入 WSL 发行版

```powershell
# 导入到指定目录
wsl --import Ubuntu-Doom D:\WSL\Ubuntu-Doom D:\WSL-Backup\ubuntu-doom-emacs.tar

# 参数说明：
# Ubuntu-Doom: 新的发行版名称（可自定义）
# D:\WSL\Ubuntu-Doom: WSL 文件系统存储位置（建议大容量磁盘）
# D:\WSL-Backup\ubuntu-doom-emacs.tar: 导出的 tar 文件路径
```

**目的**：
- 在内网机器上重建完整的 Linux 环境
- 完全离线操作，不需要任何网络连接
- 保留外网机器上的所有配置和软件

**导入过程**：
- 时间取决于文件大小和磁盘速度（通常 5-15 分钟）
- 导入完成后，WSL 发行版即可使用

### 4. 设置默认用户

```powershell
# 启动导入的发行版（默认是 root 用户）
wsl -d Ubuntu-Doom

# 查看用户列表，找到你的用户名
cat /etc/passwd | grep 1000

# 退出 WSL
exit
```

**在 WSL 内创建配置文件**：
```bash
# 重新进入 WSL
wsl -d Ubuntu-Doom

# 创建 wsl.conf
sudo nano /etc/wsl.conf
```

**添加内容**：
```ini
[user]
default=你的用户名
```

**保存后重启 WSL**：
```powershell
# 在 PowerShell 中
wsl --shutdown
wsl -d Ubuntu-Doom
```

**目的**：
- 导入的发行版默认使用 root 用户
- 设置回原来的用户，保持配置路径一致
- 避免权限问题

### 5. 验证环境

```bash
# 检查用户
whoami

# 检查 Emacs
emacs --version

# 检查 Doom
doom doctor

# 检查 Claude Code
claude-code --version

# 测试 GUI 启动
emacs &
```

**目的**：
- 全面验证迁移后的环境
- 确保所有组件正常工作
- 测试 GUI 模式是否正常弹窗

### 6. 创建 Windows 快捷方式

#### 方案 A：创建基础快捷方式

```
右键桌面 → 新建 → 快捷方式
目标位置：wsl.exe -d Ubuntu-Doom emacsclient -c
名称：Doom Emacs
```

#### 方案 B：使用 Emacs Server 模式（推荐）

**首次启动 Emacs daemon**：
```bash
wsl -d Ubuntu-Doom
emacs --daemon
```

**配置自动启动**（可选）：
```bash
# 编辑 ~/.bashrc
echo 'if ! pgrep -u "$USER" emacs > /dev/null; then emacs --daemon > /dev/null 2>&1; fi' >> ~/.bashrc
```

**创建快捷方式**：
```
目标位置：wsl.exe -d Ubuntu-Doom emacsclient -c
```

**设置图标**：
```
右键快捷方式 → 属性 → 更改图标
浏览到：C:\Program Files\Emacs\bin\runemacs.exe
（如果有宿主机 Emacs）
```

**目的**：
- 方案 A：简单直接，每次启动 Emacs 需要几秒
- 方案 B：daemon 模式，启动速度极快（<1秒）
- 自定义图标：统一界面风格，方便识别

---

## 使用指南

### 从 Windows 启动 Doom Emacs

**方式 1：双击桌面快捷方式**
- 会弹出独立的 GUI 窗口
- 和原生 Windows 应用一样的体验

**方式 2：通过 PowerShell**
```powershell
# GUI 模式
wsl -d Ubuntu-Doom emacsclient -c

# 终端模式
wsl -d Ubuntu-Doom emacsclient -nw

# 打开特定文件
wsl -d Ubuntu-Doom emacsclient -c /mnt/c/Users/你的用户名/Documents/file.md
```

### 访问 Windows 文件

在 WSL/Emacs 中，Windows 文件系统挂载在 `/mnt/` 下：

```
C:\ → /mnt/c/
D:\ → /mnt/d/
```

**示例**：
```bash
# 在 Emacs 中打开 Windows 文档
C-x C-f /mnt/c/Users/Michael/Documents/project.md
```

### 日常维护

```bash
# 更新 Doom Emacs
doom upgrade

# 同步配置（修改 ~/.doom.d/ 后）
doom sync

# 清理缓存
doom clean
```

---

## 故障排查

### WSLg GUI 不工作

**症状**：运行 `emacs` 后没有窗口弹出

**解决**：
```powershell
# 检查 WSLg 状态
wsl --version

# 重启 WSL
wsl --shutdown
wsl -d Ubuntu-Doom

# 测试简单 GUI 程序
wsl -d Ubuntu-Doom
sudo apt install x11-apps
xeyes  # 应弹出眼睛窗口
```

### 默认用户不正确

**症状**：启动 WSL 后是 root 用户

**解决**：参考"设置默认用户"章节

### Doom 包缺失或错误

**症状**：启动 Emacs 报错，提示缺少包

**解决**：
```bash
# 重新同步
doom sync

# 诊断
doom doctor

# 如果需要重新安装
rm -rf ~/.emacs.d/.local
doom install
```

### Claude Code 无法使用

**症状**：命令找不到或运行报错

**原因可能**：
- 未正确安装
- 需要 API key 且未配置
- 需要联网验证

**解决**：
```bash
# 检查安装
which claude-code

# 重新安装（如果有离线包）
npm install -g /path/to/offline-package.tgz

# 检查配置
claude-code --help
```

---

## 优化建议

### 性能优化

1. **使用 Emacs Server 模式**：显著提升启动速度
2. **调整 WSL 内存限制**（如果需要）：
   ```
   # 在 Windows 用户目录创建 .wslconfig
   C:\Users\你的用户名\.wslconfig
   
   [wsl2]
   memory=8GB
   processors=4
   ```

### 备份策略

1. **定期导出配置**：
   ```bash
   # 只备份配置文件
   tar -czf doom-config-backup.tar.gz ~/.doom.d ~/.emacs.d/.local
   ```

2. **版本控制**：
   ```bash
   # 将个人配置放入 Git
   cd ~/.doom.d
   git init
   git add .
   git commit -m "Initial config"
   ```

### 分阶段迁移（可选）

如果担心一次性导出文件太大：

1. **阶段 1**：导出基础 Ubuntu + Emacs
2. **阶段 2**：单独备份 `~/.doom.d` 和 `~/.emacs.d/.local`
3. **阶段 3**：导入基础环境后，手动复制配置文件

---

## 关键决策点总结

### 为什么选择 WSL 2？
- 提供完整的 Linux 环境
- 支持 GUI 应用（WSLg）
- 性能优于 WSL 1
- 与 Docker、开发工具集成良好

### 为什么选择 Ubuntu 24.04？
- LTS 版本，长期支持到 2029 年
- 软件包新，Emacs 版本满足要求
- 社区活跃，问题容易找到解决方案

### 为什么使用 Doom Emacs？
- 开箱即用的配置
- 性能优化
- 现代化的默认设置
- 活跃的社区和插件生态

### 为什么要离线测试？
- 验证环境的完整性
- 确保内网迁移后可用
- 避免在内网遇到意外的网络依赖

### 为什么推荐 Emacs Server 模式？
- 启动速度极快
- 共享 buffer 和会话
- 资源占用更低
- 更符合 Emacs 的设计哲学

---

## 附录

### 相关文档链接

- [WSL 官方文档](https://learn.microsoft.com/en-us/windows/wsl/)
- [Doom Emacs 官方文档](https://github.com/doomemacs/doomemacs)
- [Emacs 官方手册](https://www.gnu.org/software/emacs/manual/)

### 常用命令速查

```bash
# WSL 管理
wsl -l -v                    # 列出所有发行版
wsl -d Ubuntu-Doom          # 启动指定发行版
wsl --shutdown              # 关闭所有 WSL 实例
wsl --export <name> <file>  # 导出发行版
wsl --import <name> <path> <file>  # 导入发行版

# Doom Emacs
doom install                # 首次安装
doom sync                   # 同步配置
doom upgrade                # 升级 Doom
doom doctor                 # 诊断问题
doom clean                  # 清理缓存

# Emacs
emacs &                     # GUI 模式（后台）
emacs -nw                   # 终端模式
emacs --daemon              # 启动 daemon
emacsclient -c              # 连接 daemon，新窗口
emacsclient -nw             # 连接 daemon，终端模式
```

---

## 文档版本

- **版本**：1.0
- **日期**：2026-02-02
- **适用环境**：Windows 10/11 + WSL 2 + Ubuntu 24.04 + Doom Emacs
