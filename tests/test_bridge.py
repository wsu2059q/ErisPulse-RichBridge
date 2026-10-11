import asyncio

import pytest
from ErisPulse import BaseAdapter

from .conftest import FAKE_PNG


def _segments(adapter):
    out = []
    for msg in adapter.sent:
        out.extend(msg.segments if hasattr(msg, "segments") else msg)
    return out


async def test_markdown_sends_rendered_image(rb):
    adapter = rb.mock_adapter
    resp = await adapter.Send.To("user", "123").Markdown("# hi\n\n**bold**")
    assert resp["status"] == "ok"
    assert {"type": "image", "data": {"file": FAKE_PNG}} in _segments(adapter)
    assert rb.takumi.calls, "takumi render_html should be called"
    call = rb.takumi.calls[-1]
    assert "<h1>hi</h1>" in call["html"]
    assert "<strong>bold</strong>" in call["html"]
    assert call["width"] == 900
    assert call["height"] is None
    assert call["lang"] == "zh-CN"
    assert call["stylesheets"]


async def test_html_method_sends_rendered_image(rb):
    adapter = rb.mock_adapter
    resp = await adapter.Send.To("user", "123").Html("<b>bold</b>")
    assert resp["status"] == "ok"
    assert {"type": "image", "data": {"file": FAKE_PNG}} in _segments(adapter)
    assert "<b>bold</b>" in rb.takumi.calls[-1]["html"]


async def test_list_sends_reports_rich_methods(rb):
    from ErisPulse import adapter as adapter_mgr

    methods = adapter_mgr.list_sends(rb.platform)
    assert "Markdown" in methods
    assert "Html" in methods


async def test_at_and_reply_modifiers_still_work(rb):
    adapter = rb.mock_adapter
    resp = await adapter.Send.To("group", "g1").At("u1").Markdown("# title")
    assert resp["status"] == "ok"
    segs = _segments(adapter)
    assert {"type": "mention", "data": {"user_id": "u1"}} in segs
    assert {"type": "image", "data": {"file": FAKE_PNG}} in segs


async def test_event_reply_with_markdown_method(rb):
    from ErisPulse.Core.Event import message

    @message.on_message()
    async def handler(event):
        await event.reply("# from handler", method="Markdown")

    await rb.send_message("hello")
    last = rb.last_reply
    assert last is not None
    assert {"type": "image", "data": {"file": FAKE_PNG}} in list(last.segments)


async def test_render_failure_falls_back_to_text(rb):
    rb.takumi.fail = True
    resp = await rb.mock_adapter.Send.To("user", "123").Markdown("# boom")
    assert resp["status"] == "ok"
    assert {"type": "text", "data": {"text": "# boom"}} in _segments(rb.mock_adapter)


async def test_render_failure_without_fallback_returns_error(rb):
    cfg = rb.rb_mod.cfg
    cfg.fallback_text = False
    rb.rb_mod.cfg = cfg

    rb.takumi.fail = True
    resp = await rb.mock_adapter.Send.To("user", "123").Markdown("# boom")
    assert resp["status"] == "failed"
    assert not _segments(rb.mock_adapter)


class NativeRichAdapter(BaseAdapter):

    def __init__(self, sdk=None):
        super().__init__(sdk)
        self.sent = []

    class Send(BaseAdapter.Send):

        def Markdown(self, text):
            return self.Raw_ob12([{"type": "text", "data": {"text": f"native:{text}"}}])

        def Raw_ob12(self, message, **kwargs):
            async def _send():
                self._adapter.sent.append(message)
                return {"status": "ok", "retcode": 0, "data": {"message_id": "n1"}, "message_id": "n1", "message": "ok"}

            return asyncio.ensure_future(_send())

    async def start(self):
        pass

    async def shutdown(self):
        pass

    async def call_api(self, endpoint, **params):
        return None


async def test_native_markdown_not_overridden(rb):
    from ErisPulse import adapter as adapter_mgr
    from ErisPulse import lifecycle

    adapter_mgr.register("nativeplat", NativeRichAdapter)
    await lifecycle.submit_event(
        "adapter.load",
        msg="test native register",
        data={"platform": "nativeplat", "success": True},
    )
    await asyncio.sleep(0)

    native = adapter_mgr.get("nativeplat")
    resp = await native.Send.To("user", "9").Markdown("# keep")
    assert resp["status"] == "ok"
    assert {"type": "text", "data": {"text": "native:# keep"}} in _segments(native)

    resp = await native.Send.To("user", "9").Html("<i>i</i>")
    assert resp["status"] == "ok"
    assert {"type": "image", "data": {"file": FAKE_PNG}} in _segments(native)

    adapter_mgr._adapters.pop("nativeplat", None)
    adapter_mgr._adapter_info.pop("nativeplat", None)


async def test_exclude_platforms_skips_patch(rb):
    from ErisPulse import adapter as adapter_mgr
    from ErisPulse import module as module_mgr

    await module_mgr.unload("RichBridge")
    cfg = rb.rb_mod.cfg
    cfg.exclude_platforms = [rb.platform]
    rb.rb_mod.cfg = cfg
    await module_mgr.load("RichBridge")

    adapter = adapter_mgr.get(rb.platform)
    assert "Markdown" not in adapter_mgr.list_sends(rb.platform)
    assert not hasattr(type(adapter.Send), "Markdown")

    await module_mgr.unload("RichBridge")
    cfg = rb.rb_mod.cfg
    cfg.exclude_platforms = []
    rb.rb_mod.cfg = cfg
    await module_mgr.load("RichBridge")
    assert "Markdown" in adapter_mgr.list_sends(rb.platform)


async def test_unload_restores_send(rb):
    from ErisPulse import adapter as adapter_mgr
    from ErisPulse import module as module_mgr

    adapter = adapter_mgr.get(rb.platform)
    assert getattr(type(adapter.Send), "_richbridge_patched", False)

    await module_mgr.unload("RichBridge")

    adapter = adapter_mgr.get(rb.platform)
    assert not getattr(type(adapter.Send), "_richbridge_patched", False)
    assert not hasattr(type(adapter.Send), "Markdown")
    assert "Markdown" not in adapter_mgr.list_sends(rb.platform)

    with pytest.raises(AttributeError):
        adapter.Send.To("user", "1").Markdown("# gone")

    await module_mgr.load("RichBridge")
    assert "Markdown" in adapter_mgr.list_sends(rb.platform)
