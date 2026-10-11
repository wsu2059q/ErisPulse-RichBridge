from ErisPulse.Core.Bases import BaseI18n, I18nKey


class RichBridgeI18n(BaseI18n):

    description: I18nKey = I18nKey(
        default="为不支持富文本的适配器提供 Markdown/Html 转图片发送能力",
        zh_CN="为不支持富文本的适配器提供 Markdown/Html 转图片发送能力",
        zh_TW="為不支援富文字的介面卡提供 Markdown/Html 轉圖片傳送能力",
        en="Provide Markdown/Html-to-image sending for adapters without rich text support",
        ja="リッチテキスト非対応アダプターに Markdown/Html を画像化して送信する機能を提供",
        ru="Отправка Markdown/Html в виде изображений для адаптеров без поддержки форматов",
    )
    methods: I18nKey = I18nKey(
        default="要补装的富文本发送方法（可选 Markdown、Html，逗号分隔）",
        zh_CN="要补装的富文本发送方法（可选 Markdown、Html，逗号分隔）",
        zh_TW="要補裝的富文字傳送方法（可選 Markdown、Html，逗號分隔）",
        en="Rich text send methods to install (Markdown / Html, comma separated)",
        ja="追加するリッチテキスト送信メソッド（Markdown / Html、カンマ区切り）",
        ru="Методы отправки для установки (Markdown / Html, через запятую)",
    )
    methods_placeholder: I18nKey = I18nKey(
        default="Markdown, Html",
        zh_CN="Markdown, Html",
        zh_TW="Markdown, Html",
        en="Markdown, Html",
        ja="Markdown, Html",
        ru="Markdown, Html",
    )
    platforms: I18nKey = I18nKey(
        default="平台白名单（留空表示全部适配器）",
        zh_CN="平台白名单（留空表示全部适配器）",
        zh_TW="平台白名單（留空表示全部介面卡）",
        en="Platform whitelist (empty = all adapters)",
        ja="プラットフォームのホワイトリスト（空欄で全アダプター）",
        ru="Белый список платформ (пусто = все адаптеры)",
    )
    platforms_placeholder: I18nKey = I18nKey(
        default="留空表示全部",
        zh_CN="留空表示全部",
        zh_TW="留空表示全部",
        en="Empty = all",
        ja="空欄で全て",
        ru="Пусто = все",
    )
    exclude_platforms: I18nKey = I18nKey(
        default="平台黑名单（这些平台不补装）",
        zh_CN="平台黑名单（这些平台不补装）",
        zh_TW="平台黑名單（這些平台不補裝）",
        en="Platform blacklist (these platforms are skipped)",
        ja="プラットフォームのブラックリスト（対象外）",
        ru="Черный список платформ (пропускаются)",
    )
    fallback_text: I18nKey = I18nKey(
        default="渲染失败时回退为纯文本发送",
        zh_CN="渲染失败时回退为纯文本发送",
        zh_TW="渲染失敗時回退為純文字傳送",
        en="Fall back to plain text when rendering fails",
        ja="レンダリング失敗時にプレーンテキストへフォールバック",
        ru="При ошибке рендеринга отправлять простой текст",
    )
    width: I18nKey = I18nKey(
        default="渲染宽度（像素）",
        zh_CN="渲染宽度（像素）",
        zh_TW="渲染寬度（像素）",
        en="Render width (pixels)",
        ja="レンダリング幅（ピクセル）",
        ru="Ширина рендеринга (пиксели)",
    )
    theme: I18nKey = I18nKey(
        default="渲染主题",
        zh_CN="渲染主题",
        zh_TW="渲染主題",
        en="Render theme",
        ja="レンダリングテーマ",
        ru="Тема рендеринга",
    )
    option_theme_light: I18nKey = I18nKey(
        default="浅色",
        zh_CN="浅色",
        zh_TW="淺色",
        en="Light",
        ja="ライト",
        ru="Светлая",
    )
    option_theme_dark: I18nKey = I18nKey(
        default="深色",
        zh_CN="深色",
        zh_TW="深色",
        en="Dark",
        ja="ダーク",
        ru="Тёмная",
    )
    lang: I18nKey = I18nKey(
        default="渲染语言（影响字体选择）",
        zh_CN="渲染语言（影响字体选择）",
        zh_TW="渲染語言（影響字型選擇）",
        en="Render language (affects font selection)",
        ja="レンダリング言語（フォント選択に影響）",
        ru="Язык рендеринга (влияет на выбор шрифта)",
    )
    group_basic: I18nKey = I18nKey(
        default="基本设置",
        zh_CN="基本设置",
        zh_TW="基本設定",
        en="Basic",
        ja="基本設定",
        ru="Основные",
    )
    group_render: I18nKey = I18nKey(
        default="渲染设置",
        zh_CN="渲染设置",
        zh_TW="渲染設定",
        en="Rendering",
        ja="レンダリング設定",
        ru="Рендеринг",
    )
    group_scope: I18nKey = I18nKey(
        default="生效范围",
        zh_CN="生效范围",
        zh_TW="生效範圍",
        en="Scope",
        ja="適用範囲",
        ru="Область действия",
    )
    takumi_missing: I18nKey = I18nKey(
        default="未找到 Takumi 模块，请先安装 ErisPulse-Takumi",
        zh_CN="未找到 Takumi 模块，请先安装 ErisPulse-Takumi",
        zh_TW="未找到 Takumi 模組，請先安裝 ErisPulse-Takumi",
        en="Takumi module not found, install ErisPulse-Takumi first",
        ja="Takumi モジュールが見つかりません。先に ErisPulse-Takumi をインストールしてください",
        ru="Модуль Takumi не найден, сначала установите ErisPulse-Takumi",
    )
    log_loaded: I18nKey = I18nKey(
        default="RichBridge 已加载",
        zh_CN="RichBridge 已加载",
        zh_TW="RichBridge 已載入",
        en="RichBridge loaded",
        ja="RichBridge を読み込みました",
        ru="RichBridge загружен",
    )
    log_unloaded: I18nKey = I18nKey(
        default="RichBridge 已卸载",
        zh_CN="RichBridge 已卸载",
        zh_TW="RichBridge 已卸載",
        en="RichBridge unloaded",
        ja="RichBridge を解除しました",
        ru="RichBridge выгружен",
    )
    log_patched: I18nKey = I18nKey(
        default="平台 {platform} 已补装发送方法: {methods}",
        zh_CN="平台 {platform} 已补装发送方法: {methods}",
        zh_TW="平台 {platform} 已補裝傳送方法: {methods}",
        en="Platform {platform} gained send methods: {methods}",
        ja="プラットフォーム {platform} に送信メソッドを追加しました: {methods}",
        ru="Платформа {platform} получила методы отправки: {methods}",
    )
    log_restored: I18nKey = I18nKey(
        default="平台 {platform} 的发送方法已恢复",
        zh_CN="平台 {platform} 的发送方法已恢复",
        zh_TW="平台 {platform} 的傳送方法已恢復",
        en="Send methods restored for platform {platform}",
        ja="プラットフォーム {platform} の送信メソッドを復元しました",
        ru="Методы отправки платформы {platform} восстановлены",
    )
    log_render_failed: I18nKey = I18nKey(
        default="方法 {method} 渲染失败: {error}",
        zh_CN="方法 {method} 渲染失败: {error}",
        zh_TW="方法 {method} 渲染失敗: {error}",
        en="Method {method} render failed: {error}",
        ja="メソッド {method} のレンダリングに失敗しました: {error}",
        ru="Ошибка рендеринга метода {method}: {error}",
    )
    log_unknown_method: I18nKey = I18nKey(
        default="未知的发送方法: {method}（可选 Markdown、Html）",
        zh_CN="未知的发送方法: {method}（可选 Markdown、Html）",
        zh_TW="未知的傳送方法: {method}（可選 Markdown、Html）",
        en="Unknown send method: {method} (options: Markdown, Html)",
        ja="不明な送信メソッド: {method}（Markdown / Html）",
        ru="Неизвестный метод отправки: {method} (доступны Markdown, Html)",
    )
    log_config_updated: I18nKey = I18nKey(
        default="配置已更新，渲染参数即时生效",
        zh_CN="配置已更新，渲染参数即时生效",
        zh_TW="配置已更新，渲染參數即時生效",
        en="Config updated, render parameters take effect immediately",
        ja="設定を更新しました。レンダリング参数は即時反映されます",
        ru="Конфигурация обновлена, параметры рендеринга применяются сразу",
    )
