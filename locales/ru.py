"""
Russian Translation Pack
Telegram Media Storage Bot v3.0.4
"""

TEXTS = {
    # ============================================
    # /start
    # ============================================
    "start.welcome": "👋 <b>Добро пожаловать, {name}!</b>",
    "start.bot_desc": "🤖 <b>Telegram Media Storage Bot v3.0.4</b>\nУмный мульти-пользовательский бот для хранения медиа с автоматической дедупликацией, шифрованием на уровне пользователя и возможностью удаления файлов.",
    "start.features_title": "✨ <b>Ключевые возможности:</b>",
    "start.feature_save": "• Сохранение фото, видео и документов",
    "start.feature_dedup": "• Автоматическое определение и отклонение дубликатов (индивидуально для пользователя)",
    "start.feature_privacy": "• Изолированное хранилище — ваши файлы видны только вам",
    "start.feature_autodel": "• {desc}",
    "start.feature_spoiler": "• <b>Подписи и спойлеры игнорируются</b> (сохраняется только файл)",
    "start.feature_album": "• Полная поддержка мульти-файловых альбомов",
    "start.feature_forward": "• Пересланные медиа также сохраняются",
    "start.feature_stats": "• Полная личная статистика в реальном времени",
    "start.feature_delete": "• Удаление файлов с безопасным подтверждением",
    "start.howto_title": "🚀 <b>Как использовать:</b>",
    "start.howto_desc": "Отправьте / перешлите медиа боту — и готово!",
    "start.commands_title": "📖 <b>Команды:</b>",
    "start.cmd_get": "/get — Открыть интерактивный файловый браузер",
    "start.cmd_stats": "/stats — Статистика и аптайм",
    "start.cmd_limit": "/mylimit — Проверить оставшуюся квоту",
    "start.cmd_delete": "/delete — Удалить сохраненные файлы",
    "start.cmd_help": "/help — Полная справка",
    "start.cmd_lang": "/language — Сменить язык (доступно 8)",
    "start.cmd_admin_msg": "@admin [сообщение] — Связаться с админом",
    "start.admin_title": "🔑 <b>Режим администратора активен</b>",
    "start.admin_cmd": "/admin — Панель администратора",
    "start.privacy_title": (
        "🔒 <b>Конфиденциальность гарантирована</b>\n"
        "• Каждый ваш файл хранится <b>изолированно</b> и доступен только вам.\n"
        "• <b>Администраторы не могут просматривать</b> или открывать файлы пользователей.\n"
        "• Данные не передаются третьим лицам, включая других пользователей.\n"
        "• Наша система использует защищённое хранилище, обеспечивая постоянную конфиденциальность."
    ),
    "start.autodel_desc_media": "Медиа-сообщения автоматически удаляются через {delay} сек.",
    "start.autodel_desc_all": "Сообщения автоматически удаляются через {delay} сек.",

    # ============================================
    # /help
    # ============================================
    "help.title": "📖 <b>ПОЛНАЯ СПРАВКА</b>",
    "help.subtitle": "Telegram Media Storage Bot v3.0.4",
    "help.section1_title": "📤 <b>1. Сохранение медиа</b>",
    "help.section1_desc": "Просто отправьте или перешлите медиа боту — всё автоматически.",
    "help.section1_support": "✅ Поддерживается: Фото, Видео, Документы",
    "help.section1_album": "✅ Мульти-файловые альбомы обрабатываются автоматически",
    "help.section1_forward": "✅ Пересланное из других чатов/каналов/групп сохраняется",
    "help.section1_duplicate": "🚫 Дубликаты автоматически отклоняются в вашем аккаунте",
    "help.section1_spoiler": "🧹 Подписи и спойлеры не сохраняются (только исходный файл)",
    "help.section1_delete": "🗑️ Исходное сообщение удаляется через {delay} сек.",
    "help.section2_title": "📥 <b>2. Получение файлов — /get</b>",
    "help.section2_intro": "Используйте <code>/get</code>, чтобы открыть <b>интерактивный файловый браузер</b>.",
    "help.section2_nav_title": "🎮 <b>Навигация по файловому браузеру:</b>",
    "help.section2_nav1": "• Нажмите <b>номер файла</b> — скачать один файл",
    "help.section2_nav2": "• Нажмите <b>👁️ Просмотр страницы</b> — скачать все файлы на странице",
    "help.section2_nav3": "• ⬅️ <b>Пред.</b> / <b>След.</b> ➡️ — переключение страниц",
    "help.section2_nav4": "• Нажмите <b>📄 номер страницы</b> — перейти на страницу",
    "help.section2_nav5": "• Введите номер страницы по запросу — быстрый доступ",
    "help.section2_nav6": "• На каждой странице до 10 файлов",
    "help.section2_admin": "\n🔑 <b>Для администраторов:</b>\n" +
                          "<code>/get user [ID]</code> — Просмотр файлов другого пользователя\n" +
                          "<code>/get</code> (админ) — Просмотр ВСЕХ файлов всех пользователей",
    "help.section2_delete": "\n🗑️ Загруженные результаты автоматически удаляются через {delay} сек.",
    "help.section3_title": "📊 <b>3. Статистика — /stats</b>",
    "help.section3_files": "• Общее количество файлов и размер хранилища",
    "help.section3_breakdown": "• Разбивка по типам (фото/видео/документы)",
    "help.section3_today": "• Загрузки и дубликаты за сегодня",
    "help.section3_uptime": "• Аптайм бота (дни/часы/минуты)",
    "help.section4_title": "📋 <b>4. Квота — /mylimit</b>",
    "help.section4_default": "• По умолчанию: {limit:,} файлов на пользователя",
    "help.section4_admin": "• Админ может регулировать квоту для каждого пользователя",
    "help.section4_unlimited": "• 0 = без ограничений",
    "help.section5_title": "🗑️ <b>5. Удаление файлов — /delete</b>",
    "help.section5_cmd": "<code>/delete [номер]</code> — Удалить конкретный файл",
    "help.section5_all": "<code>/delete all</code> — Удалить все ваши файлы",
    "help.section5_note": "⚠️ Всегда требуется подтверждение перед удалением!",
    "help.section6_title": "💬 <b>6. Связаться с администратором</b>",
    "help.section6_cmd": "Напишите <code>@admin [ваше сообщение]</code>",
    "help.section6_example": "Пример: <code>@admin Бот не обрабатывает видео</code>",
    "help.section6_reply": "Админ ответит через бота.",
    "help.section7_title": "🛡️ <b>7. Конфиденциальность и безопасность</b>",
    "help.section7_private": (
        "• Каждый сохранённый файл <b>доступен только вам</b>.\n"
        "  Никто, включая администраторов, не может просматривать, открывать или скачивать ваши файлы."
    ),
    "help.section7_noshare": (
        "• <b>Нулевое распространение данных.</b> Ваши файлы никогда не будут показаны другим пользователям,\n"
        "  а ваша статистика конфиденциальна."
    ),
    "help.section7_clean": (
        "• Исходные сообщения, отправленные боту, <b>автоматически удаляются</b> через несколько секунд.\n"
        "  Остаются только файлы в вашем защищённом хранилище."
    ),
    "help.section7_dedup": (
        "• Обнаружение дубликатов работает <b>индивидуально для каждого пользователя</b>. Файлы, уже имеющиеся в вашем аккаунте,\n"
        "  не будут приняты повторно, что сохраняет эффективность хранилища."
    ),
    "help.section7_encryption": (
        "• Хранилище использует механизмы <b>строгой изоляции</b> и защиту доступа на системном уровне.\n"
        "  Ваши данные никогда не читаются процессами, кроме вашей собственной сессии."
    ),
    "help.section8_title": "🌐 <b>8. Язык — /language</b>",
    "help.section8_desc": "Сменить язык интерфейса бота (доступно 8 языков).",
    "help.section8_list": "<code>/language</code> — Показать выбор языка",
    "help.section8_set": "Нажмите кнопку нужного языка",
    "help.section8_langs": "🇮🇩 ID | 🇬🇧 EN | 🇷🇺 RU | 🇨🇳 ZH | 🇯🇵 JA | 🇪🇸 ES | 🇮🇳 HI | 🇧🇷 PT",
    "help.section9_title": "💡 <b>9. Советы</b>",
    "help.section9_tip1": "• Пересылайте медиа из каналов/групп, чтобы сохранить их",
    "help.section9_tip2": "• Используйте /get для получения файлов в любое время",
    "help.section9_tip3": "• Подписи и спойлеры не сохраняются (только исходный файл)",
    "help.section9_tip4": "• Фото/видео альбомы обрабатываются как группа (эффективно)",
    "help.admin_title": "🔑 <b>10. КОМАНДЫ АДМИНИСТРАТОРА</b>",
    "help.admin_list": "<code>/admin</code> — Панель администратора",
    "help.admin_users": "<code>/admin users</code> — Список всех пользователей",
    "help.admin_user": "<code>/admin user [id]</code> — Информация о пользователе",
    "help.admin_add": "<code>/admin add [id]</code> — Добавить администратора (только супер-админ)",
    "help.admin_remove": "<code>/admin remove [id]</code> — Удалить администратора (только супер-админ)",
    "help.admin_setlimit": "<code>/admin setlimit [id] [n]</code> — Установить квоту пользователя",
    "help.admin_stats": "<code>/admin stats</code> — Глобальная статистика",
    "help.admin_messages": "<code>/admin messages</code> — Сообщения от пользователей",
    "help.admin_ban": "<code>/ban [id]</code> — Забанить пользователя",
    "help.admin_unban": "<code>/unban [id]</code> — Разбанить пользователя",
    "help.admin_broadcast": "<code>/broadcast [сообщение]</code> — Рассылка всем пользователям",
    "help.admin_reply": "<code>/reply [id] [текст]</code> — Ответить на сообщение пользователя",
    "help.admin_delete": "<code>/delete user [id] [номер|all]</code> — Удалить файл(ы) пользователя",
    "help.admin_get_user": "<code>/get user [id]</code> — Просмотр файлов конкретного пользователя",
    "help.footer": "🏷️ <b>v3.0.4</b> | Multi-User Edition | Изоляция на пользователя",
    "help.made_with": "Сделано с ❤️ с помощью python-telegram-bot",

    "help.privacy_bottom": (
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔐 <b>Ваша безопасность — наш приоритет.</b>\n"
        "Никто, включая команду разработчиков, не может видеть содержимое ваших файлов.\n"
        "Мы никогда не передаём ваши данные третьим лицам."
    ),

    # ============================================
    # /get
    # ============================================
    "get.banned": "❌ Вы забанены в этом боте.",
    "get.max_range": "⚠️ Максимум {max_range} файлов на странице.",
    "get.no_files": "📭 Файлы не найдены. Отправьте медиа, чтобы начать.",
    "get.error": "❌ Произошла ошибка. Попробуйте позже.",
    "get.invalid_input": "❌ Неверный ID пользователя или номер страницы.",
    "get.owner_label": "👤 Владелец: {owner} (ID: {owner_id})",

    # ============================================
    # Навигация файлового браузера
    # ============================================
    "nav.view_page": "👁️ Просмотр страницы {page}",
    "nav.prev": "⬅️ Пред.",
    "nav.next": "След. ➡️",
    "nav.back_all": "🔙 Назад ко всем файлам",
    "nav.my_files": "📂 Ваши файлы",
    "nav.all_files": "📂 Все файлы (вид админа)",
    "nav.user_files": "📂 Файлы пользователя: {name} (ID: {uid})",
    "nav.page_of": "📄 {page}/{total}",
    "nav.jump_prompt": "📄 Перейти на страницу? (1-{total})\nВведите номер страницы ниже 👇",
    "nav.jump_alert": "Пожалуйста, введите номер страницы (1-{total})",
    "nav.invalid_page": "❌ Страница должна быть от 1 до {total}.",
    "nav.invalid_number": "❌ Введите корректный номер страницы.",
    "nav.file_sent": "✅ {name} отправлен!",
    "nav.send_failed": "⚠️ Не удалось отправить файл. Попробуйте ещё раз.",
    "nav.no_file": "⚠️ Файл не найден.",
    "nav.no_files_page": "⚠️ На этой странице нет файлов.",
    "nav.files_sent": "✅ {count} файлов отправлено!",
    "nav.too_fast": "⚠️ Слишком быстро! Подождите немного...",
    "nav.session_expired": "⚠️ Сессия браузера истекла. Используйте /get снова.",
    "nav.generic_error": "⚠️ Произошла ошибка. Пожалуйста, попробуйте ещё раз.",
    # Навигация по файлам (дополнительно)
    "nav.range_indicator": "{start}-{end} из {total} файлов",
    "nav.navigation_hint": "📌 {num} из {total} файлов",
    "nav.navigation_hint_range": "📌 {start}-{end} из {total} файлов",
    "nav.invalid_file": "❌ Номер файла должен быть от 1 до {total}.",

    # ============================================
    # /stats
    # ============================================
    "stats.title": "📊 ЛИЧНАЯ СТАТИСТИКА",
    "stats.total_files": "📦 Всего файлов: {count:,}",
    "stats.quota": " / {limit:,} (квота)",
    "stats.total_size": "💾 Общий размер: {size}",
    "stats.by_type": "📂 По типам:",
    "stats.type_photo": "📸 {type}: {count:,} ({size})",
    "stats.type_video": "🎥 {type}: {count:,} ({size})",
    "stats.type_document": "📄 {type}: {count:,} ({size})",
    "stats.type_other": "📎 {type}: {count:,} ({size})",
    "stats.today_added": "📤 Сегодня: +{count} файлов",
    "stats.today_dup": "🔄 Отклонено (дубликаты): {count}",
    "stats.uptime": "🕐 Аптайм: {days}д {hours}ч {minutes}м",
    "stats.privacy_note": "🔒 Эта статистика видна только вам.",

    # ============================================
    # /mylimit
    # ============================================
    "limit.unlimited": "📊 Квота: Без ограничений\n📁 Сохранено файлов: {current:,}\n💾 Хранилище: {size}",
    "limit.limited": "📊 Квота: {current:,}/{limit:,} файлов\n📥 Осталось: {remaining:,} файлов\n💾 Хранилище: {size}",
    "limit.safe_note": "🛡️ Ваши файлы в безопасности даже при заполненной квоте. Вы просто не можете добавлять новые.",

    # ============================================
    # /delete (v3.0.3)
    # ============================================
    "delete.help_title": "🗑️ <b>УДАЛЕНИЕ ФАЙЛОВ</b>",
    "delete.help_desc": "Вы можете удалять сохранённые файлы. Используйте /get для просмотра номеров файлов.",
    "delete.help_commands": "📋 <b>Команды:</b>",
    "delete.help_single": "<code>/delete [номер]</code> — Удалить файл по номеру (1 = самый новый)",
    "delete.help_all": "<code>/delete all</code> — Удалить все ваши файлы",
    "delete.help_note": "⚠️ <b>Внимание:</b> Удаление необратимо! Будет запрошено подтверждение.",
    "delete.help_total": "📁 Всего ваших файлов: <b>{count:,}</b>",
    "delete.help_size": "💾 Общий размер: <b>{size}</b>",
    "delete.help_admin": "👤 Пользователь {name} (ID: {uid})\n📁 Файлов: {count:,}\n💾 Размер: {size}\n\nИспользуйте /delete user {uid} [номер|all]",
    "delete.banned": "❌ Вы забанены в этом боте.",
    "delete.invalid_format": "❌ Неверный формат. Используйте /delete для справки.",
    "delete.not_found": "❌ Файл с номером {num} не найден. Используйте /get для просмотра списка.",
    "delete.no_files": "📭 Нет файлов для удаления.",
    "delete.confirm_single": (
        "⚠️ <b>Подтверждение удаления файла</b>\n\n"
        "{emoji} <b>#{num}</b> — {name}\n"
        "📁 Тип: {type}\n"
        "💾 Размер: {size}\n\n"
        "Вы уверены, что хотите удалить этот файл?"
    ),
    "delete.confirm_single_admin": (
        "⚠️ <b>Подтверждение удаления файла (Админ)</b>\n\n"
        "👤 ID пользователя: {uid}\n"
        "{emoji} <b>#{num}</b> — {name}\n"
        "📁 Тип: {type}\n"
        "💾 Размер: {size}\n\n"
        "Вы уверены, что хотите удалить этот файл?"
    ),
    "delete.confirm_all": (
        "⚠️ <b>Подтверждение удаления всех файлов</b>\n\n"
        "📁 Всего файлов: <b>{count:,}</b>\n"
        "💾 Общий размер: <b>{size}</b>\n\n"
        "Вы уверены, что хотите удалить <b>ВСЕ</b> файлы?\n"
        "Это действие <b>НЕОБРАТИМО!</b>"
    ),
    "delete.confirm_all_admin": (
        "⚠️ <b>Подтверждение удаления всех файлов (Админ)</b>\n\n"
        "👤 Пользователь: {name} (ID: {uid})\n"
        "📁 Всего файлов: <b>{count:,}</b>\n"
        "💾 Общий размер: <b>{size}</b>\n\n"
        "Вы уверены, что хотите удалить <b>ВСЕ</b> файлы этого пользователя?"
    ),
    "delete.btn_confirm": "✅ Да, удалить",
    "delete.btn_confirm_all": "✅ Да, удалить все",
    "delete.btn_cancel": "❌ Отмена",
    "delete.cancelled": "✅ Удаление отменено.",
    "delete.success_single": "✅ Файл <b>#{num}</b> ({name}) успешно удалён.",
    "delete.success_single_admin": "✅ Файл <b>#{num}</b> ({name}) пользователя {uid} удалён.",
    "delete.success_all": "✅ <b>{count:,}</b> файлов удалено.",
    "delete.success_all_admin": "✅ <b>{count:,}</b> файлов пользователя {uid} удалено.",
    "delete.failed": "❌ Не удалось удалить файл. Попробуйте ещё раз.",
    "delete.not_owner": "❌ Вы не владелец этого файла.",
    "delete.not_admin": "❌ У вас нет прав администратора.",
    "delete.popup_session_expired": "⚠️ Сессия истекла. Попробуйте ещё раз.",

    # ============================================
    # /language
    # ============================================
    "language.select": "🌐 <b>Выберите язык:</b>\n\nВведите /language [код]\n\n{langs}",
    "language.current": "\n\n📌 Текущий: {current}",
    "language.changed": "✅ Язык изменён на {name}",
    "language.invalid": "❌ Неподдерживаемый язык. Используйте: {codes}",
    "language.unsupported": "❌ Язык не поддерживается.",
    "language.lang_item": "{emoji} {name} — <code>/language {code}</code>\n",
    "language.select_title": "🌐 <b>Выберите язык:</b>",

    # ============================================
    # @admin
    # ============================================
    "admin_msg.format": "✍️ Формат: @admin [сообщение]\nПример: @admin Бот выдаёт ошибку",
    "admin_msg.sent": "✅ Сообщение отправлено администратору. Мы ответим как можно скорее.",
    "admin_msg.notify": "📩 Сообщение от пользователя\n👤 {name} (ID: {uid})\n💬 {message}\n\nОтвет: /reply {msg_id} [сообщение]",

    # ============================================
    # Панель администратора
    # ============================================
    "admin.access_denied": "❌ Доступ запрещён. Только для администраторов.",
    "admin.panel_title": "🔑 ПАНЕЛЬ АДМИНИСТРАТОРА",
    "admin.panel_users": "👥 Всего пользователей: {count:,}",
    "admin.panel_files": "📁 Всего файлов: {count:,}",
    "admin.panel_admins": "🛡️ Администраторов в рантайме: {count}",
    "admin.panel_unread": "📩 Новых сообщений: {count} ⚠️",
    "admin.panel_commands": (
        "📋 Команды:\n"
        "/admin users — Список всех пользователей\n"
        "/admin user [id] — Информация о пользователе\n"
        "/admin add [id] — Добавить админа\n"
        "/admin remove [id] — Удалить админа\n"
        "/admin setlimit [id] [n] — Установить лимит\n"
        "/admin stats — Глобальная статистика\n"
        "/admin messages — Сообщения от пользователей\n"
        "/ban [id] — Забанить пользователя\n"
        "/unban [id] — Разбанить пользователя\n"
        "/broadcast [сообщение] — Рассылка всем пользователям\n"
        "/reply [id] [сообщение] — Ответить на сообщение\n"
        "/delete user [id] [n|all] — Удалить файлы пользователя\n"
        "/get user [id] — Просмотр файлов конкретного пользователя"
    ),
    # ============================================
    # Админ-панель - навигация по списку пользователей
    # ============================================
    "admin_users.invalid_page": "❌ Неверная страница.",
    "admin_users.access_denied": "❌ Доступ запрещён.",
    "admin.users_title": "👥 ЗАРЕГИСТРИРОВАННЫЕ ПОЛЬЗОВАТЕЛИ",
    "admin.users_item": "{i}. {name} (ID: {uid}) — {files:,} файл(ов){banned}",
    "admin.users_more": "\n... и ещё {count}.",
    "admin.users_empty": "Зарегистрированных пользователей пока нет.",
    "admin.user_title": "👤 ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ: {name}",
    "admin.user_id": "ID: {uid}",
    "admin.user_username": "Имя пользователя: @{username}",
    "admin.user_banned": "Статус бана: {status}",
    "admin.user_files": "Файлов: {files:,} / {limit}",
    "admin.user_storage": "Хранилище: {size}",
    "admin.user_by_type": "📂 По типам:",
    "admin.user_not_found": "❌ Пользователь не найден.",
    "admin.add_super_only": "❌ Только супер-админ может добавлять администраторов.",
    "admin.add_super_cannot": "❌ Супер-админ не может быть изменён.",
    "admin.add_success": "✅ Пользователь {uid} повышен до администратора.",
    "admin.add_already": "⚠️ Пользователь уже является администратором.",
    "admin.remove_super_only": "❌ Только супер-админ может удалять администраторов.",
    "admin.remove_super_cannot": "❌ Супер-админ не может быть удалён.",
    "admin.remove_success": "✅ Пользователь {uid} понижен с администратора.",
    "admin.remove_not": "⚠️ Пользователь не является администратором.",
    "admin.setlimit_success": "✅ Лимит файлов для пользователя {uid} установлен на {limit:,}.",
    "admin.global_title": "📊 ГЛОБАЛЬНАЯ СТАТИСТИКА",
    "admin.global_users": "👥 Всего пользователей: {count:,}",
    "admin.global_files": "📁 Всего файлов: {count:,}",
    "admin.global_storage": "💾 Общий объём: {size}",
    "admin.global_served": "📤 Всего обслужено файлов: {count:,}",
    "admin.global_top": "🏆 Топ-5 пользователей:",
    "admin.global_top_item": "  {i}. {name} — {files:,} файл(ов)",
    "admin.broadcast_format": "📢 Формат: /broadcast [сообщение]\nПример: /broadcast Технические работы в 22:00 МСК",
    "admin.broadcast_sending": "📤 Отправка рассылки {total} пользователям...",
    "admin.broadcast_progress": (
        "📤 Отправка рассылки...\n"
        "▸ Прогресс: {sent}/{total}\n"
        "▸ Успешно: {success}\n"
        "▸ Ошибок: {failed}"
    ),
    "admin.broadcast_done": "✅ Рассылка завершена\n📤 Доставлено: {success}\n❌ Ошибок: {failed}\n👥 Всего: {total}",
    "admin.broadcast_msg": "📢 Объявление администратора\n\n{message}",
    "admin.broadcast_skipped": "\n⚠️ Пропущено {skipped} забаненных/неактивных пользователей",
    "admin.reply_format": "↩️ Формат: /reply [id_сообщения] [ответ]\nИспользуйте /admin messages для просмотра списка сообщений",
    "admin.reply_invalid_id": "❌ Неверный ID сообщения.",
    "admin.reply_not_found": "❌ Сообщение не найдено.",
    "admin.reply_already": "⚠️ На это сообщение уже был дан ответ.",
    "admin.reply_failed": "❌ Не удалось отправить ответ: {error}",
    "admin.reply_sent": "✅ Ответ отправлен пользователю {uid}",
    "admin.reply_to_user": "🔰 Администратор ответил на ваше сообщение:\n\n💬 Ваше сообщение: {original}\n\n↩️ Ответ администратора: {reply}",
    "admin.reply_failed_delivery": "❌ Не удалось отправить ответ: сообщение не может быть доставлено.",
    "admin.messages_title": "📩 СООБЩЕНИЯ ОТ ПОЛЬЗОВАТЕЛЕЙ",
    "admin.messages_item": "#{id} | {name} (ID: {uid})\n💬 {text}\nОтвет: /reply {id} [сообщение]\n\n",
    "admin.messages_empty": "📭 Нет новых сообщений.",
    "admin.messages_max": "\n⚠️ Показаны 20 последних сообщений.",
    "admin.ban_usage": "Использование: /ban [user_id]",
    "admin.ban_invalid": "❌ Неверный ID пользователя.",
    "admin.ban_super": "❌ Нельзя забанить супер-админа.",
    "admin.ban_success": "🚫 Пользователь {uid} забанен.",
    "admin.unban_usage": "Использование: /unban [user_id]",
    "admin.unban_success": "✅ Пользователь {uid} разбанен.",

    # ============================================
    # Подтверждение бана/разбана (v3.0.4 - i18n)
    # ============================================
    "ban.confirm_title": "⚠️ <b>Подтверждение бана</b>",
    "ban.confirm_body": "👤 Имя: <b>{name}</b>\n🆔 ID: <code>{uid}</code>\n📛 Username: {username}\n📁 Файлов: {files:,}\n\nВы уверены, что хотите <b>ЗАБАНИТЬ</b> этого пользователя?\nОн больше не сможет использовать бота.",
    "ban.already_banned": "⚠️ Пользователь {uid} уже забанен.",
    "ban.success": "🚫 <b>Пользователь забанен</b>\n\n👤 {name}\n🆔 <code>{uid}</code>\n\n✅ Этот пользователь больше не может использовать бота.\n🗑️ Его кэш очищен.",
    "unban.confirm_title": "🔓 <b>Подтверждение разбана</b>",
    "unban.confirm_body": "👤 Имя: <b>{name}</b>\n🆔 ID: <code>{uid}</code>\n📛 Username: {username}\n📁 Файлов: {files:,}\n\nВы уверены, что хотите <b>РАЗБАНИТЬ</b> этого пользователя?\nОн снова сможет пользоваться ботом.",
    "unban.not_banned": "⚠️ Пользователь {uid} не забанен.",
    "unban.success": "🔓 <b>Пользователь разбанен</b>\n\n👤 {name}\n🆔 <code>{uid}</code>\n\n✅ Теперь этот пользователь может использовать бота.",
    "ban.cancel": "✅ Операция отменена.",

    "ban.btn_confirm": "🚫 Да, забанить",
    "unban.btn_confirm": "🔓 Да, разбанить",
    "ban.btn_cancel": "❌ Отмена",

    "ban.popup_session_expired": "⚠️ Сессия истекла. Попробуйте ещё раз.",
    "ban.popup_access_denied": "❌ Доступ запрещён.",
    "ban.popup_not_initiator": "❌ Только инициировавший админ может подтвердить.",
    "ban.popup_cannot_ban_super": "❌ Нельзя забанить супер-админа!",
    "ban.popup_already_banned": "Уже забанен",
    "ban.popup_not_banned": "Не забанен",
    "ban.popup_cancelled": "Отменено",
    "ban.popup_success_ban": "✅ Пользователь успешно забанен!",
    "ban.popup_success_unban": "✅ Пользователь успешно разбанен!",

    # ============================================
    # Обработчик медиа
    # ============================================
    "media.queue_full": "⚠️ Ваша очередь заполнена (макс. {maxsize} файлов). Пожалуйста, подождите перед отправкой новых файлов.",
    "media.quota_full": "❌ Ваша квота заполнена.\nИспользуйте /mylimit для подробностей.",
    "media.file_too_large": "❌ Файл слишком большой ({size} байт).\nМаксимум: {max_mb} МБ",
    "media.global_full": "❌ Извините, глобальное хранилище заполнено.\nПожалуйста, попробуйте позже.",
}