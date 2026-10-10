"""
Portuguese (Brazil) Translation Pack
Telegram Media Storage Bot v3.0.4
"""

TEXTS = {
    # ============================================
    # /start
    # ============================================
    "start.welcome": "👋 <b>Bem-vindo(a), {name}!</b>",
    "start.bot_desc": "🤖 <b>Telegram Media Storage Bot v3.0.4</b>\nBot multiusuário inteligente de armazenamento de mídia com eliminação automática de duplicatas, criptografia por usuário e exclusão de arquivos.",
    "start.features_title": "✨ <b>Funcionalidades em Destaque:</b>",
    "start.feature_save": "• Salve fotos, vídeos e documentos",
    "start.feature_dedup": "• Detecção e rejeição automática de duplicatas (por usuário)",
    "start.feature_privacy": "• Armazenamento isolado — seus arquivos são visíveis apenas para você",
    "start.feature_autodel": "• {desc}",
    "start.feature_spoiler": "• <b>Legendas e spoilers são ignorados</b> (apenas o arquivo é salvo)",
    "start.feature_album": "• Álbuns com múltiplos arquivos totalmente suportados",
    "start.feature_forward": "• Mídias encaminhadas também são salvas",
    "start.feature_stats": "• Estatísticas pessoais completas e em tempo real",
    "start.feature_delete": "• Exclua arquivos com confirmação segura",
    "start.howto_title": "🚀 <b>Como Usar:</b>",
    "start.howto_desc": "Envie / encaminhe qualquer mídia para o bot — pronto!",
    "start.commands_title": "📖 <b>Comandos:</b>",
    "start.cmd_get": "/get — Abrir navegador interativo de arquivos",
    "start.cmd_stats": "/stats — Estatísticas e uptime",
    "start.cmd_limit": "/mylimit — Ver cota restante",
    "start.cmd_delete": "/delete — Remover arquivos armazenados",
    "start.cmd_help": "/help — Guia de ajuda completo",
    "start.cmd_lang": "/language — Mudar idioma (8 disponíveis)",
    "start.cmd_admin_msg": "@admin [mensagem] — Contatar admin",
    "start.admin_title": "🔑 <b>Modo Admin Ativo</b>",
    "start.admin_cmd": "/admin — Painel de controle do admin",
    "start.privacy_title": (
        "🔒 <b>Privacidade Garantida</b>\n"
        "• Cada arquivo seu é armazenado de forma <b>isolada</b> e acessível apenas por você.\n"
        "• <b>Os admins não podem ver</b> ou abrir nenhum arquivo de usuário.\n"
        "• Nenhum dado é compartilhado com terceiros, incluindo outros usuários.\n"
        "• Nosso sistema utiliza armazenamento protegido para manter sua privacidade sempre intacta."
    ),
    "start.autodel_desc_media": "Mensagens de mídia são excluídas automaticamente após {delay} segundos",
    "start.autodel_desc_all": "Mensagens são excluídas automaticamente após {delay} segundos",

    # ============================================
    # /help
    # ============================================
    "help.title": "📖 <b>AJUDA COMPLETA</b>",
    "help.subtitle": "Telegram Media Storage Bot v3.0.4",
    "help.section1_title": "📤 <b>1. Salvando Mídia</b>",
    "help.section1_desc": "Simplesmente envie ou encaminhe mídia para o bot — tudo automático.",
    "help.section1_support": "✅ Suportado: Fotos, Vídeos, Documentos",
    "help.section1_album": "✅ Álbuns multiarquivo processados automaticamente",
    "help.section1_forward": "✅ Encaminhamentos de outros chats/canais/grupos são salvos",
    "help.section1_duplicate": "🚫 Duplicatas são automaticamente rejeitadas na sua conta",
    "help.section1_spoiler": "🧹 Legendas e spoilers não são salvos (apenas o arquivo original)",
    "help.section1_delete": "🗑️ Mensagem original excluída após {delay} segundos",
    "help.section2_title": "📥 <b>2. Obtendo Arquivos — /get</b>",
    "help.section2_intro": "Use <code>/get</code> para abrir o <b>navegador interativo de arquivos</b>.",
    "help.section2_nav_title": "🎮 <b>Navegação do Navegador de Arquivos:</b>",
    "help.section2_nav1": "• Clique em um <b>número de arquivo</b> — baixar diretamente 1 arquivo",
    "help.section2_nav2": "• Clique em <b>👁️ Ver Página</b> — baixar todos os arquivos da página",
    "help.section2_nav3": "• ⬅️ <b>Ant</b> / <b>Próx</b> ➡️ — mudar de página",
    "help.section2_nav4": "• Clique em <b>📄 número da página</b> — pular para essa página",
    "help.section2_nav5": "• Digite o número da página quando solicitado — acesso rápido",
    "help.section2_nav6": "• Cada página mostra até 10 arquivos",
    "help.section2_admin": "\n🔑 <b>Para Admins:</b>\n" +
                          "<code>/get user [ID]</code> — Ver arquivos de outro usuário\n" +
                          "<code>/get</code> (admin) — Ver TODOS os arquivos de todos os usuários",
    "help.section2_delete": "\n🗑️ Resultados baixados são excluídos automaticamente após {delay} segundos",
    "help.section3_title": "📊 <b>3. Estatísticas — /stats</b>",
    "help.section3_files": "• Total de arquivos e tamanho do armazenamento",
    "help.section3_breakdown": "• Detalhamento por tipo (foto/vídeo/documento)",
    "help.section3_today": "• Uploads e duplicatas de hoje",
    "help.section3_uptime": "• Uptime do bot (dias/horas/minutos)",
    "help.section4_title": "📋 <b>4. Cota — /mylimit</b>",
    "help.section4_default": "• Padrão: {limit:,} arquivos por usuário",
    "help.section4_admin": "• Admin pode ajustar a cota por usuário",
    "help.section4_unlimited": "• 0 = ilimitado",
    "help.section5_title": "🗑️ <b>5. Excluir Arquivos — /delete</b>",
    "help.section5_cmd": "<code>/delete [número]</code> — Excluir arquivo específico",
    "help.section5_all": "<code>/delete all</code> — Excluir todos os seus arquivos",
    "help.section5_note": "⚠️ Sempre será pedida confirmação antes da exclusão!",
    "help.section6_title": "💬 <b>6. Contatar o Admin</b>",
    "help.section6_cmd": "Digite <code>@admin [sua mensagem]</code>",
    "help.section6_example": "Exemplo: <code>@admin O bot não está enviando vídeos</code>",
    "help.section6_reply": "O admin responderá através do bot.",
    "help.section7_title": "🛡️ <b>7. Privacidade e Segurança</b>",
    "help.section7_private": (
        "• Cada arquivo que você armazena <b>é acessível apenas por você</b>.\n"
        "  Ninguém — nem mesmo os administradores — pode ver, abrir ou baixar seus arquivos."
    ),
    "help.section7_noshare": (
        "• <b>Compartilhamento zero de dados.</b> Seus arquivos nunca serão mostrados a outros usuários,\n"
        "  e suas estatísticas permanecem privadas."
    ),
    "help.section7_clean": (
        "• As mensagens originais enviadas ao bot são <b>excluídas automaticamente</b> após alguns segundos.\n"
        "  Apenas os arquivos armazenados em seu armazenamento seguro permanecem."
    ),
    "help.section7_dedup": (
        "• A detecção de duplicatas funciona <b>por usuário</b>. Arquivos já existentes na sua conta não serão\n"
        "  aceitos novamente, mantendo o armazenamento eficiente."
    ),
    "help.section7_encryption": (
        "• O armazenamento utiliza mecanismos de <b>isolamento rígido</b> e proteção de acesso em nível de sistema.\n"
        "  Seus dados nunca são lidos por outros processos que não a sua própria sessão."
    ),
    "help.section8_title": "🌐 <b>8. Idioma — /language</b>",
    "help.section8_desc": "Altere o idioma de exibição do bot (8 idiomas disponíveis).",
    "help.section8_list": "<code>/language</code> — Abrir seleção de idioma",
    "help.section8_set": "Toque no botão do idioma desejado",
    "help.section8_langs": "🇮🇩 ID | 🇬🇧 EN | 🇷🇺 RU | 🇨🇳 ZH | 🇯🇵 JA | 🇪🇸 ES | 🇮🇳 HI | 🇧🇷 PT",
    "help.section9_title": "💡 <b>9. Dicas</b>",
    "help.section9_tip1": "• Encaminhe mídia de canais/grupos para salvá-la",
    "help.section9_tip2": "• Use /get para recuperar arquivos a qualquer momento",
    "help.section9_tip3": "• Legendas e spoilers não são armazenados (apenas o arquivo bruto)",
    "help.section9_tip4": "• Álbuns de fotos/vídeos são processados como grupo (eficiente)",
    "help.admin_title": "🔑 <b>10. COMANDOS DE ADMIN</b>",
    "help.admin_list": "<code>/admin</code> — Painel de administração",
    "help.admin_users": "<code>/admin users</code> — Listar todos os usuários",
    "help.admin_user": "<code>/admin user [id]</code> — Detalhes do usuário",
    "help.admin_add": "<code>/admin add [id]</code> — Adicionar admin (apenas super admin)",
    "help.admin_remove": "<code>/admin remove [id]</code> — Remover admin (apenas super admin)",
    "help.admin_setlimit": "<code>/admin setlimit [id] [n]</code> — Definir cota do usuário",
    "help.admin_stats": "<code>/admin stats</code> — Estatísticas globais",
    "help.admin_messages": "<code>/admin messages</code> — Mensagens dos usuários",
    "help.admin_ban": "<code>/ban [id]</code> — Banir usuário",
    "help.admin_unban": "<code>/unban [id]</code> — Desbanir usuário",
    "help.admin_broadcast": "<code>/broadcast [mensagem]</code> — Transmitir para todos os usuários",
    "help.admin_reply": "<code>/reply [id] [texto]</code> — Responder a uma mensagem de usuário",
    "help.admin_delete": "<code>/delete user [id] [número|all]</code> — Excluir arquivo(s) de usuário",
    "help.admin_get_user": "<code>/get user [id]</code> — Ver arquivos de um usuário específico",
    "help.footer": "🏷️ <b>v3.0.4</b> | Edição Multiusuário | Isolamento por Usuário",
    "help.made_with": "Feito com ❤️ usando python-telegram-bot",

    "help.privacy_bottom": (
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔐 <b>Sua segurança é nossa prioridade.</b>\n"
        "Ninguém — nem mesmo a equipe de desenvolvimento — pode ver o conteúdo dos seus arquivos.\n"
        "Nós nunca compartilhamos seus dados com terceiros."
    ),

    # ============================================
    # /get
    # ============================================
    "get.banned": "❌ Você foi banido deste bot.",
    "get.max_range": "⚠️ Máximo de {max_range} arquivos por página.",
    "get.no_files": "📭 Nenhum arquivo encontrado. Envie mídia para começar.",
    "get.error": "❌ Ocorreu um erro. Tente novamente mais tarde.",
    "get.invalid_input": "❌ ID de usuário ou número de página inválido.",
    "get.owner_label": "👤 Proprietário: {owner} (ID: {owner_id})",

    # ============================================
    # Navegação do Navegador de Arquivos
    # ============================================
    "nav.view_page": "👁️ Ver Página {page}",
    "nav.prev": "⬅️ Ant",
    "nav.next": "Próx ➡️",
    "nav.back_all": "🔙 Voltar para Todos os Arquivos",
    "nav.my_files": "📂 Seus Arquivos",
    "nav.all_files": "📂 Todos os Arquivos (Visão Admin)",
    "nav.user_files": "📂 Arquivos de: {name} (ID: {uid})",
    "nav.page_of": "📄 {page}/{total}",
    "nav.jump_prompt": "📄 Ir para página? (1-{total})\nDigite o número da página abaixo 👇",
    "nav.jump_alert": "Por favor, digite um número de página (1-{total})",
    "nav.invalid_page": "❌ A página deve estar entre 1-{total}.",
    "nav.invalid_number": "❌ Insira um número de página válido.",
    "nav.file_sent": "✅ {name} enviado!",
    "nav.send_failed": "⚠️ Falha ao enviar arquivo. Tente novamente.",
    "nav.no_file": "⚠️ Arquivo não encontrado.",
    "nav.no_files_page": "⚠️ Nenhum arquivo nesta página.",
    "nav.files_sent": "✅ {count} arquivos enviados!",
    "nav.too_fast": "⚠️ Muito rápido! Aguarde um momento...",
    "nav.session_expired": "⚠️ Sessão do navegador expirada. Use /get novamente.",
    "nav.generic_error": "⚠️ Ocorreu um erro. Tente novamente.",
    # Navegação de arquivos (adicional)
    "nav.range_indicator": "{start}-{end} de {total} arquivos",
    "nav.navigation_hint": "📌 {num} de {total} arquivos",
    "nav.navigation_hint_range": "📌 {start}-{end} de {total} arquivos",
    "nav.invalid_file": "❌ O número do arquivo deve ser 1-{total}.",

    # ============================================
    # /stats
    # ============================================
    "stats.title": "📊 ESTATÍSTICAS PESSOAIS",
    "stats.total_files": "📦 Total de arquivos: {count:,}",
    "stats.quota": " / {limit:,} (cota)",
    "stats.total_size": "💾 Tamanho total: {size}",
    "stats.by_type": "📂 Por Tipo:",
    "stats.type_photo": "📸 {type}: {count:,} ({size})",
    "stats.type_video": "🎥 {type}: {count:,} ({size})",
    "stats.type_document": "📄 {type}: {count:,} ({size})",
    "stats.type_other": "📎 {type}: {count:,} ({size})",
    "stats.today_added": "📤 Hoje: +{count} arquivos",
    "stats.today_dup": "🔄 Rejeitados (duplicatas): {count}",
    "stats.uptime": "🕐 Uptime: {days}d {hours}h {minutes}m",
    "stats.privacy_note": "🔒 Essas estatísticas são visíveis apenas para você.",

    # ============================================
    # /mylimit
    # ============================================
    "limit.unlimited": "📊 Cota: Ilimitada\n📁 Arquivos armazenados: {current:,}\n💾 Armazenamento: {size}",
    "limit.limited": "📊 Cota: {current:,}/{limit:,} arquivos\n📥 Restantes: {remaining:,} arquivos\n💾 Armazenamento: {size}",
    "limit.safe_note": "🛡️ Seus arquivos permanecem seguros mesmo com a cota cheia. Você apenas não pode adicionar novos arquivos.",

    # ============================================
    # /delete (v3.0.3)
    # ============================================
    "delete.help_title": "🗑️ <b>EXCLUIR ARQUIVOS</b>",
    "delete.help_desc": "Você pode excluir arquivos armazenados. Use /get para ver os números dos arquivos.",
    "delete.help_commands": "📋 <b>Comandos:</b>",
    "delete.help_single": "<code>/delete [número]</code> — Excluir arquivo por número (1 = mais recente)",
    "delete.help_all": "<code>/delete all</code> — Excluir todos os seus arquivos",
    "delete.help_note": "⚠️ <b>Aviso:</b> Exclusão não pode ser desfeita! A confirmação será solicitada.",
    "delete.help_total": "📁 Total de seus arquivos: <b>{count:,}</b>",
    "delete.help_size": "💾 Tamanho total: <b>{size}</b>",
    "delete.help_admin": "👤 Usuário {name} (ID: {uid})\n📁 Arquivos: {count:,}\n💾 Tamanho: {size}\n\nUse /delete user {uid} [número|all]",
    "delete.banned": "❌ Você foi banido deste bot.",
    "delete.invalid_format": "❌ Formato inválido. Use /delete para orientação.",
    "delete.not_found": "❌ Arquivo número {num} não encontrado. Use /get para listar os arquivos.",
    "delete.no_files": "📭 Não há arquivos para excluir.",
    "delete.confirm_single": (
        "⚠️ <b>Confirmar Exclusão de Arquivo</b>\n\n"
        "{emoji} <b>#{num}</b> — {name}\n"
        "📁 Tipo: {type}\n"
        "💾 Tamanho: {size}\n\n"
        "Você tem certeza que deseja excluir este arquivo?"
    ),
    "delete.confirm_single_admin": (
        "⚠️ <b>Confirmar Exclusão de Arquivo (Admin)</b>\n\n"
        "👤 ID do Usuário: {uid}\n"
        "{emoji} <b>#{num}</b> — {name}\n"
        "📁 Tipo: {type}\n"
        "💾 Tamanho: {size}\n\n"
        "Você tem certeza que deseja excluir este arquivo?"
    ),
    "delete.confirm_all": (
        "⚠️ <b>Confirmar Exclusão de Todos os Arquivos</b>\n\n"
        "📁 Total de arquivos: <b>{count:,}</b>\n"
        "💾 Tamanho total: <b>{size}</b>\n\n"
        "Você tem certeza que deseja excluir <b>TODOS</b> os arquivos?\n"
        "Esta ação <b>NÃO PODE SER DESFEITA!</b>"
    ),
    "delete.confirm_all_admin": (
        "⚠️ <b>Confirmar Exclusão de Todos os Arquivos (Admin)</b>\n\n"
        "👤 Usuário: {name} (ID: {uid})\n"
        "📁 Total de arquivos: <b>{count:,}</b>\n"
        "💾 Tamanho total: <b>{size}</b>\n\n"
        "Você tem certeza que deseja excluir <b>TODOS</b> os arquivos deste usuário?"
    ),
    "delete.btn_confirm": "✅ Sim, Excluir",
    "delete.btn_confirm_all": "✅ Sim, Excluir Todos",
    "delete.btn_cancel": "❌ Cancelar",
    "delete.cancelled": "✅ Exclusão cancelada.",
    "delete.success_single": "✅ Arquivo <b>#{num}</b> ({name}) excluído com sucesso.",
    "delete.success_single_admin": "✅ Arquivo <b>#{num}</b> ({name}) do usuário {uid} excluído.",
    "delete.success_all": "✅ <b>{count:,}</b> arquivos excluídos com sucesso.",
    "delete.success_all_admin": "✅ <b>{count:,}</b> arquivos do usuário {uid} excluídos.",
    "delete.failed": "❌ Falha ao excluir arquivo. Tente novamente.",
    "delete.not_owner": "❌ Você não é o proprietário deste arquivo.",
    "delete.not_admin": "❌ Você não possui acesso de administrador.",
    "delete.popup_session_expired": "⚠️ Sessão expirada. Tente novamente.",

    # ============================================
    # /language
    # ============================================
    "language.select": "🌐 <b>Selecionar Idioma:</b>\n\nDigite /language [código]\n\n{langs}",
    "language.current": "\n\n📌 Atual: {current}",
    "language.changed": "✅ Idioma alterado para {name}",
    "language.invalid": "❌ Idioma não suportado. Use: {codes}",
    "language.unsupported": "❌ Idioma não suportado.",
    "language.lang_item": "{emoji} {name} — <code>/language {code}</code>\n",
    "language.select_title": "🌐 <b>Selecionar Idioma:</b>",

    # ============================================
    # @admin
    # ============================================
    "admin_msg.format": "✍️ Formato: @admin [mensagem]\nExemplo: @admin O bot está com erro",
    "admin_msg.sent": "✅ Mensagem enviada ao admin. Responderemos o mais rápido possível.",
    "admin_msg.notify": "📩 Mensagem de usuário\n👤 {name} (ID: {uid})\n💬 {message}\n\nResponder: /reply {msg_id} [mensagem]",

    # ============================================
    # Painel Admin
    # ============================================
    "admin.access_denied": "❌ Acesso negado. Apenas admin.",
    "admin.panel_title": "🔑 PAINEL ADMIN",
    "admin.panel_users": "👥 Total de usuários: {count:,}",
    "admin.panel_files": "📁 Total de arquivos: {count:,}",
    "admin.panel_admins": "🛡️ Admins em tempo real: {count}",
    "admin.panel_unread": "📩 Novas mensagens: {count} ⚠️",
    "admin.panel_commands": (
        "📋 Comandos:\n"
        "/admin users — Listar todos os usuários\n"
        "/admin user [id] — Detalhes do usuário\n"
        "/admin add [id] — Adicionar admin\n"
        "/admin remove [id] — Remover admin\n"
        "/admin setlimit [id] [n] — Definir limite\n"
        "/admin stats — Estatísticas globais\n"
        "/admin messages — Mensagens de usuários\n"
        "/ban [id] — Banir usuário\n"
        "/unban [id] — Desbanir usuário\n"
        "/broadcast [mensagem] — Enviar para todos\n"
        "/reply [id] [mensagem] — Responder a um usuário\n"
        "/delete user [id] [n|all] — Excluir arquivo(s) do usuário\n"
        "/get user [id] — Ver arquivos de um usuário específico"
    ),
    # ============================================
    # Painel Admin - navegação da lista de usuários
    # ============================================
    "admin_users.invalid_page": "❌ Página inválida.",
    "admin_users.access_denied": "❌ Acesso negado.",
    "admin.users_title": "👥 USUÁRIOS REGISTRADOS",
    "admin.users_item": "{i}. {name} (ID: {uid}) — {files:,} arquivo(s){banned}",
    "admin.users_more": "\n... e mais {count}.",
    "admin.users_empty": "Nenhum usuário registrado ainda.",
    "admin.user_title": "👤 DETALHES DO USUÁRIO: {name}",
    "admin.user_id": "ID: {uid}",
    "admin.user_username": "Usuário: @{username}",
    "admin.user_banned": "Status de ban: {status}",
    "admin.user_files": "Arquivos: {files:,} / {limit}",
    "admin.user_storage": "Armazenamento: {size}",
    "admin.user_by_type": "📂 Por Tipo:",
    "admin.user_not_found": "❌ Usuário não encontrado.",
    "admin.add_super_only": "❌ Apenas o super admin pode adicionar administradores.",
    "admin.add_super_cannot": "❌ Super admin não pode ser modificado.",
    "admin.add_success": "✅ Usuário {uid} foi promovido a administrador.",
    "admin.add_already": "⚠️ O usuário já é administrador.",
    "admin.remove_super_only": "❌ Apenas o super admin pode remover administradores.",
    "admin.remove_super_cannot": "❌ Super admin não pode ser removido.",
    "admin.remove_success": "✅ Usuário {uid} foi rebaixado de administrador.",
    "admin.remove_not": "⚠️ O usuário não é administrador.",
    "admin.setlimit_success": "✅ Limite de arquivos para o usuário {uid} definido como {limit:,}.",
    "admin.global_title": "📊 ESTATÍSTICAS GLOBAIS",
    "admin.global_users": "👥 Total de usuários: {count:,}",
    "admin.global_files": "📁 Total de arquivos: {count:,}",
    "admin.global_storage": "💾 Armazenamento total: {size}",
    "admin.global_served": "📤 Total de arquivos servidos: {count:,}",
    "admin.global_top": "🏆 Top 5 Usuários:",
    "admin.global_top_item": "  {i}. {name} — {files:,} arquivo(s)",
    "admin.broadcast_format": "📢 Formato: /broadcast [mensagem]\nExemplo: /broadcast Manutenção programada às 22h",
    "admin.broadcast_sending": "📤 Enviando transmissão para {total} usuários...",
    "admin.broadcast_progress": (
        "📤 Enviando transmissão...\n"
        "▸ Progresso: {sent}/{total}\n"
        "▸ Sucesso: {success}\n"
        "▸ Falhas: {failed}"
    ),
    "admin.broadcast_done": "✅ Transmissão concluída\n📤 Entregues: {success}\n❌ Falhas: {failed}\n👥 Total: {total}",
    "admin.broadcast_msg": "📢 Comunicado do Admin\n\n{message}",
    "admin.broadcast_skipped": "\n⚠️ Ignorados {skipped} usuários banidos/inativos",
    "admin.reply_format": "↩️ Formato: /reply [id_mensagem] [resposta]\nUse /admin messages para ver a lista de mensagens",
    "admin.reply_invalid_id": "❌ ID de mensagem inválido.",
    "admin.reply_not_found": "❌ Mensagem não encontrada.",
    "admin.reply_already": "⚠️ Esta mensagem já foi respondida.",
    "admin.reply_failed": "❌ Falha ao enviar resposta: {error}",
    "admin.reply_sent": "✅ Resposta enviada ao usuário {uid}",
    "admin.reply_to_user": "🔰 Admin respondeu à sua mensagem:\n\n💬 Sua mensagem: {original}\n\n↩️ Resposta do admin: {reply}",
    "admin.reply_failed_delivery": "❌ Falha ao enviar resposta: a mensagem não pôde ser entregue.",
    "admin.messages_title": "📩 MENSAGENS DOS USUÁRIOS",
    "admin.messages_item": "#{id} | {name} (ID: {uid})\n💬 {text}\nResponder: /reply {id} [conteúdo]\n\n",
    "admin.messages_empty": "📭 Nenhuma mensagem nova.",
    "admin.messages_max": "\n⚠️ Mostrando as 20 mensagens mais recentes.",
    "admin.ban_usage": "Uso: /ban [user_id]",
    "admin.ban_invalid": "❌ ID de usuário inválido.",
    "admin.ban_super": "❌ Não é possível banir o super admin.",
    "admin.ban_success": "🚫 Usuário {uid} foi banido.",
    "admin.unban_usage": "Uso: /unban [user_id]",
    "admin.unban_success": "✅ Usuário {uid} foi desbanido.",

    # ============================================
    # Confirmação de Ban/Unban (v3.0.4 - i18n)
    # ============================================
    "ban.confirm_title": "⚠️ <b>Confirmar Banir Usuário</b>",
    "ban.confirm_body": "👤 Nome: <b>{name}</b>\n🆔 ID: <code>{uid}</code>\n📛 Usuário: {username}\n📁 Arquivos: {files:,}\n\nVocê tem certeza que deseja <b>BANIR</b> este usuário?\nEle não poderá mais usar o bot.",
    "ban.already_banned": "⚠️ O usuário {uid} já está banido.",
    "ban.success": "🚫 <b>Usuário Banido</b>\n\n👤 {name}\n🆔 <code>{uid}</code>\n\n✅ Este usuário não pode mais usar o bot.\n🗑️ O cache dele foi limpo.",
    "unban.confirm_title": "🔓 <b>Confirmar Desbanir Usuário</b>",
    "unban.confirm_body": "👤 Nome: <b>{name}</b>\n🆔 ID: <code>{uid}</code>\n📛 Usuário: {username}\n📁 Arquivos: {files:,}\n\nVocê tem certeza que deseja <b>DESBANIR</b> este usuário?\nEle poderá usar o bot novamente.",
    "unban.not_banned": "⚠️ O usuário {uid} não está banido no momento.",
    "unban.success": "🔓 <b>Usuário Desbanido</b>\n\n👤 {name}\n🆔 <code>{uid}</code>\n\n✅ Este usuário agora pode usar o bot novamente.",
    "ban.cancel": "✅ Operação cancelada.",

    "ban.btn_confirm": "🚫 Sim, Banir",
    "unban.btn_confirm": "🔓 Sim, Desbanir",
    "ban.btn_cancel": "❌ Cancelar",

    "ban.popup_session_expired": "⚠️ Sessão expirada. Tente novamente.",
    "ban.popup_access_denied": "❌ Acesso negado.",
    "ban.popup_not_initiator": "❌ Apenas o admin que iniciou pode confirmar.",
    "ban.popup_cannot_ban_super": "❌ Não é possível banir o super admin!",
    "ban.popup_already_banned": "Já banido",
    "ban.popup_not_banned": "Não banido",
    "ban.popup_cancelled": "Cancelado",
    "ban.popup_success_ban": "✅ Usuário banido com sucesso!",
    "ban.popup_success_unban": "✅ Usuário desbanido com sucesso!",

    # ============================================
    # Gerenciador de Mídia
    # ============================================
    "media.queue_full": "⚠️ Sua fila está cheia (máx. {maxsize} arquivos). Aguarde um momento antes de enviar mais.",
    "media.quota_full": "❌ Sua cota está cheia.\nUse /mylimit para ver detalhes.",
    "media.file_too_large": "❌ Arquivo muito grande ({size} bytes).\nMáximo: {max_mb} MB",
    "media.global_full": "❌ Desculpe, o armazenamento global está cheio.\nTente novamente mais tarde.",
}