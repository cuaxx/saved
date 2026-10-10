"""
Bahasa Indonesia Translation Pack
Telegram Media Storage Bot v3.0.4
"""

TEXTS = {
    # ============================================
    # /start
    # ============================================
    "start.welcome": "👋 <b>Selamat datang, {name}!</b>",
    "start.bot_desc": "🤖 <b>Telegram Media Storage Bot v3.0.4</b>\nBot penyimpanan media cerdas multi-user dengan deduplikasi otomatis, enkripsi per-user, dan fitur hapus file.",
    "start.features_title": "✨ <b>Fitur Unggulan:</b>",
    "start.feature_save": "• Simpan foto, video, dan dokumen",
    "start.feature_dedup": "• Deteksi & tolak duplikat otomatis (per-user)",
    "start.feature_privacy": "• Penyimpanan terisolasi — file Anda hanya untuk Anda",
    "start.feature_autodel": "• {desc}",
    "start.feature_spoiler": "• <b>Caption & spoiler media diabaikan</b> (hanya file disimpan)",
    "start.feature_album": "• Album multi-file didukung penuh",
    "start.feature_forward": "• Forward media tetap disimpan",
    "start.feature_stats": "• Statistik personal lengkap & real-time",
    "start.feature_delete": "• Hapus file dengan konfirmasi aman",
    "start.howto_title": "🚀 <b>Cara Pakai:</b>",
    "start.howto_desc": "Kirim / forward media ke bot — selesai!",
    "start.commands_title": "📖 <b>Commands:</b>",
    "start.cmd_get": "/get — Buka file browser interaktif",
    "start.cmd_stats": "/stats — Statistik & uptime",
    "start.cmd_limit": "/mylimit — Cek sisa kuota",
    "start.cmd_delete": "/delete — Hapus file tersimpan",
    "start.cmd_help": "/help — Bantuan lengkap",
    "start.cmd_lang": "/language — Ganti bahasa (8 bahasa)",
    "start.cmd_admin_msg": "@admin [pesan] — Hubungi admin",
    "start.admin_title": "🔑 <b>Admin Mode Active</b>",
    "start.admin_cmd": "/admin — Panel kontrol admin",
    "start.privacy_title": (
        "🔒 <b>Privasi Terjamin</b>\n"
        "• Setiap file Anda disimpan secara <b>terisolasi</b> dan hanya dapat diakses oleh Anda sendiri.\n"
        "• <b>Admin tidak dapat melihat</b> atau membuka file pengguna mana pun.\n"
        "• Tidak ada data yang dibagikan ke pihak lain, termasuk sesama pengguna.\n"
        "• Sistem kami menggunakan penyimpanan terproteksi sehingga privasi Anda selalu terjaga."
    ),
    "start.autodel_desc_media": "Pesan media dihapus otomatis setelah {delay} detik",
    "start.autodel_desc_all": "Pesan dihapus otomatis setelah {delay} detik",

    # ============================================
    # /help
    # ============================================
    "help.title": "📖 <b>BANTUAN LENGKAP</b>",
    "help.subtitle": "Telegram Media Storage Bot v3.0.4",
    "help.section1_title": "📤 <b>1. Menyimpan Media</b>",
    "help.section1_desc": "Cukup kirim atau forward media ke bot — semua otomatis.",
    "help.section1_support": "✅ Didukung: Foto, Video, Dokumen",
    "help.section1_album": "✅ Album multi-file otomatis diproses",
    "help.section1_forward": "✅ Forward dari chat/channel/grup lain tetap disimpan",
    "help.section1_duplicate": "🚫 Duplikat otomatis ditolak dalam akun Anda",
    "help.section1_spoiler": "🧹 Caption & spoiler tidak disimpan (hanya file asli)",
    "help.section1_delete": "🗑️ Pesan asli dihapus setelah {delay} detik",
    "help.section2_title": "📥 <b>2. Mengambil File — /get</b>",
    "help.section2_intro": "Gunakan <code>/get</code> untuk membuka <b>file browser interaktif</b>.",
    "help.section2_nav_title": "🎮 <b>Navigasi File Browser:</b>",
    "help.section2_nav1": "• Klik <b>nomor file</b> — langsung download 1 file",
    "help.section2_nav2": "• Klik <b>👁️ Lihat Halaman</b> — download semua file di halaman",
    "help.section2_nav3": "• ⬅️ <b>Prev</b> / <b>Next</b> ➡️ — pindah halaman",
    "help.section2_nav4": "• Klik <b>📄 nomor halaman</b> — lompat ke halaman tertentu",
    "help.section2_nav5": "• Ketik nomor halaman saat diminta — akses cepat",
    "help.section2_nav6": "• Setiap halaman menampilkan maks 10 file",
    "help.section2_admin": "\n🔑 <b>Untuk Admin:</b>\n" +
                          "<code>/get user [ID]</code> — Lihat file user lain\n" +
                          "<code>/get</code> (admin) — Lihat SEMUA file dari semua user",
    "help.section2_delete": "\n🗑️ Hasil download dihapus otomatis setelah {delay} detik",
    "help.section3_title": "📊 <b>3. Statistik — /stats</b>",
    "help.section3_files": "• Total file & ukuran storage Anda",
    "help.section3_breakdown": "• Breakdown per tipe (foto/video/dokumen)",
    "help.section3_today": "• Upload & duplikat hari ini",
    "help.section3_uptime": "• Bot uptime (hari/jam/menit)",
    "help.section4_title": "📋 <b>4. Kuota — /mylimit</b>",
    "help.section4_default": "• Default: {limit:,} file per user",
    "help.section4_admin": "• Admin dapat menyesuaikan kuota per user",
    "help.section4_unlimited": "• 0 = unlimited (tidak terbatas)",
    "help.section5_title": "🗑️ <b>5. Hapus File — /delete</b>",
    "help.section5_cmd": "<code>/delete [nomor]</code> — Hapus file tertentu",
    "help.section5_all": "<code>/delete all</code> — Hapus semua file",
    "help.section5_note": "⚠️ Konfirmasi selalu diminta sebelum penghapusan!",
    "help.section6_title": "💬 <b>6. Hubungi Admin</b>",
    "help.section6_cmd": "Ketik <code>@admin [pesan Anda]</code>",
    "help.section6_example": "Contoh: <code>@admin Bot tidak bisa upload video</code>",
    "help.section6_reply": "Admin akan membalas melalui bot.",
    "help.section7_title": "🛡️ <b>7. Privasi & Keamanan</b>",
    "help.section7_private": (
        "• Setiap file yang Anda simpan <b>hanya dapat diakses oleh Anda sendiri</b>.\n"
        "  Tidak seorang pun—termasuk administrator—dapat melihat, membuka, atau mengunduh file Anda."
    ),
    "help.section7_noshare": (
        "• <b>Nihil pembagian data.</b> File Anda tidak akan pernah ditampilkan ke pengguna lain,\n"
        "  dan statistik Anda bersifat privat."
    ),
    "help.section7_clean": (
        "• Pesan asli yang Anda kirim ke bot akan <b>dihapus otomatis</b> setelah beberapa detik.\n"
        "  Hanya file yang tersimpan di penyimpanan aman Anda yang tetap ada."
    ),
    "help.section7_dedup": (
        "• Deteksi duplikat bekerja <b>per‑pengguna</b>. File yang sudah ada di akun Anda tidak akan\n"
        "  diterima lagi, sehingga ruang penyimpanan tetap efisien."
    ),
    "help.section7_encryption": (
        "• Penyimpanan menggunakan mekanisme <b>isolasi ketat</b> dan proteksi akses tingkat sistem.\n"
        "  Data Anda tidak dibaca oleh proses lain selain sesi Anda sendiri."
    ),
    "help.section8_title": "🌐 <b>8. Bahasa — /language</b>",
    "help.section8_desc": "Ganti bahasa tampilan bot (8 bahasa tersedia).",
    "help.section8_list": "<code>/language</code> — Buka pilihan bahasa",
    "help.section8_set": "Klik tombol bahasa yang diinginkan",
    "help.section8_langs": "🇮🇩 ID | 🇬🇧 EN | 🇷🇺 RU | 🇨🇳 ZH | 🇯🇵 JA | 🇪🇸 ES | 🇮🇳 HI | 🇧🇷 PT",
    "help.section9_title": "💡 <b>9. Tips</b>",
    "help.section9_tip1": "• Forward media dari channel/grup untuk disimpan",
    "help.section9_tip2": "• Gunakan /get untuk mengambil file kapan saja",
    "help.section9_tip3": "• Caption & spoiler tidak disimpan (hanya file asli)",
    "help.section9_tip4": "• Album foto/video diproses sebagai group (efisien)",
    "help.admin_title": "🔑 <b>10. ADMIN COMMANDS</b>",
    "help.admin_list": "<code>/admin</code> — Panel admin",
    "help.admin_users": "<code>/admin users</code> — List semua user",
    "help.admin_user": "<code>/admin user [id]</code> — Detail user",
    "help.admin_add": "<code>/admin add [id]</code> — Tambah admin (super admin only)",
    "help.admin_remove": "<code>/admin remove [id]</code> — Hapus admin (super admin only)",
    "help.admin_setlimit": "<code>/admin setlimit [id] [n]</code> — Set kuota user",
    "help.admin_stats": "<code>/admin stats</code> — Statistik global",
    "help.admin_messages": "<code>/admin messages</code> — Pesan dari user",
    "help.admin_ban": "<code>/ban [id]</code> — Ban user",
    "help.admin_unban": "<code>/unban [id]</code> — Unban user",
    "help.admin_broadcast": "<code>/broadcast [pesan]</code> — Umumkan ke semua user",
    "help.admin_reply": "<code>/reply [id] [teks]</code> — Balas pesan user",
    "help.admin_delete": "<code>/delete user [id] [nomor|all]</code> — Hapus file user",
    "help.admin_get_user": "<code>/get user [id]</code> — Lihat file user tertentu",
    "help.footer": "🏷️ <b>v3.0.4</b> | Multi-User Edition | Per-User Isolation",
    "help.made_with": "Dibuat dengan ❤️ PTB",

    # Pesan penutup keamanan di /help (tambahan)
    "help.privacy_bottom": (
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔐 <b>Keamanan Anda adalah prioritas kami.</b>\n"
        "Tidak ada seorang pun—termasuk tim pengembang—yang dapat melihat isi file Anda.\n"
        "Kami tidak pernah membagikan data Anda kepada pihak ketiga."
    ),

    # ============================================
    # /get
    # ============================================
    "get.banned": "❌ Anda telah dibanned dari bot ini.",
    "get.max_range": "⚠️ Maksimal {max_range} file per halaman.",
    "get.no_files": "📭 Tidak ada file ditemukan. Kirim media untuk memulai.",
    "get.error": "❌ Terjadi kesalahan. Coba lagi nanti.",
    "get.invalid_input": "❌ ID pengguna atau nomor halaman tidak valid.",
    "get.owner_label": "👤 Owner: {owner} (ID: {owner_id})",

    # ============================================
    # Navigasi File Browser
    # ============================================
    "nav.view_page": "👁️ Lihat Halaman {page}",
    "nav.prev": "⬅️ Prev",
    "nav.next": "Next ➡️",
    "nav.back_all": "🔙 Kembali ke Semua File",
    "nav.my_files": "📂 File Anda",
    "nav.all_files": "📂 Semua File (Admin View)",
    "nav.user_files": "📂 File milik: {name} (ID: {uid})",
    "nav.page_of": "📄 {page}/{total}",
    "nav.jump_prompt": "📄 Lompat ke halaman? (1-{total})\nKetik nomor halaman di bawah 👇",
    "nav.jump_alert": "Silakan ketik nomor halaman (1-{total})",
    "nav.invalid_page": "❌ Halaman harus 1-{total}.",
    "nav.invalid_number": "❌ Masukkan nomor halaman yang valid.",
    "nav.file_sent": "✅ {name} terkirim!",
    "nav.send_failed": "⚠️ Gagal mengirim file. Coba lagi.",
    "nav.no_file": "⚠️ File tidak ditemukan.",
    "nav.no_files_page": "⚠️ Tidak ada file di halaman ini.",
    "nav.files_sent": "✅ {count} file terkirim!",
    "nav.too_fast": "⚠️ Terlalu cepat! Tunggu sebentar...",
    "nav.session_expired": "⚠️ Sesi browser expired. Gunakan /get lagi.",
    "nav.generic_error": "⚠️ Terjadi kesalahan. Silakan coba lagi.",
    # Navigasi File Browser (tambahan)
    "nav.range_indicator": "{start}-{end} dari {total} file",
    "nav.navigation_hint": "📌 {num} dari {total} file",
    "nav.navigation_hint_range": "  📌 {start}-{end} dari {total} file",
    "nav.invalid_file": "❌ Nomor file harus 1-{total}.",

    # ============================================
    # /stats
    # ============================================
    "stats.title": "📊 STATISTIK PRIBADI",
    "stats.total_files": "📦 Total file: {count:,}",
    "stats.quota": " / {limit:,} (kuota)",
    "stats.total_size": "💾 Total ukuran: {size}",
    "stats.by_type": "📂 Berdasarkan Tipe:",
    "stats.type_photo": "📸 {type}: {count:,} ({size})",
    "stats.type_video": "🎥 {type}: {count:,} ({size})",
    "stats.type_document": "📄 {type}: {count:,} ({size})",
    "stats.type_other": "📎 {type}: {count:,} ({size})",
    "stats.today_added": "📤 Hari ini: +{count} file",
    "stats.today_dup": "🔄 Ditolak (duplikat): {count}",
    "stats.uptime": "🕐 Uptime: {days}h {hours}j {minutes}m",
    "stats.privacy_note": "🔒 Statistik ini hanya terlihat oleh Anda.",

    # ============================================
    # /mylimit
    # ============================================
    "limit.unlimited": "📊 Kuota: Tidak Terbatas\n📁 File tersimpan: {current:,}\n💾 Storage: {size}",
    "limit.limited": "📊 Kuota: {current:,}/{limit:,} file\n📥 Sisa: {remaining:,} file\n💾 Storage: {size}",
    "limit.safe_note": "🛡️ File Anda tetap aman meskipun kuota penuh. Anda hanya tidak dapat menambah file baru.",

    # ============================================
    # /delete (v3.0.3)
    # ============================================
    "delete.help_title": "🗑️ <b>HAPUS FILE</b>",
    "delete.help_desc": "Anda dapat menghapus file yang telah disimpan. Gunakan /get untuk melihat nomor file.",
    "delete.help_commands": "📋 <b>Perintah:</b>",
    "delete.help_single": "<code>/delete [nomor]</code> — Hapus file berdasarkan nomor (1 = terbaru)",
    "delete.help_all": "<code>/delete all</code> — Hapus semua file Anda",
    "delete.help_note": "⚠️ <b>Perhatian:</b> Penghapusan tidak dapat dibatalkan! Konfirmasi akan diminta.",
    "delete.help_total": "📁 Total file Anda: <b>{count:,}</b>",
    "delete.help_size": "💾 Total ukuran: <b>{size}</b>",
    "delete.help_admin": "👤 User {name} (ID: {uid})\n📁 File: {count:,}\n💾 Ukuran: {size}\n\nGunakan /delete user {uid} [nomor|all]",
    "delete.banned": "❌ Anda telah dibanned dari bot ini.",
    "delete.invalid_format": "❌ Format tidak valid. Gunakan /delete untuk panduan.",
    "delete.not_found": "❌ File nomor {num} tidak ditemukan. Gunakan /get untuk lihat daftar file.",
    "delete.no_files": "📭 Tidak ada file untuk dihapus.",
    "delete.confirm_single": (
        "⚠️ <b>Konfirmasi Hapus File</b>\n\n"
        "{emoji} <b>#{num}</b> — {name}\n"
        "📁 Tipe: {type}\n"
        "💾 Ukuran: {size}\n\n"
        "Apakah Anda yakin ingin menghapus file ini?"
    ),
    "delete.confirm_single_admin": (
        "⚠️ <b>Konfirmasi Hapus File (Admin)</b>\n\n"
        "👤 User ID: {uid}\n"
        "{emoji} <b>#{num}</b> — {name}\n"
        "📁 Tipe: {type}\n"
        "💾 Ukuran: {size}\n\n"
        "Apakah Anda yakin ingin menghapus file ini?"
    ),
    "delete.confirm_all": (
        "⚠️ <b>Konfirmasi Hapus Semua File</b>\n\n"
        "📁 Total file: <b>{count:,}</b>\n"
        "💾 Total ukuran: <b>{size}</b>\n\n"
        "Apakah Anda yakin ingin menghapus <b>SEMUA</b> file?\n"
        "Tindakan ini <b>TIDAK DAPAT DIBATALKAN!</b>"
    ),
    "delete.confirm_all_admin": (
        "⚠️ <b>Konfirmasi Hapus Semua File (Admin)</b>\n\n"
        "👤 User: {name} (ID: {uid})\n"
        "📁 Total file: <b>{count:,}</b>\n"
        "💾 Total ukuran: <b>{size}</b>\n\n"
        "Apakah Anda yakin ingin menghapus <b>SEMUA</b> file user ini?"
    ),
    "delete.btn_confirm": "✅ Ya, Hapus",
    "delete.btn_confirm_all": "✅ Ya, Hapus Semua",
    "delete.btn_cancel": "❌ Batal",
    "delete.cancelled": "✅ Penghapusan dibatalkan.",
    "delete.success_single": "✅ File <b>#{num}</b> ({name}) berhasil dihapus.",
    "delete.success_single_admin": "✅ File <b>#{num}</b> ({name}) milik user {uid} berhasil dihapus.",
    "delete.success_all": "✅ <b>{count:,}</b> file berhasil dihapus.",
    "delete.success_all_admin": "✅ <b>{count:,}</b> file milik user {uid} berhasil dihapus.",
    "delete.failed": "❌ Gagal menghapus file. Silakan coba lagi.",
    "delete.not_owner": "❌ Anda bukan pemilik file ini.",
    "delete.not_admin": "❌ Anda tidak memiliki akses admin.",
    "delete.popup_session_expired": "⚠️ Sesi kedaluwarsa. Silakan coba lagi.",

    # ============================================
    # /language
    # ============================================
    "language.select": "🌐 <b>Pilih Bahasa / Select Language:</b>\n\nKetik /language [kode]\n\n{langs}",
    "language.current": "\n\n📌 Saat ini: {current}",
    "language.changed": "✅ Bahasa diubah ke {name}",
    "language.invalid": "❌ Bahasa tidak didukung. Gunakan: {codes}",
    "language.unsupported": "❌ Bahasa tidak didukung.",
    "language.lang_item": "{emoji} {name} — <code>/language {code}</code>\n",
    "language.select_title": "🌐 <b>Pilih Bahasa / Select Language:</b>",

    # ============================================
    # @admin
    # ============================================
    "admin_msg.format": "✍️ Format: @admin [pesan]\nContoh: @admin Bot nya error nih",
    "admin_msg.sent": "✅ Pesan terkirim ke admin. Kami akan merespon secepatnya.",
    "admin_msg.notify": "📩 Pesan dari user\n👤 {name} (ID: {uid})\n💬 {message}\n\nBalas: /reply {msg_id} [pesan]",

    # ============================================
    # Admin Panel
    # ============================================
    "admin.access_denied": "❌ Akses ditolak. Khusus admin.",
    "admin.panel_title": "🔑 ADMIN PANEL",
    "admin.panel_users": "👥 Total users: {count:,}",
    "admin.panel_files": "📁 Total files: {count:,}",
    "admin.panel_admins": "🛡️ Runtime admins: {count}",
    "admin.panel_unread": "📩 Pesan baru: {count} ⚠️",
    "admin.panel_commands": (
        "📋 Commands:\n"
        "/admin users — List semua user\n"
        "/admin user [id] — Detail user\n"
        "/admin add [id] — Tambah admin\n"
        "/admin remove [id] — Hapus admin\n"
        "/admin setlimit [id] [n] — Set limit\n"
        "/admin stats — Statistik global\n"
        "/admin messages — Pesan dari user\n"
        "/ban [id] — Ban user\n"
        "/unban [id] — Unban user\n"
        "/broadcast [pesan] — Kirim ke semua user\n"
        "/reply [id] [pesan] — Balas pesan user\n"
        "/delete user [id] [n|all] — Hapus file user\n"
        "/get user [id] — Lihat file user tertentu"
    ),
    # ============================================
    # Admin Panel - navigasi user list
    # ============================================
    "admin_users.invalid_page": "❌ Halaman tidak valid.",
    "admin_users.access_denied": "❌ Akses ditolak.",
    "admin.users_title": "👥 REGISTERED USERS",
    "admin.users_item": "{i}. {name} (ID: {uid}) — {files:,} file{banned}",
    "admin.users_more": "\n... dan {count} lainnya.",
    "admin.users_empty": "Belum ada user terdaftar.",
    "admin.user_title": "👤 DETAIL USER: {name}",
    "admin.user_id": "ID: {uid}",
    "admin.user_username": "Username: @{username}",
    "admin.user_banned": "Status banned: {status}",
    "admin.user_files": "File: {files:,} / {limit}",
    "admin.user_storage": "Storage: {size}",
    "admin.user_by_type": "📂 Berdasarkan Tipe:",
    "admin.user_not_found": "❌ User tidak ditemukan.",
    "admin.add_super_only": "❌ Hanya super admin yang bisa menambah admin.",
    "admin.add_super_cannot": "❌ Super admin tidak bisa dimodifikasi.",
    "admin.add_success": "✅ User {uid} telah dipromosikan menjadi admin.",
    "admin.add_already": "⚠️ User sudah menjadi admin.",
    "admin.remove_super_only": "❌ Hanya super admin yang bisa menghapus admin.",
    "admin.remove_super_cannot": "❌ Super admin tidak bisa dihapus.",
    "admin.remove_success": "✅ User {uid} telah diturunkan dari admin.",
    "admin.remove_not": "⚠️ User bukan admin.",
    "admin.setlimit_success": "✅ Limit file untuk user {uid} diset ke {limit:,}.",
    "admin.global_title": "📊 STATISTIK GLOBAL",
    "admin.global_users": "👥 Total user: {count:,}",
    "admin.global_files": "📁 Total file: {count:,}",
    "admin.global_storage": "💾 Total storage: {size}",
    "admin.global_served": "📤 Total file disajikan: {count:,}",
    "admin.global_top": "🏆 Top 5 User:",
    "admin.global_top_item": "  {i}. {name} — {files:,} file",
    "admin.broadcast_format": "📢 Format: /broadcast [pesan]\nContoh: /broadcast Bot akan maintenance jam 22:00 WIB",
    "admin.broadcast_sending": "📤 Mengirim broadcast ke {total} user...",
    "admin.broadcast_progress": (
        "📤 Mengirim broadcast...\n"
        "▸ Progress: {sent}/{total}\n"
        "▸ Berhasil: {success}\n"
        "▸ Gagal: {failed}"
    ),
    "admin.broadcast_done": "✅ Broadcast selesai\n📤 Terkirim: {success}\n❌ Gagal: {failed}\n👥 Total: {total}",
    "admin.broadcast_msg": "📢 Pengumuman Admin\n\n{message}",
    "admin.broadcast_skipped": "\n⚠️ Melewati {skipped} pengguna yang di-ban/tidak aktif",
    "admin.reply_format": "↩️ Format: /reply [id_pesan] [balasan]\nGunakan /admin messages untuk lihat daftar pesan",
    "admin.reply_invalid_id": "❌ ID pesan tidak valid.",
    "admin.reply_not_found": "❌ Pesan tidak ditemukan.",
    "admin.reply_already": "⚠️ Pesan ini sudah dibalas sebelumnya.",
    "admin.reply_failed": "❌ Gagal mengirim balasan: {error}",
    "admin.reply_sent": "✅ Balasan terkirim ke user {uid}",
    "admin.reply_to_user": "🔰 Admin membalas pesan Anda:\n\n💬 Pesan Anda: {original}\n\n↩️ Balasan Admin: {reply}",
    "admin.reply_failed_delivery": "❌ Gagal mengirim balasan: Pesan tidak dapat dikirim.",
    "admin.messages_title": "📩 PESAN DARI USER",
    "admin.messages_item": "#{id} | {name} (ID: {uid})\n💬 {text}\nBalas: /reply {id} [isi]\n\n",
    "admin.messages_empty": "📭 Tidak ada pesan baru.",
    "admin.messages_max": "\n⚠️ Menampilkan 20 pesan terbaru.",
    "admin.ban_usage": "Penggunaan: /ban [user_id]",
    "admin.ban_invalid": "❌ ID user tidak valid.",
    "admin.ban_super": "❌ Tidak bisa mem-ban super admin.",
    "admin.ban_success": "🚫 User {uid} telah di-ban.",
    "admin.unban_usage": "Penggunaan: /unban [user_id]",
    "admin.unban_success": "✅ User {uid} telah di-unban.",

    # ============================================
    # Ban/Unban confirmation (v3.0.4 - i18n)
    # ============================================
    "ban.confirm_title": "⚠️ <b>Konfirmasi Ban User</b>",
    "ban.confirm_body": "👤 Nama: <b>{name}</b>\n🆔 ID: <code>{uid}</code>\n📛 Username: {username}\n📁 File: {files:,}\n\nApakah Anda yakin ingin <b>MEM-BAN</b> user ini?\nMereka tidak akan bisa menggunakan bot lagi.",
    "ban.already_banned": "⚠️ User {uid} sudah di-ban.",
    "ban.success": "🚫 <b>User Di-ban</b>\n\n👤 {name}\n🆔 <code>{uid}</code>\n\n✅ User ini tidak bisa lagi menggunakan bot.\n🗑️ Cache mereka telah dibersihkan.",
    "unban.confirm_title": "🔓 <b>Konfirmasi Unban User</b>",
    "unban.confirm_body": "👤 Nama: <b>{name}</b>\n🆔 ID: <code>{uid}</code>\n📛 Username: {username}\n📁 File: {files:,}\n\nApakah Anda yakin ingin <b>MEMBUKA BAN</b> user ini?\nMereka akan dapat menggunakan bot kembali.",
    "unban.not_banned": "⚠️ User {uid} tidak sedang di-ban.",
    "unban.success": "🔓 <b>User Di-unban</b>\n\n👤 {name}\n🆔 <code>{uid}</code>\n\n✅ User ini sekarang bisa menggunakan bot kembali.",
    "ban.cancel": "✅ Operasi dibatalkan.",

    # Tombol konfirmasi ban/unban
    "ban.btn_confirm": "🚫 Ya, Ban",
    "unban.btn_confirm": "🔓 Ya, Unban",
    "ban.btn_cancel": "❌ Batal",

    # Pop-up alert (jawaban singkat yang muncul di atas)
    "ban.popup_session_expired": "⚠️ Sesi kedaluwarsa. Silakan coba lagi.",
    "ban.popup_access_denied": "❌ Akses ditolak.",
    "ban.popup_not_initiator": "❌ Hanya admin yang memulai yang dapat mengonfirmasi.",
    "ban.popup_cannot_ban_super": "❌ Tidak bisa mem‑ban super admin!",
    "ban.popup_already_banned": "Sudah di‑ban",
    "ban.popup_not_banned": "Tidak di‑ban",
    "ban.popup_cancelled": "Dibatalkan",
    "ban.popup_success_ban": "✅ User berhasil di‑ban!",
    "ban.popup_success_unban": "✅ User berhasil di‑unban!",

    # ============================================
    # Media Handler
    # ============================================
    "media.queue_full": "⚠️ Antrean Anda penuh (maks {maxsize} file). Mohon tunggu sebentar sebelum mengirim lagi.",
    "media.quota_full": "❌ Kuota Anda sudah penuh.\nGunakan /mylimit untuk cek detail.",
    "media.file_too_large": "❌ File terlalu besar ({size} bytes).\nMaksimum: {max_mb} MB",
    "media.global_full": "❌ Maaf, storage global sedang penuh.\nSilakan coba lagi nanti.",
}