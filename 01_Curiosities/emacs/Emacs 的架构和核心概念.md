## Emacs 架构组件图

```
┌─────────────────────────────────────────────────────────────┐
│                     Emacs 应用层                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐         │
│  │   用户配置    │ │  扩展包      │ │  主题/UI     │         │
│  │  (~/.emacs)  │ │  (packages)  │ │  (themes)    │         │
│  └──────────────┘ └──────────────┘ └──────────────┘         │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                   Elisp 运行时环境                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Elisp 解释器 (Evaluator)                 │   │
│  │  • 表达式求值  • 函数调用  • 变量绑定                  │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │   垃圾回收    │ │  符号表      │ │  字节码编译器 │        │
│  │   (GC)       │ │  (obarray)   │ │  (byte-comp) │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                     编辑器核心层                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                  Buffer 管理系统                       │   │
│  │  • Buffer 列表  • Buffer 切换  • Buffer 属性          │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │  Window      │ │  Frame       │ │  Mode        │        │
│  │  窗口系统     │ │  框架系统     │ │  模式系统     │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              文本属性与标记系统                         │   │
│  │  • Point/Mark  • Text Properties  • Overlays         │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                      C 核心层                                 │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │  文本存储     │ │  显示引擎     │ │  输入处理     │        │
│  │  (gap buffer)│ │  (redisplay)  │ │  (keyboard)  │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           底层 Elisp 原语实现                          │   │
│  │  • 基础数据类型  • 内存管理  • 系统调用                 │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    操作系统层                                 │
│         文件系统 | 进程管理 | 网络 | 终端/GUI                 │
└─────────────────────────────────────────────────────────────┘
```

## Emacs 作为编辑器的核心概念

### 1. **Buffer (缓冲区)**
- **定义**: 文本的内存表示,不一定对应文件
- **特点**: 
  - 每个 buffer 有唯一名称
  - 可以是文件内容、程序输出、临时数据等
  - 拥有自己的 mode、局部变量

```elisp
;; Buffer 操作示例
(get-buffer "*scratch*")           ; 获取 buffer 对象
(buffer-name)                      ; 当前 buffer 名称
(switch-to-buffer "myfile.txt")    ; 切换 buffer
(with-current-buffer "*Messages*"  ; 在指定 buffer 中执行
  (insert "Hello"))
```

### 2. **Point 和 Mark**
- **Point**: 光标位置(整数,表示字符位置)
- **Mark**: 标记位置,与 Point 形成 Region(选区)
- **关系**: Point 和 Mark 之间的文本就是当前选中区域

```elisp
(point)                  ; 返回当前 point 位置
(mark)                   ; 返回 mark 位置
(region-beginning)       ; 选区开始
(region-end)            ; 选区结束
(goto-char 100)         ; 移动 point 到位置 100
```

### 3. **Window (窗口)**
- **定义**: Buffer 的显示视口
- **关系**: 一个 buffer 可以在多个 window 中显示
- **分割**: 可水平/垂直分割

```elisp
(selected-window)               ; 当前窗口
(split-window-horizontally)     ; 水平分割
(split-window-vertically)       ; 垂直分割
(window-buffer)                 ; 窗口显示的 buffer
```

### 4. **Frame (框架)**
- **定义**: 操作系统级别的窗口
- **关系**: 一个 frame 包含多个 window
- **环境**: 终端模式下通常只有一个 frame

```elisp
(selected-frame)        ; 当前 frame
(make-frame)           ; 创建新 frame
(frame-list)           ; 所有 frame
```

### 5. **Mode (模式)**
分为两类:

**Major Mode (主模式)**:
- 每个 buffer 只有一个
- 定义了 buffer 的基本行为
- 例如: `text-mode`, `java-mode`, `org-mode`

**Minor Mode (次模式)**:
- 可以同时启用多个
- 提供额外功能
- 例如: `auto-fill-mode`, `line-number-mode`

```elisp
;; Mode 示例
(major-mode)                    ; 查看当前主模式
(text-mode)                     ; 切换到 text-mode
(auto-fill-mode 1)              ; 启用自动换行
```

### 6. **Keymap (键映射)**
- **定义**: 键盘输入到命令的映射表
- **层级**: Global → Major Mode → Minor Mode → Local
- **优先级**: 越局部优先级越高

```elisp
;; 定义键绑定
(global-set-key (kbd "C-c h") 'hello-function)
(define-key text-mode-map (kbd "C-c t") 'my-command)
```

### 7. **Hook (钩子)**
- **定义**: 特定事件发生时调用的函数列表
- **用途**: 在特定时机执行自定义代码

```elisp
;; Hook 示例
(add-hook 'text-mode-hook 'turn-on-auto-fill)
(add-hook 'before-save-hook 'delete-trailing-whitespace)
```

## 核心概念协同工作流程

```
用户按键
   ↓
键映射系统 (Keymap) 解析
   ↓
查找命令 (Command)
   ↓
执行 Elisp 函数
   ↓
操作 Buffer (修改文本、移动 Point)
   ↓
触发 Hook (如 after-change-functions)
   ↓
重新显示 (Redisplay)
   ↓
更新 Window 显示
```

### 实际例子:打开文件的流程

```elisp
;; 1. 用户按下 C-x C-f
;; 2. Keymap 找到对应命令: find-file

;; 3. find-file 函数执行:
(defun find-file (filename)
  ;; 4. 创建或获取 buffer
  (let ((buf (get-file-buffer filename)))
    (unless buf
      ;; 5. 创建新 buffer
      (setq buf (create-file-buffer filename))
      ;; 6. 读取文件内容到 buffer
      (with-current-buffer buf
        (insert-file-contents filename)
        ;; 7. 设置 major mode (根据文件扩展名)
        (normal-mode)
        ;; 8. 运行 mode hooks
        (run-hooks 'find-file-hook)))
    ;; 9. 在当前 window 显示 buffer
    (switch-to-buffer buf)))
```

## Buffer-Window-Frame 关系图

```
┌─────────────────────────────────────────┐
│  Frame 1 (GUI 窗口)                      │
│  ┌─────────────────┬─────────────────┐  │
│  │ Window 1        │ Window 2        │  │
│  │ Buffer: init.el │ Buffer: *help*  │  │
│  │ Point: 150      │ Point: 1        │  │
│  │ Mode: emacs-lisp│ Mode: help-mode │  │
│  └─────────────────┴─────────────────┘  │
│  ┌───────────────────────────────────┐  │
│  │ Window 3 (横向分割)                 │  │
│  │ Buffer: *Messages*                │  │
│  │ Mode: messages-mode               │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘

Buffer 列表 (内存中):
- init.el (在 Window 1 显示)
- *help* (在 Window 2 显示)
- *Messages* (在 Window 3 显示)
- config.org (未显示)
- *scratch* (未显示)
```

## 关键要点

1. **分离关注点**: Buffer(数据) 与 Window(视图) 分离
2. **多重显示**: 同一 buffer 可在多个窗口显示,各有独立的 point
3. **模式系统**: Major Mode 定义行为,Minor Mode 增强功能
4. **事件驱动**: Hook 机制实现松耦合的扩展
5. **双层架构**: C 核心提供性能,Elisp 提供灵活性
