"""
English Translation Pack
Telegram Media Storage Bot v3.0.4
"""

TEXTS = {
    # ============================================
    # /start
    # ============================================
    "start.welcome": "👋 <b>Welcome, {name}!</b>",
    "start.bot_desc": "🤖 <b>Telegram Media Storage Bot v3.0.4</b>\nA smart multi-user media storage bot with automatic deduplication, per-user encryption, and file deletion features.",
    "start.features_title": "✨ <b>Key Features:</b>",
    "start.feature_save": "• Save photos, videos, and documents",
    "start.feature_dedup": "• Automatic duplicate detection & rejection (per user)",
    "start.feature_privacy": "• Isolated storage — your files are visible only to you",
    "start.feature_autodel": "• {desc}",
    "start.feature_spoiler": "• <b>Captions & spoilers are ignored</b> (only files stored)",
    "start.feature_album": "• Multi-file albums fully supported",
    "start.feature_forward": "• Forwarded media is saved as well",
    "start.feature_stats": "• Complete & real-time personal statistics",
    "start.feature_delete": "• Delete files with safe confirmation",
    "start.howto_title": "🚀 <b>How to Use:</b>",
    "start.howto_desc": "Send / forward any media to the bot — done!",
    "start.commands_title": "📖 <b>Commands:</b>",
    "start.cmd_get": "/get — Open interactive file browser",
    "start.cmd_stats": "/stats — Statistics & uptime",
    "start.cmd_limit": "/mylimit — Check remaining quota",
    "start.cmd_delete": "/delete — Remove stored files",
    "start.cmd_help": "/help — Full help guide",
    "start.cmd_lang": "/language — Switch language (8 available)",
    "start.cmd_admin_msg": "@admin [message] — Contact admin",
    "start.admin_title": "🔑 <b>Admin Mode Active</b>",
    "start.admin_cmd": "/admin — Admin control panel",
    "start.privacy_title": (
        "🔒 <b>Privacy Guaranteed</b>\n"
        "• Each of your files is stored <b>in isolation</b> and accessible only by you.\n"
        "• <b>Admins cannot view</b> or open any user's files.\n"
        "• No data is shared with third parties, including other users.\n"
        "• Our system uses protected storage to keep your privacy always intact."
    ),
    "start.autodel_desc_media": "Media messages are auto-deleted after {delay} seconds",
    "start.autodel_desc_all": "Messages are auto-deleted after {delay} seconds",

    # ============================================
    # /help
    # ============================================
    "help.title": "📖 <b>COMPLETE HELP</b>",
    "help.subtitle": "Telegram Media Storage Bot v3.0.4",
    "help.section1_title": "📤 <b>1. Saving Media</b>",
    "help.section1_desc": "Simply send or forward any media to the bot — everything is automatic.",
    "help.section1_support": "✅ Supported: Photos, Videos, Documents",
    "help.section1_album": "✅ Multi-file albums processed automatically",
    "help.section1_forward": "✅ Forwards from other chats/channels/groups are saved",
    "help.section1_duplicate": "🚫 Duplicates are automatically rejected within your account",
    "help.section1_spoiler": "🧹 Captions & spoilers not saved (original file only)",
    "help.section1_delete": "🗑️ Original message deleted after {delay} seconds",
    "help.section2_title": "📥 <b>2. Retrieving Files — /get</b>",
    "help.section2_intro": "Use <code>/get</code> to open <b>the interactive file browser</b>.",
    "help.section2_nav_title": "🎮 <b>File Browser Navigation:</b>",
    "help.section2_nav1": "• Click a <b>file number</b> — download that single file",
    "help.section2_nav2": "• Click <b>👁️ View Page</b> — download all files on the page",
    "help.section2_nav3": "• ⬅️ <b>Prev</b> / <b>Next</b> ➡️ — switch pages",
    "help.section2_nav4": "• Click a <b>📄 page number</b> — jump to that page",
    "help.section2_nav5": "• Type a page number when prompted — quick access",
    "help.section2_nav6": "• Each page shows up to 10 files",
    "help.section2_admin": "\n🔑 <b>For Admins:</b>\n" +
                          "<code>/get user [ID]</code> — View another user's files\n" +
                          "<code>/get</code> (admin) — View ALL files from all users",
    "help.section2_delete": "\n🗑️ Downloaded results auto-delete after {delay} seconds",
    "help.section3_title": "📊 <b>3. Statistics — /stats</b>",
    "help.section3_files": "• Total file count & storage size",
    "help.section3_breakdown": "• Breakdown by type (photo/video/document)",
    "help.section3_today": "• Today's uploads & duplicates",
    "help.section3_uptime": "• Bot uptime (days/hours/minutes)",
    "help.section4_title": "📋 <b>4. Quota — /mylimit</b>",
    "help.section4_default": "• Default: {limit:,} files per user",
    "help.section4_admin": "• Admin can adjust per-user quota",
    "help.section4_unlimited": "• 0 = unlimited",
    "help.section5_title": "🗑️ <b>5. Delete Files — /delete</b>",
    "help.section5_cmd": "<code>/delete [number]</code> — Delete a specific file",
    "help.section5_all": "<code>/delete all</code> — Delete all your files",
    "help.section5_note": "⚠️ Confirmation is always required before deletion!",
    "help.section6_title": "💬 <b>6. Contact Admin</b>",
    "help.section6_cmd": "Type <code>@admin [your message]</code>",
    "help.section6_example": "Example: <code>@admin Upload fails to process videos</code>",
    "help.section6_reply": "Admin will reply through the bot.",
    "help.section7_title": "🛡️ <b>7. Privacy & Security</b>",
    "help.section7_private": (
        "• Every file you store is <b>accessible only by you</b>.\n"
        "  No one — including administrators — can view, open, or download your files."
    ),
    "help.section7_noshare": (
        "• <b>Zero data sharing.</b> Your files will never be shown to other users,\n"
        "  and your statistics remain private."
    ),
    "help.section7_clean": (
        "• The original messages you send to the bot are <b>auto-deleted</b> after a few seconds.\n"
        "  Only files stored in your secure storage remain."
    ),
    "help.section7_dedup": (
        "• Duplicate detection works <b>per‑user</b>. Files already in your account will not\n"
        "  be accepted again, keeping storage efficient."
    ),
    "help.section7_encryption": (
        "• Storage uses <b>strict isolation</b> mechanisms and system‑level access protection.\n"
        "  Your data is never read by processes other than your own session."
    ),
    "help.section8_title": "🌐 <b>8. Language — /language</b>",
    "help.section8_desc": "Change the bot's display language (8 languages available).",
    "help.section8_list": "<code>/language</code> — Show language selection",
    "help.section8_set": "Tap the desired language button",
    "help.section8_langs": "🇮🇩 ID | 🇬🇧 EN | 🇷🇺 RU | 🇨🇳 ZH | 🇯🇵 JA | 🇪🇸 ES | 🇮🇳 HI | 🇧🇷 PT",
    "help.section9_title": "💡 <b>9. Tips</b>",
    "help.section9_tip1": "• Forward media from channels/groups to save them",
    "help.section9_tip2": "• Use /get to retrieve files anytime",
    "help.section9_tip3": "• Captions & spoilers are not stored (only the raw file)",
    "help.section9_tip4": "• Photo/video albums are processed as a group (efficient)",
    "help.admin_title": "🔑 <b>10. ADMIN COMMANDS</b>",
    "help.admin_list": "<code>/admin</code> — Admin panel",
    "help.admin_users": "<code>/admin users</code> — List all users",
    "help.admin_user": "<code>/admin user [id]</code> — User details",
    "help.admin_add": "<code>/admin add [id]</code> — Add admin (super admin only)",
    "help.admin_remove": "<code>/admin remove [id]</code> — Remove admin (super admin only)",
    "help.admin_setlimit": "<code>/admin setlimit [id] [n]</code> — Set user quota",
    "help.admin_stats": "<code>/admin stats</code> — Global statistics",
    "help.admin_messages": "<code>/admin messages</code> — Messages from users",
    "help.admin_ban": "<code>/ban [id]</code> — Ban user",
    "help.admin_unban": "<code>/unban [id]</code> — Unban user",
    "help.admin_broadcast": "<code>/broadcast [message]</code> — Broadcast to all users",
    "help.admin_reply": "<code>/reply [id] [text]</code> — Reply to a user message",
    "help.admin_delete": "<code>/delete user [id] [number|all]</code> — Delete user's file(s)",
    "help.admin_get_user": "<code>/get user [id]</code> — View specific user's files",
    "help.footer": "🏷️ <b>v3.0.4</b> | Multi-User Edition | Per-User Isolation",
    "help.made_with": "Made with ❤️ using python-telegram-bot",

    "help.privacy_bottom": (
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔐 <b>Your security is our priority.</b>\n"
        "No one — including the development team — can see the contents of your files.\n"
        "We never share your data with third parties."
    ),

    # ============================================
    # /get
    # ============================================
    "get.banned": "❌ You have been banned from this bot.",
    "get.max_range": "⚠️ Maximum {max_range} files per page.",
    "get.no_files": "📭 No files found. Send some media to get started.",
    "get.error": "❌ An error occurred. Try again later.",
    "get.invalid_input": "❌ Invalid user ID or page number.",
    "get.owner_label": "👤 Owner: {owner} (ID: {owner_id})",

    # ============================================
    # File Browser Navigation
    # ============================================
    "nav.view_page": "👁️ View Page {page}",
    "nav.prev": "⬅️ Prev",
    "nav.next": "Next ➡️",
    "nav.back_all": "🔙 Back to All Files",
    "nav.my_files": "📂 Your Files",
    "nav.all_files": "📂 All Files (Admin View)",
    "nav.user_files": "📂 Files of: {name} (ID: {uid})",
    "nav.page_of": "📄 {page}/{total}",
    "nav.jump_prompt": "📄 Jump to page? (1-{total})\nType a page number below 👇",
    "nav.jump_alert": "Please type a page number (1-{total})",
    "nav.invalid_page": "❌ Page must be between 1-{total}.",
    "nav.invalid_number": "❌ Enter a valid page number.",
    "nav.file_sent": "✅ {name} sent!",
    "nav.send_failed": "⚠️ Failed to send file. Try again.",
    "nav.no_file": "⚠️ File not found.",
    "nav.no_files_page": "⚠️ No files on this page.",
    "nav.files_sent": "✅ {count} files sent!",
    "nav.too_fast": "⚠️ Too fast! Please wait a moment...",
    "nav.session_expired": "⚠️ Browser session expired. Use /get again.",
    "nav.generic_error": "⚠️ An error occurred. Please try again.",
    # Navigation File Browser (additional)
    "nav.range_indicator": "{start}-{end} of {total} files",
    "nav.navigation_hint": "📌 {num} of {total} files",
    "nav.navigation_hint_range": "📌 {start}-{end} of {total} files",
    "nav.invalid_file": "❌ File number must be 1-{total}.",

    # ============================================
    # /stats
    # ============================================
    "stats.title": "📊 PERSONAL STATISTICS",
    "stats.total_files": "📦 Total files: {count:,}",
    "stats.quota": " / {limit:,} (quota)",
    "stats.total_size": "💾 Total size: {size}",
    "stats.by_type": "📂 By Type:",
    "stats.type_photo": "📸 {type}: {count:,} ({size})",
    "stats.type_video": "🎥 {type}: {count:,} ({size})",
    "stats.type_document": "📄 {type}: {count:,} ({size})",
    "stats.type_other": "📎 {type}: {count:,} ({size})",
    "stats.today_added": "📤 Today: +{count} files",
    "stats.today_dup": "🔄 Rejected (duplicates): {count}",
    "stats.uptime": "🕐 Uptime: {days}d {hours}h {minutes}m",
    "stats.privacy_note": "🔒 These stats are visible only to you.",

    # ============================================
    # /mylimit
    # ============================================
    "limit.unlimited": "📊 Quota: Unlimited\n📁 Stored files: {current:,}\n💾 Storage: {size}",
    "limit.limited": "📊 Quota: {current:,}/{limit:,} files\n📥 Remaining: {remaining:,} files\n💾 Storage: {size}",
    "limit.safe_note": "🛡️ Your files remain safe even when quota is full. You just cannot add new files.",

    # ============================================
    # /delete (v3.0.3)
    # ============================================
    "delete.help_title": "🗑️ <b>DELETE FILES</b>",
    "delete.help_desc": "You can delete stored files. Use /get to see file numbers.",
    "delete.help_commands": "📋 <b>Commands:</b>",
    "delete.help_single": "<code>/delete [number]</code> — Delete file by number (1 = newest)",
    "delete.help_all": "<code>/delete all</code> — Delete all your files",
    "delete.help_note": "⚠️ <b>Warning:</b> Deletion cannot be undone! Confirmation will be requested.",
    "delete.help_total": "📁 Your total files: <b>{count:,}</b>",
    "delete.help_size": "💾 Total size: <b>{size}</b>",
    "delete.help_admin": "👤 User {name} (ID: {uid})\n📁 Files: {count:,}\n💾 Size: {size}\n\nUse /delete user {uid} [number|all]",
    "delete.banned": "❌ You have been banned from this bot.",
    "delete.invalid_format": "❌ Invalid format. Use /delete for guidance.",
    "delete.not_found": "❌ File number {num} not found. Use /get to list files.",
    "delete.no_files": "📭 No files to delete.",
    "delete.confirm_single": (
        "⚠️ <b>Confirm File Deletion</b>\n\n"
        "{emoji} <b>#{num}</b> — {name}\n"
        "📁 Type: {type}\n"
        "💾 Size: {size}\n\n"
        "Are you sure you want to delete this file?"
    ),
    "delete.confirm_single_admin": (
        "⚠️ <b>Confirm File Deletion (Admin)</b>\n\n"
        "👤 User ID: {uid}\n"
        "{emoji} <b>#{num}</b> — {name}\n"
        "📁 Type: {type}\n"
        "💾 Size: {size}\n\n"
        "Are you sure you want to delete this file?"
    ),
    "delete.confirm_all": (
        "⚠️ <b>Confirm Delete All Files</b>\n\n"
        "📁 Total files: <b>{count:,}</b>\n"
        "💾 Total size: <b>{size}</b>\n\n"
        "Are you sure you want to delete <b>ALL</b> files?\n"
        "This action <b>CANNOT BE UNDONE!</b>"
    ),
    "delete.confirm_all_admin": (
        "⚠️ <b>Confirm Delete All Files (Admin)</b>\n\n"
        "👤 User: {name} (ID: {uid})\n"
        "📁 Total files: <b>{count:,}</b>\n"
        "💾 Total size: <b>{size}</b>\n\n"
        "Are you sure you want to delete <b>ALL</b> files of this user?"
    ),
    "delete.btn_confirm": "✅ Yes, Delete",
    "delete.btn_confirm_all": "✅ Yes, Delete All",
    "delete.btn_cancel": "❌ Cancel",
    "delete.cancelled": "✅ Deletion cancelled.",
    "delete.success_single": "✅ File <b>#{num}</b> ({name}) has been deleted.",
    "delete.success_single_admin": "✅ File <b>#{num}</b> ({name}) of user {uid} has been deleted.",
    "delete.success_all": "✅ <b>{count:,}</b> files have been deleted.",
    "delete.success_all_admin": "✅ <b>{count:,}</b> files of user {uid} have been deleted.",
    "delete.failed": "❌ Failed to delete file. Please try again.",
    "delete.not_owner": "❌ You are not the owner of this file.",
    "delete.not_admin": "❌ You do not have admin access.",
    "delete.popup_session_expired": "⚠️ Session expired. Please try again.",

    # ============================================
    # /language
    # ============================================
    "language.select": "🌐 <b>Select Language:</b>\n\nType /language [code]\n\n{langs}",
    "language.current": "\n\n📌 Current: {current}",
    "language.changed": "✅ Language changed to {name}",
    "language.invalid": "❌ Unsupported language. Use: {codes}",
    "language.unsupported": "❌ Language not supported.",
    "language.lang_item": "{emoji} {name} — <code>/language {code}</code>\n",
    "language.select_title": "🌐 <b>Select Language:</b>",

    # ============================================
    # @admin
    # ============================================
    "admin_msg.format": "✍️ Format: @admin [message]\nExample: @admin The bot is having an error",
    "admin_msg.sent": "✅ Message sent to admin. We will respond as soon as possible.",
    "admin_msg.notify": "📩 Message from user\n👤 {name} (ID: {uid})\n💬 {message}\n\nReply: /reply {msg_id} [message]",

    # ============================================
    # Admin Panel
    # ============================================
    "admin.access_denied": "❌ Access denied. Admin only.",
    "admin.panel_title": "🔑 ADMIN PANEL",
    "admin.panel_users": "👥 Total users: {count:,}",
    "admin.panel_files": "📁 Total files: {count:,}",
    "admin.panel_admins": "🛡️ Runtime admins: {count}",
    "admin.panel_unread": "📩 New messages: {count} ⚠️",
    "admin.panel_commands": (
        "📋 Commands:\n"
        "/admin users — List all users\n"
        "/admin user [id] — User detail\n"
        "/admin add [id] — Add admin\n"
        "/admin remove [id] — Remove admin\n"
        "/admin setlimit [id] [n] — Set limit\n"
        "/admin stats — Global stats\n"
        "/admin messages — Messages from users\n"
        "/ban [id] — Ban user\n"
        "/unban [id] — Unban user\n"
        "/broadcast [message] — Send to all users\n"
        "/reply [id] [message] — Reply to a user message\n"
        "/delete user [id] [n|all] — Delete user's file(s)\n"
        "/get user [id] — View specific user's files"
    ),
    # ============================================
    # Admin Panel - user list navigation
    # ============================================
    "admin_users.invalid_page": "❌ Invalid page.",
    "admin_users.access_denied": "❌ Access denied.",
    "admin.users_title": "👥 REGISTERED USERS",
    "admin.users_item": "{i}. {name} (ID: {uid}) — {files:,} file(s){banned}",
    "admin.users_more": "\n... and {count} more.",
    "admin.users_empty": "No registered users yet.",
    "admin.user_title": "👤 USER DETAIL: {name}",
    "admin.user_id": "ID: {uid}",
    "admin.user_username": "Username: @{username}",
    "admin.user_banned": "Banned status: {status}",
    "admin.user_files": "Files: {files:,} / {limit}",
    "admin.user_storage": "Storage: {size}",
    "admin.user_by_type": "📂 By Type:",
    "admin.user_not_found": "❌ User not found.",
    "admin.add_super_only": "❌ Only super admin can add admins.",
    "admin.add_super_cannot": "❌ Super admin cannot be modified.",
    "admin.add_success": "✅ User {uid} has been promoted to admin.",
    "admin.add_already": "⚠️ User is already an admin.",
    "admin.remove_super_only": "❌ Only super admin can remove admins.",
    "admin.remove_super_cannot": "❌ Super admin cannot be removed.",
    "admin.remove_success": "✅ User {uid} has been demoted from admin.",
    "admin.remove_not": "⚠️ User is not an admin.",
    "admin.setlimit_success": "✅ File limit for user {uid} set to {limit:,}.",
    "admin.global_title": "📊 GLOBAL STATISTICS",
    "admin.global_users": "👥 Total users: {count:,}",
    "admin.global_files": "📁 Total files: {count:,}",
    "admin.global_storage": "💾 Total storage: {size}",
    "admin.global_served": "📤 Total files served: {count:,}",
    "admin.global_top": "🏆 Top 5 Users:",
    "admin.global_top_item": "  {i}. {name} — {files:,} file(s)",
    "admin.broadcast_format": "📢 Format: /broadcast [message]\nExample: /broadcast Server maintenance at 22:00 UTC",
    "admin.broadcast_sending": "📤 Sending broadcast to {total} users...",
    "admin.broadcast_progress": (
        "📤 Sending broadcast...\n"
        "▸ Progress: {sent}/{total}\n"
        "▸ Successful: {success}\n"
        "▸ Failed: {failed}"
    ),
    "admin.broadcast_done": "✅ Broadcast completed\n📤 Delivered: {success}\n❌ Failed: {failed}\n👥 Total: {total}",
    "admin.broadcast_msg": "📢 Admin Announcement\n\n{message}",
    "admin.broadcast_skipped": "\n⚠️ Skipped {skipped} banned/inactive users",
    "admin.reply_format": "↩️ Format: /reply [message_id] [reply]\nUse /admin messages to view the message list",
    "admin.reply_invalid_id": "❌ Invalid message ID.",
    "admin.reply_not_found": "❌ Message not found.",
    "admin.reply_already": "⚠️ This message has already been replied to.",
    "admin.reply_failed": "❌ Failed to send reply: {error}",
    "admin.reply_sent": "✅ Reply sent to user {uid}",
    "admin.reply_to_user": "🔰 Admin replied to your message:\n\n💬 Your message: {original}\n\n↩️ Admin reply: {reply}",
    "admin.reply_failed_delivery": "❌ Failed to send reply: message could not be delivered.",
    "admin.messages_title": "📩 MESSAGES FROM USERS",
    "admin.messages_item": "#{id} | {name} (ID: {uid})\n💬 {text}\nReply: /reply {id} [message]\n\n",
    "admin.messages_empty": "📭 No new messages.",
    "admin.messages_max": "\n⚠️ Showing 20 most recent messages.",
    "admin.ban_usage": "Usage: /ban [user_id]",
    "admin.ban_invalid": "❌ Invalid user ID.",
    "admin.ban_super": "❌ Cannot ban super admin.",
    "admin.ban_success": "🚫 User {uid} has been banned.",
    "admin.unban_usage": "Usage: /unban [user_id]",
    "admin.unban_success": "✅ User {uid} has been unbanned.",

    # ============================================
    # Ban/Unban confirmation (v3.0.4 - i18n)
    # ============================================
    "ban.confirm_title": "⚠️ <b>Confirm Ban User</b>",
    "ban.confirm_body": "👤 Name: <b>{name}</b>\n🆔 ID: <code>{uid}</code>\n📛 Username: {username}\n📁 Files: {files:,}\n\nAre you sure you want to <b>BAN</b> this user?\nThey will no longer be able to use the bot.",
    "ban.already_banned": "⚠️ User {uid} is already banned.",
    "ban.success": "🚫 <b>User Banned</b>\n\n👤 {name}\n🆔 <code>{uid}</code>\n\n✅ This user can no longer use the bot.\n🗑️ Their cache has been cleared.",
    "unban.confirm_title": "🔓 <b>Confirm Unban User</b>",
    "unban.confirm_body": "👤 Name: <b>{name}</b>\n🆔 ID: <code>{uid}</code>\n📛 Username: {username}\n📁 Files: {files:,}\n\nAre you sure you want to <b>UNBAN</b> this user?\nThey will be able to use the bot again.",
    "unban.not_banned": "⚠️ User {uid} is not currently banned.",
    "unban.success": "🔓 <b>User Unbanned</b>\n\n👤 {name}\n🆔 <code>{uid}</code>\n\n✅ This user can now use the bot again.",
    "ban.cancel": "✅ Operation cancelled.",

    # Ban/unban confirmation buttons
    "ban.btn_confirm": "🚫 Yes, Ban",
    "unban.btn_confirm": "🔓 Yes, Unban",
    "ban.btn_cancel": "❌ Cancel",

    # Pop-up alerts
    "ban.popup_session_expired": "⚠️ Session expired. Please try again.",
    "ban.popup_access_denied": "❌ Access denied.",
    "ban.popup_not_initiator": "❌ Only the admin who initiated can confirm.",
    "ban.popup_cannot_ban_super": "❌ Cannot ban a super admin!",
    "ban.popup_already_banned": "Already banned",
    "ban.popup_not_banned": "Not banned",
    "ban.popup_cancelled": "Cancelled",
    "ban.popup_success_ban": "✅ User banned successfully!",
    "ban.popup_success_unban": "✅ User unbanned successfully!",

    # ============================================
    # Media Handler
    # ============================================
    "media.queue_full": "⚠️ Your queue is full (max {maxsize} files). Please wait a moment before sending more.",
    "media.quota_full": "❌ Your quota is full.\nUse /mylimit to check details.",
    "media.file_too_large": "❌ File too large ({size} bytes).\nMaximum: {max_mb} MB",
    "media.global_full": "❌ Sorry, global storage is full.\nPlease try again later.",
}