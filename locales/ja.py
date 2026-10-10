"""
Japanese Translation Pack
Telegram Media Storage Bot v3.0.4
"""

TEXTS = {
    # ============================================
    # /start
    # ============================================
    "start.welcome": "👋 <b>ようこそ、{name}さん！</b>",
    "start.bot_desc": "🤖 <b>Telegram Media Storage Bot v3.0.4</b>\n自動重複除去、ユーザーごとの暗号化、ファイル削除機能を備えた多ユーザー対応スマートメディアストレージボット。",
    "start.features_title": "✨ <b>主な機能:</b>",
    "start.feature_save": "• 写真、動画、ドキュメントを保存",
    "start.feature_dedup": "• ユーザーごとの自動重複検出・拒否",
    "start.feature_privacy": "• 分離ストレージ — ファイルはあなただけが閲覧可能",
    "start.feature_autodel": "• {desc}",
    "start.feature_spoiler": "• <b>キャプションとスポイラーは無視</b>（ファイルのみ保存）",
    "start.feature_album": "• 複数ファイルのアルバムに完全対応",
    "start.feature_forward": "• 転送されたメディアも保存",
    "start.feature_stats": "• 完全なリアルタイム個人統計",
    "start.feature_delete": "• 安全な確認付きファイル削除",
    "start.howto_title": "🚀 <b>使い方:</b>",
    "start.howto_desc": "メディアを送信または転送するだけ！",
    "start.commands_title": "📖 <b>コマンド:</b>",
    "start.cmd_get": "/get — インタラクティブファイルブラウザを開く",
    "start.cmd_stats": "/stats — 統計と稼働時間",
    "start.cmd_limit": "/mylimit — 残りクォータを確認",
    "start.cmd_delete": "/delete — 保存ファイルを削除",
    "start.cmd_help": "/help — 完全ヘルプ",
    "start.cmd_lang": "/language — 言語切替（8言語）",
    "start.cmd_admin_msg": "@admin [メッセージ] — 管理者に連絡",
    "start.admin_title": "🔑 <b>管理者モード有効</b>",
    "start.admin_cmd": "/admin — 管理パネル",
    "start.privacy_title": (
        "🔒 <b>プライバシー保証</b>\n"
        "• 各ファイルは<b>分離して保存</b>され、あなただけがアクセスできます。\n"
        "• <b>管理者もユーザーのファイルを閲覧・開封できません。</b>\n"
        "• 他のユーザーを含む第三者とデータを共有することはありません。\n"
        "• 当システムは保護されたストレージを使用し、常にプライバシーを守ります。"
    ),
    "start.autodel_desc_media": "メディアメッセージは {delay} 秒後に自動削除",
    "start.autodel_desc_all": "メッセージは {delay} 秒後に自動削除",

    # ============================================
    # /help
    # ============================================
    "help.title": "📖 <b>完全ヘルプ</b>",
    "help.subtitle": "Telegram Media Storage Bot v3.0.4",
    "help.section1_title": "📤 <b>1. メディアの保存</b>",
    "help.section1_desc": "ボットにメディアを送信または転送するだけ — すべて自動です。",
    "help.section1_support": "✅ 対応: 写真、動画、ドキュメント",
    "help.section1_album": "✅ 複数ファイルアルバムも自動処理",
    "help.section1_forward": "✅ 他のチャット/チャンネル/グループからの転送も保存",
    "help.section1_duplicate": "🚫 アカウント内の重複は自動拒否",
    "help.section1_spoiler": "🧹 キャプションとスポイラーは非保存（元ファイルのみ）",
    "help.section1_delete": "🗑️ 元メッセージは {delay} 秒後に削除",
    "help.section2_title": "📥 <b>2. ファイルの取得 — /get</b>",
    "help.section2_intro": "<code>/get</code>で<b>インタラクティブファイルブラウザ</b>を開きます。",
    "help.section2_nav_title": "🎮 <b>ファイルブラウザの操作:</b>",
    "help.section2_nav1": "• <b>ファイル番号</b>をクリック — そのファイルをダウンロード",
    "help.section2_nav2": "• <b>👁️ ページ表示</b>をクリック — ページ内の全ファイルをダウンロード",
    "help.section2_nav3": "• ⬅️ <b>前へ</b> / <b>次へ</b> ➡️ — ページ移動",
    "help.section2_nav4": "• <b>📄 ページ番号</b>をクリック — 任意のページにジャンプ",
    "help.section2_nav5": "• プロンプトでページ番号を入力 — クイックアクセス",
    "help.section2_nav6": "• 各ページ最大10ファイル表示",
    "help.section2_admin": "\n🔑 <b>管理者向け:</b>\n" +
                          "<code>/get user [ID]</code> — 他ユーザーのファイルを表示\n" +
                          "<code>/get</code> (管理者) — 全ユーザーの全ファイルを表示",
    "help.section2_delete": "\n🗑️ ダウンロード結果は {delay} 秒後に自動削除",
    "help.section3_title": "📊 <b>3. 統計 — /stats</b>",
    "help.section3_files": "• 総ファイル数とストレージサイズ",
    "help.section3_breakdown": "• タイプ別内訳（写真/動画/ドキュメント）",
    "help.section3_today": "• 本日のアップロード数と重複数",
    "help.section3_uptime": "• ボット稼働時間（日/時間/分）",
    "help.section4_title": "📋 <b>4. クォータ — /mylimit</b>",
    "help.section4_default": "• デフォルト: 1ユーザーあたり {limit:,} ファイル",
    "help.section4_admin": "• 管理者はユーザーごとのクォータを調整可能",
    "help.section4_unlimited": "• 0 = 無制限",
    "help.section5_title": "🗑️ <b>5. ファイル削除 — /delete</b>",
    "help.section5_cmd": "<code>/delete [番号]</code> — 指定番号のファイルを削除",
    "help.section5_all": "<code>/delete all</code> — 自分の全ファイルを削除",
    "help.section5_note": "⚠️ 削除前には必ず確認が求められます！",
    "help.section6_title": "💬 <b>6. 管理者への連絡</b>",
    "help.section6_cmd": "<code>@admin [メッセージ]</code> と入力",
    "help.section6_example": "例: <code>@admin 動画のアップロードに失敗します</code>",
    "help.section6_reply": "管理者がボットを通じて返信します。",
    "help.section7_title": "🛡️ <b>7. プライバシーとセキュリティ</b>",
    "help.section7_private": (
        "• 保存されたファイルは<b>あなただけがアクセス可能</b>です。\n"
        "  管理者を含め、誰もあなたのファイルを閲覧・開封・ダウンロードできません。"
    ),
    "help.section7_noshare": (
        "• <b>データ共有ゼロ。</b> あなたのファイルが他のユーザーに表示されることはなく、\n"
        "  統計情報も非公開です。"
    ),
    "help.section7_clean": (
        "• ボットに送信した元メッセージは<b>数秒後に自動削除</b>されます。\n"
        "  安全なストレージに保存されたファイルだけが残ります。"
    ),
    "help.section7_dedup": (
        "• 重複検出は<b>ユーザーごとに</b>行われます。既にアカウントにあるファイルは\n"
        "  再受付されず、ストレージ効率が保たれます。"
    ),
    "help.section7_encryption": (
        "• ストレージは<b>厳格な分離</b>とシステムレベルのアクセス保護を使用。\n"
        "  あなたのデータが自分のセッション以外で読み取られることはありません。"
    ),
    "help.section8_title": "🌐 <b>8. 言語 — /language</b>",
    "help.section8_desc": "ボットの表示言語を変更（8言語対応）。",
    "help.section8_list": "<code>/language</code> — 言語選択を表示",
    "help.section8_set": "希望の言語ボタンをタップ",
    "help.section8_langs": "🇮🇩 ID | 🇬🇧 EN | 🇷🇺 RU | 🇨🇳 ZH | 🇯🇵 JA | 🇪🇸 ES | 🇮🇳 HI | 🇧🇷 PT",
    "help.section9_title": "💡 <b>9. ヒント</b>",
    "help.section9_tip1": "• チャンネル/グループからメディアを転送して保存",
    "help.section9_tip2": "• いつでも /get でファイルを取り出せます",
    "help.section9_tip3": "• キャプションとスポイラーは保存されません（元ファイルのみ）",
    "help.section9_tip4": "• 写真/動画アルバムはグループとして効率的に処理",
    "help.admin_title": "🔑 <b>10. 管理者コマンド</b>",
    "help.admin_list": "<code>/admin</code> — 管理パネル",
    "help.admin_users": "<code>/admin users</code> — 全ユーザー一覧",
    "help.admin_user": "<code>/admin user [id]</code> — ユーザー詳細",
    "help.admin_add": "<code>/admin add [id]</code> — 管理者追加（スーパー管理者のみ）",
    "help.admin_remove": "<code>/admin remove [id]</code> — 管理者削除（スーパー管理者のみ）",
    "help.admin_setlimit": "<code>/admin setlimit [id] [n]</code> — ユーザークォータ設定",
    "help.admin_stats": "<code>/admin stats</code> — 全体統計",
    "help.admin_messages": "<code>/admin messages</code> — ユーザーからのメッセージ",
    "help.admin_ban": "<code>/ban [id]</code> — ユーザーをBAN",
    "help.admin_unban": "<code>/unban [id]</code> — BAN解除",
    "help.admin_broadcast": "<code>/broadcast [メッセージ]</code> — 全ユーザーに一斉送信",
    "help.admin_reply": "<code>/reply [id] [テキスト]</code> — ユーザーメッセージに返信",
    "help.admin_delete": "<code>/delete user [id] [番号|all]</code> — ユーザーファイル削除",
    "help.admin_get_user": "<code>/get user [id]</code> — 特定ユーザーのファイルを表示",
    "help.footer": "🏷️ <b>v3.0.4</b> | マルチユーザー版 | ユーザーごとの分離",
    "help.made_with": "❤️ を込めて python-telegram-bot で作成",

    "help.privacy_bottom": (
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔐 <b>お客様のセキュリティは私たちの最優先事項です。</b>\n"
        "開発チームを含め、誰もあなたのファイル内容を見ることはできません。\n"
        "お客様のデータを第三者と共有することは決してありません。"
    ),

    # ============================================
    # /get
    # ============================================
    "get.banned": "❌ あなたはこのボットからBANされています。",
    "get.max_range": "⚠️ 1ページ最大 {max_range} ファイルです。",
    "get.no_files": "📭 ファイルが見つかりません。メディアを送信して開始してください。",
    "get.error": "❌ エラーが発生しました。後でもう一度お試しください。",
    "get.invalid_input": "❌ 無効なユーザーIDまたはページ番号です。",
    "get.owner_label": "👤 所有者: {owner} (ID: {owner_id})",

    # ============================================
    # ファイルブラウザナビゲーション
    # ============================================
    "nav.view_page": "👁️ ページ {page} を表示",
    "nav.prev": "⬅️ 前へ",
    "nav.next": "次へ ➡️",
    "nav.back_all": "🔙 全ファイルに戻る",
    "nav.my_files": "📂 あなたのファイル",
    "nav.all_files": "📂 全ファイル (管理者ビュー)",
    "nav.user_files": "📂 {name}のファイル (ID: {uid})",
    "nav.page_of": "📄 {page}/{total}",
    "nav.jump_prompt": "📄 ページジャンプ (1-{total})\nページ番号を入力してください 👇",
    "nav.jump_alert": "ページ番号を入力してください (1-{total})",
    "nav.invalid_page": "❌ ページは1-{total}の範囲で指定してください。",
    "nav.invalid_number": "❌ 有効なページ番号を入力してください。",
    "nav.file_sent": "✅ {name} を送信しました！",
    "nav.send_failed": "⚠️ ファイル送信に失敗しました。再試行してください。",
    "nav.no_file": "⚠️ ファイルが見つかりません。",
    "nav.no_files_page": "⚠️ このページにはファイルがありません。",
    "nav.files_sent": "✅ {count} ファイルを送信しました！",
    "nav.too_fast": "⚠️ 操作が速すぎます！少し待ってください...",
    "nav.session_expired": "⚠️ ブラウザセッションが期限切れです。再度 /get を使用してください。",
    "nav.generic_error": "⚠️ エラーが発生しました。もう一度お試しください。",
    # ファイルナビゲーション（追加）
    "nav.range_indicator": "{start}-{end} / 全 {total} ファイル",
    "nav.navigation_hint": "📌 {num} / 全 {total} ファイル",
    "nav.navigation_hint_range": "📌 {start}-{end} / 全 {total} ファイル",
    "nav.invalid_file": "❌ ファイル番号は 1～{total} の範囲で入力してください。",

    # ============================================
    # /stats
    # ============================================
    "stats.title": "📊 個人統計",
    "stats.total_files": "📦 総ファイル数: {count:,}",
    "stats.quota": " / {limit:,} (クォータ)",
    "stats.total_size": "💾 総サイズ: {size}",
    "stats.by_type": "📂 タイプ別:",
    "stats.type_photo": "📸 {type}: {count:,} ({size})",
    "stats.type_video": "🎥 {type}: {count:,} ({size})",
    "stats.type_document": "📄 {type}: {count:,} ({size})",
    "stats.type_other": "📎 {type}: {count:,} ({size})",
    "stats.today_added": "📤 本日: +{count} ファイル",
    "stats.today_dup": "🔄 拒否 (重複): {count}",
    "stats.uptime": "🕐 稼働時間: {days}日 {hours}時間 {minutes}分",
    "stats.privacy_note": "🔒 この統計はあなただけが閲覧できます。",

    # ============================================
    # /mylimit
    # ============================================
    "limit.unlimited": "📊 クォータ: 無制限\n📁 保存ファイル: {current:,}\n💾 ストレージ: {size}",
    "limit.limited": "📊 クォータ: {current:,}/{limit:,} ファイル\n📥 残り: {remaining:,} ファイル\n💾 ストレージ: {size}",
    "limit.safe_note": "🛡️ クォータが満杯でもファイルは安全です。新しいファイルを追加できないだけです。",

    # ============================================
    # /delete (v3.0.3)
    # ============================================
    "delete.help_title": "🗑️ <b>ファイル削除</b>",
    "delete.help_desc": "保存したファイルを削除できます。番号は /get で確認してください。",
    "delete.help_commands": "📋 <b>コマンド:</b>",
    "delete.help_single": "<code>/delete [番号]</code> — 番号でファイルを削除（1=最新）",
    "delete.help_all": "<code>/delete all</code> — 全ファイルを削除",
    "delete.help_note": "⚠️ <b>警告:</b> 削除は元に戻せません！確認が求められます。",
    "delete.help_total": "📁 あなたのファイル総数: <b>{count:,}</b>",
    "delete.help_size": "💾 総サイズ: <b>{size}</b>",
    "delete.help_admin": "👤 ユーザー {name} (ID: {uid})\n📁 ファイル数: {count:,}\n💾 サイズ: {size}\n\n使用: /delete user {uid} [番号|all]",
    "delete.banned": "❌ あなたはBANされています。",
    "delete.invalid_format": "❌ 無効な形式です。/delete でヘルプを表示。",
    "delete.not_found": "❌ ファイル番号 {num} は見つかりません。/get で一覧を確認。",
    "delete.no_files": "📭 削除するファイルがありません。",
    "delete.confirm_single": (
        "⚠️ <b>ファイル削除の確認</b>\n\n"
        "{emoji} <b>#{num}</b> — {name}\n"
        "📁 タイプ: {type}\n"
        "💾 サイズ: {size}\n\n"
        "このファイルを削除してよろしいですか？"
    ),
    "delete.confirm_single_admin": (
        "⚠️ <b>ファイル削除の確認 (管理者)</b>\n\n"
        "👤 ユーザーID: {uid}\n"
        "{emoji} <b>#{num}</b> — {name}\n"
        "📁 タイプ: {type}\n"
        "💾 サイズ: {size}\n\n"
        "このファイルを削除してよろしいですか？"
    ),
    "delete.confirm_all": (
        "⚠️ <b>全ファイル削除の確認</b>\n\n"
        "📁 総ファイル数: <b>{count:,}</b>\n"
        "💾 総サイズ: <b>{size}</b>\n\n"
        "<b>すべて</b>のファイルを削除してよろしいですか？\n"
        "この操作は<b>元に戻せません！</b>"
    ),
    "delete.confirm_all_admin": (
        "⚠️ <b>全ファイル削除の確認 (管理者)</b>\n\n"
        "👤 ユーザー: {name} (ID: {uid})\n"
        "📁 総ファイル数: <b>{count:,}</b>\n"
        "💾 総サイズ: <b>{size}</b>\n\n"
        "このユーザーの<b>すべて</b>のファイルを削除してよろしいですか？"
    ),
    "delete.btn_confirm": "✅ はい、削除",
    "delete.btn_confirm_all": "✅ はい、すべて削除",
    "delete.btn_cancel": "❌ キャンセル",
    "delete.cancelled": "✅ 削除をキャンセルしました。",
    "delete.success_single": "✅ ファイル <b>#{num}</b> ({name}) を削除しました。",
    "delete.success_single_admin": "✅ ユーザー {uid} のファイル <b>#{num}</b> ({name}) を削除しました。",
    "delete.success_all": "✅ <b>{count:,}</b> ファイルを削除しました。",
    "delete.success_all_admin": "✅ ユーザー {uid} の <b>{count:,}</b> ファイルを削除しました。",
    "delete.failed": "❌ ファイル削除に失敗しました。再試行してください。",
    "delete.not_owner": "❌ あなたはこのファイルの所有者ではありません。",
    "delete.not_admin": "❌ 管理者権限がありません。",
    "delete.popup_session_expired": "⚠️ セッションが期限切れです。再試行してください。",

    # ============================================
    # /language
    # ============================================
    "language.select": "🌐 <b>言語選択:</b>\n\n言語コードを入力: /language [code]\n\n{langs}",
    "language.current": "\n\n📌 現在: {current}",
    "language.changed": "✅ 言語を {name} に変更しました",
    "language.invalid": "❌ 未対応の言語です。使用可能: {codes}",
    "language.unsupported": "❌ 未対応の言語です。",
    "language.lang_item": "{emoji} {name} — <code>/language {code}</code>\n",
    "language.select_title": "🌐 <b>言語選択:</b>",

    # ============================================
    # @admin
    # ============================================
    "admin_msg.format": "✍️ 形式: @admin [メッセージ]\n例: @admin ボットがエラーになりました",
    "admin_msg.sent": "✅ 管理者にメッセージを送信しました。できるだけ早く返信します。",
    "admin_msg.notify": "📩 ユーザーからのメッセージ\n👤 {name} (ID: {uid})\n💬 {message}\n\n返信: /reply {msg_id} [メッセージ]",

    # ============================================
    # 管理パネル
    # ============================================
    "admin.access_denied": "❌ アクセス拒否。管理者専用です。",
    "admin.panel_title": "🔑 管理パネル",
    "admin.panel_users": "👥 総ユーザー数: {count:,}",
    "admin.panel_files": "📁 総ファイル数: {count:,}",
    "admin.panel_admins": "🛡️ 現在の管理者数: {count}",
    "admin.panel_unread": "📩 新着メッセージ: {count} ⚠️",
    "admin.panel_commands": (
        "📋 コマンド:\n"
        "/admin users — 全ユーザー一覧\n"
        "/admin user [id] — ユーザー詳細\n"
        "/admin add [id] — 管理者追加\n"
        "/admin remove [id] — 管理者削除\n"
        "/admin setlimit [id] [n] — 制限設定\n"
        "/admin stats — 全体統計\n"
        "/admin messages — ユーザーメッセージ\n"
        "/ban [id] — ユーザーBAN\n"
        "/unban [id] — BAN解除\n"
        "/broadcast [メッセージ] — 全ユーザーに配信\n"
        "/reply [id] [メッセージ] — 返信\n"
        "/delete user [id] [n|all] — ユーザーファイル削除\n"
        "/get user [id] — 特定ユーザーファイル表示"
    ),
    # ============================================
    # 管理パネル - ユーザー一覧ナビゲーション
    # ============================================
    "admin_users.invalid_page": "❌ 無効なページです。",
    "admin_users.access_denied": "❌ アクセス拒否。",
    "admin.users_title": "👥 登録ユーザー",
    "admin.users_item": "{i}. {name} (ID: {uid}) — {files:,} ファイル{banned}",
    "admin.users_more": "\n... 他 {count} 人",
    "admin.users_empty": "まだ登録ユーザーがいません。",
    "admin.user_title": "👤 ユーザー詳細: {name}",
    "admin.user_id": "ID: {uid}",
    "admin.user_username": "ユーザー名: @{username}",
    "admin.user_banned": "BAN状態: {status}",
    "admin.user_files": "ファイル: {files:,} / {limit}",
    "admin.user_storage": "ストレージ: {size}",
    "admin.user_by_type": "📂 タイプ別:",
    "admin.user_not_found": "❌ ユーザーが見つかりません。",
    "admin.add_super_only": "❌ 管理者追加はスーパー管理者のみ可能です。",
    "admin.add_super_cannot": "❌ スーパー管理者は変更できません。",
    "admin.add_success": "✅ ユーザー {uid} を管理者に昇格しました。",
    "admin.add_already": "⚠️ 既に管理者です。",
    "admin.remove_super_only": "❌ 管理者削除はスーパー管理者のみ可能です。",
    "admin.remove_super_cannot": "❌ スーパー管理者は削除できません。",
    "admin.remove_success": "✅ ユーザー {uid} を管理者から降格しました。",
    "admin.remove_not": "⚠️ 管理者ではありません。",
    "admin.setlimit_success": "✅ ユーザー {uid} のファイル制限を {limit:,} に設定しました。",
    "admin.global_title": "📊 全体統計",
    "admin.global_users": "👥 総ユーザー数: {count:,}",
    "admin.global_files": "📁 総ファイル数: {count:,}",
    "admin.global_storage": "💾 総ストレージ: {size}",
    "admin.global_served": "📤 提供ファイル総数: {count:,}",
    "admin.global_top": "🏆 トップ5 ユーザー:",
    "admin.global_top_item": "  {i}. {name} — {files:,} ファイル",
    "admin.broadcast_format": "📢 形式: /broadcast [メッセージ]\n例: /broadcast 22:00よりメンテナンス",
    "admin.broadcast_sending": "📤 {total} 人のユーザーにブロードキャスト送信中...",
    "admin.broadcast_progress": (
        "📤 送信中...\n"
        "▸ 進捗: {sent}/{total}\n"
        "▸ 成功: {success}\n"
        "▸ 失敗: {failed}"
    ),
    "admin.broadcast_done": "✅ ブロードキャスト完了\n📤 送信完了: {success}\n❌ 失敗: {failed}\n👥 合計: {total}",
    "admin.broadcast_msg": "📢 管理者からのお知らせ\n\n{message}",
    "admin.broadcast_skipped": "\n⚠️ BAN/無効ユーザー {skipped} 人をスキップ",
    "admin.reply_format": "↩️ 形式: /reply [メッセージID] [返信内容]\n/admin messages でメッセージ一覧を表示",
    "admin.reply_invalid_id": "❌ 無効なメッセージIDです。",
    "admin.reply_not_found": "❌ メッセージが見つかりません。",
    "admin.reply_already": "⚠️ このメッセージには既に返信済みです。",
    "admin.reply_failed": "❌ 返信送信失敗: {error}",
    "admin.reply_sent": "✅ ユーザー {uid} に返信を送信しました",
    "admin.reply_to_user": "🔰 管理者があなたのメッセージに返信しました:\n\n💬 あなたのメッセージ: {original}\n\n↩️ 管理者の返信: {reply}",
    "admin.reply_failed_delivery": "❌ 返信送信失敗: メッセージを配信できませんでした。",
    "admin.messages_title": "📩 ユーザーからのメッセージ",
    "admin.messages_item": "#{id} | {name} (ID: {uid})\n💬 {text}\n返信: /reply {id} [内容]\n\n",
    "admin.messages_empty": "📭 新着メッセージなし。",
    "admin.messages_max": "\n⚠️ 最新20件のメッセージを表示中。",
    "admin.ban_usage": "使用法: /ban [user_id]",
    "admin.ban_invalid": "❌ 無効なユーザーID。",
    "admin.ban_super": "❌ スーパー管理者はBANできません。",
    "admin.ban_success": "🚫 ユーザー {uid} をBANしました。",
    "admin.unban_usage": "使用法: /unban [user_id]",
    "admin.unban_success": "✅ ユーザー {uid} のBANを解除しました。",

    # ============================================
    # BAN/解除確認 (v3.0.4 - i18n)
    # ============================================
    "ban.confirm_title": "⚠️ <b>ユーザーBAN確認</b>",
    "ban.confirm_body": "👤 名前: <b>{name}</b>\n🆔 ID: <code>{uid}</code>\n📛 ユーザー名: {username}\n📁 ファイル数: {files:,}\n\nこのユーザーを<b>BAN</b>してよろしいですか？\nボットを使用できなくなります。",
    "ban.already_banned": "⚠️ ユーザー {uid} は既にBANされています。",
    "ban.success": "🚫 <b>ユーザーBAN完了</b>\n\n👤 {name}\n🆔 <code>{uid}</code>\n\n✅ このユーザーはボットを使用できません。\n🗑️ キャッシュがクリアされました。",
    "unban.confirm_title": "🔓 <b>BAN解除確認</b>",
    "unban.confirm_body": "👤 名前: <b>{name}</b>\n🆔 ID: <code>{uid}</code>\n📛 ユーザー名: {username}\n📁 ファイル数: {files:,}\n\nこのユーザーの<b>BANを解除</b>してよろしいですか？\n再びボットを使用できるようになります。",
    "unban.not_banned": "⚠️ ユーザー {uid} はBANされていません。",
    "unban.success": "🔓 <b>BAN解除完了</b>\n\n👤 {name}\n🆔 <code>{uid}</code>\n\n✅ このユーザーは再びボットを使用できます。",
    "ban.cancel": "✅ 操作をキャンセルしました。",

    "ban.btn_confirm": "🚫 はい、BANする",
    "unban.btn_confirm": "🔓 はい、解除する",
    "ban.btn_cancel": "❌ キャンセル",

    "ban.popup_session_expired": "⚠️ セッション期限切れ。再試行してください。",
    "ban.popup_access_denied": "❌ アクセス拒否。",
    "ban.popup_not_initiator": "❌ 操作を開始した管理者のみ確認できます。",
    "ban.popup_cannot_ban_super": "❌ スーパー管理者はBANできません！",
    "ban.popup_already_banned": "BAN済み",
    "ban.popup_not_banned": "BANされていません",
    "ban.popup_cancelled": "キャンセルしました",
    "ban.popup_success_ban": "✅ ユーザーをBANしました！",
    "ban.popup_success_unban": "✅ BANを解除しました！",

    # ============================================
    # メディアハンドラー
    # ============================================
    "media.queue_full": "⚠️ キューがいっぱいです（最大 {maxsize} ファイル）。しばらく待ってから送信してください。",
    "media.quota_full": "❌ クォータが上限に達しています。\n/mylimit で詳細を確認。",
    "media.file_too_large": "❌ ファイルが大きすぎます ({size} バイト)。\n最大: {max_mb} MB",
    "media.global_full": "❌ 申し訳ありません、全体ストレージが満杯です。\nしばらく経ってからお試しください。",
}