import pytest
from ErisPulse.Core.Bases import BaseModule
from ErisPulse.Core.Bases.module import ModuleMeta
from ErisPulse.loaders import ModuleLoadStrategy

from RichBridge.Core import Main

FAKE_PNG = b"\x89PNG\r\n\x1a\nRICHBRIDGE-FAKE"

_DEFAULT_CFG = {
    "methods": ["Markdown", "Html"],
    "platforms": [],
    "exclude_platforms": [],
    "fallback_text": True,
    "width": 900,
    "theme": "light",
    "lang": "zh-CN",
}


@pytest.fixture(scope="session", autouse=True)
def _storage_teardown():
    yield
    from ErisPulse import sdk

    try:
        sdk.storage.close()
    except Exception:
        pass


class FakeTakumiMain(BaseModule):

    def __init__(self, sdk):
        self.sdk = sdk
        self.logger = sdk.logger.get_child("FakeTakumi")
        self.calls = []
        self.fail = False

    @staticmethod
    def get_load_strategy():
        return ModuleLoadStrategy(lazy_load=False, priority=100)

    @staticmethod
    def get_meta():
        return ModuleMeta(name="Takumi", description="fake takumi for tests", version="0.0.0")

    async def on_load(self, event):
        return True

    async def on_unload(self, event):
        return True

    def render_html(self, html, stylesheets=None, width=None, height=None, lang=None, **kwargs):
        if self.fail:
            raise RuntimeError("render boom")
        self.calls.append(
            {
                "html": html,
                "stylesheets": stylesheets,
                "width": width,
                "height": height,
                "lang": lang,
            }
        )
        return FAKE_PNG


@pytest.fixture
async def rb(make_testbot):
    from ErisPulse import i18n

    prev_lang = i18n.get_language()
    i18n.set_language("zh-CN")

    async with make_testbot() as bot:
        from ErisPulse import config

        config.setConfig("RichBridge", dict(_DEFAULT_CFG))
        await bot.load_module(FakeTakumiMain)
        await bot.load_module(Main)

        from ErisPulse import adapter as adapter_mgr
        from ErisPulse import module as module_mgr

        bot.rb_mod = module_mgr.get("RichBridge")
        bot.takumi = module_mgr.get("Takumi")
        bot.mock_adapter = adapter_mgr.get(bot.platform)
        yield bot

    i18n.set_language(prev_lang)
