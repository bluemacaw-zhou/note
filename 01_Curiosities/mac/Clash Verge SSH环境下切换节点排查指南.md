# Clash Verge SSH 环境下切换节点排查指南

## 背景

在无图形界面的 SSH 环境下，Clash Verge 代理出现 `502 Bad Gateway`，需要通过命令行排查并切换节点。

## 排查步骤

### 第一步：确认 Clash 进程在运行

```bash
ps aux | grep clash
```

预期输出：
```
michael  5992  ...  /Applications/Clash Verge.app/Contents/MacOS/verge-mihomo ...
```

进程名为 `verge-mihomo`，说明 Clash Verge 正在运行。

---

### 第二步：确认端口在监听

```bash
lsof -i :7897
```

预期输出：
```
COMMAND   PID     USER   FD   TYPE  ...  NAME
verge-mih 5992  michael  12u  IPv6  ...  TCP *:7897 (LISTEN)
verge-mih 5992  michael  13u  IPv6  ...  UDP *:7897
```

看到 `LISTEN` 说明端口正常监听。

---

### 第三步：测试代理是否工作（用国内站点）

```bash
curl -vv --proxy http://127.0.0.1:7897 http://www.baidu.com
```

预期输出：
```
* Connected to 127.0.0.1 (127.0.0.1) port 7897
< HTTP/1.1 200 OK
```

百度能通说明代理本身正常，问题在于当前节点无法访问目标网站。

---

### 第四步：找到 API 端口

```bash
grep "external-controller" "/Users/michael/Library/Application Support/io.github.clash-verge-rev.clash-verge-rev/config.yaml"
```

预期输出：
```
external-controller: 127.0.0.1:9097
external-controller-unix: /tmp/verge/verge-mihomo.sock
```

记住 Unix socket 路径 `/tmp/verge/verge-mihomo.sock`，后续步骤使用。

---

### 第五步：通过 Unix Socket 获取节点列表

```bash
curl -s --unix-socket /tmp/verge/verge-mihomo.sock http://mihomo/proxies | python3 -c "
import json, sys
data = json.load(sys.stdin)
for name in data['proxies']:
    print(name)
"
```

预期输出：
```
COMPATIBLE
DIRECT
GLOBAL
美国 01
美国 02
美国 03
...
香港 01
日本 01
```

---

### 第六步：查看当前选中节点

```bash
curl -s --unix-socket /tmp/verge/verge-mihomo.sock http://mihomo/proxies/GLOBAL | python3 -m json.tool | grep -E '"now"|"name"'
```

预期输出：
```
"name": "GLOBAL",
"now": "美国 10",
```

---

### 第七步：批量测试节点延迟

以美国节点为例：

```bash
for i in 01 02 03 04 05 06 07 08 09 10; do
  result=$(curl -s --unix-socket /tmp/verge/verge-mihomo.sock "http://mihomo/proxies/%E7%BE%8E%E5%9B%BD%20$i/delay?timeout=5000&url=http://www.google.com")
  echo "美国 $i: $result"
done
```

预期输出：
```
美国 01: {"delay":2434}
美国 02: {"delay":982}
美国 03: {"delay":669}
美国 04: {"delay":720}
...
```

节点无响应会返回 `{"message":"...timeout..."}` 或空，选延迟最低的节点。

> 节点名 URL 编码：美国 = `%E7%BE%8E%E5%9B%BD`，空格 = `%20`

---

### 第八步：切换到低延迟节点

```bash
curl -s -X PUT --unix-socket /tmp/verge/verge-mihomo.sock http://mihomo/proxies/GLOBAL -H "Content-Type: application/json" -d '{"name": "美国 03"}'
```

无报错即切换成功。

---

### 第九步：验证

```bash
curl -vv www.google.com
```

预期输出：
```
< HTTP/1.1 200 OK
```

---

## 常见节点名 URL 编码

| 节点名 | URL 编码 |
|--------|---------|
| 美国   | `%E7%BE%8E%E5%9B%BD` |
| 香港   | `%E9%A6%99%E6%B8%AF` |
| 日本   | `%E6%97%A5%E6%9C%AC` |
| 新加坡 | `%E6%96%B0%E5%8A%A0%E5%9D%A1` |
| 台湾   | `%E5%8F%B0%E6%B9%BE` |

---

## 根因总结

`502 Bad Gateway` = 代理能连上，但当前节点转发失败（节点失效或被封）。
解决方法：通过 Unix socket API 批量测试延迟，切换到可用节点。
