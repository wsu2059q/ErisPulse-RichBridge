<div align="center">

<img src=".github/assets/ErisPulseLogo.png" width="180" alt="ErisPulse RichBridge" />

# ErisPulse RichBridge

**Transparent Markdown / Html sending for adapters without rich text support.**

After loading, the module installs `Markdown` and `Html` methods on adapters whose Send class lacks them: content is rendered to an image via [Takumi](https://pypi.org/project/ErisPulse-Takumi/) and sent as `Image`. Neither adapters nor business code need any change.

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

## How It Works

```
business code                      RichBridge                          platform
────────────                      ──────────                          ────────
Send.To(...).Markdown(md)  ──►  markdown → HTML → Takumi PNG  ──►  Image(png)
event.reply(md, method="Markdown") ──┘
adapter.send(..., method="Markdown") ──┘
```

- On load the module listens for `adapter.load` / `adapter.start` events and, for adapters whose Send class lacks `Markdown` / `Html`, creates a subclass with the methods installed and replaces the adapter's `Send` instance
- Afterwards `sdk.adapter.list_sends(platform)` and `event.supports("Markdown")` report the new capability normally
- Adapters that natively implement `Markdown` / `Html` are left untouched
- On render failure an optional plain-text fallback is available
- Unloading the module restores the adapters to their original state

## Install

```bash
epsdk install RichBridge
```

The [ErisPulse-Takumi](https://pypi.org/project/ErisPulse-Takumi/) rendering module is also required:

```bash
epsdk install Takumi
```

## Usage

No code changes are required. Adapters that only support images can immediately use:

```python
from ErisPulse import sdk

adapter = sdk.adapter.get("myplatform")

await adapter.Send.To("user", "123").Markdown("# Title\n\n**bold** text")
await adapter.Send.To("user", "123").Html("<b>bold</b>")
```

Event replies work as well:

```python
@message.on_message()
async def handler(event):
    if event.supports("Markdown"):
        await event.reply("# Received\n\n- item", method="Markdown")
```

## Configuration

The `[RichBridge]` section of `config.toml`:

| Option | Type | Default | Description |
|---|---|---|---|
| `methods` | list | `["Markdown", "Html"]` | Send methods to install |
| `width` | int | `900` | Render width (pixels), height adapts to content |
| `theme` | str | `"light"` | Render theme: `light` / `dark` |
| `lang` | str | `"zh-CN"` | Render language (affects font selection) |
| `platforms` | list | `[]` | Platform whitelist, empty = all adapters |
| `exclude_platforms` | list | `[]` | Platform blacklist |
| `fallback_text` | bool | `true` | Fall back to plain text when rendering fails |

Render parameters take effect immediately after config changes, no restart needed.

## Dependencies

- [ErisPulse](https://github.com/ErisPulse/ErisPulse) >= 2.7.0
- [ErisPulse-Takumi](https://pypi.org/project/ErisPulse-Takumi/) (rendering backend, module dependency)
- `markdown`, `pygments` (Markdown conversion and code highlighting, installed with the package)

## License

[MIT](./LICENSE)
