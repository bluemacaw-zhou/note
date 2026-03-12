---
type: curiosity
topic: Emacs
date: 2026-03-12
tags: [Emacs, Doom Emacs, Projectile]
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
