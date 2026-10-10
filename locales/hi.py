"""
Hindi Translation Pack
Telegram Media Storage Bot v3.0.4
"""

TEXTS = {
    # ============================================
    # /start
    # ============================================
    "start.welcome": "👋 <b>स्वागत है, {name}!</b>",
    "start.bot_desc": "🤖 <b>Telegram Media Storage Bot v3.0.4</b>\nस्वचालित डीडुप्लीकेशन, प्रति-उपयोगकर्ता एन्क्रिप्शन और फ़ाइल हटाने की सुविधाओं वाला स्मार्ट मल्टी-यूज़र मीडिया स्टोरेज बॉट।",
    "start.features_title": "✨ <b>मुख्य विशेषताएं:</b>",
    "start.feature_save": "• फ़ोटो, वीडियो और दस्तावेज़ सहेजें",
    "start.feature_dedup": "• डुप्लीकेट का स्वतः पता लगाना और अस्वीकार (प्रति उपयोगकर्ता)",
    "start.feature_privacy": "• पृथक भंडारण — आपकी फ़ाइलें केवल आपको दिखाई देती हैं",
    "start.feature_autodel": "• {desc}",
    "start.feature_spoiler": "• <b>कैप्शन और स्पॉइलर अनदेखे</b> (केवल फ़ाइल सहेजी जाती है)",
    "start.feature_album": "• मल्टी-फ़ाइल एल्बम पूरी तरह समर्थित",
    "start.feature_forward": "• फ़ॉरवर्ड किया गया मीडिया भी सहेजा जाता है",
    "start.feature_stats": "• संपूर्ण और रीयल-टाइम व्यक्तिगत आंकड़े",
    "start.feature_delete": "• सुरक्षित पुष्टि के साथ फ़ाइलें हटाएं",
    "start.howto_title": "🚀 <b>उपयोग कैसे करें:</b>",
    "start.howto_desc": "मीडिया को बॉट को भेजें / फ़ॉरवर्ड करें — बस!",
    "start.commands_title": "📖 <b>कमांड्स:</b>",
    "start.cmd_get": "/get — इंटरएक्टिव फ़ाइल ब्राउज़र खोलें",
    "start.cmd_stats": "/stats — आंकड़े और अपटाइम",
    "start.cmd_limit": "/mylimit — शेष कोटा जांचें",
    "start.cmd_delete": "/delete — सहेजी गई फ़ाइलें हटाएं",
    "start.cmd_help": "/help — पूर्ण सहायता",
    "start.cmd_lang": "/language — भाषा बदलें (8 उपलब्ध)",
    "start.cmd_admin_msg": "@admin [संदेश] — एडमिन से संपर्क करें",
    "start.admin_title": "🔑 <b>एडमिन मोड सक्रिय</b>",
    "start.admin_cmd": "/admin — एडमिन नियंत्रण पैनल",
    "start.privacy_title": (
        "🔒 <b>गोपनीयता की गारंटी</b>\n"
        "• आपकी हर फ़ाइल <b>पृथक रूप में</b> संग्रहीत है और केवल आप ही उसे देख सकते हैं।\n"
        "• <b>एडमिन किसी भी उपयोगकर्ता की फ़ाइलें नहीं देख सकते</b> या खोल सकते।\n"
        "• कोई डेटा तीसरे पक्ष, यहाँ तक कि अन्य उपयोगकर्ताओं को भी साझा नहीं किया जाता।\n"
        "• हमारी प्रणाली सुरक्षित स्टोरेज का उपयोग करती है ताकि आपकी गोपनीयता हमेशा सुरक्षित रहे।"
    ),
    "start.autodel_desc_media": "मीडिया संदेश {delay} सेकंड बाद स्वतः हटा दिए जाते हैं",
    "start.autodel_desc_all": "संदेश {delay} सेकंड बाद स्वतः हटा दिए जाते हैं",

    # ============================================
    # /help
    # ============================================
    "help.title": "📖 <b>पूर्ण सहायता</b>",
    "help.subtitle": "Telegram Media Storage Bot v3.0.4",
    "help.section1_title": "📤 <b>1. मीडिया सहेजना</b>",
    "help.section1_desc": "बस मीडिया को बॉट को भेजें या फ़ॉरवर्ड करें — सब कुछ स्वचालित है।",
    "help.section1_support": "✅ समर्थित: फ़ोटो, वीडियो, दस्तावेज़",
    "help.section1_album": "✅ मल्टी-फ़ाइल एल्बम स्वचालित रूप से प्रोसेस होते हैं",
    "help.section1_forward": "✅ अन्य चैट/चैनल/ग्रुप से फ़ॉरवर्ड भी सहेजे जाते हैं",
    "help.section1_duplicate": "🚫 आपके खाते में डुप्लीकेट स्वतः अस्वीकार",
    "help.section1_spoiler": "🧹 कैप्शन और स्पॉइलर नहीं सहेजे जाते (केवल मूल फ़ाइल)",
    "help.section1_delete": "🗑️ मूल संदेश {delay} सेकंड बाद हटा दिया जाता है",
    "help.section2_title": "📥 <b>2. फ़ाइलें प्राप्त करना — /get</b>",
    "help.section2_intro": "<b>इंटरएक्टिव फ़ाइल ब्राउज़र</b> खोलने के लिए <code>/get</code> का उपयोग करें।",
    "help.section2_nav_title": "🎮 <b>फ़ाइल ब्राउज़र नेविगेशन:</b>",
    "help.section2_nav1": "• <b>फ़ाइल नंबर</b> पर क्लिक करें — वह एकल फ़ाइल डाउनलोड करें",
    "help.section2_nav2": "• <b>👁️ पेज देखें</b> पर क्लिक करें — पेज की सभी फ़ाइलें डाउनलोड करें",
    "help.section2_nav3": "• ⬅️ <b>पिछला</b> / <b>अगला</b> ➡️ — पेज बदलें",
    "help.section2_nav4": "• <b>📄 पेज नंबर</b> पर क्लिक करें — उस पेज पर जाएं",
    "help.section2_nav5": "• पूछे जाने पर पेज नंबर टाइप करें — त्वरित पहुँच",
    "help.section2_nav6": "• प्रत्येक पेज अधिकतम 10 फ़ाइलें दिखाता है",
    "help.section2_admin": "\n🔑 <b>एडमिन के लिए:</b>\n" +
                          "<code>/get user [ID]</code> — किसी अन्य उपयोगकर्ता की फ़ाइलें देखें\n" +
                          "<code>/get</code> (एडमिन) — सभी उपयोगकर्ताओं की सभी फ़ाइलें देखें",
    "help.section2_delete": "\n🗑️ डाउनलोड परिणाम {delay} सेकंड बाद स्वतः हटा दिए जाते हैं",
    "help.section3_title": "📊 <b>3. आंकड़े — /stats</b>",
    "help.section3_files": "• कुल फ़ाइलें और स्टोरेज आकार",
    "help.section3_breakdown": "• प्रकार के अनुसार विवरण (फ़ोटो/वीडियो/दस्तावेज़)",
    "help.section3_today": "• आज के अपलोड और डुप्लीकेट",
    "help.section3_uptime": "• बॉट का अपटाइम (दिन/घंटे/मिनट)",
    "help.section4_title": "📋 <b>4. कोटा — /mylimit</b>",
    "help.section4_default": "• डिफ़ॉल्ट: प्रति उपयोगकर्ता {limit:,} फ़ाइलें",
    "help.section4_admin": "• एडमिन प्रति-उपयोगकर्ता कोटा समायोजित कर सकता है",
    "help.section4_unlimited": "• 0 = असीमित",
    "help.section5_title": "🗑️ <b>5. फ़ाइलें हटाना — /delete</b>",
    "help.section5_cmd": "<code>/delete [नंबर]</code> — विशेष फ़ाइल हटाएं",
    "help.section5_all": "<code>/delete all</code> — अपनी सभी फ़ाइलें हटाएं",
    "help.section5_note": "⚠️ हमेशा हटाने से पहले पुष्टि मांगी जाती है!",
    "help.section6_title": "💬 <b>6. एडमिन से संपर्क</b>",
    "help.section6_cmd": "<code>@admin [अपना संदेश]</code> टाइप करें",
    "help.section6_example": "उदाहरण: <code>@admin वीडियो अपलोड में त्रुटि हो रही है</code>",
    "help.section6_reply": "एडमिन बॉट के माध्यम से उत्तर देगा।",
    "help.section7_title": "🛡️ <b>7. गोपनीयता और सुरक्षा</b>",
    "help.section7_private": (
        "• आपके द्वारा सहेजी गई हर फ़ाइल <b>केवल आपके लिए सुलभ</b> है।\n"
        "  कोई भी — प्रशासकों सहित — आपकी फ़ाइलें नहीं देख, खोल या डाउनलोड कर सकता।"
    ),
    "help.section7_noshare": (
        "• <b>शून्य डेटा साझाकरण।</b> आपकी फ़ाइलें कभी भी अन्य उपयोगकर्ताओं को नहीं दिखाई जाएंगी,\n"
        "  और आपके आंकड़े निजी रहते हैं।"
    ),
    "help.section7_clean": (
        "• बॉट को भेजे गए मूल संदेश <b>कुछ सेकंड में स्वतः हटा</b> दिए जाते हैं।\n"
        "  केवल सुरक्षित भंडारण में सहेजी गई फ़ाइलें ही रहती हैं।"
    ),
    "help.section7_dedup": (
        "• डुप्लीकेट पहचान <b>प्रति-उपयोगकर्ता</b> काम करती है। जो फ़ाइलें पहले से आपके खाते में हैं,\n"
        "  उन्हें दोबारा स्वीकार नहीं किया जाएगा, जिससे भंडारण कुशल बना रहता है।"
    ),
    "help.section7_encryption": (
        "• भंडारण <b>सख्त पृथक्करण</b> और सिस्टम-स्तरीय अभिगम सुरक्षा का उपयोग करता है।\n"
        "  आपका डेटा आपके स्वयं के सत्र के अलावा किसी अन्य प्रक्रिया द्वारा कभी नहीं पढ़ा जाता।"
    ),
    "help.section8_title": "🌐 <b>8. भाषा — /language</b>",
    "help.section8_desc": "बॉट की प्रदर्शन भाषा बदलें (8 भाषाएं उपलब्ध)।",
    "help.section8_list": "<code>/language</code> — भाषा चयन दिखाएं",
    "help.section8_set": "इच्छित भाषा का बटन टैप करें",
    "help.section8_langs": "🇮🇩 ID | 🇬🇧 EN | 🇷🇺 RU | 🇨🇳 ZH | 🇯🇵 JA | 🇪🇸 ES | 🇮🇳 HI | 🇧🇷 PT",
    "help.section9_title": "💡 <b>9. सुझाव</b>",
    "help.section9_tip1": "• चैनल/ग्रुप से मीडिया फ़ॉरवर्ड करके सहेजें",
    "help.section9_tip2": "• कभी भी फ़ाइलें प्राप्त करने के लिए /get का उपयोग करें",
    "help.section9_tip3": "• कैप्शन और स्पॉइलर स्टोर नहीं होते (केवल मूल फ़ाइल)",
    "help.section9_tip4": "• फ़ोटो/वीडियो एल्बम समूह के रूप में प्रोसेस किए जाते हैं (कुशल)",
    "help.admin_title": "🔑 <b>10. एडमिन कमांड</b>",
    "help.admin_list": "<code>/admin</code> — एडमिन पैनल",
    "help.admin_users": "<code>/admin users</code> — सभी उपयोगकर्ताओं की सूची",
    "help.admin_user": "<code>/admin user [id]</code> — उपयोगकर्ता विवरण",
    "help.admin_add": "<code>/admin add [id]</code> — एडमिन जोड़ें (केवल सुपर एडमिन)",
    "help.admin_remove": "<code>/admin remove [id]</code> — एडमिन हटाएं (केवल सुपर एडमिन)",
    "help.admin_setlimit": "<code>/admin setlimit [id] [n]</code> — उपयोगकर्ता कोटा सेट करें",
    "help.admin_stats": "<code>/admin stats</code> — वैश्विक आंकड़े",
    "help.admin_messages": "<code>/admin messages</code> — उपयोगकर्ताओं के संदेश",
    "help.admin_ban": "<code>/ban [id]</code> — उपयोगकर्ता पर प्रतिबंध लगाएं",
    "help.admin_unban": "<code>/unban [id]</code> — प्रतिबंध हटाएं",
    "help.admin_broadcast": "<code>/broadcast [संदेश]</code> — सभी उपयोगकर्ताओं को प्रसारित करें",
    "help.admin_reply": "<code>/reply [id] [पाठ]</code> — उपयोगकर्ता संदेश का उत्तर दें",
    "help.admin_delete": "<code>/delete user [id] [नंबर|all]</code> — उपयोगकर्ता की फ़ाइल(ें) हटाएं",
    "help.admin_get_user": "<code>/get user [id]</code> — विशेष उपयोगकर्ता की फ़ाइलें देखें",
    "help.footer": "🏷️ <b>v3.0.4</b> | मल्टी-यूज़र संस्करण | प्रति-उपयोगकर्ता पृथक्करण",
    "help.made_with": "Python-telegram-bot के साथ ❤️ से बनाया गया",

    "help.privacy_bottom": (
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔐 <b>आपकी सुरक्षा हमारी प्राथमिकता है।</b>\n"
        "कोई भी — विकास टीम सहित — आपकी फ़ाइलों की सामग्री नहीं देख सकता।\n"
        "हम कभी भी आपका डेटा तीसरे पक्ष को साझा नहीं करते।"
    ),

    # ============================================
    # /get
    # ============================================
    "get.banned": "❌ आप इस बॉट से प्रतिबंधित हैं।",
    "get.max_range": "⚠️ अधिकतम {max_range} फ़ाइलें प्रति पेज।",
    "get.no_files": "📭 कोई फ़ाइल नहीं मिली। प्रारंभ करने के लिए मीडिया भेजें।",
    "get.error": "❌ एक त्रुटि हुई। बाद में पुनः प्रयास करें।",
    "get.invalid_input": "❌ अमान्य उपयोगकर्ता आईडी या पेज नंबर।",
    "get.owner_label": "👤 स्वामी: {owner} (आईडी: {owner_id})",

    # ============================================
    # फ़ाइल ब्राउज़र नेविगेशन
    # ============================================
    "nav.view_page": "👁️ पेज {page} देखें",
    "nav.prev": "⬅️ पिछला",
    "nav.next": "अगला ➡️",
    "nav.back_all": "🔙 सभी फ़ाइलों पर वापस जाएं",
    "nav.my_files": "📂 आपकी फ़ाइलें",
    "nav.all_files": "📂 सभी फ़ाइलें (एडमिन दृश्य)",
    "nav.user_files": "📂 {name} की फ़ाइलें (आईडी: {uid})",
    "nav.page_of": "📄 {page}/{total}",
    "nav.jump_prompt": "📄 पेज पर जाएं? (1-{total})\nनीचे पेज नंबर टाइप करें 👇",
    "nav.jump_alert": "कृपया पेज नंबर टाइप करें (1-{total})",
    "nav.invalid_page": "❌ पेज 1-{total} के बीच होना चाहिए।",
    "nav.invalid_number": "❌ एक मान्य पेज नंबर दर्ज करें।",
    "nav.file_sent": "✅ {name} भेज दी गई!",
    "nav.send_failed": "⚠️ फ़ाइल भेजने में विफल। पुनः प्रयास करें।",
    "nav.no_file": "⚠️ फ़ाइल नहीं मिली।",
    "nav.no_files_page": "⚠️ इस पेज पर कोई फ़ाइल नहीं है।",
    "nav.files_sent": "✅ {count} फ़ाइलें भेजी गईं!",
    "nav.too_fast": "⚠️ बहुत तेज़! कृपया थोड़ी देर प्रतीक्षा करें...",
    "nav.session_expired": "⚠️ ब्राउज़र सत्र समाप्त। कृपया पुनः /get का उपयोग करें।",
    "nav.generic_error": "⚠️ एक त्रुटि हुई। कृपया पुनः प्रयास करें।",
    # फ़ाइल नेविगेशन (अतिरिक्त)
    "nav.range_indicator": "{start}-{end} / कुल {total} फ़ाइलें",
    "nav.navigation_hint": "📌 {num} / कुल {total} फ़ाइलें",
    "nav.navigation_hint_range": "📌 {start}-{end} / कुल {total} फ़ाइलें",
    "nav.invalid_file": "❌ फ़ाइल संख्या 1-{total} के बीच होनी चाहिए।",

    # ============================================
    # /stats
    # ============================================
    "stats.title": "📊 व्यक्तिगत आंकड़े",
    "stats.total_files": "📦 कुल फ़ाइलें: {count:,}",
    "stats.quota": " / {limit:,} (कोटा)",
    "stats.total_size": "💾 कुल आकार: {size}",
    "stats.by_type": "📂 प्रकार के अनुसार:",
    "stats.type_photo": "📸 {type}: {count:,} ({size})",
    "stats.type_video": "🎥 {type}: {count:,} ({size})",
    "stats.type_document": "📄 {type}: {count:,} ({size})",
    "stats.type_other": "📎 {type}: {count:,} ({size})",
    "stats.today_added": "📤 आज: +{count} फ़ाइलें",
    "stats.today_dup": "🔄 अस्वीकृत (डुप्लीकेट): {count}",
    "stats.uptime": "🕐 अपटाइम: {days}दिन {hours}घंटे {minutes}मिनट",
    "stats.privacy_note": "🔒 ये आंकड़े केवल आपको दिखाई देते हैं।",

    # ============================================
    # /mylimit
    # ============================================
    "limit.unlimited": "📊 कोटा: असीमित\n📁 सहेजी गई फ़ाइलें: {current:,}\n💾 स्टोरेज: {size}",
    "limit.limited": "📊 कोटा: {current:,}/{limit:,} फ़ाइलें\n📥 शेष: {remaining:,} फ़ाइलें\n💾 स्टोरेज: {size}",
    "limit.safe_note": "🛡️ कोटा पूरा होने पर भी आपकी फ़ाइलें सुरक्षित हैं। आप केवल नई फ़ाइलें नहीं जोड़ सकते।",

    # ============================================
    # /delete (v3.0.3)
    # ============================================
    "delete.help_title": "🗑️ <b>फ़ाइलें हटाएं</b>",
    "delete.help_desc": "आप सहेजी गई फ़ाइलें हटा सकते हैं। फ़ाइल नंबर देखने के लिए /get का उपयोग करें।",
    "delete.help_commands": "📋 <b>कमांड:</b>",
    "delete.help_single": "<code>/delete [नंबर]</code> — नंबर द्वारा फ़ाइल हटाएं (1 = सबसे नई)",
    "delete.help_all": "<code>/delete all</code> — अपनी सभी फ़ाइलें हटाएं",
    "delete.help_note": "⚠️ <b>चेतावनी:</b> हटाने को वापस नहीं लाया जा सकता! पुष्टि मांगी जाएगी।",
    "delete.help_total": "📁 आपकी कुल फ़ाइलें: <b>{count:,}</b>",
    "delete.help_size": "💾 कुल आकार: <b>{size}</b>",
    "delete.help_admin": "👤 उपयोगकर्ता {name} (आईडी: {uid})\n📁 फ़ाइलें: {count:,}\n💾 आकार: {size}\n\nउपयोग करें /delete user {uid} [नंबर|all]",
    "delete.banned": "❌ आप प्रतिबंधित हैं।",
    "delete.invalid_format": "❌ अमान्य प्रारूप। सहायता के लिए /delete का उपयोग करें।",
    "delete.not_found": "❌ फ़ाइल नंबर {num} नहीं मिली। सूची देखने के लिए /get का उपयोग करें।",
    "delete.no_files": "📭 हटाने के लिए कोई फ़ाइल नहीं।",
    "delete.confirm_single": (
        "⚠️ <b>फ़ाइल हटाने की पुष्टि करें</b>\n\n"
        "{emoji} <b>#{num}</b> — {name}\n"
        "📁 प्रकार: {type}\n"
        "💾 आकार: {size}\n\n"
        "क्या आप वाकई यह फ़ाइल हटाना चाहते हैं?"
    ),
    "delete.confirm_single_admin": (
        "⚠️ <b>फ़ाइल हटाने की पुष्टि (एडमिन)</b>\n\n"
        "👤 उपयोगकर्ता आईडी: {uid}\n"
        "{emoji} <b>#{num}</b> — {name}\n"
        "📁 प्रकार: {type}\n"
        "💾 आकार: {size}\n\n"
        "क्या आप वाकई यह फ़ाइल हटाना चाहते हैं?"
    ),
    "delete.confirm_all": (
        "⚠️ <b>सभी फ़ाइलें हटाने की पुष्टि</b>\n\n"
        "📁 कुल फ़ाइलें: <b>{count:,}</b>\n"
        "💾 कुल आकार: <b>{size}</b>\n\n"
        "क्या आप वाकई <b>सभी</b> फ़ाइलें हटाना चाहते हैं?\n"
        "यह क्रिया <b>वापस नहीं ली जा सकती!</b>"
    ),
    "delete.confirm_all_admin": (
        "⚠️ <b>सभी फ़ाइलें हटाने की पुष्टि (एडमिन)</b>\n\n"
        "👤 उपयोगकर्ता: {name} (आईडी: {uid})\n"
        "📁 कुल फ़ाइलें: <b>{count:,}</b>\n"
        "💾 कुल आकार: <b>{size}</b>\n\n"
        "क्या आप इस उपयोगकर्ता की <b>सभी</b> फ़ाइलें हटाना चाहते हैं?"
    ),
    "delete.btn_confirm": "✅ हाँ, हटाएं",
    "delete.btn_confirm_all": "✅ हाँ, सभी हटाएं",
    "delete.btn_cancel": "❌ रद्द करें",
    "delete.cancelled": "✅ हटाना रद्द कर दिया गया।",
    "delete.success_single": "✅ फ़ाइल <b>#{num}</b> ({name}) हटा दी गई।",
    "delete.success_single_admin": "✅ उपयोगकर्ता {uid} की फ़ाइल <b>#{num}</b> ({name}) हटा दी गई।",
    "delete.success_all": "✅ <b>{count:,}</b> फ़ाइलें हटा दी गईं।",
    "delete.success_all_admin": "✅ उपयोगकर्ता {uid} की <b>{count:,}</b> फ़ाइलें हटा दी गईं।",
    "delete.failed": "❌ फ़ाइल हटाने में विफल। पुनः प्रयास करें।",
    "delete.not_owner": "❌ आप इस फ़ाइल के स्वामी नहीं हैं।",
    "delete.not_admin": "❌ आपके पास एडमिन पहुंच नहीं है।",
    "delete.popup_session_expired": "⚠️ सत्र समाप्त हो गया। पुनः प्रयास करें।",

    # ============================================
    # /language
    # ============================================
    "language.select": "🌐 <b>भाषा चुनें:</b>\n\nकोड के साथ /language [कोड] टाइप करें\n\n{langs}",
    "language.current": "\n\n📌 वर्तमान: {current}",
    "language.changed": "✅ भाषा बदलकर {name} कर दी गई",
    "language.invalid": "❌ असमर्थित भाषा। उपयोग करें: {codes}",
    "language.unsupported": "❌ भाषा समर्थित नहीं है।",
    "language.lang_item": "{emoji} {name} — <code>/language {code}</code>\n",
    "language.select_title": "🌐 <b>भाषा चुनें:</b>",

    # ============================================
    # @admin
    # ============================================
    "admin_msg.format": "✍️ प्रारूप: @admin [संदेश]\nउदाहरण: @admin बॉट में त्रुटि हो रही है",
    "admin_msg.sent": "✅ संदेश एडमिन को भेज दिया गया। हम जल्द से जल्द जवाब देंगे।",
    "admin_msg.notify": "📩 उपयोगकर्ता का संदेश\n👤 {name} (आईडी: {uid})\n💬 {message}\n\nउत्तर: /reply {msg_id} [संदेश]",

    # ============================================
    # एडमिन पैनल
    # ============================================
    "admin.access_denied": "❌ पहुँच अस्वीकृत। केवल एडमिन।",
    "admin.panel_title": "🔑 एडमिन पैनल",
    "admin.panel_users": "👥 कुल उपयोगकर्ता: {count:,}",
    "admin.panel_files": "📁 कुल फ़ाइलें: {count:,}",
    "admin.panel_admins": "🛡️ रनटाइम एडमिन: {count}",
    "admin.panel_unread": "📩 नए संदेश: {count} ⚠️",
    "admin.panel_commands": (
        "📋 कमांड:\n"
        "/admin users — सभी उपयोगकर्ताओं की सूची\n"
        "/admin user [id] — उपयोगकर्ता विवरण\n"
        "/admin add [id] — एडमिन जोड़ें\n"
        "/admin remove [id] — एडमिन हटाएं\n"
        "/admin setlimit [id] [n] — सीमा सेट करें\n"
        "/admin stats — वैश्विक आंकड़े\n"
        "/admin messages — उपयोगकर्ताओं के संदेश\n"
        "/ban [id] — उपयोगकर्ता पर प्रतिबंध लगाएं\n"
        "/unban [id] — प्रतिबंध हटाएं\n"
        "/broadcast [संदेश] — सभी को प्रसारित करें\n"
        "/reply [id] [संदेश] — उपयोगकर्ता संदेश का उत्तर दें\n"
        "/delete user [id] [n|all] — उपयोगकर्ता की फ़ाइल(ें) हटाएं\n"
        "/get user [id] — विशेष उपयोगकर्ता की फ़ाइलें देखें"
    ),
    # ============================================
    # एडमिन पैनल - उपयोगकर्ता सूची नेविगेशन
    # ============================================
    "admin_users.invalid_page": "❌ अमान्य पेज।",
    "admin_users.access_denied": "❌ पहुँच अस्वीकृत।",
    "admin.users_title": "👥 पंजीकृत उपयोगकर्ता",
    "admin.users_item": "{i}. {name} (आईडी: {uid}) — {files:,} फ़ाइल(ें){banned}",
    "admin.users_more": "\n... और {count} अन्य।",
    "admin.users_empty": "अभी तक कोई पंजीकृत उपयोगकर्ता नहीं।",
    "admin.user_title": "👤 उपयोगकर्ता विवरण: {name}",
    "admin.user_id": "आईडी: {uid}",
    "admin.user_username": "उपयोगकर्ता नाम: @{username}",
    "admin.user_banned": "प्रतिबंध स्थिति: {status}",
    "admin.user_files": "फ़ाइलें: {files:,} / {limit}",
    "admin.user_storage": "स्टोरेज: {size}",
    "admin.user_by_type": "📂 प्रकार के अनुसार:",
    "admin.user_not_found": "❌ उपयोगकर्ता नहीं मिला।",
    "admin.add_super_only": "❌ केवल सुपर एडमिन ही एडमिन जोड़ सकता है।",
    "admin.add_super_cannot": "❌ सुपर एडमिन को संशोधित नहीं किया जा सकता।",
    "admin.add_success": "✅ उपयोगकर्ता {uid} को एडमिन पद पर पदोन्नत किया गया।",
    "admin.add_already": "⚠️ उपयोगकर्ता पहले से ही एडमिन है।",
    "admin.remove_super_only": "❌ केवल सुपर एडमिन ही एडमिन हटा सकता है।",
    "admin.remove_super_cannot": "❌ सुपर एडमिन को हटाया नहीं जा सकता।",
    "admin.remove_success": "✅ उपयोगकर्ता {uid} को एडमिन पद से हटा दिया गया।",
    "admin.remove_not": "⚠️ उपयोगकर्ता एडमिन नहीं है।",
    "admin.setlimit_success": "✅ उपयोगकर्ता {uid} के लिए फ़ाइल सीमा {limit:,} सेट कर दी गई।",
    "admin.global_title": "📊 वैश्विक आंकड़े",
    "admin.global_users": "👥 कुल उपयोगकर्ता: {count:,}",
    "admin.global_files": "📁 कुल फ़ाइलें: {count:,}",
    "admin.global_storage": "💾 कुल स्टोरेज: {size}",
    "admin.global_served": "📤 प्रदान की गई कुल फ़ाइलें: {count:,}",
    "admin.global_top": "🏆 शीर्ष 5 उपयोगकर्ता:",
    "admin.global_top_item": "  {i}. {name} — {files:,} फ़ाइल(ें)",
    "admin.broadcast_format": "📢 प्रारूप: /broadcast [संदेश]\nउदाहरण: /broadcast रात 10 बजे अनुरक्षण होगा",
    "admin.broadcast_sending": "📤 {total} उपयोगकर्ताओं को प्रसारण भेजा जा रहा है...",
    "admin.broadcast_progress": (
        "📤 प्रसारण भेज रहा है...\n"
        "▸ प्रगति: {sent}/{total}\n"
        "▸ सफल: {success}\n"
        "▸ विफल: {failed}"
    ),
    "admin.broadcast_done": "✅ प्रसारण पूरा हुआ\n📤 भेजा गया: {success}\n❌ विफल: {failed}\n👥 कुल: {total}",
    "admin.broadcast_msg": "📢 एडमिन घोषणा\n\n{message}",
    "admin.broadcast_skipped": "\n⚠️ {skipped} प्रतिबंधित/निष्क्रिय उपयोगकर्ताओं को छोड़ा गया",
    "admin.reply_format": "↩️ प्रारूप: /reply [संदेश_आईडी] [उत्तर]\nसंदेश सूची देखने के लिए /admin messages का उपयोग करें",
    "admin.reply_invalid_id": "❌ अमान्य संदेश आईडी।",
    "admin.reply_not_found": "❌ संदेश नहीं मिला।",
    "admin.reply_already": "⚠️ इस संदेश का उत्तर पहले ही दिया जा चुका है।",
    "admin.reply_failed": "❌ उत्तर भेजने में विफल: {error}",
    "admin.reply_sent": "✅ उपयोगकर्ता {uid} को उत्तर भेज दिया गया",
    "admin.reply_to_user": "🔰 एडमिन ने आपके संदेश का उत्तर दिया:\n\n💬 आपका संदेश: {original}\n\n↩️ एडमिन का उत्तर: {reply}",
    "admin.reply_failed_delivery": "❌ उत्तर भेजने में विफल: संदेश वितरित नहीं किया जा सका।",
    "admin.messages_title": "📩 उपयोगकर्ताओं के संदेश",
    "admin.messages_item": "#{id} | {name} (आईडी: {uid})\n💬 {text}\nउत्तर: /reply {id} [सामग्री]\n\n",
    "admin.messages_empty": "📭 कोई नया संदेश नहीं।",
    "admin.messages_max": "\n⚠️ 20 सबसे हालिया संदेश दिखाए जा रहे हैं।",
    "admin.ban_usage": "उपयोग: /ban [user_id]",
    "admin.ban_invalid": "❌ अमान्य उपयोगकर्ता आईडी।",
    "admin.ban_super": "❌ सुपर एडमिन पर प्रतिबंध नहीं लगाया जा सकता।",
    "admin.ban_success": "🚫 उपयोगकर्ता {uid} पर प्रतिबंध लगा दिया गया।",
    "admin.unban_usage": "उपयोग: /unban [user_id]",
    "admin.unban_success": "✅ उपयोगकर्ता {uid} से प्रतिबंध हटा लिया गया।",

    # ============================================
    # बैन/अनबैन पुष्टि (v3.0.4 - i18n)
    # ============================================
    "ban.confirm_title": "⚠️ <b>प्रतिबंध की पुष्टि करें</b>",
    "ban.confirm_body": "👤 नाम: <b>{name}</b>\n🆔 आईडी: <code>{uid}</code>\n📛 उपयोगकर्ता नाम: {username}\n📁 फ़ाइलें: {files:,}\n\nक्या आप वाकई इस उपयोगकर्ता पर <b>प्रतिबंध</b> लगाना चाहते हैं?\nवे बॉट का उपयोग नहीं कर पाएंगे।",
    "ban.already_banned": "⚠️ उपयोगकर्ता {uid} पहले से प्रतिबंधित है।",
    "ban.success": "🚫 <b>उपयोगकर्ता प्रतिबंधित</b>\n\n👤 {name}\n🆔 <code>{uid}</code>\n\n✅ यह उपयोगकर्ता अब बॉट का उपयोग नहीं कर सकता।\n🗑️ उनका कैश साफ़ कर दिया गया है।",
    "unban.confirm_title": "🔓 <b>प्रतिबंध हटाने की पुष्टि करें</b>",
    "unban.confirm_body": "👤 नाम: <b>{name}</b>\n🆔 आईडी: <code>{uid}</code>\n📛 उपयोगकर्ता नाम: {username}\n📁 फ़ाइलें: {files:,}\n\nक्या आप वाकई इस उपयोगकर्ता का <b>प्रतिबंध हटाना</b> चाहते हैं?\nवे पुनः बॉट का उपयोग कर पाएंगे।",
    "unban.not_banned": "⚠️ उपयोगकर्ता {uid} वर्तमान में प्रतिबंधित नहीं है।",
    "unban.success": "🔓 <b>प्रतिबंध हटा</b>\n\n👤 {name}\n🆔 <code>{uid}</code>\n\n✅ अब यह उपयोगकर्ता फिर से बॉट का उपयोग कर सकता है।",
    "ban.cancel": "✅ संक्रिया रद्द।",

    "ban.btn_confirm": "🚫 हाँ, प्रतिबंधित करें",
    "unban.btn_confirm": "🔓 हाँ, प्रतिबंध हटाएं",
    "ban.btn_cancel": "❌ रद्द करें",

    "ban.popup_session_expired": "⚠️ सत्र समाप्त। पुनः प्रयास करें।",
    "ban.popup_access_denied": "❌ पहुँच अस्वीकृत।",
    "ban.popup_not_initiator": "❌ केवल शुरू करने वाला एडमिन ही पुष्टि कर सकता है।",
    "ban.popup_cannot_ban_super": "❌ सुपर एडमिन पर प्रतिबंध नहीं लगाया जा सकता!",
    "ban.popup_already_banned": "पहले से प्रतिबंधित",
    "ban.popup_not_banned": "प्रतिबंधित नहीं",
    "ban.popup_cancelled": "रद्द किया गया",
    "ban.popup_success_ban": "✅ उपयोगकर्ता सफलतापूर्वक प्रतिबंधित!",
    "ban.popup_success_unban": "✅ प्रतिबंध सफलतापूर्वक हटाया गया!",

    # ============================================
    # मीडिया हैंडलर
    # ============================================
    "media.queue_full": "⚠️ आपकी क्यू भर गई है (अधिकतम {maxsize} फ़ाइलें)। कृपया थोड़ी देर प्रतीक्षा करें।",
    "media.quota_full": "❌ आपका कोटा पूर्ण है।\nविवरण के लिए /mylimit का उपयोग करें।",
    "media.file_too_large": "❌ फ़ाइल बहुत बड़ी है ({size} बाइट्स)।\nअधिकतम: {max_mb} MB",
    "media.global_full": "❌ क्षमा करें, वैश्विक स्टोरेज भर गया है।\nबाद में पुनः प्रयास करें।",
}