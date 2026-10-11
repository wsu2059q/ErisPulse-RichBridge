import asyncio
import weakref

from ErisPulse.Core.Bases import BaseModule
from ErisPulse.Core.Bases.module import ModuleMeta
from ErisPulse.loaders import ModuleLoadStrategy

from .Config import RichBridgeConfig
from .I18n import RichBridgeI18n
from .Render import Renderer

_SUPPORTED_METHODS = ("Markdown", "Html")


class Main(BaseModule):

    ConfigClass = RichBridgeConfig
    I18nClass = RichBridgeI18n

    def __init__(self, sdk):
        self.sdk = sdk
        self.logger = sdk.logger.get_child("RichBridge")
        self.i18n = sdk.i18n
        self._renderer = Renderer(sdk)
        self._patched: dict[int, tuple] = {}

    @staticmethod
    def get_load_strategy() -> ModuleLoadStrategy:
        return ModuleLoadStrategy(lazy_load=False, priority=200, depends=["Takumi"])

    @staticmethod
    def get_meta() -> ModuleMeta:
        return ModuleMeta(
            name="RichBridge",
            description={
                "i18n": "RichBridge.description",
                "default": "为不支持富文本的适配器提供 Markdown/Html 转图片发送能力",
            },
            version="1.0.0",
            author="wsu2059q",
            homepage="https://github.com/ErisPulse/ErisPulse-RichBridge",
            group="adapter",
            tags=["rich-text", "markdown", "image", "render", "takumi"],
            min_sdk_version="2.7.0",
        )

    async def on_load(self, event: dict) -> bool:
        if not self.sdk.module.exists("Takumi"):
            self.logger.error(self.i18n.t("RichBridge.takumi_missing"))
            return False
        self.sdk.lifecycle.register("adapter.load", self._on_adapter_load)
        self.sdk.lifecycle.register("adapter.start", self._on_adapter_start)
        for platform in self.sdk.adapter.list_items():
            self._patch_platform(platform)
        self.logger.info(self.i18n.t("RichBridge.log_loaded"))
        return True

    async def on_unload(self, event: dict) -> bool:
        for _, (ref, original) in list(self._patched.items()):
            adapter = ref()
            if adapter is None:
                continue
            current = getattr(adapter, "Send", None)
            if getattr(type(current), "_richbridge_patched", False):
                adapter.Send = original
                self.logger.info(
                    self.i18n.t(
                        "RichBridge.log_restored",
                        platform=getattr(adapter, "_platform", "") or "",
                    )
                )
        self._patched.clear()
        self.logger.info(self.i18n.t("RichBridge.log_unloaded"))
        return True

    def on_config_update(self, old_config, new_config):
        self.logger.info(self.i18n.t("RichBridge.log_config_updated"))

    async def _on_adapter_load(self, event) -> None:
        data = self._event_data(event)
        platform = data.get("platform")
        if platform and data.get("success", True):
            self._patch_platform(platform)

    async def _on_adapter_start(self, event) -> None:
        data = self._event_data(event)
        for platform in data.get("platforms") or []:
            self._patch_platform(platform)

    @staticmethod
    def _event_data(event) -> dict:
        if not isinstance(event, dict):
            return {}
        data = event.get("data")
        if isinstance(data, dict):
            return data
        return event

    def _resolve_methods(self, cfg) -> list[str]:
        resolved: list[str] = []
        for raw in cfg.methods:
            name = str(raw).strip().lower()
            matched = next((m for m in _SUPPORTED_METHODS if m.lower() == name), None)
            if matched is None:
                self.logger.warning(self.i18n.t("RichBridge.log_unknown_method", method=raw))
                continue
            if matched not in resolved:
                resolved.append(matched)
        return resolved

    @staticmethod
    def _platform_allowed(cfg, platform: str) -> bool:
        lowered = platform.lower()
        if cfg.platforms:
            allowed = {str(p).strip().lower() for p in cfg.platforms}
            if lowered not in allowed:
                return False
        excluded = {str(p).strip().lower() for p in cfg.exclude_platforms}
        return lowered not in excluded

    def _patch_platform(self, platform: str) -> None:
        cfg = self.cfg
        if not self._platform_allowed(cfg, platform):
            return
        adapter = self.sdk.adapter.get(platform)
        if adapter is None:
            return
        key = id(adapter)
        if key in self._patched:
            return
        send_cls = type(adapter.Send)
        targets = [name for name in self._resolve_methods(cfg) if not hasattr(send_cls, name)]
        if not targets:
            return
        namespace = {"_richbridge_patched": True}
        for name in targets:
            namespace[name] = self._make_send_method(name)
        patched_cls = type(f"RichBridgeSend_{platform}", (send_cls,), namespace)
        self._patched[key] = (weakref.ref(adapter), adapter.Send)
        adapter.Send = patched_cls(adapter)
        self.logger.info(
            self.i18n.t(
                "RichBridge.log_patched",
                platform=platform,
                methods=", ".join(targets),
            )
        )

    @staticmethod
    def _delegate_raw(self_send, fn, *args):
        self_send._in_rule_wrap = True
        try:
            return fn(self_send, *args)
        finally:
            self_send._in_rule_wrap = False

    def _make_send_method(self, method_name: str):
        module = self

        def send_method(self_send, content: str, **kwargs):
            async def _run():
                cfg = module.cfg
                try:
                    png = await asyncio.to_thread(
                        module._renderer.render,
                        method_name,
                        content,
                        cfg.width,
                        cfg.theme,
                        cfg.lang,
                    )
                except Exception as e:
                    module.logger.error(
                        module.i18n.t("RichBridge.log_render_failed", method=method_name, error=e)
                    )
                    if cfg.fallback_text:
                        text_fn = getattr(type(self_send), "Text", None)
                        if callable(text_fn):
                            return await module._delegate_raw(self_send, text_fn, content)
                    return self_send._adapter.make_error(
                        message=module.i18n.t("RichBridge.log_render_failed", method=method_name, error=e)
                    )
                image_fn = getattr(type(self_send), "Image")
                return await module._delegate_raw(self_send, image_fn, png)

            try:
                return asyncio.create_task(_run())
            except RuntimeError:
                return asyncio.ensure_future(_run())

        send_method.__name__ = method_name
        return send_method
