"""
Spanish Translation Pack
Telegram Media Storage Bot v3.0.4
"""

TEXTS = {
    # ============================================
    # /start
    # ============================================
    "start.welcome": "👋 <b>¡Bienvenido, {name}!</b>",
    "start.bot_desc": "🤖 <b>Telegram Media Storage Bot v3.0.4</b>\nBot inteligente multiusuario de almacenamiento de medios con deduplicación automática, cifrado por usuario y eliminación de archivos.",
    "start.features_title": "✨ <b>Características Destacadas:</b>",
    "start.feature_save": "• Guarda fotos, videos y documentos",
    "start.feature_dedup": "• Detección y rechazo automático de duplicados (por usuario)",
    "start.feature_privacy": "• Almacenamiento aislado — tus archivos solo visibles para ti",
    "start.feature_autodel": "• {desc}",
    "start.feature_spoiler": "• <b>Se ignoran subtítulos y spoilers</b> (solo se guarda el archivo)",
    "start.feature_album": "• Álbumes con múltiples archivos totalmente compatibles",
    "start.feature_forward": "• Los medios reenviados también se guardan",
    "start.feature_stats": "• Estadísticas personales completas en tiempo real",
    "start.feature_delete": "• Elimina archivos con confirmación segura",
    "start.howto_title": "🚀 <b>Cómo usar:</b>",
    "start.howto_desc": "Envía o reenvía cualquier medio al bot — ¡listo!",
    "start.commands_title": "📖 <b>Comandos:</b>",
    "start.cmd_get": "/get — Abre el navegador interactivo de archivos",
    "start.cmd_stats": "/stats — Estadísticas y uptime",
    "start.cmd_limit": "/mylimit — Ver cuota restante",
    "start.cmd_delete": "/delete — Eliminar archivos guardados",
    "start.cmd_help": "/help — Guía de ayuda completa",
    "start.cmd_lang": "/language — Cambiar idioma (8 disponibles)",
    "start.cmd_admin_msg": "@admin [mensaje] — Contactar al admin",
    "start.admin_title": "🔑 <b>Modo Admin Activo</b>",
    "start.admin_cmd": "/admin — Panel de administración",
    "start.privacy_title": (
        "🔒 <b>Privacidad Garantizada</b>\n"
        "• Cada archivo tuyo se guarda de forma <b>aislada</b> y solo tú puedes acceder a él.\n"
        "• <b>Los administradores no pueden ver</b> ni abrir los archivos de ningún usuario.\n"
        "• No se comparten datos con terceros, incluyendo otros usuarios.\n"
        "• Nuestro sistema utiliza almacenamiento protegido para mantener tu privacidad siempre segura."
    ),
    "start.autodel_desc_media": "Los mensajes multimedia se eliminan automáticamente después de {delay} segundos",
    "start.autodel_desc_all": "Los mensajes se eliminan automáticamente después de {delay} segundos",

    # ============================================
    # /help
    # ============================================
    "help.title": "📖 <b>AYUDA COMPLETA</b>",
    "help.subtitle": "Telegram Media Storage Bot v3.0.4",
    "help.section1_title": "📤 <b>1. Guardando Medios</b>",
    "help.section1_desc": "Simplemente envía o reenvía medios al bot — todo automático.",
    "help.section1_support": "✅ Soportado: Fotos, Videos, Documentos",
    "help.section1_album": "✅ Álbumes multiarchivo procesados automáticamente",
    "help.section1_forward": "✅ Los reenvíos desde otros chats/canales/grupos se guardan",
    "help.section1_duplicate": "🚫 Duplicados rechazados automáticamente dentro de tu cuenta",
    "help.section1_spoiler": "🧹 Subtítulos y spoilers no se guardan (solo archivo original)",
    "help.section1_delete": "🗑️ Mensaje original eliminado después de {delay} segundos",
    "help.section2_title": "📥 <b>2. Recuperar Archivos — /get</b>",
    "help.section2_intro": "Usa <code>/get</code> para abrir el <b>navegador interactivo de archivos</b>.",
    "help.section2_nav_title": "🎮 <b>Navegación del Navegador de Archivos:</b>",
    "help.section2_nav1": "• Pulsa un <b>número de archivo</b> — descarga ese archivo",
    "help.section2_nav2": "• Pulsa <b>👁️ Ver Página</b> — descarga todos los archivos de la página",
    "help.section2_nav3": "• ⬅️ <b>Ant</b> / <b>Sig</b> ➡️ — cambiar de página",
    "help.section2_nav4": "• Pulsa un <b>📄 número de página</b> — saltar a esa página",
    "help.section2_nav5": "• Escribe un número de página cuando se solicite — acceso rápido",
    "help.section2_nav6": "• Cada página muestra hasta 10 archivos",
    "help.section2_admin": "\n🔑 <b>Para Administradores:</b>\n" +
                          "<code>/get user [ID]</code> — Ver archivos de otro usuario\n" +
                          "<code>/get</code> (admin) — Ver TODOS los archivos de todos los usuarios",
    "help.section2_delete": "\n🗑️ Los resultados descargados se eliminan automáticamente después de {delay} segundos",
    "help.section3_title": "📊 <b>3. Estadísticas — /stats</b>",
    "help.section3_files": "• Total de archivos y tamaño de almacenamiento",
    "help.section3_breakdown": "• Desglose por tipo (foto/video/documento)",
    "help.section3_today": "• Subidas y duplicados de hoy",
    "help.section3_uptime": "• Uptime del bot (días/horas/minutos)",
    "help.section4_title": "📋 <b>4. Cuota — /mylimit</b>",
    "help.section4_default": "• Por defecto: {limit:,} archivos por usuario",
    "help.section4_admin": "• Los administradores pueden ajustar la cuota por usuario",
    "help.section4_unlimited": "• 0 = ilimitado",
    "help.section5_title": "🗑️ <b>5. Eliminar Archivos — /delete</b>",
    "help.section5_cmd": "<code>/delete [número]</code> — Eliminar un archivo específico",
    "help.section5_all": "<code>/delete all</code> — Eliminar todos tus archivos",
    "help.section5_note": "⚠️ ¡Siempre se pide confirmación antes de eliminar!",
    "help.section6_title": "💬 <b>6. Contactar al Admin</b>",
    "help.section6_cmd": "Escribe <code>@admin [tu mensaje]</code>",
    "help.section6_example": "Ejemplo: <code>@admin El bot falla al subir videos</code>",
    "help.section6_reply": "El admin responderá a través del bot.",
    "help.section7_title": "🛡️ <b>7. Privacidad y Seguridad</b>",
    "help.section7_private": (
        "• Cada archivo que guardas <b>es accesible solo por ti</b>.\n"
        "  Nadie —incluidos los administradores— puede ver, abrir o descargar tus archivos."
    ),
    "help.section7_noshare": (
        "• <b>Cero compartición de datos.</b> Tus archivos nunca se mostrarán a otros usuarios,\n"
        "  y tus estadísticas son privadas."
    ),
    "help.section7_clean": (
        "• Los mensajes originales que envías al bot se <b>eliminan automáticamente</b> después de unos segundos.\n"
        "  Solo quedan los archivos almacenados en tu almacenamiento seguro."
    ),
    "help.section7_dedup": (
        "• La detección de duplicados funciona <b>por usuario</b>. Los archivos ya existentes en tu cuenta\n"
        "  no serán aceptados de nuevo, manteniendo el almacenamiento eficiente."
    ),
    "help.section7_encryption": (
        "• El almacenamiento utiliza mecanismos de <b>aislamiento estricto</b> y protección de acceso a nivel de sistema.\n"
        "  Tus datos nunca son leídos por procesos que no sean tu propia sesión."
    ),
    "help.section8_title": "🌐 <b>8. Idioma — /language</b>",
    "help.section8_desc": "Cambia el idioma de la interfaz del bot (8 idiomas disponibles).",
    "help.section8_list": "<code>/language</code> — Mostrar selección de idioma",
    "help.section8_set": "Toca el botón del idioma deseado",
    "help.section8_langs": "🇮🇩 ID | 🇬🇧 EN | 🇷🇺 RU | 🇨🇳 ZH | 🇯🇵 JA | 🇪🇸 ES | 🇮🇳 HI | 🇧🇷 PT",
    "help.section9_title": "💡 <b>9. Consejos</b>",
    "help.section9_tip1": "• Reenvía medios desde canales/grupos para guardarlos",
    "help.section9_tip2": "• Usa /get para recuperar archivos en cualquier momento",
    "help.section9_tip3": "• Los subtítulos y spoilers no se almacenan (solo el archivo original)",
    "help.section9_tip4": "• Álbumes de fotos/videos se procesan como grupo (eficiente)",
    "help.admin_title": "🔑 <b>10. COMANDOS DE ADMIN</b>",
    "help.admin_list": "<code>/admin</code> — Panel de administración",
    "help.admin_users": "<code>/admin users</code> — Lista de todos los usuarios",
    "help.admin_user": "<code>/admin user [id]</code> — Detalles del usuario",
    "help.admin_add": "<code>/admin add [id]</code> — Agregar admin (solo super admin)",
    "help.admin_remove": "<code>/admin remove [id]</code> — Quitar admin (solo super admin)",
    "help.admin_setlimit": "<code>/admin setlimit [id] [n]</code> — Establecer cuota",
    "help.admin_stats": "<code>/admin stats</code> — Estadísticas globales",
    "help.admin_messages": "<code>/admin messages</code> — Mensajes de usuarios",
    "help.admin_ban": "<code>/ban [id]</code> — Banear usuario",
    "help.admin_unban": "<code>/unban [id]</code> — Desbanear usuario",
    "help.admin_broadcast": "<code>/broadcast [mensaje]</code> — Difundir a todos los usuarios",
    "help.admin_reply": "<code>/reply [id] [texto]</code> — Responder a un mensaje de usuario",
    "help.admin_delete": "<code>/delete user [id] [número|all]</code> — Eliminar archivo(s) de usuario",
    "help.admin_get_user": "<code>/get user [id]</code> — Ver archivos de un usuario específico",
    "help.footer": "🏷️ <b>v3.0.4</b> | Edición Multiusuario | Aislamiento por Usuario",
    "help.made_with": "Hecho con ❤️ usando python-telegram-bot",

    "help.privacy_bottom": (
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔐 <b>Tu seguridad es nuestra prioridad.</b>\n"
        "Nadie —incluido el equipo de desarrollo— puede ver el contenido de tus archivos.\n"
        "Nunca compartimos tus datos con terceros."
    ),

    # ============================================
    # /get
    # ============================================
    "get.banned": "❌ Has sido baneado de este bot.",
    "get.max_range": "⚠️ Máximo {max_range} archivos por página.",
    "get.no_files": "📭 No se encontraron archivos. Envía medios para comenzar.",
    "get.error": "❌ Ocurrió un error. Intenta más tarde.",
    "get.invalid_input": "❌ ID de usuario o número de página no válido.",
    "get.owner_label": "👤 Propietario: {owner} (ID: {owner_id})",

    # ============================================
    # Navegación del Navegador de Archivos
    # ============================================
    "nav.view_page": "👁️ Ver Página {page}",
    "nav.prev": "⬅️ Ant",
    "nav.next": "Sig ➡️",
    "nav.back_all": "🔙 Volver a Todos los Archivos",
    "nav.my_files": "📂 Tus Archivos",
    "nav.all_files": "📂 Todos los Archivos (Vista Admin)",
    "nav.user_files": "📂 Archivos de: {name} (ID: {uid})",
    "nav.page_of": "📄 {page}/{total}",
    "nav.jump_prompt": "📄 ¿Saltar a página? (1-{total})\nEscribe el número de página abajo 👇",
    "nav.jump_alert": "Por favor escribe un número de página (1-{total})",
    "nav.invalid_page": "❌ La página debe estar entre 1-{total}.",
    "nav.invalid_number": "❌ Introduce un número de página válido.",
    "nav.file_sent": "✅ ¡{name} enviado!",
    "nav.send_failed": "⚠️ Error al enviar archivo. Intenta de nuevo.",
    "nav.no_file": "⚠️ Archivo no encontrado.",
    "nav.no_files_page": "⚠️ No hay archivos en esta página.",
    "nav.files_sent": "✅ ¡{count} archivos enviados!",
    "nav.too_fast": "⚠️ ¡Demasiado rápido! Espera un momento...",
    "nav.session_expired": "⚠️ La sesión del navegador expiró. Usa /get de nuevo.",
    "nav.generic_error": "⚠️ Ocurrió un error. Inténtalo de nuevo.",
    # Navegación de archivos (adicional)
    "nav.range_indicator": "{start}-{end} de {total} archivos",
    "nav.navigation_hint": "📌 {num} de {total} archivos",
    "nav.navigation_hint_range": "📌 {start}-{end} de {total} archivos",
    "nav.invalid_file": "❌ El número de archivo debe ser 1-{total}.",

    # ============================================
    # /stats
    # ============================================
    "stats.title": "📊 ESTADÍSTICAS PERSONALES",
    "stats.total_files": "📦 Total archivos: {count:,}",
    "stats.quota": " / {limit:,} (cuota)",
    "stats.total_size": "💾 Tamaño total: {size}",
    "stats.by_type": "📂 Por Tipo:",
    "stats.type_photo": "📸 {type}: {count:,} ({size})",
    "stats.type_video": "🎥 {type}: {count:,} ({size})",
    "stats.type_document": "📄 {type}: {count:,} ({size})",
    "stats.type_other": "📎 {type}: {count:,} ({size})",
    "stats.today_added": "📤 Hoy: +{count} archivos",
    "stats.today_dup": "🔄 Rechazados (duplicados): {count}",
    "stats.uptime": "🕐 Uptime: {days}d {hours}h {minutes}m",
    "stats.privacy_note": "🔒 Estas estadísticas solo son visibles para ti.",

    # ============================================
    # /mylimit
    # ============================================
    "limit.unlimited": "📊 Cuota: Ilimitada\n📁 Archivos guardados: {current:,}\n💾 Almacenamiento: {size}",
    "limit.limited": "📊 Cuota: {current:,}/{limit:,} archivos\n📥 Restantes: {remaining:,} archivos\n💾 Almacenamiento: {size}",
    "limit.safe_note": "🛡️ Tus archivos permanecen seguros incluso si la cuota está llena. Simplemente no puedes agregar nuevos archivos.",

    # ============================================
    # /delete (v3.0.3)
    # ============================================
    "delete.help_title": "🗑️ <b>ELIMINAR ARCHIVOS</b>",
    "delete.help_desc": "Puedes eliminar archivos guardados. Usa /get para ver los números de archivo.",
    "delete.help_commands": "📋 <b>Comandos:</b>",
    "delete.help_single": "<code>/delete [número]</code> — Eliminar archivo por número (1 = más nuevo)",
    "delete.help_all": "<code>/delete all</code> — Eliminar todos tus archivos",
    "delete.help_note": "⚠️ <b>Advertencia:</b> ¡La eliminación no se puede deshacer! Se pedirá confirmación.",
    "delete.help_total": "📁 Total de tus archivos: <b>{count:,}</b>",
    "delete.help_size": "💾 Tamaño total: <b>{size}</b>",
    "delete.help_admin": "👤 Usuario {name} (ID: {uid})\n📁 Archivos: {count:,}\n💾 Tamaño: {size}\n\nUsa /delete user {uid} [número|all]",
    "delete.banned": "❌ Has sido baneado de este bot.",
    "delete.invalid_format": "❌ Formato no válido. Usa /delete para ayuda.",
    "delete.not_found": "❌ Archivo número {num} no encontrado. Usa /get para ver la lista.",
    "delete.no_files": "📭 No hay archivos para eliminar.",
    "delete.confirm_single": (
        "⚠️ <b>Confirmar Eliminación de Archivo</b>\n\n"
        "{emoji} <b>#{num}</b> — {name}\n"
        "📁 Tipo: {type}\n"
        "💾 Tamaño: {size}\n\n"
        "¿Estás seguro de que deseas eliminar este archivo?"
    ),
    "delete.confirm_single_admin": (
        "⚠️ <b>Confirmar Eliminación de Archivo (Admin)</b>\n\n"
        "👤 ID de Usuario: {uid}\n"
        "{emoji} <b>#{num}</b> — {name}\n"
        "📁 Tipo: {type}\n"
        "💾 Tamaño: {size}\n\n"
        "¿Estás seguro de que deseas eliminar este archivo?"
    ),
    "delete.confirm_all": (
        "⚠️ <b>Confirmar Eliminar Todos los Archivos</b>\n\n"
        "📁 Total archivos: <b>{count:,}</b>\n"
        "💾 Tamaño total: <b>{size}</b>\n\n"
        "¿Estás seguro de que deseas eliminar <b>TODOS</b> los archivos?\n"
        "¡Esta acción <b>NO SE PUEDE DESHACER!</b>"
    ),
    "delete.confirm_all_admin": (
        "⚠️ <b>Confirmar Eliminar Todos los Archivos (Admin)</b>\n\n"
        "👤 Usuario: {name} (ID: {uid})\n"
        "📁 Total archivos: <b>{count:,}</b>\n"
        "💾 Tamaño total: <b>{size}</b>\n\n"
        "¿Estás seguro de que deseas eliminar <b>TODOS</b> los archivos de este usuario?"
    ),
    "delete.btn_confirm": "✅ Sí, Eliminar",
    "delete.btn_confirm_all": "✅ Sí, Eliminar Todos",
    "delete.btn_cancel": "❌ Cancelar",
    "delete.cancelled": "✅ Eliminación cancelada.",
    "delete.success_single": "✅ Archivo <b>#{num}</b> ({name}) eliminado correctamente.",
    "delete.success_single_admin": "✅ Archivo <b>#{num}</b> ({name}) del usuario {uid} eliminado.",
    "delete.success_all": "✅ <b>{count:,}</b> archivos eliminados correctamente.",
    "delete.success_all_admin": "✅ <b>{count:,}</b> archivos del usuario {uid} eliminados.",
    "delete.failed": "❌ Error al eliminar archivo. Intenta de nuevo.",
    "delete.not_owner": "❌ No eres el propietario de este archivo.",
    "delete.not_admin": "❌ No tienes acceso de administrador.",
    "delete.popup_session_expired": "⚠️ Sesión expirada. Intenta de nuevo.",

    # ============================================
    # /language
    # ============================================
    "language.select": "🌐 <b>Seleccionar Idioma:</b>\n\nEscribe /language [código]\n\n{langs}",
    "language.current": "\n\n📌 Actual: {current}",
    "language.changed": "✅ Idioma cambiado a {name}",
    "language.invalid": "❌ Idioma no soportado. Usa: {codes}",
    "language.unsupported": "❌ Idioma no soportado.",
    "language.lang_item": "{emoji} {name} — <code>/language {code}</code>\n",
    "language.select_title": "🌐 <b>Seleccionar Idioma:</b>",

    # ============================================
    # @admin
    # ============================================
    "admin_msg.format": "✍️ Formato: @admin [mensaje]\nEjemplo: @admin El bot está fallando",
    "admin_msg.sent": "✅ Mensaje enviado al admin. Responderemos lo antes posible.",
    "admin_msg.notify": "📩 Mensaje de usuario\n👤 {name} (ID: {uid})\n💬 {message}\n\nResponder: /reply {msg_id} [mensaje]",

    # ============================================
    # Panel de Administración
    # ============================================
    "admin.access_denied": "❌ Acceso denegado. Solo admin.",
    "admin.panel_title": "🔑 PANEL DE ADMIN",
    "admin.panel_users": "👥 Total usuarios: {count:,}",
    "admin.panel_files": "📁 Total archivos: {count:,}",
    "admin.panel_admins": "🛡️ Admins en runtime: {count}",
    "admin.panel_unread": "📩 Nuevos mensajes: {count} ⚠️",
    "admin.panel_commands": (
        "📋 Comandos:\n"
        "/admin users — Listar todos los usuarios\n"
        "/admin user [id] — Detalle de usuario\n"
        "/admin add [id] — Agregar admin\n"
        "/admin remove [id] — Quitar admin\n"
        "/admin setlimit [id] [n] — Establecer límite\n"
        "/admin stats — Estadísticas globales\n"
        "/admin messages — Mensajes de usuarios\n"
        "/ban [id] — Banear usuario\n"
        "/unban [id] — Desbanear usuario\n"
        "/broadcast [mensaje] — Enviar a todos los usuarios\n"
        "/reply [id] [mensaje] — Responder a un mensaje\n"
        "/delete user [id] [n|all] — Eliminar archivo(s) de usuario\n"
        "/get user [id] — Ver archivos de un usuario específico"
    ),
    # ============================================
    # Panel de Admin - navegación de lista de usuarios
    # ============================================
    "admin_users.invalid_page": "❌ Página no válida.",
    "admin_users.access_denied": "❌ Acceso denegado.",
    "admin.users_title": "👥 USUARIOS REGISTRADOS",
    "admin.users_item": "{i}. {name} (ID: {uid}) — {files:,} archivo(s){banned}",
    "admin.users_more": "\n... y {count} más.",
    "admin.users_empty": "Aún no hay usuarios registrados.",
    "admin.user_title": "👤 DETALLE DE USUARIO: {name}",
    "admin.user_id": "ID: {uid}",
    "admin.user_username": "Usuario: @{username}",
    "admin.user_banned": "Estado de baneo: {status}",
    "admin.user_files": "Archivos: {files:,} / {limit}",
    "admin.user_storage": "Almacenamiento: {size}",
    "admin.user_by_type": "📂 Por Tipo:",
    "admin.user_not_found": "❌ Usuario no encontrado.",
    "admin.add_super_only": "❌ Solo el super admin puede agregar administradores.",
    "admin.add_super_cannot": "❌ El super admin no puede ser modificado.",
    "admin.add_success": "✅ El usuario {uid} ha sido promovido a administrador.",
    "admin.add_already": "⚠️ El usuario ya es administrador.",
    "admin.remove_super_only": "❌ Solo el super admin puede quitar administradores.",
    "admin.remove_super_cannot": "❌ El super admin no puede ser eliminado.",
    "admin.remove_success": "✅ El usuario {uid} ha sido degradado de administrador.",
    "admin.remove_not": "⚠️ El usuario no es administrador.",
    "admin.setlimit_success": "✅ Límite de archivos para el usuario {uid} establecido en {limit:,}.",
    "admin.global_title": "📊 ESTADÍSTICAS GLOBALES",
    "admin.global_users": "👥 Total usuarios: {count:,}",
    "admin.global_files": "📁 Total archivos: {count:,}",
    "admin.global_storage": "💾 Almacenamiento total: {size}",
    "admin.global_served": "📤 Archivos servidos: {count:,}",
    "admin.global_top": "🏆 Top 5 Usuarios:",
    "admin.global_top_item": "  {i}. {name} — {files:,} archivo(s)",
    "admin.broadcast_format": "📢 Formato: /broadcast [mensaje]\nEjemplo: /broadcast Mantenimiento programado a las 22:00 UTC",
    "admin.broadcast_sending": "📤 Enviando difusión a {total} usuarios...",
    "admin.broadcast_progress": (
        "📤 Enviando difusión...\n"
        "▸ Progreso: {sent}/{total}\n"
        "▸ Exitosos: {success}\n"
        "▸ Fallidos: {failed}"
    ),
    "admin.broadcast_done": "✅ Difusión completada\n📤 Entregados: {success}\n❌ Fallidos: {failed}\n👥 Total: {total}",
    "admin.broadcast_msg": "📢 Anuncio del Administrador\n\n{message}",
    "admin.broadcast_skipped": "\n⚠️ Omitidos {skipped} usuarios baneados/inactivos",
    "admin.reply_format": "↩️ Formato: /reply [id_mensaje] [respuesta]\nUsa /admin messages para ver la lista de mensajes",
    "admin.reply_invalid_id": "❌ ID de mensaje no válido.",
    "admin.reply_not_found": "❌ Mensaje no encontrado.",
    "admin.reply_already": "⚠️ Este mensaje ya ha sido respondido.",
    "admin.reply_failed": "❌ Error al enviar respuesta: {error}",
    "admin.reply_sent": "✅ Respuesta enviada al usuario {uid}",
    "admin.reply_to_user": "🔰 El administrador respondió a tu mensaje:\n\n💬 Tu mensaje: {original}\n\n↩️ Respuesta del admin: {reply}",
    "admin.reply_failed_delivery": "❌ Error al enviar respuesta: no se pudo entregar el mensaje.",
    "admin.messages_title": "📩 MENSAJES DE USUARIOS",
    "admin.messages_item": "#{id} | {name} (ID: {uid})\n💬 {text}\nResponder: /reply {id} [contenido]\n\n",
    "admin.messages_empty": "📭 No hay mensajes nuevos.",
    "admin.messages_max": "\n⚠️ Mostrando los 20 mensajes más recientes.",
    "admin.ban_usage": "Uso: /ban [user_id]",
    "admin.ban_invalid": "❌ ID de usuario no válido.",
    "admin.ban_super": "❌ No se puede banear al super admin.",
    "admin.ban_success": "🚫 El usuario {uid} ha sido baneado.",
    "admin.unban_usage": "Uso: /unban [user_id]",
    "admin.unban_success": "✅ El usuario {uid} ha sido desbaneado.",

    # ============================================
    # Confirmación de Ban/Desban (v3.0.4 - i18n)
    # ============================================
    "ban.confirm_title": "⚠️ <b>Confirmar Banear Usuario</b>",
    "ban.confirm_body": "👤 Nombre: <b>{name}</b>\n🆔 ID: <code>{uid}</code>\n📛 Usuario: {username}\n📁 Archivos: {files:,}\n\n¿Estás seguro de que deseas <b>BANEAR</b> a este usuario?\nNo podrá volver a usar el bot.",
    "ban.already_banned": "⚠️ El usuario {uid} ya está baneado.",
    "ban.success": "🚫 <b>Usuario Baneado</b>\n\n👤 {name}\n🆔 <code>{uid}</code>\n\n✅ Este usuario ya no puede usar el bot.\n🗑️ Su caché ha sido limpiado.",
    "unban.confirm_title": "🔓 <b>Confirmar Desbanear Usuario</b>",
    "unban.confirm_body": "👤 Nombre: <b>{name}</b>\n🆔 ID: <code>{uid}</code>\n📛 Usuario: {username}\n📁 Archivos: {files:,}\n\n¿Estás seguro de que deseas <b>DESBANEAR</b> a este usuario?\nPodrá volver a usar el bot.",
    "unban.not_banned": "⚠️ El usuario {uid} no está baneado actualmente.",
    "unban.success": "🔓 <b>Usuario Desbaneado</b>\n\n👤 {name}\n🆔 <code>{uid}</code>\n\n✅ Ahora este usuario puede usar el bot nuevamente.",
    "ban.cancel": "✅ Operación cancelada.",

    "ban.btn_confirm": "🚫 Sí, Banear",
    "unban.btn_confirm": "🔓 Sí, Desbanear",
    "ban.btn_cancel": "❌ Cancelar",

    "ban.popup_session_expired": "⚠️ Sesión expirada. Intenta de nuevo.",
    "ban.popup_access_denied": "❌ Acceso denegado.",
    "ban.popup_not_initiator": "❌ Solo el administrador que inició puede confirmar.",
    "ban.popup_cannot_ban_super": "❌ ¡No se puede banear al super admin!",
    "ban.popup_already_banned": "Ya baneado",
    "ban.popup_not_banned": "No baneado",
    "ban.popup_cancelled": "Cancelado",
    "ban.popup_success_ban": "✅ ¡Usuario baneado exitosamente!",
    "ban.popup_success_unban": "✅ ¡Usuario desbaneado exitosamente!",

    # ============================================
    # Manejador de Medios
    # ============================================
    "media.queue_full": "⚠️ Tu cola está llena (máx. {maxsize} archivos). Espera un momento antes de enviar más.",
    "media.quota_full": "❌ Tu cuota está llena.\nUsa /mylimit para ver detalles.",
    "media.file_too_large": "❌ Archivo demasiado grande ({size} bytes).\nMáximo: {max_mb} MB",
    "media.global_full": "❌ Lo sentimos, el almacenamiento global está lleno.\nIntenta de nuevo más tarde.",
}