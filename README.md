<div align="center">

<img src=".github/assets/ErisPulseLogo.png" width="180" alt="ErisPulse RichBridge" />

# ErisPulse RichBridge

**为不支持富文本的适配器透明提供 Markdown / Html 发送能力。**

模块在加载后为缺少富文本发送方法的适配器补装 `Markdown` 与 `Html` 方法：调用时将内容经 [Takumi](https://pypi.org/project/ErisPulse-Takumi/) 渲染为图片，再以 `Image` 方式发送。适配器与业务代码均无需改动。

<p>
  <a href="https://pypi.org/project/ErisPulse-RichBridge/"><img src="https://img.shields.io/pypi/v/ErisPulse-RichBridge?style=for-the-badge&logo=pypi&logoColor=white" alt="PyPI"></a>
  <a href="https://pypi.org/project/ErisPulse-RichBridge/"><img src="https://img.shields.io/badge/Python-3.10+-FFD43B?style=for-the-badge&logo=python&logoColor=blue" alt="Python"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="License"></a>
  <a href="https://github.com/ErisPulse/ErisPulse-RichBridge"><img src="https://img.shields.io/github/stars/ErisPulse/ErisPulse-RichBridge?style=for-the-badge&logo=github&color=brightgreen" alt="Stars"></a>
  <a href="https://pepy.tech/project/ErisPulse-RichBridge"><img src="https://img.shields.io/pepy/dt/ErisPulse-RichBridge?style=for-the-badge&color=blue" alt="Downloads"></a>
  <a href="https://github.com/ErisPulse/ErisPulse"><img src="https://img.shields.io/badge/Powered_by-ErisPulse-FF6B9D?style=for-the-badge&logo=bookstack&logoColor=white" alt="ErisPulse"></a>
</p>

<p>
  <a href="./README.md">简体中文</a> | <a href="./README.en.md">English</a>
</p>

</div>

---

## 工作原理

```
业务代码调用                        RichBridge                          平台
────────────                      ──────────                          ────
Send.To(...).Markdown(md)  ──►  markdown → HTML → Takumi 渲染 PNG  ──►  Image(png)
event.reply(md, method="Markdown") ──┘
adapter.send(..., method="Markdown") ──┘
```

- 模块加载时监听 `adapter.load` / `adapter.start` 事件，对 Send 类缺少 `Markdown` / `Html` 方法的适配器创建补装子类并替换其 `Send` 实例
- 补装后 `sdk.adapter.list_sends(platform)` 与 `event.supports("Markdown")` 会正常报告新能力
- 原生已实现 `Markdown` / `Html` 的适配器不受影响
- 渲染失败时可配置回退为纯文本发送
- 模块卸载时自动恢复适配器原始状态

## 安装

```bash
epsdk install RichBridge
```

需要同时安装 [ErisPulse-Takumi](https://pypi.org/project/ErisPulse-Takumi/) 渲染模块：

```bash
epsdk install Takumi
```

## 使用

安装后无需任何代码改动。原本只支持图片的适配器即可使用：

```python
from ErisPulse import sdk

adapter = sdk.adapter.get("myplatform")

await adapter.Send.To("user", "123").Markdown("# 标题\n\n**加粗** 内容")
await adapter.Send.To("user", "123").Html("<b>加粗</b>")
```

事件回复同样生效：

```python
@message.on_message()
async def handler(event):
    if event.supports("Markdown"):
        await event.reply("# 收到\n\n- 列表项", method="Markdown")
```

## 配置

配置文件 `config.toml` 中的 `[RichBridge]` 节：

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `methods` | list | `["Markdown", "Html"]` | 要补装的发送方法 |
| `width` | int | `900` | 渲染宽度（像素），高度按内容自适应 |
| `theme` | str | `"light"` | 渲染主题：`light` / `dark` |
| `lang` | str | `"zh-CN"` | 渲染语言（影响字体选择） |
| `platforms` | list | `[]` | 平台白名单，留空表示全部适配器 |
| `exclude_platforms` | list | `[]` | 平台黑名单 |
| `fallback_text` | bool | `true` | 渲染失败时回退为纯文本发送 |

配置修改后无需重启，渲染参数即时生效。

## 依赖

- [ErisPulse](https://github.com/ErisPulse/ErisPulse) >= 2.7.0
- [ErisPulse-Takumi](https://pypi.org/project/ErisPulse-Takumi/)（渲染后端，模块依赖）
- `markdown`、`pygments`（Markdown 转换与代码高亮，随包安装）

## 许可证

[MIT](./LICENSE)
