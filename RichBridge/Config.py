from dataclasses import dataclass, field

from ErisPulse.Core.Bases import BaseConfig


@dataclass
class RichBridgeConfig(BaseConfig):

    methods: list = field(
        default_factory=lambda: ["Markdown", "Html"],
        metadata={
            "description": {
                "i18n": "RichBridge.methods",
                "default": "要补装的富文本发送方法（可选 Markdown、Html，逗号分隔）",
            },
            "ui": {"widget": "text", "group": "basic", "order": 2, "placeholder": {"i18n": "RichBridge.methods_placeholder", "default": "Markdown, Html"}},
        },
    )
    platforms: list = field(
        default_factory=list,
        metadata={
            "description": {
                "i18n": "RichBridge.platforms",
                "default": "平台白名单（留空表示全部适配器）",
            },
            "ui": {"widget": "text", "group": "scope", "order": 6, "placeholder": {"i18n": "RichBridge.platforms_placeholder", "default": "留空表示全部"}},
        },
    )
    exclude_platforms: list = field(
        default_factory=list,
        metadata={
            "description": {
                "i18n": "RichBridge.exclude_platforms",
                "default": "平台黑名单（这些平台不补装）",
            },
            "ui": {"widget": "text", "group": "scope", "order": 7},
        },
    )
    fallback_text: bool = field(
        default=True,
        metadata={
            "description": {
                "i18n": "RichBridge.fallback_text",
                "default": "渲染失败时回退为纯文本发送",
            },
            "ui": {"widget": "switch", "group": "scope", "order": 8},
        },
    )
    width: int = field(
        default=900,
        metadata={
            "description": {"i18n": "RichBridge.width", "default": "渲染宽度（像素）"},
            "ui": {"widget": "number", "group": "render", "order": 3},
        },
    )
    theme: str = field(
        default="light",
        metadata={
            "description": {"i18n": "RichBridge.theme", "default": "渲染主题"},
            "ui": {
                "widget": "select",
                "group": "render",
                "order": 4,
                "options": [
                    {"label": {"i18n": "RichBridge.option_theme_light", "default": "浅色"}, "value": "light"},
                    {"label": {"i18n": "RichBridge.option_theme_dark", "default": "深色"}, "value": "dark"},
                ],
            },
        },
    )
    lang: str = field(
        default="zh-CN",
        metadata={
            "description": {"i18n": "RichBridge.lang", "default": "渲染语言（影响字体选择）"},
            "ui": {"widget": "text", "group": "render", "order": 5},
        },
    )

    _schema_meta = {
        "group_labels": {
            "basic": {"i18n": "RichBridge.group_basic", "default": "基本设置"},
            "render": {"i18n": "RichBridge.group_render", "default": "渲染设置"},
            "scope": {"i18n": "RichBridge.group_scope", "default": "生效范围"},
        }
    }
