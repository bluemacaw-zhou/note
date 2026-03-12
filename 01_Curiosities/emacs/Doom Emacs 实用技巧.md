---
type: curiosity
topic: Emacs
date: 2026-03-12
tags: [Emacs, Doom Emacs, Projectile, vterm, SSH]
---

# Doom Emacs 实用技巧

## Projectile 找不到新建文件

**现象：** 外部工具（如 AI、终端）新建的文件，用 `SPC SPC` 在项目中搜索不到。

**原因：** Projectile 的文件索引是缓存的，且缓存持久化到磁盘（`~/.emacs.d/.local/cache/projectile.cache`），重启 Emacs 也不会自动更新。

**临时解决：**

```
SPC p i    ; projectile-invalidate-cache，清除缓存立即生效
```

**一劳永逸：** 在 `config.el` 中关闭缓存：

```elisp
(after! projectile
  (setq projectile-enable-caching nil))
```

笔记库、小型项目感觉不到性能差异，直接关掉最省心。

## SSH 链路下 vterm 复制文本

**场景：** 多跳 SSH（如 Deepin → Ubuntu → Mac）连接远端 Doom Emacs，在 vterm 中需要复制终端输出。

**现象：** `M-w` 等 Emacs 快捷键被本地终端模拟器拦截，无法正常复制。

**解决：** 在本地终端模拟器中，按住 `Shift` + 鼠标拖选，绕过 vterm 的鼠标捕获，触发终端原生选择，再正常复制。

> vterm-copy-mode（`C-c C-t`）的方案在多跳 SSH 下按键易被拦截，不如 Shift + 拖选可靠。
