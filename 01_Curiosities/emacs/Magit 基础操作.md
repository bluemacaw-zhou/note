# Magit 基础操作

## 打开 Magit

```
SPC g g
```

进入 Magit Status 界面，这是所有操作的起点。

---

## 拉取代码

在 Magit Status 界面：

```
F p
```

`F` → Fetch/Pull 菜单，`p` → pull from upstream（等同于 `git pull`）

---

## 提交代码

### 第一步：暂存文件（Stage）

在 Magit Status 界面，光标移到想暂存的文件上：

```
s        # 暂存单个文件
S        # 暂存所有改动文件
u        # 取消暂存单个文件
```

### 第二步：提交（Commit）

```
c c
```

`c` → Commit 菜单，`c` → 创建新提交

此时会弹出一个编辑窗口，输入提交信息后：

```
SPC m k   # 或者
C-c C-c   # 确认提交
C-c C-k   # 取消提交
```

### 第三步：推送（Push）

```
P p
```

`P` → Push 菜单，`p` → push to upstream（等同于 `git push`）

---

## 完整流程速查

| 步骤 | 按键 | 说明 |
|------|------|------|
| 打开 Magit | `SPC g g` | 进入 Status 界面 |
| 拉取 | `F p` | git pull |
| 暂存文件 | `s` / `S` | stage |
| 提交 | `c c` → 写信息 → `C-c C-c` | git commit |
| 推送 | `P p` | git push |

---

## 其他常用操作

```
d d      # 查看 diff（光标在文件上）
l l      # 查看 git log
z z      # stash 当前改动
b b      # 切换分支
b c      # 创建新分支
```
