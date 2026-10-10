"""
Chinese (Simplified) Translation Pack
Telegram Media Storage Bot v3.0.4
"""

TEXTS = {
    # ============================================
    # /start
    # ============================================
    "start.welcome": "👋 <b>欢迎，{name}！</b>",
    "start.bot_desc": "🤖 <b>Telegram 媒体存储机器人 v3.0.4</b>\n智能多用户媒体存储，支持自动去重、每用户加密和文件删除功能。",
    "start.features_title": "✨ <b>主要功能：</b>",
    "start.feature_save": "• 保存照片、视频和文档",
    "start.feature_dedup": "• 自动检测并拒绝重复文件（按用户隔离）",
    "start.feature_privacy": "• 隔离存储 — 您的文件仅自己可见",
    "start.feature_autodel": "• {desc}",
    "start.feature_spoiler": "• <b>图片说明与隐藏内容将被忽略</b>（仅保存文件本身）",
    "start.feature_album": "• 完全支持多文件相册",
    "start.feature_forward": "• 转发的媒体也会被保存",
    "start.feature_stats": "• 完整的实时个人统计",
    "start.feature_delete": "• 安全确认后删除文件",
    "start.howto_title": "🚀 <b>使用方法：</b>",
    "start.howto_desc": "发送或转发任意媒体给机器人即可！",
    "start.commands_title": "📖 <b>指令列表：</b>",
    "start.cmd_get": "/get — 打开交互式文件浏览器",
    "start.cmd_stats": "/stats — 统计信息与运行时间",
    "start.cmd_limit": "/mylimit — 查看剩余配额",
    "start.cmd_delete": "/delete — 删除已存储文件",
    "start.cmd_help": "/help — 完整帮助指南",
    "start.cmd_lang": "/language — 切换语言（共8种）",
    "start.cmd_admin_msg": "@admin [消息] — 联系管理员",
    "start.admin_title": "🔑 <b>管理员模式已激活</b>",
    "start.admin_cmd": "/admin — 管理员控制面板",
    "start.privacy_title": (
        "🔒 <b>隐私保证</b>\n"
        "• 您的每个文件 <b>隔离存储</b>，仅您可访问。\n"
        "• <b>管理员无法查看</b> 或打开任何用户文件。\n"
        "• 不与任何第三方（包括其他用户）共享数据。\n"
        "• 系统使用受保护的存储，始终保障您的隐私。"
    ),
    "start.autodel_desc_media": "媒体消息将在 {delay} 秒后自动删除",
    "start.autodel_desc_all": "消息将在 {delay} 秒后自动删除",

    # ============================================
    # /help
    # ============================================
    "help.title": "📖 <b>完整帮助</b>",
    "help.subtitle": "Telegram 媒体存储机器人 v3.0.4",
    "help.section1_title": "📤 <b>1. 保存媒体</b>",
    "help.section1_desc": "只需发送或转发媒体给机器人，一切自动完成。",
    "help.section1_support": "✅ 支持：照片、视频、文档",
    "help.section1_album": "✅ 多文件相册自动处理",
    "help.section1_forward": "✅ 从其他会话/频道/群组转发的媒体同样保存",
    "help.section1_duplicate": "🚫 账户内重复文件自动拒绝",
    "help.section1_spoiler": "🧹 图片说明与隐藏内容不保存（仅保存原始文件）",
    "help.section1_delete": "🗑️ 原始消息在 {delay} 秒后删除",
    "help.section2_title": "📥 <b>2. 获取文件 — /get</b>",
    "help.section2_intro": "使用 <code>/get</code> 打开 <b>交互式文件浏览器</b>。",
    "help.section2_nav_title": "🎮 <b>文件浏览器导航：</b>",
    "help.section2_nav1": "• 点击 <b>文件编号</b> — 直接下载该文件",
    "help.section2_nav2": "• 点击 <b>👁️ 查看页面</b> — 下载本页所有文件",
    "help.section2_nav3": "• ⬅️ <b>上一页</b> / <b>下一页</b> ➡️ — 翻页",
    "help.section2_nav4": "• 点击 <b>📄 页码</b> — 跳转至该页",
    "help.section2_nav5": "• 在提示时输入页码 — 快速跳转",
    "help.section2_nav6": "• 每页最多显示 10 个文件",
    "help.section2_admin": "\n🔑 <b>管理员专用：</b>\n" +
                          "<code>/get user [ID]</code> — 查看其他用户的文件\n" +
                          "<code>/get</code>（管理员） — 查看所有用户的全部文件",
    "help.section2_delete": "\n🗑️ 下载结果将在 {delay} 秒后自动删除",
    "help.section3_title": "📊 <b>3. 统计 — /stats</b>",
    "help.section3_files": "• 文件总数与存储大小",
    "help.section3_breakdown": "• 按类型细分（照片/视频/文档）",
    "help.section3_today": "• 今日上传与重复数量",
    "help.section3_uptime": "• 机器人运行时间（天/小时/分钟）",
    "help.section4_title": "📋 <b>4. 配额 — /mylimit</b>",
    "help.section4_default": "• 默认每用户限制：{limit:,} 个文件",
    "help.section4_admin": "• 管理员可调整每位用户的配额",
    "help.section4_unlimited": "• 0 = 无限制",
    "help.section5_title": "🗑️ <b>5. 删除文件 — /delete</b>",
    "help.section5_cmd": "<code>/delete [编号]</code> — 删除指定编号的文件",
    "help.section5_all": "<code>/delete all</code> — 删除您的所有文件",
    "help.section5_note": "⚠️ 删除前总是需要确认！",
    "help.section6_title": "💬 <b>6. 联系管理员</b>",
    "help.section6_cmd": "输入 <code>@admin [您的消息]</code>",
    "help.section6_example": "示例：<code>@admin 上传视频失败</code>",
    "help.section6_reply": "管理员将通过机器人回复。",
    "help.section7_title": "🛡️ <b>7. 隐私与安全</b>",
    "help.section7_private": (
        "• 您存储的每一个文件 <b>只有您可以访问</b>。\n"
        "  任何人——包括管理员——都无法查看、打开或下载您的文件。"
    ),
    "help.section7_noshare": (
        "• <b>数据零共享。</b> 您的文件绝不会展示给其他用户，\n"
        "  您的统计数据也是私密的。"
    ),
    "help.section7_clean": (
        "• 您发送给机器人的原始消息将在几秒后 <b>自动删除</b>。\n"
        "  只有安全存储中的文件会被保留。"
    ),
    "help.section7_dedup": (
        "• 重复检测 <b>按用户进行</b>。已存在于您账户中的文件不会被\n"
        "  再次接受，从而保持存储高效。"
    ),
    "help.section7_encryption": (
        "• 存储采用 <b>严格隔离</b> 机制和系统级访问保护。\n"
        "  您的数据绝不会被您自身会话以外的进程读取。"
    ),
    "help.section8_title": "🌐 <b>8. 语言 — /language</b>",
    "help.section8_desc": "更改机器人的显示语言（共8种语言可选）。",
    "help.section8_list": "<code>/language</code> — 显示语言选择菜单",
    "help.section8_set": "点击所需语言的按钮",
    "help.section8_langs": "🇮🇩 ID | 🇬🇧 EN | 🇷🇺 RU | 🇨🇳 ZH | 🇯🇵 JA | 🇪🇸 ES | 🇮🇳 HI | 🇧🇷 PT",
    "help.section9_title": "💡 <b>9. 小贴士</b>",
    "help.section9_tip1": "• 转发来自频道/群组的媒体以保存它们",
    "help.section9_tip2": "• 随时使用 /get 取回文件",
    "help.section9_tip3": "• 图片说明与隐藏内容不会被存储（仅原始文件）",
    "help.section9_tip4": "• 照片/视频相册以组为单位处理（高效）",
    "help.admin_title": "🔑 <b>10. 管理员命令</b>",
    "help.admin_list": "<code>/admin</code> — 管理员面板",
    "help.admin_users": "<code>/admin users</code> — 列出所有用户",
    "help.admin_user": "<code>/admin user [id]</code> — 用户详情",
    "help.admin_add": "<code>/admin add [id]</code> — 添加管理员（仅超级管理员）",
    "help.admin_remove": "<code>/admin remove [id]</code> — 移除管理员（仅超级管理员）",
    "help.admin_setlimit": "<code>/admin setlimit [id] [n]</code> — 设置用户配额",
    "help.admin_stats": "<code>/admin stats</code> — 全局统计",
    "help.admin_messages": "<code>/admin messages</code> — 用户消息",
    "help.admin_ban": "<code>/ban [id]</code> — 封禁用户",
    "help.admin_unban": "<code>/unban [id]</code> — 解封用户",
    "help.admin_broadcast": "<code>/broadcast [消息]</code> — 向全体用户广播",
    "help.admin_reply": "<code>/reply [id] [文本]</code> — 回复用户消息",
    "help.admin_delete": "<code>/delete user [id] [编号|all]</code> — 删除用户文件",
    "help.admin_get_user": "<code>/get user [id]</code> — 查看特定用户的文件",
    "help.footer": "🏷️ <b>v3.0.4</b> | 多用户版 | 每用户隔离",
    "help.made_with": "用 ❤️ 和 python-telegram-bot 制作",

    "help.privacy_bottom": (
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔐 <b>您的安全是我们的首要任务。</b>\n"
        "任何人——包括开发团队——都无法查看您文件的内容。\n"
        "我们绝不会将您的数据分享给第三方。"
    ),

    # ============================================
    # /get
    # ============================================
    "get.banned": "❌ 您已被此机器人封禁。",
    "get.max_range": "⚠️ 每页最多 {max_range} 个文件。",
    "get.no_files": "📭 未找到文件。请发送媒体以开始。",
    "get.error": "❌ 发生错误。请稍后重试。",
    "get.invalid_input": "❌ 无效的用户 ID 或页码。",
    "get.owner_label": "👤 所有者：{owner} (ID: {owner_id})",

    # ============================================
    # 文件浏览器导航
    # ============================================
    "nav.view_page": "👁️ 查看第 {page} 页",
    "nav.prev": "⬅️ 上一页",
    "nav.next": "下一页 ➡️",
    "nav.back_all": "🔙 返回全部文件",
    "nav.my_files": "📂 我的文件",
    "nav.all_files": "📂 全部文件（管理员视图）",
    "nav.user_files": "📂 {name} 的文件 (ID: {uid})",
    "nav.page_of": "📄 {page}/{total}",
    "nav.jump_prompt": "📄 跳转到第？页 (1-{total})\n在下方输入页码 👇",
    "nav.jump_alert": "请输入页码 (1-{total})",
    "nav.invalid_page": "❌ 页码必须在 1-{total} 之间。",
    "nav.invalid_number": "❌ 请输入有效的页码。",
    "nav.file_sent": "✅ {name} 已发送！",
    "nav.send_failed": "⚠️ 文件发送失败。请重试。",
    "nav.no_file": "⚠️ 文件未找到。",
    "nav.no_files_page": "⚠️ 本页没有文件。",
    "nav.files_sent": "✅ 已发送 {count} 个文件！",
    "nav.too_fast": "⚠️ 操作过快！请稍候...",
    "nav.session_expired": "⚠️ 浏览器会话已过期。请重新使用 /get。",
    "nav.generic_error": "⚠️ 发生错误。请重试。",
    # 文件导航（附加）
    "nav.range_indicator": "{start}-{end} / 共 {total} 个文件",
    "nav.navigation_hint": "📌 {num} / 共 {total} 个文件",
    "nav.navigation_hint_range": "📌 {start}-{end} / 共 {total} 个文件",
    "nav.invalid_file": "❌ 文件编号必须在 1-{total} 之间。",

    # ============================================
    # /stats
    # ============================================
    "stats.title": "📊 个人统计",
    "stats.total_files": "📦 文件总数：{count:,}",
    "stats.quota": " / {limit:,}（配额）",
    "stats.total_size": "💾 总大小：{size}",
    "stats.by_type": "📂 按类型：",
    "stats.type_photo": "📸 {type}：{count:,}（{size}）",
    "stats.type_video": "🎥 {type}：{count:,}（{size}）",
    "stats.type_document": "📄 {type}：{count:,}（{size}）",
    "stats.type_other": "📎 {type}：{count:,}（{size}）",
    "stats.today_added": "📤 今日新增：+{count} 个文件",
    "stats.today_dup": "🔄 已拒绝（重复）：{count}",
    "stats.uptime": "🕐 运行时间：{days}天 {hours}小时 {minutes}分",
    "stats.privacy_note": "🔒 这些统计只有您自己可见。",

    # ============================================
    # /mylimit
    # ============================================
    "limit.unlimited": "📊 配额：无限制\n📁 已存储文件：{current:,}\n💾 存储占用：{size}",
    "limit.limited": "📊 配额：{current:,}/{limit:,} 个文件\n📥 剩余：{remaining:,} 个文件\n💾 存储占用：{size}",
    "limit.safe_note": "🛡️ 即使配额已满，您的文件仍然安全。只是无法添加新文件。",

    # ============================================
    # /delete (v3.0.3)
    # ============================================
    "delete.help_title": "🗑️ <b>删除文件</b>",
    "delete.help_desc": "您可以删除已存储的文件。使用 /get 查看文件编号。",
    "delete.help_commands": "📋 <b>命令：</b>",
    "delete.help_single": "<code>/delete [编号]</code> — 按编号删除文件（1 = 最新）",
    "delete.help_all": "<code>/delete all</code> — 删除您的全部文件",
    "delete.help_note": "⚠️ <b>警告：</b> 删除不可撤销！操作前需要确认。",
    "delete.help_total": "📁 您的文件总数：<b>{count:,}</b>",
    "delete.help_size": "💾 总大小：<b>{size}</b>",
    "delete.help_admin": "👤 用户 {name} (ID: {uid})\n📁 文件数：{count:,}\n💾 大小：{size}\n\n使用 /delete user {uid} [编号|all]",
    "delete.banned": "❌ 您已被封禁。",
    "delete.invalid_format": "❌ 格式无效。使用 /delete 查看帮助。",
    "delete.not_found": "❌ 未找到编号为 {num} 的文件。用 /get 查看文件列表。",
    "delete.no_files": "📭 没有可删除的文件。",
    "delete.confirm_single": (
        "⚠️ <b>确认删除文件</b>\n\n"
        "{emoji} <b>#{num}</b> — {name}\n"
        "📁 类型：{type}\n"
        "💾 大小：{size}\n\n"
        "您确定要删除这个文件吗？"
    ),
    "delete.confirm_single_admin": (
        "⚠️ <b>确认删除文件（管理员）</b>\n\n"
        "👤 用户 ID：{uid}\n"
        "{emoji} <b>#{num}</b> — {name}\n"
        "📁 类型：{type}\n"
        "💾 大小：{size}\n\n"
        "您确定要删除这个文件吗？"
    ),
    "delete.confirm_all": (
        "⚠️ <b>确认删除全部文件</b>\n\n"
        "📁 文件总数：<b>{count:,}</b>\n"
        "💾 总大小：<b>{size}</b>\n\n"
        "您确定要删除 <b>全部</b> 文件吗？\n"
        "此操作 <b>不可撤销！</b>"
    ),
    "delete.confirm_all_admin": (
        "⚠️ <b>确认删除全部文件（管理员）</b>\n\n"
        "👤 用户：{name} (ID: {uid})\n"
        "📁 文件总数：<b>{count:,}</b>\n"
        "💾 总大小：<b>{size}</b>\n\n"
        "您确定要删除此用户的 <b>全部</b> 文件吗？"
    ),
    "delete.btn_confirm": "✅ 是的，删除",
    "delete.btn_confirm_all": "✅ 是的，全部删除",
    "delete.btn_cancel": "❌ 取消",
    "delete.cancelled": "✅ 删除已取消。",
    "delete.success_single": "✅ 文件 <b>#{num}</b>（{name}）已删除。",
    "delete.success_single_admin": "✅ 用户 {uid} 的文件 <b>#{num}</b>（{name}）已删除。",
    "delete.success_all": "✅ 已删除 <b>{count:,}</b> 个文件。",
    "delete.success_all_admin": "✅ 已删除用户 {uid} 的 <b>{count:,}</b> 个文件。",
    "delete.failed": "❌ 删除文件失败。请重试。",
    "delete.not_owner": "❌ 您不是该文件的所有者。",
    "delete.not_admin": "❌ 您没有管理员权限。",
    "delete.popup_session_expired": "⚠️ 会话已过期。请重试。",

    # ============================================
    # /language
    # ============================================
    "language.select": "🌐 <b>选择语言：</b>\n\n输入 /language [代码]\n\n{langs}",
    "language.current": "\n\n📌 当前：{current}",
    "language.changed": "✅ 语言已切换为 {name}",
    "language.invalid": "❌ 不支持的语言。可用：{codes}",
    "language.unsupported": "❌ 不支持该语言。",
    "language.lang_item": "{emoji} {name} — <code>/language {code}</code>\n",
    "language.select_title": "🌐 <b>选择语言：</b>",

    # ============================================
    # @admin
    # ============================================
    "admin_msg.format": "✍️ 格式：@admin [消息]\n示例：@admin 机器人出错了",
    "admin_msg.sent": "✅ 消息已发送给管理员。我们会尽快回复。",
    "admin_msg.notify": "📩 用户消息\n👤 {name} (ID: {uid})\n💬 {message}\n\n回复：/reply {msg_id} [消息]",

    # ============================================
    # 管理员面板
    # ============================================
    "admin.access_denied": "❌ 拒绝访问。仅限管理员。",
    "admin.panel_title": "🔑 管理员面板",
    "admin.panel_users": "👥 用户总数：{count:,}",
    "admin.panel_files": "📁 文件总数：{count:,}",
    "admin.panel_admins": "🛡️ 当前管理员：{count}",
    "admin.panel_unread": "📩 新消息：{count} ⚠️",
    "admin.panel_commands": (
        "📋 命令：\n"
        "/admin users — 列出所有用户\n"
        "/admin user [id] — 用户详情\n"
        "/admin add [id] — 添加管理员\n"
        "/admin remove [id] — 移除管理员\n"
        "/admin setlimit [id] [n] — 设置限制\n"
        "/admin stats — 全局统计\n"
        "/admin messages — 用户消息\n"
        "/ban [id] — 封禁用户\n"
        "/unban [id] — 解封用户\n"
        "/broadcast [消息] — 广播给所有用户\n"
        "/reply [id] [消息] — 回复用户消息\n"
        "/delete user [id] [n|all] — 删除用户文件\n"
        "/get user [id] — 查看特定用户的文件"
    ),
    # ============================================
    # 管理员面板 - 用户列表导航
    # ============================================
    "admin_users.invalid_page": "❌ 无效的页码。",
    "admin_users.access_denied": "❌ 拒绝访问。",
    "admin.users_title": "👥 已注册用户",
    "admin.users_item": "{i}. {name} (ID: {uid}) — {files:,} 个文件{banned}",
    "admin.users_more": "\n... 还有 {count} 人。",
    "admin.users_empty": "暂无注册用户。",
    "admin.user_title": "👤 用户详情：{name}",
    "admin.user_id": "ID：{uid}",
    "admin.user_username": "用户名：@{username}",
    "admin.user_banned": "封禁状态：{status}",
    "admin.user_files": "文件：{files:,} / {limit}",
    "admin.user_storage": "存储：{size}",
    "admin.user_by_type": "📂 按类型：",
    "admin.user_not_found": "❌ 用户未找到。",
    "admin.add_super_only": "❌ 仅超级管理员可添加管理员。",
    "admin.add_super_cannot": "❌ 无法修改超级管理员。",
    "admin.add_success": "✅ 用户 {uid} 已提升为管理员。",
    "admin.add_already": "⚠️ 该用户已是管理员。",
    "admin.remove_super_only": "❌ 仅超级管理员可移除管理员。",
    "admin.remove_super_cannot": "❌ 无法移除超级管理员。",
    "admin.remove_success": "✅ 已免除用户 {uid} 的管理员权限。",
    "admin.remove_not": "⚠️ 该用户不是管理员。",
    "admin.setlimit_success": "✅ 用户 {uid} 的文件限制已设为 {limit:,}。",
    "admin.global_title": "📊 全局统计",
    "admin.global_users": "👥 用户总数：{count:,}",
    "admin.global_files": "📁 文件总数：{count:,}",
    "admin.global_storage": "💾 总存储：{size}",
    "admin.global_served": "📤 已提供文件总数：{count:,}",
    "admin.global_top": "🏆 Top 5 用户：",
    "admin.global_top_item": "  {i}. {name} — {files:,} 个文件",
    "admin.broadcast_format": "📢 格式：/broadcast [消息]\n示例：/broadcast 服务器将于22:00维护",
    "admin.broadcast_sending": "📤 正在向 {total} 位用户发送广播...",
    "admin.broadcast_progress": (
        "📤 正在发送广播...\n"
        "▸ 进度：{sent}/{total}\n"
        "▸ 成功：{success}\n"
        "▸ 失败：{failed}"
    ),
    "admin.broadcast_done": "✅ 广播完成\n📤 已送达：{success}\n❌ 失败：{failed}\n👥 总计：{total}",
    "admin.broadcast_msg": "📢 管理员公告\n\n{message}",
    "admin.broadcast_skipped": "\n⚠️ 已跳过 {skipped} 位被封禁/不活跃用户",
    "admin.reply_format": "↩️ 格式：/reply [消息id] [回复内容]\n使用 /admin messages 查看消息列表",
    "admin.reply_invalid_id": "❌ 无效的消息 ID。",
    "admin.reply_not_found": "❌ 消息未找到。",
    "admin.reply_already": "⚠️ 该消息已被回复。",
    "admin.reply_failed": "❌ 回复发送失败：{error}",
    "admin.reply_sent": "✅ 回复已发送给用户 {uid}",
    "admin.reply_to_user": "🔰 管理员回复了您的消息：\n\n💬 您的消息：{original}\n\n↩️ 管理员回复：{reply}",
    "admin.reply_failed_delivery": "❌ 回复发送失败：消息无法送达。",
    "admin.messages_title": "📩 用户消息",
    "admin.messages_item": "#{id} | {name} (ID: {uid})\n💬 {text}\n回复：/reply {id} [内容]\n\n",
    "admin.messages_empty": "📭 暂无新消息。",
    "admin.messages_max": "\n⚠️ 显示最近 20 条消息。",
    "admin.ban_usage": "用法：/ban [user_id]",
    "admin.ban_invalid": "❌ 无效的用户 ID。",
    "admin.ban_super": "❌ 无法封禁超级管理员。",
    "admin.ban_success": "🚫 用户 {uid} 已被封禁。",
    "admin.unban_usage": "用法：/unban [user_id]",
    "admin.unban_success": "✅ 用户 {uid} 已解封。",

    # ============================================
    # 封禁/解封确认 (v3.0.4 - i18n)
    # ============================================
    "ban.confirm_title": "⚠️ <b>确认封禁用户</b>",
    "ban.confirm_body": "👤 姓名：<b>{name}</b>\n🆔 ID：<code>{uid}</code>\n📛 用户名：{username}\n📁 文件数：{files:,}\n\n您确定要 <b>封禁</b> 此用户吗？\n他将无法再使用机器人。",
    "ban.already_banned": "⚠️ 用户 {uid} 已被封禁。",
    "ban.success": "🚫 <b>用户已封禁</b>\n\n👤 {name}\n🆔 <code>{uid}</code>\n\n✅ 该用户不能再使用机器人。\n🗑️ 其缓存已清除。",
    "unban.confirm_title": "🔓 <b>确认解封用户</b>",
    "unban.confirm_body": "👤 姓名：<b>{name}</b>\n🆔 ID：<code>{uid}</code>\n📛 用户名：{username}\n📁 文件数：{files:,}\n\n您确定要 <b>解封</b> 此用户吗？\n他将可以重新使用机器人。",
    "unban.not_banned": "⚠️ 用户 {uid} 当前未被封禁。",
    "unban.success": "🔓 <b>用户已解封</b>\n\n👤 {name}\n🆔 <code>{uid}</code>\n\n✅ 该用户现在可以重新使用机器人。",
    "ban.cancel": "✅ 操作已取消。",

    "ban.btn_confirm": "🚫 是，封禁",
    "unban.btn_confirm": "🔓 是，解封",
    "ban.btn_cancel": "❌ 取消",

    "ban.popup_session_expired": "⚠️ 会话已过期。请重试。",
    "ban.popup_access_denied": "❌ 拒绝访问。",
    "ban.popup_not_initiator": "❌ 只有发起操作的管理员可以确认。",
    "ban.popup_cannot_ban_super": "❌ 无法封禁超级管理员！",
    "ban.popup_already_banned": "已被封禁",
    "ban.popup_not_banned": "未被封禁",
    "ban.popup_cancelled": "已取消",
    "ban.popup_success_ban": "✅ 用户封禁成功！",
    "ban.popup_success_unban": "✅ 用户解封成功！",

    # ============================================
    # 媒体处理
    # ============================================
    "media.queue_full": "⚠️ 您的队列已满（最多 {maxsize} 个文件）。请稍后再发送。",
    "media.quota_full": "❌ 您的配额已满。\n使用 /mylimit 查看详情。",
    "media.file_too_large": "❌ 文件过大（{size} 字节）。\n最大允许：{max_mb} MB",
    "media.global_full": "❌ 抱歉，全局存储已满。\n请稍后再试。",
}