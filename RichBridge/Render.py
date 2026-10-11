import markdown
from pygments.formatters import HtmlFormatter

_PAGE = '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body>{body}</body></html>'

_MD_EXTENSIONS = ["extra", "codehilite"]
_MD_EXTENSION_CONFIGS = {"codehilite": {"guess_lang": False}}

_PYGMENTS_STYLE = {"light": "friendly", "dark": "monokai"}
_PYGMENTS_CSS: dict[str, str] = {}

_THEMES: dict[str, str] = {
    "light": """
body {
    margin: 0;
    padding: 28px 32px;
    background: #ffffff;
    color: #1f2328;
    font-size: 16px;
    line-height: 1.75;
}
h1, h2, h3, h4, h5, h6 {
    margin-top: 1.4em;
    margin-bottom: 0.6em;
    line-height: 1.3;
}
h1:first-child, h2:first-child, h3:first-child {
    margin-top: 0;
}
h1 {
    font-size: 1.65em;
    padding-bottom: 0.3em;
    border-bottom: 1px solid #d8dee4;
}
h2 {
    font-size: 1.35em;
    padding-bottom: 0.3em;
    border-bottom: 1px solid #d8dee4;
}
h3 {
    font-size: 1.15em;
}
h4 {
    font-size: 1.05em;
}
p {
    margin: 0.6em 0;
}
ul, ol {
    margin: 0.6em 0;
    padding-left: 2em;
}
li {
    margin: 0.25em 0;
}
code {
    background: #eff1f3;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.88em;
}
pre {
    background: #f6f8fa;
    padding: 14px 16px;
    border-radius: 8px;
    margin: 0.8em 0;
    white-space: pre-wrap;
    word-break: break-word;
}
pre code {
    background: none;
    padding: 0;
    font-size: 0.88em;
}
blockquote {
    margin: 0.8em 0;
    padding: 4px 16px;
    border-left: 4px solid #d0d7de;
    color: #57606a;
}
table {
    border-collapse: collapse;
    margin: 0.8em 0;
}
th, td {
    border: 1px solid #d0d7de;
    padding: 6px 13px;
}
th {
    background: #f6f8fa;
}
a {
    color: #0969da;
}
img {
    max-width: 100%;
}
hr {
    border: none;
    border-top: 1px solid #d8dee4;
    margin: 1.2em 0;
}
""",
    "dark": """
body {
    margin: 0;
    padding: 28px 32px;
    background: #0d1117;
    color: #e6edf3;
    font-size: 16px;
    line-height: 1.75;
}
h1, h2, h3, h4, h5, h6 {
    margin-top: 1.4em;
    margin-bottom: 0.6em;
    line-height: 1.3;
}
h1:first-child, h2:first-child, h3:first-child {
    margin-top: 0;
}
h1 {
    font-size: 1.65em;
    padding-bottom: 0.3em;
    border-bottom: 1px solid #30363d;
}
h2 {
    font-size: 1.35em;
    padding-bottom: 0.3em;
    border-bottom: 1px solid #30363d;
}
h3 {
    font-size: 1.15em;
}
h4 {
    font-size: 1.05em;
}
p {
    margin: 0.6em 0;
}
ul, ol {
    margin: 0.6em 0;
    padding-left: 2em;
}
li {
    margin: 0.25em 0;
}
code {
    background: #262c36;
    color: #f0f3f6;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.88em;
}
pre {
    background: #161b22;
    padding: 14px 16px;
    border-radius: 8px;
    margin: 0.8em 0;
    white-space: pre-wrap;
    word-break: break-word;
}
pre code {
    background: none;
    padding: 0;
    font-size: 0.88em;
}
blockquote {
    margin: 0.8em 0;
    padding: 4px 16px;
    border-left: 4px solid #3d444d;
    color: #9198a1;
}
table {
    border-collapse: collapse;
    margin: 0.8em 0;
}
th, td {
    border: 1px solid #3d444d;
    padding: 6px 13px;
}
th {
    background: #161b22;
}
a {
    color: #4493f8;
}
img {
    max-width: 100%;
}
hr {
    border: none;
    border-top: 1px solid #30363d;
    margin: 1.2em 0;
}
""",
}


def _pygments_css(theme: str) -> str:
    css = _PYGMENTS_CSS.get(theme)
    if css is None:
        css = HtmlFormatter(style=_PYGMENTS_STYLE.get(theme, "friendly")).get_style_defs(".codehilite")
        _PYGMENTS_CSS[theme] = css
    return css


class Renderer:

    def __init__(self, sdk):
        self.sdk = sdk

    def _takumi(self):
        takumi = self.sdk.module.get("Takumi")
        if takumi is None:
            raise RuntimeError(self.sdk.i18n.t("RichBridge.takumi_missing"))
        return takumi

    def render(self, method: str, content: str, width: int, theme: str, lang: str) -> bytes:
        if method == "Markdown":
            body = markdown.markdown(
                content,
                extensions=_MD_EXTENSIONS,
                extension_configs=_MD_EXTENSION_CONFIGS,
            )
        else:
            body = content
        if theme not in _THEMES:
            theme = "light"
        css = _THEMES[theme] + "\n" + _pygments_css(theme)
        html = _PAGE.replace("{body}", body)
        return self._takumi().render_html(
            html,
            stylesheets=[css],
            width=width,
            height=None,
            lang=lang,
        )
