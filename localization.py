# --- START OF FILE bot/localization.py ---

# Default language for fallback if a specific translation is missing for a message
DEFAULT_LOC_LANG = "en"

# { 
#   "message_key": {
#     "lang_code1": "Translation for lang1",
#     "lang_code2": "Translation for lang2",
#     ...
#   },
#   ...
# }

TEMPLATES = {
    "welcome_body": {
        "en": "Hello {first_name}!\nI'm your AI Study Helper. I will now try to speak with you in {greeting_lang_display_name}.",
        "es": "¡Hola {first_name}!\nSoy tu Ayudante de Estudio AI. Ahora intentaré hablar contigo en {greeting_lang_display_name}.",
        "fr": "Bonjour {first_name} !\nJe suis votre Assistant d'Étude IA. Je vais maintenant essayer de parler avec vous en {greeting_lang_display_name}.",
        "kk": "Сәлем, {first_name}!\nМен сіздің AI Оқу Жәрдемшіңізбін. Енді мен сізбен {greeting_lang_display_name} тілінде сөйлесуге тырысамын.",
        "de": "Hallo {first_name}!\nIch bin dein KI-Lernassistent. Ich werde jetzt versuchen, mit dir auf {greeting_lang_display_name} zu sprechen.",
        "ru": "Привет, {first_name}!\nЯ — твой AI-помощник в учебе. Теперь я постараюсь говорить с тобой на {greeting_lang_display_name}.",
        "zh-CN": "你好，{first_name}！\n我是你的AI学习助手。现在我将尝试使用{greeting_lang_display_name}与你交流。",
        "ja": "こんにちは、{first_name}さん！\n私はあなたのAI学習アシスタントです。これから{greeting_lang_display_name}で話すようにします。",
        "ko": "안녕하세요, {first_name}님!\n저는 당신의 AI 학습 도우미입니다. 이제부터 {greeting_lang_display_name}로 말해보겠습니다.",
        "pt-BR": "Olá {first_name}!\nSou seu Assistente de Estudos com IA. Agora vou tentar falar com você em {greeting_lang_display_name}.",
        "it": "Ciao {first_name}!\nSono il tuo Assistente di Studio AI. Ora cercherò di parlarti in {greeting_lang_display_name}.",
        "ar": "مرحبًا {first_name}!\nأنا مساعدك الدراسي الذكي. سأحاول الآن التحدث معك بـ{greeting_lang_display_name}.",
        "hi": "नमस्ते {first_name}!\nमैं आपका एआई अध्ययन सहायक हूँ। अब मैं आपसे {greeting_lang_display_name} में बात करने की कोशिश करूँगा।",
        "tr": "Merhaba {first_name}!\nBen senin AI Eğitim Yardımcınım. Artık seninle {greeting_lang_display_name} dilinde konuşmaya çalışacağım.",
        "nl": "Hoi {first_name}!\nIk ben je AI Studiehulp. Ik zal nu proberen met je te praten in {greeting_lang_display_name}.",
        "pl": "Cześć {first_name}!\nJestem twoim AI Asystentem Nauki. Teraz spróbuję mówić do ciebie po {greeting_lang_display_name}.",
        "sv": "Hej {first_name}!\nJag är din AI-studiehjälp. Jag kommer nu att försöka tala med dig på {greeting_lang_display_name}.",
        "fi": "Hei {first_name}!\nOlen tekoälyopiskeluavustajasi. Yritän nyt puhua kanssasi {greeting_lang_display_name}-kielellä.",
        "no": "Hei {first_name}!\nJeg er din AI-studiehjelper. Nå vil jeg prøve å snakke med deg på {greeting_lang_display_name}.",
        "da": "Hej {first_name}!\nJeg er din AI-studiehjælper. Jeg vil nu forsøge at tale med dig på {greeting_lang_display_name}.",
        "cs": "Ahoj {first_name}!\nJsem tvůj AI studijní pomocník. Teď se pokusím s tebou mluvit v {greeting_lang_display_name}.",
        "hu": "Szia {first_name}!\nÉn vagyok az AI tanulási segéded. Mostantól megpróbálok {greeting_lang_display_name} nyelven beszélni veled.",
        "ro": "Bună {first_name}!\nSunt Asistentul tău AI pentru studiu. Acum voi încerca să vorbesc cu tine în {greeting_lang_display_name}.",
        "el": "Γεια σου {first_name}!\nΕίμαι ο Βοηθός Μελέτης AI σου. Τώρα θα προσπαθήσω να σου μιλήσω στα {greeting_lang_display_name}.",
        "he": "שלום {first_name}!\nאני העוזר החכם שלך ללמידה. עכשיו אנסה לדבר איתך ב־{greeting_lang_display_name}.",
        "th": "สวัสดี {first_name}!\nฉันคือผู้ช่วยเรียนรู้ AI ของคุณ ตอนนี้ฉันจะพยายามพูดกับคุณเป็นภาษา {greeting_lang_display_name}",
        "vi": "Xin chào {first_name}!\nTôi là Trợ lý học tập AI của bạn. Giờ tôi sẽ cố gắng nói chuyện với bạn bằng {greeting_lang_display_name}.",
        "id": "Halo {first_name}!\nSaya Asisten Belajar AI Anda. Sekarang saya akan mencoba berbicara dengan Anda dalam {greeting_lang_display_name}.",
        "ms": "Hai {first_name}!\nSaya Pembantu Pembelajaran AI anda. Sekarang saya akan cuba bercakap dengan anda dalam {greeting_lang_display_name}.",
        "uk": "Привіт, {first_name}!\nЯ твій AI-помічник у навчанні. Тепер я намагатимусь говорити з тобою {greeting_lang_display_name}.",
        "uz": "Salom, {first_name}!\nMen sizning sun’iy intellekt asosidagi o‘quv yordamchingizman. Endi men {greeting_lang_display_name} tilida gapirishga harakat qilaman.",
        "zh-TW": "你好，{first_name}！\n我是你的AI學習助手。現在我將嘗試用{greeting_lang_display_name}與你對話。",
        "pt-PT": "Olá {first_name}!\nSou o seu Assistente de Estudos AI. Agora tentarei falar consigo em {greeting_lang_display_name}."
    },
    "language_change_instruction": {
        "en": "You can change my response language using the /language command.",
        "es": "Puedes cambiar el idioma de mis respuestas usando el comando /language.",
        "fr": "Vous pouvez changer la langue de mes réponses en utilisant la commande /language.",
        "kk": "Менің жауап беру тілімді /language пәрмені арқылы өзгерте аласыз.",
        "de": "Du kannst meine Antwortsprache mit dem Befehl /language ändern.",
        "ru": "Вы можете изменить язык моих ответов с помощью команды /language.",
        "zh-CN": "你可以使用 /language 命令更改我的回复语言。",
        "ja": "返信言語は /language コマンドで変更できます。",
        "ko": "/language 명령어를 사용하여 내 응답 언어를 변경할 수 있어요.",
        "pt-BR": "Você pode alterar meu idioma de resposta usando o comando /language.",
        "it": "Puoi cambiare la lingua delle mie risposte usando il comando /language.",
        "ar": "يمكنك تغيير لغة ردودي باستخدام الأمر /language.",
        "hi": "आप /language कमांड का उपयोग करके मेरी उत्तर भाषा बदल सकते हैं।",
        "tr": "/language komutunu kullanarak yanıt dilimi değiştirebilirsin.",
        "nl": "Je kunt mijn antwoordtaal wijzigen met het /language-commando.",
        "pl": "Możesz zmienić język moich odpowiedzi za pomocą komendy /language.",
        "sv": "Du kan ändra mitt svarspråk med kommandot /language.",
        "fi": "Voit vaihtaa vastauskieleni komennolla /language.",
        "no": "Du kan endre svaret mitt ved å bruke kommandoen /language.",
        "da": "Du kan ændre mit sprog for svar med kommandoen /language.",
        "cs": "Můžeš změnit jazyk mých odpovědí pomocí příkazu /language.",
        "hu": "A /language paranccsal megváltoztathatod a válasz nyelvét.",
        "ro": "Poți schimba limba răspunsurilor mele folosind comanda /language.",
        "el": "Μπορείς να αλλάξεις τη γλώσσα των απαντήσεών μου με την εντολή /language.",
        "he": "באפשרותך לשנות את שפת התשובות שלי באמצעות הפקודה /language.",
        "th": "คุณสามารถเปลี่ยนภาษาที่ฉันใช้ตอบได้โดยใช้คำสั่ง /language",
        "vi": "Bạn có thể thay đổi ngôn ngữ phản hồi của tôi bằng lệnh /language.",
        "id": "Kamu bisa mengganti bahasa jawabanku dengan perintah /language.",
        "ms": "Anda boleh menukar bahasa jawapan saya menggunakan arahan /language.",
        "uk": "Ви можете змінити мову моїх відповідей за допомогою команди /language.",
        "uz": "Mening javob tilimni /language buyrug‘i orqali o‘zgartirishingiz mumkin.",
        "zh-TW": "你可以使用 /language 指令更改我的回應語言。",
        "pt-PT": "Pode mudar o idioma das minhas respostas com o comando /language."
    },
    "reset_history_prompt": {
        "en": "Do you also want to reset our conversation history? This cannot be undone.",
        "es": "¿También quieres restablecer nuestro historial de conversación? Esto no puede deshacerse.",
        "fr": "Voulez-vous également réinitialiser notre historique de conversation ? Ceci ne peut pas être annulé.",
        "kk": "Сұхбат тарихымызды да тазартқыңыз келе ме? Бұл әрекетті кейін қайтару мүмкін емес.",
        "de": "Möchtest du auch unseren Gesprächsverlauf zurücksetzen? Dies kann nicht rückgängig gemacht werden.",
        "ru": "Вы также хотите сбросить нашу историю переписки? Это действие нельзя отменить.",
        "zh-CN": "你也想重置我们的聊天记录吗？此操作无法撤销。",
        "ja": "会話履歴もリセットしますか？この操作は元に戻せません。",
        "ko": "대화 기록도 초기화하시겠습니까? 이 작업은 되돌릴 수 없습니다.",
        "pt-BR": "Você também deseja limpar nosso histórico de conversa? Isso não pode ser desfeito.",
        "it": "Vuoi anche reimpostare la nostra cronologia delle conversazioni? Questa azione è irreversibile.",
        "ar": "هل تريد أيضًا إعادة تعيين سجل المحادثة الخاص بنا؟ لا يمكن التراجع عن هذا.",
        "hi": "क्या आप हमारी बातचीत का इतिहास भी रीसेट करना चाहते हैं? यह पूर्ववत नहीं किया जा सकता।",
        "tr": "Konuşma geçmişimizi de sıfırlamak ister misin? Bu işlem geri alınamaz.",
        "nl": "Wil je ook onze gespreksgeschiedenis wissen? Dit kan niet ongedaan worden gemaakt.",
        "pl": "Czy chcesz również zresetować naszą historię rozmów? Tego nie można cofnąć.",
        "sv": "Vill du också återställa vår konversationshistorik? Detta kan inte ångras.",
        "fi": "Haluatko myös tyhjentää keskusteluhistoriamme? Tätä ei voi perua.",
        "no": "Vil du også tilbakestille samtalehistorikken vår? Dette kan ikke angres.",
        "da": "Vil du også nulstille vores samtalehistorik? Dette kan ikke fortrydes.",
        "cs": "Chceš také vymazat naši historii konverzace? To nelze vrátit zpět.",
        "hu": "Szeretnéd törölni a beszélgetési előzményeket is? Ez nem visszavonható.",
        "ro": "Dorești să resetezi și istoricul conversațiilor noastre? Această acțiune nu poate fi anulată.",
        "el": "Θέλεις επίσης να διαγράψουμε το ιστορικό συνομιλίας μας; Αυτό δεν μπορεί να αναιρεθεί.",
        "he": "האם ברצונך לאפס גם את היסטוריית השיחה שלנו? לא ניתן לבטל פעולה זו.",
        "th": "คุณต้องการรีเซ็ตประวัติการสนทนาของเราด้วยหรือไม่? ไม่สามารถย้อนกลับได้",
        "vi": "Bạn cũng muốn đặt lại lịch sử trò chuyện của chúng ta không? Hành động này không thể hoàn tác.",
        "id": "Apakah kamu juga ingin mereset riwayat percakapan kita? Ini tidak dapat dibatalkan.",
        "ms": "Adakah anda juga mahu menetapkan semula sejarah perbualan kita? Ini tidak boleh dibatalkan.",
        "uk": "Ви також хочете скинути історію нашого спілкування? Це не можна скасувати.",
        "uz": "Suhbat tariximizni ham tozalamoqchimisiz? Bu amalni bekor qilib bo‘lmaydi.",
        "zh-TW": "你也想重設我們的對話歷史嗎？此操作無法還原。",
        "pt-PT": "Também quer limpar o nosso histórico de conversas? Isto não pode ser desfeito."
    },
    "yes_button_text": {
        "en": "Yes, clear history",
        "es": "Sí, borrar historial",
        "fr": "Oui, effacer l'historique",
        "kk": "Иә, тарихты тазарту",
        "de": "Ja, Verlauf löschen",
        "ru": "Да, очистить историю",
        "zh-CN": "是的，清除记录",
        "ja": "はい、履歴を消去",
        "ko": "예, 기록 삭제",
        "pt-BR": "Sim, limpar histórico",
        "it": "Sì, cancella la cronologia",
        "ar": "نعم، مسح السجل",
        "hi": "हां, इतिहास मिटाएं",
        "tr": "Evet, geçmişi sil",
        "nl": "Ja, geschiedenis wissen",
        "pl": "Tak, wyczyść historię",
        "sv": "Ja, rensa historik",
        "fi": "Kyllä, tyhjennä historia",
        "no": "Ja, slett historikk",
        "da": "Ja, ryd historik",
        "cs": "Ano, vymazat historii",
        "hu": "Igen, töröld az előzményeket",
        "ro": "Da, șterge istoricul",
        "el": "Ναι, διαγραφή ιστορικού",
        "he": "כן, מחק היסטוריה",
        "th": "ใช่ ล้างประวัติ",
        "vi": "Có, xóa lịch sử",
        "id": "Ya, hapus riwayat",
        "ms": "Ya, padam sejarah",
        "uk": "Так, очистити історію",
        "uz": "Ha, tarixni tozalash",
        "zh-TW": "是的，清除歷史記錄",
        "pt-PT": "Sim, limpar histórico"
    },
    "no_button_text": {
        "en": "No, cancel",
        "es": "No, cancelar",
        "fr": "Non, annuler",
        "kk": "Жоқ, болдырмау",
        "de": "Nein, abbrechen",
        "ru": "Нет, отмена",
        "zh-CN": "不，取消",
        "ja": "いいえ、キャンセル",
        "ko": "아니요, 취소",
        "pt-BR": "Não, cancelar",
        "it": "No, annulla",
        "ar": "لا، إلغاء",
        "hi": "नहीं, रद्द करें",
        "tr": "Hayır, iptal et",
        "nl": "Nee, annuleren",
        "pl": "Nie, anuluj",
        "sv": "Nej, avbryt",
        "fi": "Ei, peruuta",
        "no": "Nei, avbryt",
        "da": "Nej, annuller",
        "cs": "Ne, zrušit",
        "hu": "Nem, mégsem",
        "ro": "Nu, anulează",
        "el": "Όχι, ακύρωση",
        "he": "לא, בטל",
        "th": "ไม่ ยกเลิก",
        "vi": "Không, hủy",
        "id": "Tidak, batalkan",
        "ms": "Tidak, batal",
        "uk": "Ні, скасувати",
        "uz": "Yo‘q, bekor qilish",
        "zh-TW": "不，取消",
        "pt-PT": "Não, cancelar"
    },
    "history_cleared_confirmation": {
        "en": "Okay, our conversation history has been cleared! I will continue speaking in {response_lang_display_name}.\nHow can I help you study today?",
        "es": "¡De acuerdo, nuestro historial de conversación ha sido borrado! Continuaré hablando en {response_lang_display_name}.\n¿Cómo puedo ayudarte a estudiar hoy?",
        "fr": "D'accord, notre historique de conversation a été effacé ! Je continuerai à parler en {response_lang_display_name}.\nComment puis-je vous aider à étudier aujourd'hui ?",
        "kk": "Жарайды, сұхбат тарихымыз тазартылды! Мен {response_lang_display_name} тілінде сөйлесуді жалғастырамын.\nБүгін оқуыңа қалай көмектесе аламын?",
        "de": "Okay, unser Gesprächsverlauf wurde gelöscht! Ich werde weiterhin auf {response_lang_display_name} sprechen.\nWie kann ich dir heute beim Lernen helfen?",
        "ru": "Хорошо, история нашей беседы очищена! Я продолжу говорить на {response_lang_display_name}.\nКак я могу помочь тебе сегодня в учебе?",
        "zh-CN": "好的，我们的聊天记录已被清除！我将继续用{response_lang_display_name}与你交流。\n我今天怎么能帮你学习？",
        "ja": "了解しました。会話履歴はクリアされました！今後も{response_lang_display_name}で話し続けます。\n今日はどうやって勉強を手伝いましょうか？",
        "ko": "좋아요, 대화 기록이 삭제되었습니다! 앞으로도 {response_lang_display_name}로 대화를 계속하겠습니다.\n오늘 무엇을 도와드릴까요?",
        "pt-BR": "Tudo certo, nosso histórico de conversa foi limpo! Continuarei falando em {response_lang_display_name}.\nComo posso te ajudar a estudar hoje?",
        "it": "Ok, la nostra cronologia di conversazione è stata cancellata! Continuerò a parlare in {response_lang_display_name}.\nCome posso aiutarti a studiare oggi?",
        "ar": "حسنًا، تم مسح سجل المحادثة! سأواصل الحديث بـ{response_lang_display_name}.\nكيف يمكنني مساعدتك في الدراسة اليوم؟",
        "hi": "ठीक है, हमारी बातचीत का इतिहास साफ़ कर दिया गया है! मैं {response_lang_display_name} में बात करना जारी रखूंगा।\nमैं आज आपकी पढ़ाई में कैसे मदद कर सकता हूँ?",
        "tr": "Tamam, konuşma geçmişimiz temizlendi! {response_lang_display_name} dilinde konuşmaya devam edeceğim.\nBugün sana nasıl yardımcı olabilirim?",
        "nl": "Oké, onze gespreksgeschiedenis is gewist! Ik blijf verder praten in {response_lang_display_name}.\nHoe kan ik je vandaag helpen studeren?",
        "pl": "W porządku, nasza historia rozmów została wyczyszczona! Będę kontynuować rozmowę w języku {response_lang_display_name}.\nJak mogę ci dziś pomóc w nauce?",
        "sv": "Okej, vår konversationshistorik har rensats! Jag fortsätter att prata på {response_lang_display_name}.\nHur kan jag hjälpa dig att studera idag?",
        "fi": "Selvä, keskusteluhistoriamme on tyhjennetty! Jatkan puhumista kielellä {response_lang_display_name}.\nMiten voin auttaa sinua opiskelemaan tänään?",
        "no": "OK, samtalehistorikken vår er slettet! Jeg fortsetter å snakke på {response_lang_display_name}.\nHvordan kan jeg hjelpe deg med å studere i dag?",
        "da": "Okay, vores samtalehistorik er blevet slettet! Jeg fortsætter med at tale {response_lang_display_name}.\nHvordan kan jeg hjælpe dig med studierne i dag?",
        "cs": "Dobře, naše historie konverzací byla vymazána! Budu nadále mluvit {response_lang_display_name}.\nJak ti mohu dnes pomoci s učením?",
        "hu": "Rendben, töröltem a beszélgetési előzményeket! Folytatom a beszélgetést {response_lang_display_name} nyelven.\nHogyan segíthetek ma a tanulásban?",
        "ro": "Bine, istoricul conversațiilor a fost șters! Voi continua să vorbesc în {response_lang_display_name}.\nCu ce te pot ajuta să studiezi azi?",
        "el": "Εντάξει, το ιστορικό της συνομιλίας μας διαγράφηκε! Θα συνεχίσω να μιλάω στα {response_lang_display_name}.\nΠώς μπορώ να σε βοηθήσω σήμερα στο διάβασμα;",
        "he": "אוקיי, היסטוריית השיחה שלנו נוקתה! אמשיך לדבר ב־{response_lang_display_name}.\nאיך אני יכול לעזור לך בלימודים היום?",
        "th": "ตกลง ประวัติการสนทนาของเราถูกล้างแล้ว! ฉันจะพูดกับคุณต่อเป็นภาษา {response_lang_display_name}\nวันนี้ฉันสามารถช่วยคุณเรียนรู้อะไรได้บ้าง?",
        "vi": "Được rồi, lịch sử trò chuyện đã được xóa! Tôi sẽ tiếp tục nói chuyện bằng {response_lang_display_name}.\nHôm nay tôi có thể giúp bạn học gì?",
        "id": "Baik, riwayat percakapan kita telah dihapus! Saya akan terus berbicara dalam bahasa {response_lang_display_name}.\nBagaimana saya bisa membantu kamu belajar hari ini?",
        "ms": "Baik, sejarah perbualan kita telah dibersihkan! Saya akan terus bercakap dalam bahasa {response_lang_display_name}.\nBagaimana saya boleh bantu anda belajar hari ini?",
        "uk": "Гаразд, нашу історію розмов очищено! Я продовжу говорити {response_lang_display_name}.\nЧим я можу допомогти тобі з навчанням сьогодні?",
        "uz": "Yaxshi, suhbat tariximiz tozalandi! Endi {response_lang_display_name} tilida gaplashishni davom ettiraman.\nBugun o‘qishda sizga qanday yordam bera olaman?",
        "zh-TW": "好的，我們的對話紀錄已清除！我將繼續使用{response_lang_display_name}與你對話。\n今天我能如何幫助你學習？",
        "pt-PT": "Está bem, o nosso histórico de conversas foi limpo! Continuarei a falar em {response_lang_display_name}.\nComo posso ajudá-lo a estudar hoje?"
    },
    "reset_cancelled_confirmation": {
        "en": "Okay, reset cancelled. Our previous conversation remains, and I'll continue speaking in {response_lang_display_name}.",
        "es": "De acuerdo, reinicio cancelado. Nuestra conversación anterior permanece, y continuaré hablando en {response_lang_display_name}.",
        "fr": "D'accord, réinitialisation annulée. Notre conversation précédente demeure, et je continuerai à parler en {response_lang_display_name}.",
        "kk": "Жарайды, қалпына келтіру болдырылмады. Алдыңғы сұхбатымыз сақталады, мен {response_lang_display_name} тілінде сөйлесуді жалғастырамын.",
        "de": "Okay, Zurücksetzen abgebrochen. Unser vorheriges Gespräch bleibt bestehen, ich spreche weiterhin auf {response_lang_display_name}.",
        "ru": "Хорошо, сброс отменён. Наш предыдущий разговор сохранён, я продолжу говорить на {response_lang_display_name}.",
        "zh-CN": "好的，已取消重置。我们之前的对话依然保留，我将继续使用{response_lang_display_name}进行交流。",
        "ja": "了解しました。リセットはキャンセルされました。以前の会話は保持され、今後も{response_lang_display_name}で話します。",
        "ko": "좋아요, 초기화가 취소되었습니다. 이전 대화는 그대로 유지되며, {response_lang_display_name}로 계속 대화하겠습니다.",
        "pt-BR": "Tudo certo, redefinição cancelada. Nossa conversa anterior permanece e continuarei falando em {response_lang_display_name}.",
        "it": "Ok, ripristino annullato. La nostra precedente conversazione resta e continuerò a parlare in {response_lang_display_name}.",
        "ar": "حسنًا، تم إلغاء إعادة التعيين. ستظل محادثتنا السابقة كما هي، وسأستمر في التحدث بـ{response_lang_display_name}.",
        "hi": "ठीक है, रीसेट रद्द किया गया। हमारी पिछली बातचीत बनी रहेगी और मैं {response_lang_display_name} में बोलता रहूंगा।",
        "tr": "Tamam, sıfırlama iptal edildi. Önceki konuşmamız duruyor ve {response_lang_display_name} dilinde konuşmaya devam edeceğim.",
        "nl": "Oké, reset geannuleerd. Ons vorige gesprek blijft behouden en ik zal doorgaan in {response_lang_display_name}.",
        "pl": "OK, reset został anulowany. Nasza wcześniejsza rozmowa pozostaje, a ja będę kontynuować w języku {response_lang_display_name}.",
        "sv": "Okej, återställning avbröts. Vår tidigare konversation kvarstår och jag fortsätter att prata på {response_lang_display_name}.",
        "fi": "Selvä, palautus peruttu. Edellinen keskustelumme säilyy ja jatkan puhumista kielellä {response_lang_display_name}.",
        "no": "OK, tilbakestilling avbrutt. Forrige samtale beholdes og jeg fortsetter å snakke {response_lang_display_name}.",
        "da": "Okay, nulstilling annulleret. Vores tidligere samtale bevares, og jeg fortsætter med at tale {response_lang_display_name}.",
        "cs": "Dobře, reset byl zrušen. Naše předchozí konverzace zůstává a budu pokračovat v jazyce {response_lang_display_name}.",
        "hu": "Rendben, a visszaállítás megszakítva. Előző beszélgetésünk megmarad, és folytatom a beszélgetést {response_lang_display_name} nyelven.",
        "ro": "Bine, resetarea a fost anulată. Conversația anterioară rămâne, voi continua în limba {response_lang_display_name}.",
        "el": "Εντάξει, η επαναφορά ακυρώθηκε. Η προηγούμενη συνομιλία μας παραμένει και θα συνεχίσω να μιλάω στα {response_lang_display_name}.",
        "he": "אוקיי, האיפוס בוטל. השיחה הקודמת שלנו נותרה, ואמשיך לדבר ב־{response_lang_display_name}.",
        "th": "ตกลง การรีเซ็ตถูกยกเลิกแล้ว บทสนทนาก่อนหน้ายังคงอยู่ ฉันจะพูดต่อเป็น {response_lang_display_name}",
        "vi": "Được rồi, việc đặt lại đã bị hủy. Cuộc trò chuyện trước đó vẫn giữ nguyên, tôi sẽ tiếp tục sử dụng {response_lang_display_name}.",
        "id": "Oke, pengaturan ulang dibatalkan. Percakapan sebelumnya tetap ada dan saya akan terus berbicara dalam {response_lang_display_name}.",
        "ms": "Baik, tetapan semula dibatalkan. Perbualan kita sebelum ini kekal dan saya akan terus bercakap dalam {response_lang_display_name}.",
        "uk": "Гаразд, скидання скасовано. Наша попередня розмова збережена, я продовжую говорити на {response_lang_display_name}.",
        "uz": "Xo‘p, qayta sozlash bekor qilindi. Oldingi suhbatimiz saqlanadi, {response_lang_display_name} tilida davom etaman.",
        "zh-TW": "好的，已取消重設。之前的對話仍然保留，我會繼續使用{response_lang_display_name}與你交談。",
        "pt-PT": "Está bem, redefinição cancelada. A nossa conversa anterior mantém-se e continuarei a falar em {response_lang_display_name}."
    },
    "language_set_confirmation": {
        "en": "Language set to: {lang_name}.",
        "es": "Idioma establecido a: {lang_name}.",
        "fr": "Langue définie sur : {lang_name}.",
        "kk": "Тіл {lang_name} тіліне орнатылды.",
        "de": "Sprache eingestellt auf: {lang_name}.",
        "ru": "Язык установлен: {lang_name}.",
        "zh-CN": "语言已设置为：{lang_name}。",
        "ja": "言語を {lang_name} に設定しました。",
        "ko": "언어가 {lang_name}(으)로 설정되었습니다.",
        "pt-BR": "Idioma definido como: {lang_name}.",
        "it": "Lingua impostata su: {lang_name}.",
        "ar": "تم تعيين اللغة إلى: {lang_name}.",
        "hi": "भाषा सेट की गई: {lang_name}।",
        "tr": "Dil ayarlandı: {lang_name}.",
        "nl": "Taal ingesteld op: {lang_name}.",
        "pl": "Ustawiono język: {lang_name}.",
        "sv": "Språk inställt på: {lang_name}.",
        "fi": "Kieli asetettu: {lang_name}.",
        "no": "Språket er satt til: {lang_name}.",
        "da": "Sprog indstillet til: {lang_name}.",
        "cs": "Jazyk nastaven na: {lang_name}.",
        "hu": "Nyelv beállítva: {lang_name}.",
        "ro": "Limba setată: {lang_name}.",
        "el": "Η γλώσσα ορίστηκε σε: {lang_name}.",
        "he": "השפה הוגדרה ל־{lang_name}.",
        "th": "ตั้งค่าภาษาเป็น: {lang_name}",
        "vi": "Ngôn ngữ đã đặt: {lang_name}.",
        "id": "Bahasa diatur ke: {lang_name}.",
        "ms": "Bahasa ditetapkan kepada: {lang_name}.",
        "uk": "Мову встановлено: {lang_name}.",
        "uz": "Til sozlandi: {lang_name}.",
        "zh-TW": "語言已設為：{lang_name}。",
        "pt-PT": "Idioma definido como: {lang_name}."
    },
    "help_text_body": { # Renamed from help_message to match the key used in your help_command
        "en": (
            "I'm your _StudyHelper\\_Bot_! Send me any message related to your studies.\n"
            "I try to remember our recent conversation and respond in your preferred language (set with `/language`).\n\n"
            # "{help_message_title}\n" # Placeholder if you use the title above
            "*Available commands:*\n"
            "`/start` - Ask to clear our chat history and see a welcome message.\n"
            "`/help` - Show this help message.\n"
            "`/language` - Choose your preferred language for my responses."
        ),
        "es": (
            "¡Soy tu _StudyHelper\\_Bot_! Envíame cualquier mensaje relacionado con tus estudios.\n"
            "Intento recordar nuestra conversación reciente y responder en tu idioma preferido (configurado con `/language`).\n\n"
            "*Comandos disponibles:*\n"
            "`/start` - Pide borrar nuestro historial de chat y ver un mensaje de bienvenida.\n"
            "`/help` - Muestra este mensaje de ayuda.\n"
            "`/language` - Elige tu idioma preferido para mis respuestas."
        ),
        "fr": (
            "Je suis votre _StudyHelper\\_Bot_ ! Envoyez-moi tout message concernant vos études.\n"
            "J'essaie de me souvenir de notre conversation récente et de répondre dans votre langue préférée (définie avec `/language`).\n\n"
            "*Commandes disponibles :*\n"
            "`/start` - Demandez à effacer notre historique de discussion et voir un message de bienvenue.\n"
            "`/help` - Affiche ce message d'aide.\n"
            "`/language` - Choisissez votre langue préférée pour mes réponses."
        ),
        "de": (
            "Ich bin dein _StudyHelper\\_Bot_! Schick mir jede Nachricht, die mit deinem Studium zu tun hat.\n"
            "Ich versuche, mich an unser letztes Gespräch zu erinnern und in deiner bevorzugten Sprache zu antworten (mit `/language` eingestellt).\n\n"
            "*Verfügbare Befehle:*\n"
            "`/start` - Fordere das Löschen unseres Chatverlaufs und eine Begrüßungsnachricht an.\n"
            "`/help` - Zeige diese Hilfenachricht.\n"
            "`/language` - Wähle deine bevorzugte Sprache für meine Antworten."
        ),
        "ru": (
            "Я ваш _StudyHelper\\_Bot_! Отправляйте мне любые сообщения, связанные с учебой.\n"
            "Я стараюсь помнить наш недавний разговор и отвечать на вашем предпочтительном языке (устанавливается командой `/language`).\n\n"
            "*Доступные команды:*\n"
            "`/start` - Запрос на очистку истории чата и приветственное сообщение.\n"
            "`/help` - Показать это сообщение помощи.\n"
            "`/language` - Выберите предпочитаемый язык для моих ответов."
        ),
        "zh-CN": (
            "我是你的 _StudyHelper\\_Bot_！发送任何与你学习相关的信息给我。\n"
            "我会尝试记住我们最近的对话，并用你偏好的语言回复（通过 `/language` 设置）。\n\n"
            "*可用命令：*\n"
            "`/start` - 请求清除聊天记录并显示欢迎信息。\n"
            "`/help` - 显示此帮助信息。\n"
            "`/language` - 选择我回复时使用的语言。"
        ),
        "kk": (
            "Мен сіздің _StudyHelper\\_Bot_ болып табыламын! Оқуыңызға қатысты кез келген хабарламаны жіберіңіз.\n"
            "Мен соңғы сұхбатымызды есте сақтауға және сіздің таңдаған тіліңізде жауап беруге тырысамын (`/language` арқылы орнатылады).\n\n"
            "*Қолжетімді пәрмендер:*\n"
            "`/start` - Сұхбат тарихын тазартуды сұрау және сәлемдесу хабарламасын көру.\n"
            "`/help` - Осы көмек хабарламасын көрсету.\n"
            "`/language` - Менің жауаптарым үшін қалаған тіліңізді таңдаңыз."
        ),
        "ja": (
            "私はあなたの_StudyHelper\\_Bot_です！勉強に関するメッセージを送ってください。\n"
            "最近の会話を覚えており、あなたの希望する言語（`/language`で設定）で返信します。\n\n"
            "*利用可能なコマンド:*\n"
            "`/start` - チャット履歴をクリアしてウェルカムメッセージを表示します。\n"
            "`/help` - このヘルプメッセージを表示します。\n"
            "`/language` - 返信に使う言語を選択します。"
        ),
        "ko": (
            "저는 당신의 _StudyHelper\\_Bot_입니다! 공부와 관련된 메시지를 보내주세요.\n"
            "최근 대화를 기억하며, 선호하는 언어(`/language`로 설정)로 답변합니다.\n\n"
            "*사용 가능한 명령어:*\n"
            "`/start` - 대화 기록을 삭제하고 환영 메시지를 봅니다.\n"
            "`/help` - 이 도움말 메시지를 표시합니다.\n"
            "`/language` - 답변에 사용할 언어를 선택하세요."
        ),
        "pt-BR": (
            "Eu sou seu _StudyHelper\\_Bot_! Envie qualquer mensagem relacionada aos seus estudos.\n"
            "Eu tento lembrar nossa conversa recente e responder no seu idioma preferido (configurado com `/language`).\n\n"
            "*Comandos disponíveis:*\n"
            "`/start` - Peça para limpar o histórico do chat e ver uma mensagem de boas-vindas.\n"
            "`/help` - Mostrar esta mensagem de ajuda.\n"
            "`/language` - Escolha seu idioma preferido para minhas respostas."
        ),
        "it": (
            "Sono il tuo _StudyHelper\\_Bot_! Inviami qualsiasi messaggio relativo ai tuoi studi.\n"
            "Cerco di ricordare la nostra conversazione recente e rispondere nella lingua preferita (impostata con `/language`).\n\n"
            "*Comandi disponibili:*\n"
            "`/start` - Richiedi di cancellare la cronologia chat e visualizzare un messaggio di benvenuto.\n"
            "`/help` - Mostra questo messaggio di aiuto.\n"
            "`/language` - Scegli la lingua preferita per le mie risposte."
        ),
        "ar": (
            # For Arabic, which is Right-to-Left, Markdown behavior with mixed LTR/RTL can be tricky.
            # The _StudyHelper\_Bot_ part is LTR.
            # It's usually best to ensure LTR segments are clearly delineated if issues arise.
            # Using backticks for the bot name might be safer if _..._ causes issues with RTL flow.
            # For now, applying the standard fix:
            "أنا بوت _StudyHelper\\_Bot_ الخاص بك! أرسل لي أي رسالة تتعلق بدراستك.\n"
            "أحاول تذكر محادثتنا الأخيرة والرد بلغتك المفضلة (تُحدد باستخدام `/language`).\n\n"
            "*الأوامر المتاحة:*\n"
            "`/start` - اطلب مسح سجل الدردشة ورؤية رسالة ترحيب.\n"
            "`/help` - عرض رسالة المساعدة هذه.\n"
            "`/language` - اختر لغتك المفضلة لردودي."
        ),
        "hi": (
            "मैं आपका _StudyHelper\\_Bot_ हूँ! मुझे अपनी पढ़ाई से संबंधित कोई भी संदेश भेजें।\n"
            "मैं हमारी हाल की बातचीत याद रखने की कोशिश करता हूँ और आपकी पसंदीदा भाषा में जवाब देता हूँ (`/language` से सेट)।\n\n"
            "*उपलब्ध कमांड:*\n"
            "`/start` - चैट इतिहास साफ़ करने और स्वागत संदेश देखने के लिए कहें।\n"
            "`/help` - यह सहायता संदेश दिखाएँ।\n"
            "`/language` - मेरी प्रतिक्रियाओं के लिए अपनी पसंदीदा भाषा चुनें।"
        ),
        "tr": (
            "Ben senin _StudyHelper\\_Bot_'unum! Bana çalışmalarınla ilgili herhangi bir mesaj gönder.\n"
            "Son sohbetimizi hatırlamaya çalışır ve tercih ettiğin dilde cevap veririm (`/language` ile ayarlanır).\n\n"
            "*Mevcut komutlar:*\n"
            "`/start` - Sohbet geçmişimizi temizlemeyi ve bir karşılama mesajı görmeyi iste.\n"
            "`/help` - Bu yardım mesajını göster.\n"
            "`/language` - Yanıtlarım için tercih ettiğin dili seç."
        ),
        "nl": (
            "Ik ben je _StudyHelper\\_Bot_! Stuur me een bericht over je studie.\n"
            "Ik probeer ons recente gesprek te onthouden en te antwoorden in je voorkeurstaal (ingesteld met `/language`).\n\n"
            "*Beschikbare commando's:*\n"
            "`/start` - Vraag om onze chatgeschiedenis te wissen en een welkomstbericht te zien.\n"
            "`/help` - Toon dit helpbericht.\n"
            "`/language` - Kies je voorkeurs taal voor mijn antwoorden."
        ),
        "pl": (
            "Jestem twoim _StudyHelper\\_Bot_! Wyślij mi dowolną wiadomość związaną z nauką.\n"
            "Staram się pamiętać naszą ostatnią rozmowę i odpowiadać w twoim preferowanym języku (ustawiane przez `/language`).\n\n"
            "*Dostępne polecenia:*\n"
            "`/start` - Poproś o wyczyszczenie historii czatu i wyświetlenie powitalnej wiadomości.\n"
            "`/help` - Pokaż tę wiadomość pomocy.\n"
            "`/language` - Wybierz preferowany język moich odpowiedzi."
        ),
        "sv": (
            "Jag är din _StudyHelper\\_Bot_! Skicka mig ett meddelande om dina studier.\n"
            "Jag försöker komma ihåg vår senaste konversation och svara på ditt föredragna språk (inställt med `/language`).\n\n"
            "*Tillgängliga kommandon:*\n"
            "`/start` - Be om att rensa vår chatt-historik och visa ett välkomstmeddelande.\n"
            "`/help` - Visa detta hjälpmeddelande.\n"
            "`/language` - Välj ditt föredragna språk för mina svar."
        ),
        "fi": (
            "Olen _StudyHelper\\_Bot_! Lähetä minulle mitä tahansa opintoihisi liittyvää viestiä.\n"
            "Yritän muistaa viimeisimmän keskustelumme ja vastata valitsemallasi kielellä (`/language`).\n\n"
            "*Saatavilla olevat komennot:*\n"
            "`/start` - Pyydä tyhjentämään keskusteluhistoria ja näkemään tervetuloviesti.\n"
            "`/help` - Näytä tämä ohjeviesti.\n"
            "`/language` - Valitse vastausteni kieli."
        ),
        "no": (
            "Jeg er din _StudyHelper\\_Bot_! Send meg en melding relatert til studiene dine.\n"
            "Jeg prøver å huske vår siste samtale og svare på ditt foretrukne språk (innstilt med `/language`).\n\n"
            "*Tilgjengelige kommandoer:*\n"
            "`/start` - Be om å tømme chatthistorikken og se en velkomstmelding.\n"
            "`/help` - Vis denne hjelpeteksten.\n"
            "`/language` - Velg ditt foretrukne språk for mine svar."
        ),
        "da": (
            "Jeg er din _StudyHelper\\_Bot_! Send mig en besked relateret til dine studier.\n"
            "Jeg prøver at huske vores seneste samtale og svare på dit foretrukne sprog (indstillet med `/language`).\n\n"
            "*Tilgængelige kommandoer:*\n"
            "`/start` - Bed om at rydde chat historikken og se en velkomstbesked.\n"
            "`/help` - Vis denne hjælpetekst.\n"
            "`/language` - Vælg dit foretrukne sprog for mine svar."
        ),
        "cs": (
            "Jsem váš _StudyHelper\\_Bot_! Pošlete mi jakoukoli zprávu týkající se vašich studií.\n"
            "Snažím se pamatovat na naši nedávnou konverzaci a odpovídat ve vámi preferovaném jazyce (nastaveném příkazem `/language`).\n\n"
            "*Dostupné příkazy:*\n"
            "`/start` - Požádejte o vymazání historie chatu a zobrazení uvítací zprávy.\n"
            "`/help` - Zobrazit tuto nápovědu.\n"
            "`/language` - Vyberte preferovaný jazyk pro mé odpovědi."
        ),
        "hu": (
            "Én vagyok a te _StudyHelper\\_Bot_-od! Küldj nekem bármilyen tanulmányokkal kapcsolatos üzenetet.\n"
            "Megpróbálom megjegyezni a legutóbbi beszélgetésünket és a preferált nyelveden válaszolni (`/language`-vel beállítható).\n\n"
            "*Elérhető parancsok:*\n"
            "`/start` - Kérd a csevegési előzmények törlését és egy üdvözlő üzenet megjelenítését.\n"
            "`/help` - Mutasd ezt a súgóüzenetet.\n"
            "`/language` - Válaszd ki a válaszaim nyelvét."
        ),
        "ro": (
            "Sunt _StudyHelper\\_Bot_-ul tău! Trimite-mi orice mesaj legat de studiile tale.\n"
            "Încerc să îmi amintesc conversația recentă și să răspund în limba ta preferată (setată cu `/language`).\n\n"
            "*Comenzi disponibile:*\n"
            "`/start` - Cere să se șteargă istoricul conversației și să vezi un mesaj de bun venit.\n"
            "`/help` - Arată acest mesaj de ajutor.\n"
            "`/language` - Alege limba preferată pentru răspunsurile mele."
        ),
        "el": (
            "Είμαι ο _StudyHelper\\_Bot_ σου! Στείλε μου οποιοδήποτε μήνυμα σχετικό με τις σπουδές σου.\n"
            "Προσπαθώ να θυμάμαι την πρόσφατη συνομιλία μας και να απαντώ στη γλώσσα που προτιμάς (ορίζεται με `/language`).\n\n"
            "*Διαθέσιμες εντολές:*\n"
            "`/start` - Ζήτα να διαγραφεί το ιστορικό συνομιλιών και να δεις ένα μήνυμα καλωσορίσματος.\n"
            "`/help` - Εμφάνιση αυτού του μηνύματος βοήθειας.\n"
            "`/language` - Επέλεξε την προτιμώμενη γλώσσα για τις απαντήσεις μου."
        ),
        "he": (
            "אני ה_StudyHelper\\_Bot_ שלך! שלח לי כל הודעה שקשורה ללימודים שלך.\n"
            "אני מנסה לזכור את השיחה האחרונה שלנו ולהגיב בשפה המועדפת עליך (נבחרת באמצעות `/language`).\n\n"
            "*פקודות זמינות:*\n"
            "`/start` - בקש לנקות את היסטוריית הצ׳אט ולקבל הודעת ברכה.\n"
            "`/help` - הצג הודעת עזרה זו.\n"
            "`/language` - בחר את שפת התשובות שלי."
        ),
        "th": (
            "ฉันคือ _StudyHelper\\_Bot_ ของคุณ! ส่งข้อความที่เกี่ยวกับการเรียนของคุณมาได้เลย\n"
            "ฉันพยายามจำบทสนทนาล่าสุดและตอบกลับเป็นภาษาที่คุณเลือกไว้ (`/language`).\n\n"
            "*คำสั่งที่ใช้ได้:*\n"
            "`/start` - ขอเคลียร์ประวัติแชทและดูข้อความต้อนรับ\n"
            "`/help` - แสดงข้อความช่วยเหลือนี้\n"
            "`/language` - เลือกภาษาที่ต้องการให้ฉันตอบกลับ"
        ),
        "vi": (
            "Tôi là _StudyHelper\\_Bot_ của bạn! Gửi cho tôi bất kỳ tin nhắn nào liên quan đến việc học của bạn.\n"
            "Tôi cố gắng ghi nhớ cuộc trò chuyện gần đây và trả lời bằng ngôn ngữ bạn chọn (đặt bằng `/language`).\n\n"
            "*Các lệnh có sẵn:*\n"
            "`/start` - Yêu cầu xóa lịch sử trò chuyện và xem tin nhắn chào mừng.\n"
            "`/help` - Hiển thị tin nhắn trợ giúp này.\n"
            "`/language` - Chọn ngôn ngữ ưu tiên để tôi trả lời."
        ),
        "id": (
            "Saya _StudyHelper\\_Bot_ Anda! Kirimkan pesan apa pun yang berhubungan dengan studi Anda.\n"
            "Saya mencoba mengingat percakapan terbaru dan merespons dalam bahasa pilihan Anda (diatur dengan `/language`).\n\n"
            "*Perintah yang tersedia:*\n"
            "`/start` - Minta untuk menghapus riwayat chat dan melihat pesan sambutan.\n"
            "`/help` - Tampilkan pesan bantuan ini.\n"
            "`/language` - Pilih bahasa pilihan Anda untuk respons saya."
        ),
        "ms": (
            "Saya adalah _StudyHelper\\_Bot_ anda! Hantar apa-apa mesej berkaitan dengan pembelajaran anda.\n"
            "Saya cuba mengingati perbualan terkini dan membalas dalam bahasa pilihan anda (ditetapkan dengan `/language`).\n\n"
            "*Perintah tersedia:*\n"
            "`/start` - Minta untuk membersihkan sejarah chat dan lihat mesej alu-aluan.\n"
            "`/help` - Tunjukkan mesej bantuan ini.\n"
            "`/language` - Pilih bahasa pilihan anda untuk balasan saya."
        ),
        "uk": (
            "Я ваш _StudyHelper\\_Bot_! Надсилайте мені будь-які повідомлення, що стосуються ваших навчань.\n"
            "Я намагаюся пам’ятати нашу недавню розмову і відповідати вашою обраною мовою (встановлюється командою `/language`).\n\n"
            "*Доступні команди:*\n"
            "`/start` - Попросити очистити історію чату і побачити привітальне повідомлення.\n"
            "`/help` - Показати це повідомлення допомоги.\n"
            "`/language` - Оберіть бажану мову для моїх відповідей."
        ),
        "uz": (
            "Men sizning _StudyHelper\\_Bot_ man! O'qishingizga oid har qanday xabarni menga yuboring.\n"
            "So‘nggi suhbatimizni eslab qolishga harakat qilaman va javoblarni siz tanlagan tilingizda beraman (`/language` yordamida sozlanadi).\n\n"
            "*Mavjud buyruqlar:*\n"
            "`/start` - Suhbat tariximizni tozalash va xush kelibsiz xabarini ko‘rishni so‘rashingiz mumkin.\n"
            "`/help` - Ushbu yordam xabarini ko‘rsatish.\n"
            "`/language` - Javoblarim uchun afzal tilingizni tanlang."
        ),
        "zh-TW": (
            "我是你的_StudyHelper\\_Bot_！發送任何與你的學習相關的訊息給我。\n"
            "我會嘗試記住我們最近的對話，並用你設定的語言回覆（通過 `/language` 設定）。\n\n"
            "*可用指令：*\n"
            "`/start` - 請求清除我們的聊天記錄並查看歡迎訊息。\n"
            "`/help` - 顯示此幫助訊息。\n"
            "`/language` - 選擇你希望我使用的回覆語言。"
        ),
        "pt-PT": (
            "Sou o teu _StudyHelper\\_Bot_! Envia-me qualquer mensagem relacionada com os teus estudos.\n"
            "Tento lembrar a nossa conversa recente e responder na língua que preferires (definido com `/language`).\n\n"
            "*Comandos disponíveis:*\n"
            "`/start` - Pede para limpar o histórico do chat e vê uma mensagem de boas-vindas.\n"
            "`/help` - Mostra esta mensagem de ajuda.\n"
            "`/language` - Escolhe a tua língua preferida para as minhas respostas."
        ),
    },
    "current_language_is": {
        "en": "Your current language: *{current_lang_name}*.",
        "es": "Tu idioma actual: *{current_lang_name}*.",
        "fr": "Votre langue actuelle : *{current_lang_name}*.",
        "kk": "Сіздің қазіргі тіліңіз: *{current_lang_name}*.",
        "de": "Ihre aktuelle Sprache: *{current_lang_name}*.",
        "ru": "Ваш текущий язык: *{current_lang_name}*.",
        "zh-CN": "您当前的语言是：*{current_lang_name}*。",
        "ja": "現在の言語：*{current_lang_name}*。",
        "ko": "현재 언어: *{current_lang_name}*.",
        "pt-BR": "Seu idioma atual: *{current_lang_name}*.",
        "it": "La tua lingua attuale: *{current_lang_name}*.",
        "ar": "لغتك الحالية: *{current_lang_name}*.",
        "hi": "आपकी वर्तमान भाषा: *{current_lang_name}*।",
        "tr": "Mevcut diliniz: *{current_lang_name}*.",
        "nl": "Je huidige taal: *{current_lang_name}*.",
        "pl": "Twój obecny język: *{current_lang_name}*.",
        "sv": "Ditt nuvarande språk: *{current_lang_name}*.",
        "fi": "Nykyinen kielesi: *{current_lang_name}*.",
        "no": "Ditt nåværende språk: *{current_lang_name}*.",
        "da": "Dit nuværende sprog: *{current_lang_name}*.",
        "cs": "Váš aktuální jazyk: *{current_lang_name}*.",
        "hu": "Jelenlegi nyelved: *{current_lang_name}*.",
        "ro": "Limba ta curentă: *{current_lang_name}*.",
        "el": "Η τρέχουσα γλώσσα σας: *{current_lang_name}*.",
        "he": "השפה הנוכחית שלך: *{current_lang_name}*.",
        "th": "ภาษาปัจจุบันของคุณ: *{current_lang_name}*.",
        "vi": "Ngôn ngữ hiện tại của bạn: *{current_lang_name}*.",
        "id": "Bahasa Anda saat ini: *{current_lang_name}*.",
        "ms": "Bahasa semasa anda: *{current_lang_name}*.",
        "uk": "Поточна мова: *{current_lang_name}*.",
        "uz": "Joriy tilingiz: *{current_lang_name}*.",
        "zh-TW": "您目前的語言：*{current_lang_name}*。",
        "pt-PT": "A sua língua atual: *{current_lang_name}*.",
    },
    "choose_preferred_language_paginated": {
        "en": "Choose your preferred language (Page {page_display_number}):",
        "es": "Elige tu idioma preferido (Página {page_display_number}):",
        "fr": "Choisissez votre langue préférée (Page {page_display_number}) :",
        "kk": "Қалаған тіліңізді таңдаңыз (Бет {page_display_number}):",
        "de": "Wähle deine bevorzugte Sprache (Seite {page_display_number}):",
        "ru": "Выберите предпочитаемый язык (Страница {page_display_number}):",
        "zh-CN": "选择你喜欢的语言（第 {page_display_number} 页）：",
        "ja": "希望する言語を選択してください（ページ {page_display_number}）：",
        "ko": "선호하는 언어를 선택하세요 (페이지 {page_display_number}):",
        "pt-BR": "Escolha seu idioma preferido (Página {page_display_number}):",
        "it": "Scegli la tua lingua preferita (Pagina {page_display_number}):",
        "ar": "اختر لغتك المفضلة (الصفحة {page_display_number}):",
        "hi": "अपनी पसंदीदा भाषा चुनें (पृष्ठ {page_display_number}):",
        "tr": "Tercih ettiğiniz dili seçin (Sayfa {page_display_number}):",
        "nl": "Kies je voorkeurstaal (Pagina {page_display_number}):",
        "pl": "Wybierz preferowany język (Strona {page_display_number}):",
        "sv": "Välj ditt föredragna språk (Sida {page_display_number}):",
        "fi": "Valitse haluamasi kieli (Sivu {page_display_number}):",
        "no": "Velg ditt foretrukne språk (Side {page_display_number}):",
        "da": "Vælg dit foretrukne sprog (Side {page_display_number}):",
        "cs": "Vyberte preferovaný jazyk (Stránka {page_display_number}):",
        "hu": "Válassza ki a kívánt nyelvet (Oldal {page_display_number}):",
        "ro": "Alegeți limba preferată (Pagina {page_display_number}):",
        "el": "Επιλέξτε την προτιμώμενη γλώσσα (Σελίδα {page_display_number}):",
        "he": "בחר את השפה המועדפת עליך (עמוד {page_display_number}):",
        "th": "เลือกภาษาที่คุณต้องการ (หน้า {page_display_number}):",
        "vi": "Chọn ngôn ngữ ưa thích của bạn (Trang {page_display_number}):",
        "id": "Pilih bahasa pilihan Anda (Halaman {page_display_number}):",
        "ms": "Pilih bahasa pilihan anda (Muka Surat {page_display_number}):",
        "uk": "Виберіть бажану мову (Сторінка {page_display_number}):",
        "uz": "Afzal ko'rgan tilingizni tanlang (Sahifa {page_display_number}):",
        "zh-TW": "選擇您偏好的語言（第 {page_display_number} 頁）：",
        "pt-PT": "Escolha a sua língua preferida (Página {page_display_number}):",
    },
    "previous_button": {
        "en": "⬅️ Previous",
        "es": "⬅️ Anterior",
        "fr": "⬅️ Précédent",
        "kk": "⬅️ Алдыңғы",
        "de": "⬅️ Zurück",
        "ru": "⬅️ Назад",
        "zh-CN": "⬅️ 上一页",
        "ja": "⬅️ 前へ",
        "ko": "⬅️ 이전",
        "pt-BR": "⬅️ Anterior",
        "it": "⬅️ Precedente",
        "ar": "⬅️ السابق",
        "hi": "⬅️ पिछला",
        "tr": "⬅️ Önceki",
        "nl": "⬅️ Vorige",
        "pl": "⬅️ Poprzedni",
        "sv": "⬅️ Föregående",
        "fi": "⬅️ Edellinen",
        "no": "⬅️ Forrige",
        "da": "⬅️ Forrige",
        "cs": "⬅️ Předchozí",
        "hu": "⬅️ Előző",
        "ro": "⬅️ Anterior",
        "el": "⬅️ Προηγούμενο",
        "he": "⬅️ הקודם",
        "th": "⬅️ ก่อนหน้า",
        "vi": "⬅️ Trước",
        "id": "⬅️ Sebelumnya",
        "ms": "⬅️ Sebelumnya",
        "uk": "⬅️ Попередній",
        "uz": "⬅️ Oldingi",
        "zh-TW": "⬅️ 上一頁",
        "pt-PT": "⬅️ Anterior",
    },
    "more_button": {
        "en": "More ➡️",
        "es": "Más ➡️",
        "fr": "Plus ➡️",
        "kk": "Көбірек ➡️",
        "de": "Mehr ➡️",
        "ru": "Еще ➡️",
        "zh-CN": "更多 ➡️",
        "ja": "もっと ➡️",
        "ko": "더 보기 ➡️",
        "pt-BR": "Mais ➡️",
        "it": "Altro ➡️",
        "ar": "المزيد ➡️",
        "hi": "अधिक ➡️",
        "tr": "Daha fazla ➡️",
        "nl": "Meer ➡️",
        "pl": "Więcej ➡️",
        "sv": "Mer ➡️",
        "fi": "Lisää ➡️",
        "no": "Mer ➡️",
        "da": "Mere ➡️",
        "cs": "Více ➡️",
        "hu": "Több ➡️",
        "ro": "Mai mult ➡️",
        "el": "Περισσότερα ➡️",
        "he": "עוד ➡️",
        "th": "เพิ่มเติม ➡️",
        "vi": "Thêm ➡️",
        "id": "Lagi ➡️",
        "ms": "Lagi ➡️",
        "uk": "Більше ➡️",
        "uz": "Ko‘proq ➡️",
        "zh-TW": "更多 ➡️",
        "pt-PT": "Mais ➡️",
    },
    "error_loading_language_page": {
        "en": "Error: Could not load language page.",
        "es": "Error: No se pudo cargar la página de idiomas.",
        "fr": "Erreur : Impossible de charger la page des langues.",
        "kk": "Қате: Тілдер бетін жүктеу мүмкін болмады.",
        "de": "Fehler: Sprachseite konnte nicht geladen werden.",
        "ru": "Ошибка: Не удалось загрузить страницу языка.",
        "zh-CN": "错误：无法加载语言页面。",
        "ja": "エラー：言語ページを読み込めませんでした。",
        "ko": "오류: 언어 페이지를 불러올 수 없습니다.",
        "pt-BR": "Erro: Não foi possível carregar a página de idiomas.",
        "it": "Errore: Impossibile caricare la pagina della lingua.",
        "ar": "خطأ: تعذر تحميل صفحة اللغة.",
        "hi": "त्रुटि: भाषा पृष्ठ लोड नहीं हो सका।",
        "tr": "Hata: Dil sayfası yüklenemedi.",
        "nl": "Fout: Kan taalpagina niet laden.",
        "pl": "Błąd: Nie można załadować strony języka.",
        "sv": "Fel: Kunde inte ladda språk sidan.",
        "fi": "Virhe: Kieli sivua ei voitu ladata.",
        "no": "Feil: Kunne ikke laste språk siden.",
        "da": "Fejl: Kunne ikke indlæse sprogsiden.",
        "cs": "Chyba: Nelze načíst stránku jazyka.",
        "hu": "Hiba: Nem sikerült betölteni a nyelvi oldalt.",
        "ro": "Eroare: Nu s-a putut încărca pagina limbii.",
        "el": "Σφάλμα: Αδυναμία φόρτωσης της σελίδας γλώσσας.",
        "he": "שגיאה: לא ניתן לטעון את דף השפה.",
        "th": "ข้อผิดพลาด: ไม่สามารถโหลดหน้าภาษาได้",
        "vi": "Lỗi: Không thể tải trang ngôn ngữ.",
        "id": "Kesalahan: Tidak dapat memuat halaman bahasa.",
        "ms": "Ralat: Tidak dapat memuat halaman bahasa.",
        "uk": "Помилка: Не вдалося завантажити сторінку мови.",
        "uz": "Xato: Til sahifasini yuklab bo‘lmadi.",
        "zh-TW": "錯誤：無法載入語言頁面。",
        "pt-PT": "Erro: Não foi possível carregar a página de idioma.",
    },
    "error_updating_language_page":  {
        "en": "Error updating language page.",
        "es": "Error al actualizar la página de idiomas.",
        "fr": "Erreur lors de la mise à jour de la page des langues.",
        "kk": "Тілдер бетін жаңарту кезінде қате орын алды.",
        "de": "Fehler beim Aktualisieren der Sprachseite.",
        "ru": "Ошибка при обновлении страницы языка.",
        "zh-CN": "更新语言页面时出错。",
        "ja": "言語ページの更新中にエラーが発生しました。",
        "ko": "언어 페이지 업데이트 오류가 발생했습니다.",
        "pt-BR": "Erro ao atualizar a página de idiomas.",
        "it": "Errore durante l'aggiornamento della pagina della lingua.",
        "ar": "خطأ في تحديث صفحة اللغة.",
        "hi": "भाषा पृष्ठ अपडेट करने में त्रुटि।",
        "tr": "Dil sayfası güncellenirken hata oluştu.",
        "nl": "Fout bij het bijwerken van de taalpagina.",
        "pl": "Błąd podczas aktualizacji strony języka.",
        "sv": "Fel vid uppdatering av språk sidan.",
        "fi": "Virhe päivittäessä kielisivua.",
        "no": "Feil ved oppdatering av språk siden.",
        "da": "Fejl ved opdatering af sprogsiden.",
        "cs": "Chyba při aktualizaci stránky jazyka.",
        "hu": "Hiba a nyelvi oldal frissítésekor.",
        "ro": "Eroare la actualizarea paginii limbii.",
        "el": "Σφάλμα κατά την ενημέρωση της σελίδας γλώσσας.",
        "he": "שגיאה בעדכון דף השפה.",
        "th": "ข้อผิดพลาดในการอัปเดตหน้าภาษา",
        "vi": "Lỗi khi cập nhật trang ngôn ngữ.",
        "id": "Kesalahan saat memperbarui halaman bahasa.",
        "ms": "Ralat semasa mengemas kini halaman bahasa.",
        "uk": "Помилка під час оновлення сторінки мови.",
        "uz": "Til sahifasini yangilashda xato yuz berdi.",
        "zh-TW": "更新語言頁面時出錯。",
        "pt-PT": "Erro ao atualizar a página de idioma.",
    },
    "invalid_language_selection_error": {
        "en": "Error: Invalid language selection.",
        "es": "Error: Selección de idioma inválida.",
        "fr": "Erreur : Sélection de langue invalide.",
        "kk": "Қате: Жарамсыз тіл таңдалды.",
        "de": "Fehler: Ungültige Sprachauswahl.",
        "ru": "Ошибка: Недопустимый выбор языка.",
        "zh-CN": "错误：无效的语言选择。",
        "ja": "エラー：無効な言語選択です。",
        "ko": "오류: 잘못된 언어 선택입니다.",
        "pt-BR": "Erro: Seleção de idioma inválida.",
        "it": "Errore: Selezione della lingua non valida.",
        "ar": "خطأ: اختيار لغة غير صالح.",
        "hi": "त्रुटि: अमान्य भाषा चयन।",
        "tr": "Hata: Geçersiz dil seçimi.",
        "nl": "Fout: Ongeldige taalkeuze.",
        "pl": "Błąd: Nieprawidłowy wybór języka.",
        "sv": "Fel: Ogiltigt språkval.",
        "fi": "Virhe: Virheellinen kielivalinta.",
        "no": "Feil: Ugyldig språkvvalg.",
        "da": "Fejl: Ugyldigt sprogvalg.",
        "cs": "Chyba: Neplatný výběr jazyka.",
        "hu": "Hiba: Érvénytelen nyelvválasztás.",
        "ro": "Eroare: Selecție invalidă a limbii.",
        "el": "Σφάλμα: Μη έγκυρη επιλογή γλώσσας.",
        "he": "שגיאה: בחירת שפה לא תקינה.",
        "th": "ข้อผิดพลาด: การเลือกภาษาที่ไม่ถูกต้อง",
        "vi": "Lỗi: Lựa chọn ngôn ngữ không hợp lệ.",
        "id": "Kesalahan: Pilihan bahasa tidak valid.",
        "ms": "Ralat: Pilihan bahasa tidak sah.",
        "uk": "Помилка: Недійсний вибір мови.",
        "uz": "Xato: Noto‘g‘ri til tanlovi.",
        "zh-TW": "錯誤：無效的語言選擇。",
        "pt-PT": "Erro: Seleção de idioma inválida.",
    },
    "processing_error": {
        "en": "Error processing your request.",
        "es": "Error al procesar tu solicitud.",
        "fr": "Erreur lors du traitement de votre demande.",
        "kk": "Сұранысыңызды өңдеу кезінде қате пайда болды.",
        "de": "Fehler bei der Verarbeitung Ihrer Anfrage.",
        "ru": "Ошибка при обработке вашего запроса.",
        "zh-CN": "处理您的请求时出错。",
        "ja": "リクエストの処理中にエラーが発生しました。",
        "ko": "요청 처리 중 오류가 발생했습니다.",
        "pt-BR": "Erro ao processar sua solicitação.",
        "it": "Errore durante l'elaborazione della tua richiesta.",
        "ar": "خطأ في معالجة طلبك.",
        "hi": "आपके अनुरोध को संसाधित करने में त्रुटि।",
        "tr": "İsteğiniz işlenirken hata oluştu.",
        "nl": "Fout bij het verwerken van uw verzoek.",
        "pl": "Błąd podczas przetwarzania twojego żądania.",
        "sv": "Fel vid behandling av din förfrågan.",
        "fi": "Virhe pyyntösi käsittelyssä.",
        "no": "Feil ved behandling av forespørselen din.",
        "da": "Fejl ved behandling af din anmodning.",
        "cs": "Chyba při zpracování vaší žádosti.",
        "hu": "Hiba a kérés feldolgozása közben.",
        "ro": "Eroare la procesarea cererii tale.",
        "el": "Σφάλμα κατά την επεξεργασία του αιτήματός σας.",
        "he": "שגיאה בעיבוד הבקשה שלך.",
        "th": "เกิดข้อผิดพลาดในการประมวลผลคำขอของคุณ",
        "vi": "Lỗi khi xử lý yêu cầu của bạn.",
        "id": "Kesalahan saat memproses permintaan Anda.",
        "ms": "Ralat semasa memproses permintaan anda.",
        "uk": "Помилка при обробці вашого запиту.",
        "uz": "So‘rovingizni qayta ishlashda xato yuz berdi.",
        "zh-TW": "處理您的請求時出錯。",
        "pt-PT": "Erro ao processar seu pedido.",
    },
    "unexpected_error": {
        "en": "An unexpected error occurred.",
        "es": "Ocurrió un error inesperado.",
        "fr": "Une erreur inattendue s'est produite.",
        "kk": "Күтпеген қате орын алды.",
        "de": "Ein unerwarteter Fehler ist aufgetreten.",
        "ru": "Произошла непредвиденная ошибка.",
        "zh-CN": "发生了意外错误。",
        "ja": "予期しないエラーが発生しました。",
        "ko": "예기치 않은 오류가 발생했습니다.",
        "pt-BR": "Ocorreu um erro inesperado.",
        "it": "Si è verificato un errore imprevisto.",
        "ar": "حدث خطأ غير متوقع.",
        "hi": "अप्रत्याशित त्रुटि हुई।",
        "tr": "Beklenmeyen bir hata oluştu.",
        "nl": "Er is een onverwachte fout opgetreden.",
        "pl": "Wystąpił nieoczekiwany błąd.",
        "sv": "Ett oväntat fel uppstod.",
        "fi": "Tapahtui odottamaton virhe.",
        "no": "En uventet feil oppstod.",
        "da": "Der opstod en uventet fejl.",
        "cs": "Došlo k neočekávané chybě.",
        "hu": "Váratlan hiba történt.",
        "ro": "A apărut o eroare neașteptată.",
        "el": "Παρουσιάστηκε απρόβλεπτο σφάλμα.",
        "he": "אירעה שגיאה בלתי צפויה.",
        "th": "เกิดข้อผิดพลาดที่ไม่คาดคิดขึ้น",
        "vi": "Đã xảy ra lỗi không mong muốn.",
        "id": "Terjadi kesalahan tak terduga.",
        "ms": "Ralat yang tidak dijangka berlaku.",
        "uk": "Сталася несподівана помилка.",
        "uz": "Kutilmagan xato yuz berdi.",
        "zh-TW": "發生了意外錯誤。",
        "pt-PT": "Ocorreu um erro inesperado.",
    },
    "current_lang_label": {
        "en": "Your current language:",
        "es": "Tu idioma actual:",
        "fr": "Votre langue actuelle :",
        "kk": "Сіздің қазіргі тіліңіз:",
        "de": "Ihre aktuelle Sprache:",
        "ru": "Ваш текущий язык:",
        "zh-CN": "您当前的语言：",
        "ja": "現在の言語：",
        "ko": "현재 언어:",
        "pt-BR": "Seu idioma atual:",
        "it": "La tua lingua attuale:",
        "ar": "لغتك الحالية:",
        "hi": "आपकी वर्तमान भाषा:",
        "tr": "Mevcut diliniz:",
        "nl": "Je huidige taal:",
        "pl": "Twój obecny język:",
        "sv": "Ditt nuvarande språk:",
        "fi": "Nykyinen kielesi:",
        "no": "Ditt nåværende språk:",
        "da": "Dit nuværende sprog:",
        "cs": "Váš aktuální jazyk:",
        "hu": "Az aktuális nyelved:",
        "ro": "Limba ta curentă:",
        "el": "Η τρέχουσα γλώσσα σας:",
        "he": "השפה הנוכחית שלך:",
        "th": "ภาษาปัจจุบันของคุณ:",
        "vi": "Ngôn ngữ hiện tại của bạn:",
        "id": "Bahasa Anda saat ini:",
        "ms": "Bahasa semasa anda:",
        "uk": "Ваша поточна мова:",
        "uz": "Joriy tilingiz:",
        "zh-TW": "您目前的語言：",
        "pt-PT": "A sua língua atual:",
    },
    "choose_lang_label": {
        "en": "Choose your preferred language",
        "es": "Elige tu idioma preferido",
        "fr": "Choisissez votre langue préférée",
        "kk": "Қалаған тіліңізді таңдаңыз",
        "de": "Wählen Sie Ihre bevorzugte Sprache",
        "ru": "Выберите предпочитаемый язык",
        "zh-CN": "选择您喜欢的语言",
        "ja": "希望する言語を選択してください",
        "ko": "선호하는 언어를 선택하세요",
        "pt-BR": "Escolha seu idioma preferido",
        "it": "Scegli la tua lingua preferita",
        "ar": "اختر لغتك المفضلة",
        "hi": "अपनी पसंदीदा भाषा चुनें",
        "tr": "Tercih ettiğiniz dili seçin",
        "nl": "Kies je voorkeurstaal",
        "pl": "Wybierz preferowany język",
        "sv": "Välj ditt föredragna språk",
        "fi": "Valitse haluamasi kieli",
        "no": "Velg ditt foretrukne språk",
        "da": "Vælg dit foretrukne sprog",
        "cs": "Vyberte preferovaný jazyk",
        "hu": "Válaszd ki a preferált nyelvet",
        "ro": "Alege limba preferată",
        "el": "Επιλέξτε την προτιμώμενη γλώσσα σας",
        "he": "בחר את השפה המועדפת עליך",
        "th": "เลือกภาษาที่คุณต้องการ",
        "vi": "Chọn ngôn ngữ bạn ưu tiên",
        "id": "Pilih bahasa pilihan Anda",
        "ms": "Pilih bahasa pilihan anda",
        "uk": "Виберіть бажану мову",
        "uz": "Istalgan tilingizni tanlang",
        "zh-TW": "選擇您偏好的語言",
        "pt-PT": "Escolha a sua língua preferida",
    },
    "page_label": {
        "en": "Page",
        "es": "Página",
        "fr": "Page",
        "kk": "Бет",
        "de": "Seite",
        "ru": "Страница",
        "zh-CN": "页",
        "ja": "ページ",
        "ko": "페이지",
        "pt-BR": "Página",
        "it": "Pagina",
        "ar": "صفحة",
        "hi": "पृष्ठ",
        "tr": "Sayfa",
        "nl": "Pagina",
        "pl": "Strona",
        "sv": "Sida",
        "fi": "Sivu",
        "no": "Side",
        "da": "Side",
        "cs": "Stránka",
        "hu": "Oldal",
        "ro": "Pagină",
        "el": "Σελίδα",
        "he": "עמוד",
        "th": "หน้า",
        "vi": "Trang",
        "id": "Halaman",
        "ms": "Halaman",
        "uk": "Сторінка",
        "uz": "Sahifa",
        "zh-TW": "頁",
        "pt-PT": "Página",
    },



    "processing_document": {
        "en": "Processing document: {file_name}... ⏳",
        "es": "Procesando documento: {file_name}... ⏳",
        "fr": "Traitement du document : {file_name}... ⏳",
        "kk": "Құжат өңделуде: {file_name}... ⏳",
        "de": "Dokument wird verarbeitet: {file_name}... ⏳",
        "ru": "Обработка документа: {file_name}... ⏳",
        "zh-CN": "正在处理文档：{file_name}... ⏳",
        "ja": "ドキュメントを処理中: {file_name}... ⏳",
        "ko": "문서 처리 중: {file_name}... ⏳",
        "pt-BR": "Processando documento: {file_name}... ⏳",
        "it": "Elaborazione del documento: {file_name}... ⏳",
        "ar": "جارٍ معالجة المستند: {file_name}... ⏳",
        "hi": "दस्तावेज़ प्रोसेस हो रहा है: {file_name}... ⏳",
        "tr": "Belge işleniyor: {file_name}... ⏳",
        "nl": "Document verwerken: {file_name}... ⏳",
        "pl": "Przetwarzanie dokumentu: {file_name}... ⏳",
        "sv": "Bearbetar dokument: {file_name}... ⏳",
        "fi": "Käsitellään asiakirjaa: {file_name}... ⏳",
        "no": "Behandler dokument: {file_name}... ⏳",
        "da": "Behandler dokument: {file_name}... ⏳",
        "cs": "Zpracovávání dokumentu: {file_name}... ⏳",
        "hu": "Dokumentum feldolgozása: {file_name}... ⏳",
        "ro": "Se procesează documentul: {file_name}... ⏳",
        "el": "Επεξεργασία εγγράφου: {file_name}... ⏳",
        "he": "מעבד מסמך: {file_name}... ⏳",
        "th": "กำลังประมวลผลเอกสาร: {file_name}... ⏳",
        "vi": "Đang xử lý tài liệu: {file_name}... ⏳",
        "id": "Memproses dokumen: {file_name}... ⏳",
        "ms": "Memproses dokumen: {file_name}... ⏳",
        "uk": "Обробка документа: {file_name}... ⏳",
        "uz": "Hujjat qayta ishlanmoqda: {file_name}... ⏳",
        "zh-TW": "正在處理文件：{file_name}... ⏳",
        "pt-PT": "A processar documento: {file_name}... ⏳"
    },
    "thinking": {
        "en": "🧠 Thinking...",
        "es": "🧠 Pensando...",
        "fr": "🧠 Réflexion...",
        "kk": "🧠 Ойлануда...",
        "de": "🧠 Denkt nach...",
        "ru": "🧠 Думаю...",
        "zh-CN": "🧠 思考中...",
        "ja": "🧠 考え中...",
        "ko": "🧠 생각 중...",
        "pt-BR": "🧠 Pensando...",
        "it": "🧠 Sto pensando...",
        "ar": "🧠 يفكر...",
        "hi": "🧠 सोच रहा है...",
        "tr": "🧠 Düşünüyor...",
        "nl": "🧠 Aan het nadenken...",
        "pl": "🧠 Myślenie...",
        "sv": "🧠 Tänker...",
        "fi": "🧠 Ajattelee...",
        "no": "🧠 Tenker...",
        "da": "🧠 Tænker...",
        "cs": "🧠 Přemýšlím...",
        "hu": "🧠 Gondolkodom...",
        "ro": "🧠 Mă gândesc...",
        "el": "🧠 Σκέφτεται...",
        "he": "🧠 חושב...",
        "th": "🧠 กำลังคิด...",
        "vi": "🧠 Đang suy nghĩ...",
        "id": "🧠 Sedang berpikir...",
        "ms": "🧠 Sedang berfikir...",
        "uk": "🧠 Думаю...",
        "uz": "🧠 O‘ylayapman...",
        "zh-TW": "🧠 思考中...",
        "pt-PT": "🧠 A pensar..."
    },
    "continuing_response": {
        "en": "...continuing response...",
        "es": "...continuando la respuesta...",
        "fr": "...suite de la réponse...",
        "kk": "...жауап жалғасуда...",
        "de": "...Antwort wird fortgesetzt...",
        "ru": "...продолжаю ответ...",
        "zh-CN": "...继续回答中...",
        "ja": "...回答を続けています...",
        "ko": "...응답 계속 중...",
        "pt-BR": "...continuando a resposta...",
        "it": "...continuando la risposta...",
        "ar": "...يتم متابعة الرد...",
        "hi": "...जवाब जारी है...",
        "tr": "...cevap devam ediyor...",
        "nl": "...antwoord wordt voortgezet...",
        "pl": "...kontynuowanie odpowiedzi...",
        "sv": "...fortsätter svaret...",
        "fi": "...jatketaan vastausta...",
        "no": "...fortsetter svaret...",
        "da": "...fortsætter svaret...",
        "cs": "...pokračuji v odpovědi...",
        "hu": "...válasz folytatódik...",
        "ro": "...se continuă răspunsul...",
        "el": "...συνέχεια της απάντησης...",
        "he": "...ממשיך בתגובה...",
        "th": "...กำลังตอบต่อ...",
        "vi": "...tiếp tục phản hồi...",
        "id": "...melanjutkan tanggapan...",
        "ms": "...meneruskan jawapan...",
        "uk": "...продовжую відповідь...",
        "uz": "...javob davom etmoqda...",
        "zh-TW": "...繼續回應中...",
        "pt-PT": "...a continuar a resposta..."
    },
    "response_continued_below": {
        "en": "...(response continues in new messages below)...",
        "es": "...(la respuesta continúa en los mensajes siguientes)...",
        "fr": "...(la réponse continue dans les messages ci-dessous)...",
        "kk": "...(жауап төмендегі хабарламаларда жалғасуда)...",
        "de": "...(Antwort wird in den folgenden Nachrichten fortgesetzt)...",
        "ru": "...(ответ продолжается в следующих сообщениях)...",
        "zh-CN": "...（回复在下方消息中继续）...",
        "ja": "...（応答は以下のメッセージに続きます）...",
        "ko": "...(응답은 아래 메시지에서 계속됩니다)...",
        "pt-BR": "...(a resposta continua nas mensagens abaixo)...",
        "it": "...(la risposta continua nei messaggi sottostanti)...",
        "ar": "...(يستمر الرد في الرسائل التالية)...",
        "hi": "...(उत्तर नीचे दिए गए संदेशों में जारी है)...",
        "tr": "...(cevap aşağıdaki mesajlarda devam ediyor)...",
        "nl": "...(reactie gaat verder in onderstaande berichten)...",
        "pl": "...(odpowiedź kontynuowana jest w poniższych wiadomościach)...",
        "sv": "...(svaret fortsätter i meddelanden nedan)...",
        "fi": "...(vastaus jatkuu alla olevissa viesteissä)...",
        "no": "...(svaret fortsetter i meldingene nedenfor)...",
        "da": "...(svaret fortsætter i beskederne nedenfor)...",
        "cs": "...(odpověď pokračuje v následujících zprávách)...",
        "hu": "...(a válasz az alábbi üzenetekben folytatódik)...",
        "ro": "...(răspunsul continuă în mesajele de mai jos)...",
        "el": "...(η απάντηση συνεχίζεται στα παρακάτω μηνύματα)...",
        "he": "...(התשובה נמשכת בהודעות למטה)...",
        "th": "...(การตอบกลับดำเนินต่อในข้อความด้านล่าง)...",
        "vi": "...(phản hồi tiếp tục trong các tin nhắn bên dưới)...",
        "id": "...(tanggapan berlanjut di pesan di bawah)...",
        "ms": "...(jawapan diteruskan dalam mesej di bawah)...",
        "uk": "...(відповідь продовжується в наступних повідомленнях)...",
        "uz": "...(javob quyidagi xabarlarda davom etadi)...",
        "zh-TW": "...（回應繼續於下方訊息）...",
        "pt-PT": "...(a resposta continua nas mensagens abaixo)..."
    },
    "response_complete": {
        "en": "✅ Done.",
        "es": "✅ Hecho.",
        "fr": "✅ Terminé.",
        "kk": "✅ Дайын.",
        "de": "✅ Fertig.",
        "ru": "✅ Готово.",
        "zh-CN": "✅ 完成。",
        "ja": "✅ 完了。",
        "ko": "✅ 완료.",
        "pt-BR": "✅ Concluído.",
        "it": "✅ Fatto.",
        "ar": "✅ تم.",
        "hi": "✅ पूर्ण हुआ।",
        "tr": "✅ Tamamlandı.",
        "nl": "✅ Klaar.",
        "pl": "✅ Gotowe.",
        "sv": "✅ Klar.",
        "fi": "✅ Valmis.",
        "no": "✅ Ferdig.",
        "da": "✅ Færdig.",
        "cs": "✅ Hotovo.",
        "hu": "✅ Kész.",
        "ro": "✅ Gata.",
        "el": "✅ Έγινε.",
        "he": "✅ בוצע.",
        "th": "✅ เสร็จสิ้น",
        "vi": "✅ Hoàn tất.",
        "id": "✅ Selesai.",
        "ms": "✅ Selesai.",
        "uk": "✅ Готово.",
        "uz": "✅ Tayyor.",
        "zh-TW": "✅ 完成。",
        "pt-PT": "✅ Concluído."
    },
    "gemini_no_response_text": {
        "en": "🤷 I couldn't generate a response for that.",
        "es": "🤷 No pude generar una respuesta para eso.",
        "fr": "🤷 Je n'ai pas pu générer de réponse.",
        "kk": "🤷 Мен ол үшін жауап жасай алмадым.",
        "de": "🤷 Ich konnte keine Antwort darauf generieren.",
        "ru": "🤷 Я не смог сгенерировать ответ на это.",
        "zh-CN": "🤷 我无法生成对此的回复。",
        "ja": "🤷 それには応答を生成できませんでした。",
        "ko": "🤷 이에 대한 응답을 생성할 수 없었습니다.",
        "pt-BR": "🤷 Não consegui gerar uma resposta para isso.",
        "it": "🤷 Non sono riuscito a generare una risposta.",
        "ar": "🤷 لم أتمكن من إنشاء رد على ذلك.",
        "hi": "🤷 मैं इसके लिए उत्तर नहीं बना सका।",
        "tr": "🤷 Bunun için bir yanıt üretemedim.",
        "nl": "🤷 Ik kon daar geen antwoord op genereren.",
        "pl": "🤷 Nie mogłem wygenerować odpowiedzi.",
        "sv": "🤷 Jag kunde inte generera ett svar.",
        "fi": "🤷 En pystynyt luomaan vastausta siihen.",
        "no": "🤷 Jeg kunne ikke generere et svar.",
        "da": "🤷 Jeg kunne ikke generere et svar.",
        "cs": "🤷 Nepodařilo se mi vygenerovat odpověď.",
        "hu": "🤷 Nem tudtam választ generálni.",
        "ro": "🤷 Nu am putut genera un răspuns.",
        "el": "🤷 Δεν κατάφερα να δημιουργήσω απάντηση.",
        "he": "🤷 לא הצלחתי ליצור תגובה לכך.",
        "th": "🤷 ฉันไม่สามารถสร้างคำตอบได้",
        "vi": "🤷 Tôi không thể tạo phản hồi cho điều đó.",
        "id": "🤷 Saya tidak dapat membuat tanggapan untuk itu.",
        "ms": "🤷 Saya tidak dapat menjana jawapan untuk itu.",
        "uk": "🤷 Я не зміг згенерувати відповідь.",
        "uz": "🤷 Men bunga javob bera olmadim.",
        "zh-TW": "🤷 我無法生成回應。",
        "pt-PT": "🤷 Não consegui gerar uma resposta para isso."
    },
    "error_initiating_response": {
        "en": "⚠️ Error: Could not start response processing. Please try again.",
        "es": "⚠️ Error: No se pudo iniciar el procesamiento de la respuesta. Inténtalo de nuevo.",
        "fr": "⚠️ Erreur : Impossible de démarrer le traitement de la réponse. Veuillez réessayer.",
        "kk": "⚠️ Қате: Жауапты өңдеу басталмады. Қайта көріңіз.",
        "de": "⚠️ Fehler: Antwortverarbeitung konnte nicht gestartet werden. Bitte versuchen Sie es erneut.",
        "ru": "⚠️ Ошибка: Не удалось начать обработку ответа. Пожалуйста, попробуйте снова.",
        "zh-CN": "⚠️ 错误：无法开始响应处理。请重试。",
        "ja": "⚠️ エラー：応答の処理を開始できませんでした。もう一度お試しください。",
        "ko": "⚠️ 오류: 응답 처리를 시작할 수 없습니다. 다시 시도해 주세요.",
        "pt-BR": "⚠️ Erro: Não foi possível iniciar o processamento da resposta. Tente novamente.",
        "it": "⚠️ Errore: impossibile avviare l'elaborazione della risposta. Riprova.",
        "ar": "⚠️ خطأ: تعذر بدء معالجة الرد. يرجى المحاولة مرة أخرى.",
        "hi": "⚠️ त्रुटि: उत्तर प्रसंस्करण शुरू नहीं हो सका। कृपया पुनः प्रयास करें।",
        "tr": "⚠️ Hata: Yanıt işleme başlatılamadı. Lütfen tekrar deneyin.",
        "nl": "⚠️ Fout: Kon reactie niet starten. Probeer het opnieuw.",
        "pl": "⚠️ Błąd: Nie można rozpocząć przetwarzania odpowiedzi. Spróbuj ponownie.",
        "sv": "⚠️ Fel: Kunde inte starta svarshantering. Försök igen.",
        "fi": "⚠️ Virhe: Vastausta ei voitu aloittaa. Yritä uudelleen.",
        "no": "⚠️ Feil: Kunne ikke starte svarbehandling. Prøv igjen.",
        "da": "⚠️ Fejl: Kunne ikke starte svarbehandling. Prøv igen.",
        "cs": "⚠️ Chyba: Nelze zahájit zpracování odpovědi. Zkuste to znovu.",
        "hu": "⚠️ Hiba: A válasz feldolgozása nem indult el. Kérlek, próbáld újra.",
        "ro": "⚠️ Eroare: Nu s-a putut începe procesarea răspunsului. Vă rugăm să încercați din nou.",
        "el": "⚠️ Σφάλμα: Δεν ήταν δυνατή η έναρξη της επεξεργασίας απάντησης. Δοκιμάστε ξανά.",
        "he": "⚠️ שגיאה: לא ניתן היה להתחיל בעיבוד התגובה. אנא נסה שוב.",
        "th": "⚠️ ข้อผิดพลาด: ไม่สามารถเริ่มประมวลผลคำตอบได้ โปรดลองอีกครั้ง",
        "vi": "⚠️ Lỗi: Không thể bắt đầu xử lý phản hồi. Vui lòng thử lại.",
        "id": "⚠️ Kesalahan: Tidak dapat memulai pemrosesan tanggapan. Silakan coba lagi.",
        "ms": "⚠️ Ralat: Tidak dapat memulakan pemprosesan jawapan. Sila cuba lagi.",
        "uk": "⚠️ Помилка: Не вдалося почати обробку відповіді. Спробуйте ще раз.",
        "uz": "⚠️ Xato: Javobni qayta ishlashni boshlash imkoni bo‘lmadi. Qayta urinib ko‘ring.",
        "zh-TW": "⚠️ 錯誤：無法開始處理回應。請再試一次。",
        "pt-PT": "⚠️ Erro: Não foi possível iniciar o processamento da resposta. Tente novamente."
    },
    "unexpected_error_processing": {
    "en": "⚠️ An unexpected error occurred while processing your request. Please try again.",
    "es": "⚠️ Ocurrió un error inesperado al procesar tu solicitud. Por favor, inténtalo de nuevo.",
    "fr": "⚠️ Une erreur inattendue s'est produite lors du traitement de votre requête. Veuillez réessayer.",
    "kk": "⚠️ Сіздің сұранысыңызды өңдеу кезінде күтпеген қате болды. Қайта көріңізші.",
    "de": "⚠️ Ein unerwarteter Fehler ist bei der Verarbeitung Ihrer Anfrage aufgetreten. Bitte versuchen Sie es erneut.",
    "ru": "⚠️ При обработке вашего запроса произошла непредвиденная ошибка. Пожалуйста, попробуйте ещё раз.",
    "zh-CN": "⚠️ 处理您的请求时发生意外错误。请再试一次。",
    "ja": "⚠️ リクエストの処理中に予期せぬエラーが発生しました。もう一度お試しください。",
    "ko": "⚠️ 요청을 처리하는 동안 예기치 않은 오류가 발생했습니다. 다시 시도해 주세요.",
    "pt-BR": "⚠️ Ocorreu um erro inesperado ao processar sua solicitação. Por favor, tente novamente.",
    "it": "⚠️ Si è verificato un errore imprevisto durante l'elaborazione della tua richiesta. Per favore riprova.",
    "ar": "⚠️ حدث خطأ غير متوقع أثناء معالجة طلبك. يرجى المحاولة مرة أخرى.",
    "hi": "⚠️ आपके अनुरोध को संसाधित करते समय एक अप्रत्याशित त्रुटि हुई। कृपया पुनः प्रयास करें।",
    "tr": "⚠️ İsteğiniz işlenirken beklenmeyen bir hata oluştu. Lütfen tekrar deneyin.",
    "nl": "⚠️ Er is een onverwachte fout opgetreden bij het verwerken van uw verzoek. Probeer het opnieuw.",
    "pl": "⚠️ Wystąpił nieoczekiwany błąd podczas przetwarzania Twojego żądania. Spróbuj ponownie.",
    "sv": "⚠️ Ett oväntat fel uppstod vid behandling av din begäran. Försök igen.",
    "fi": "⚠️ Odottamaton virhe ilmeni pyynnön käsittelyssä. Yritä uudelleen.",
    "no": "⚠️ En uventet feil oppstod under behandling av forespørselen din. Vennligst prøv igjen.",
    "da": "⚠️ En uventet fejl opstod ved behandling af din anmodning. Prøv igen.",
    "cs": "⚠️ Při zpracování vašeho požadavku došlo k neočekávané chybě. Zkuste to prosím znovu.",
    "hu": "⚠️ Váratlan hiba történt a kérés feldolgozása közben. Kérlek, próbáld újra.",
    "ro": "⚠️ A apărut o eroare neașteptată în procesarea cererii tale. Te rog încearcă din nou.",
    "el": "⚠️ Παρουσιάστηκε ένα απρόσμενο σφάλμα κατά την επεξεργασία του αιτήματός σας. Παρακαλώ δοκιμάστε ξανά.",
    "he": "⚠️ ארעה שגיאה לא צפויה בעת עיבוד הבקשה שלך. אנא נסה שוב.",
    "th": "⚠️ เกิดข้อผิดพลาดที่ไม่คาดคิดระหว่างการประมวลผลคำขอของคุณ โปรดลองอีกครั้ง",
    "vi": "⚠️ Đã xảy ra lỗi không mong muốn khi xử lý yêu cầu của bạn. Vui lòng thử lại.",
    "id": "⚠️ Terjadi kesalahan tak terduga saat memproses permintaan Anda. Silakan coba lagi.",
    "ms": "⚠️ Ralat tak dijangka berlaku semasa memproses permintaan anda. Sila cuba lagi.",
    "uk": "⚠️ Під час обробки вашого запиту сталася непередбачена помилка. Будь ласка, спробуйте ще раз.",
    "uz": "⚠️ So‘rovingizni qayta ishlashda kutilmagan xato yuz berdi. Iltimos, qaytadan urinib ko‘ring.",
    "zh-TW": "⚠️ 處理您的請求時發生意外錯誤。請再試一次。",
    "pt-PT": "⚠️ Ocorreu um erro inesperado ao processar o seu pedido. Por favor, tente novamente."
    },
    "analyzing_image": {
    "en": "Analyzing image... 🖼️✨",
    "es": "Analizando imagen... 🖼️✨",
    "fr": "Analyse de l'image... 🖼️✨",
    "kk": "Сурет талданып жатыр... 🖼️✨",
    "de": "Bild wird analysiert... 🖼️✨",
    "ru": "Анализ изображения... 🖼️✨",
    "zh-CN": "正在分析图像... 🖼️✨",
    "ja": "画像を解析中... 🖼️✨",
    "ko": "이미지 분석 중... 🖼️✨",
    "pt-BR": "Analisando imagem... 🖼️✨",
    "it": "Analisi dell'immagine in corso... 🖼️✨",
    "ar": "جارٍ تحليل الصورة... 🖼️✨",
    "hi": "छवि विश्लेषण हो रही है... 🖼️✨",
    "tr": "Görsel analiz ediliyor... 🖼️✨",
    "nl": "Afbeelding wordt geanalyseerd... 🖼️✨",
    "pl": "Analiza obrazu... 🖼️✨",
    "sv": "Analyserar bilden... 🖼️✨",
    "fi": "Analysoidaan kuvaa... 🖼️✨",
    "no": "Analyserer bilde... 🖼️✨",
    "da": "Analyzerer billede... 🖼️✨",
    "cs": "Analýza obrázku... 🖼️✨",
    "hu": "Kép elemzése... 🖼️✨",
    "ro": "Analizând imagine... 🖼️✨",
    "el": "Ανάλυση εικόνας... 🖼️✨",
    "he": "מנתח תמונה... 🖼️✨",
    "th": "กำลังวิเคราะห์ภาพ... 🖼️✨",
    "vi": "Đang phân tích hình ảnh... 🖼️✨",
    "id": "Menganalisis gambar... 🖼️✨",
    "ms": "Menganalisis imej... 🖼️✨",
    "uk": "Аналіз зображення... 🖼️✨",
    "uz": "Rasm tahlil qilinmoqda... 🖼️✨",
    "zh-TW": "正在分析圖片... 🖼️✨",
    "pt-PT": "Analisando imagem... 🖼️✨"
    },
    "gemini_vision_prompt_general": {
    "en": "Please analyze this image and its content (including any text or diagrams). Explain the key concepts, objects, or information present in the image. If it seems to be a problem or question, help me understand it and how to approach it. Act as a study helper.",
    "es": "Por favor, analiza esta imagen y su contenido (incluido cualquier texto o diagrama). Explica los conceptos clave, objetos o información presente. Si parece un problema o pregunta, ayúdame a entenderlo y cómo abordarlo. Actúa como un asistente de estudio.",
    "fr": "Veuillez analyser cette image et son contenu (y compris tout texte ou diagramme). Expliquez les concepts clés, objets ou informations présents. S'il s'agit d'un problème ou d'une question, aidez-moi à le comprendre et à l'aborder. Agissez comme un assistant d'étude.",
    "kk": "Осы суретті және оның мазмұнын (мәтін немесе диаграммалар) талдаңыз. Негізгі тұжырымдамалар мен объектілерді түсіндіріңіз. Мәселе немесе сұрақ сияқты көрінсе, мені түсінуге және оған қалай қарау керектігіне бағыттаңыз. Оқу көмекшісі ретінде әрекет етіңіз.",
    "de": "Bitte analysieren Sie dieses Bild und seinen Inhalt (einschließlich aller Texte oder Diagramme). Erklären Sie die Schlüsselkonzepte, Objekte oder Informationen im Bild. Wenn es sich um ein Problem oder eine Frage handelt, helfen Sie mir, es zu verstehen und anzugehen. Agieren Sie als Lernhelfer.",
    "ru": "Проанализируйте это изображение и его содержимое (включая текст или диаграммы). Объясните ключевые концепции, объекты или информацию. Если это задача или вопрос, помогите понять его и как к нему подойти. Выступите как помощник по учебе.",
    "zh-CN": "请分析此图像及其内容（包括任何文本或图表）。解释图像中的关键概念、对象或信息。如果它看起来是一个问题或题目，请帮助我理解并解决它。作为学习助手。",
    "ja": "この画像とその内容（テキストや図を含む）を分析してください。画像に含まれる重要な概念や物体、情報を説明してください。問題や質問のようであれば、それを理解し、どのように取り組むかを助けてください。学習のサポーターとして振る舞ってください。",
    "ko": "이 이미지와 그 내용(텍스트 또는 다이어그램 포함)을 분석해주세요. 이미지에 있는 주요 개념, 객체 또는 정보를 설명해주세요. 문제나 질문이라면 이해하고 접근하는 방법을 도와주세요. 학습 도우미 역할을 해주세요.",
    "pt-BR": "Por favor, analise esta imagem e seu conteúdo (incluindo qualquer texto ou diagrama). Explique os conceitos-chave, objetos ou informações presentes. Se parecer um problema ou pergunta, ajude-me a entendê-lo e como abordá-lo. Atue como um assistente de estudos.",
    "it": "Per favore analizza questa immagine e il suo contenuto (inclusi testo o diagrammi). Spiega i concetti chiave, oggetti o informazioni presenti. Se sembra essere un problema o una domanda, aiutami a comprenderla e come affrontarla. Agisci come un tutor di studio.",
    "ar": "يرجى تحليل هذه الصورة ومحتواها (بما في ذلك أي نص أو رسوم بيانية). شرح المفاهيم الرئيسية، الكائنات أو المعلومات الموجودة في الصورة. إذا بدا أنها مسألة أو سؤال، ساعدني على فهمها وكيفية الاقتراب منها. تصرف كمساعد دراسي.",
    "hi": "कृपया इस चित्र और इसकी सामग्री (किसी भी पाठ या आरेख सहित) का विश्लेषण करें। चित्र में मौजूद मुख्य अवधारणाओं, वस्तुओं या जानकारी को समझाएं। यदि यह एक समस्या या प्रश्न लगता है, तो मुझे इसे समझने और इससे कैसे निपटने में मदद करें। एक अध्ययन सहायक की तरह कार्य करें।",
    "tr": "Lütfen bu resmi ve içeriğini (herhangi bir metin veya diyagram da dahil) analiz edin. Görüntüdeki kilit kavramları, nesneleri veya bilgileri açıklayın. Eğer bir problem veya soru gibi görünüyorsa, anlamama ve nasıl yaklaşmama yardımcı olun. Bir çalışma yardımcısı gibi davranın.",
    "nl": "Analyseer alsjeblieft deze afbeelding en de inhoud ervan (inclusief tekst of diagrammen). Leg de kernconcepten, objecten of informatie in de afbeelding uit. Als het een probleem of vraag lijkt, help me het te begrijpen en hoe ik het moet aanpakken. Gedraag je als een studiemaat.",
    "pl": "Proszę przeanalizować ten obraz i jego zawartość (w tym teksty lub diagramy). Wyjaśnij kluczowe pojęcia, obiekty lub informacje zawarte na obrazie. Jeśli wydaje się to problemem lub pytaniem, pomóż mi go zrozumieć i podejść do niego. Zachowuj się jak pomocnik nauki.",
    "sv": "Vänligen analysera den här bilden och dess innehåll (inklusive text eller diagram). Förklara nyckelkoncepten, objekt eller information som finns i bilden. Om det verkar vara ett problem eller en fråga, hjälp mig att förstå det och hur jag ska närma mig det. Agera som en studiekamrat.",
    "fi": "Analysoi tämä kuva ja sen sisältö (mukaan lukien mahdollinen teksti tai kaaviot). Selitä kuvan keskeiset käsitteet, objektit tai tiedot. Jos se vaikuttaa ongelmalta tai kysymykseltä, auta minua ymmärtämään se ja miten lähestyä sitä. Toimi opiskeluavustajana.",
    "no": "Analyser dette bildet og innholdet (inkludert tekst eller diagrammer). Forklar nøkkelbegrepene, objektene eller informasjonen i bildet. Hvis det ser ut som et problem eller spørsmål, hjelp meg å forstå det og hvordan jeg skal angripe det. Oppfør deg som en studieveileder.",
    "da": "Analyser venligst dette billede og dets indhold (inklusive tekst eller diagrammer). Forklar nøglebegreberne, objekterne eller oplysningerne i billedet. Hvis det ser ud til at være et problem eller et spørgsmål, hjælp mig med at forstå det og hvordan jeg skal gribe det an. Opfør dig som en studievejleder.",
    "cs": "Prosím, analyzujte tento obrázek a jeho obsah (včetně textu nebo diagramů). Vysvětlete klíčové koncepty, objekty nebo informace na obrázku. Pokud se zdá, že jde o problém nebo otázku, pomozte mi pochopit ji a jak se k ní přiblížit. Chovejte se jako studijní pomocník.",
    "hu": "Kérlek elemezd ezt a képet és tartalmát (beleértve bármilyen szöveget vagy diagramot). Magyarázd el a kulcsfontosságú fogalmakat, tárgyakat vagy információkat a képen. Ha úgy tűnik, hogy ez egy feladat vagy kérdés, segíts megérteni és megközelíteni. Viselkedj tanulást segítőként.",
    "ro": "Vă rog analizați această imagine și conținutul său (inclusiv orice text sau diagrame). Explicați conceptele cheie, obiectele sau informațiile prezente. Dacă pare a fi o problemă sau o întrebare, ajutați-mă să o înțeleg și cum să o abordez. Acționați ca un ajutor de studiu.",
    "el": "Παρακαλώ αναλύστε αυτή την εικόνα και το περιεχόμενό της (συμπεριλαμβανομένου οποιουδήποτε κειμένου ή διαγραμμάτων). Εξηγήστε τις βασικές έννοιες, αντικείμενα ή πληροφορίες στην εικόνα. Αν μοιάζει με πρόβλημα ή ερώτηση, βοηθήστε με να το κατανοήσω και πώς να το προσεγγίσω. Λειτουργήστε ως βοηθός μελέτης.",
    "he": "אנא נתח/י את התמונה ותוכנה (כולל כל טקסט או משלב). הסבר/י את המושגים המרכזיים, העצמים או המידע המופיעים בתמונה. אם זה נראה כבעיה או שאלה, עזור/י לי להבין איך לגשת לזה. תפעל/י כעוזר/ת לימודים.",
    "th": "โปรดวิเคราะห์ภาพนี้และเนื้อหาของมัน (รวมถึงข้อความหรือแผนภาพใดๆ) อธิบายแนวคิดสำคัญ วัตถุ หรือข้อมูลที่ปรากฏ หากดูเหมือนจะเป็นโจทย์หรือคำถาม ให้ช่วยฉันเข้าใจและวิธีการแก้ไข ทำหน้าที่เป็นผู้ช่วยเรียน",
    "vi": "Vui lòng phân tích hình ảnh này và nội dung của nó (bao gồm bất kỳ văn bản hoặc sơ đồ nào). Giải thích các khái niệm chính, đối tượng hoặc thông tin có trong hình. Nếu nó giống như một vấn đề hoặc câu hỏi, hãy giúp tôi hiểu và cách tiếp cận nó. Hãy đóng vai trò là trợ lý học tập.",
    "id": "Tolong analisis gambar ini dan isinya (termasuk teks atau diagram apa pun). Jelaskan konsep utama, objek, atau informasi dalam gambar. Jika tampaknya sebuah masalah atau pertanyaan, bantu saya memahaminya dan cara mendekatinya. Bertindaklah sebagai asisten belajar.",
    "ms": "Sila analisis imej ini dan kandungannya (termasuk mana-mana teks atau rajah). Terangkan konsep utama, objek atau maklumat dalam imej. Jika ia kelihatan seperti masalah atau soalan, bantu saya memahaminya dan bagaimana untuk mendekatinya. Bertindak sebagai pembantu belajar.",
    "uk": "Будь ласка, проаналізуйте це зображення та його вміст (включаючи текст або діаграми). Поясніть ключові концепції, об’єкти чи інформацію, присутні на зображенні. Якщо це схоже на задачу чи запитання, допоможіть мені зрозуміти й як до неї підійти. Поводьтеся як навчальний помічник.",
    "uz": "Iltimos, ushbu rasm va uning mazmunini (matn yoki diagrammalarni o‘z ichiga olgan holda) tahlil qiling. Rasmda mavjud asosiy tushunchalar, ob'ektlar yoki ma'lumotlarni tushuntiring. Agar bu masala yoki savolga o‘xshasa, uni tushunishga va unga qanday yondashishga yordam bering. O‘quv yordamchisi sifatida harakat qiling.",
    "zh-TW": "請分析這張圖片及其內容（包括任何文字或圖表）。解釋圖中的關鍵概念、物件或資訊。如果它看起來是一個題目或問題，請幫助我理解並該如何處理。扮演學習助手。",
    "pt-PT": "Por favor, analisa esta imagem e o seu conteúdo (incluindo texto ou diagramas). Explica os conceitos-chave, objetos ou informações presentes na imagem. Se parecer um problema ou pergunta, ajuda-me a compreendê-lo e como abordá-lo. Age como um assistente de estudo."
    },
    "unidentified_image_error": {
    "en": "⚠️ Could not identify the image format. Please try a common format like JPEG or PNG.",
    "es": "⚠️ No se pudo identificar el formato de la imagen. Por favor, use un formato común como JPEG o PNG.",
    "fr": "⚠️ Impossible d’identifier le format de l’image. Veuillez essayer un format courant comme JPEG ou PNG.",
    "kk": "⚠️ Сурет формат анықталмады. JPEG немесе PNG секілді форматты қолданып көріңіз.",
    "de": "⚠️ Bildformat konnte nicht erkannt werden. Bitte versuchen Sie ein gängiges Format wie JPEG oder PNG.",
    "ru": "⚠️ Не удалось определить формат изображения. Пожалуйста, попробуйте распространённый формат, например JPEG или PNG.",
    "zh-CN": "⚠️ 无法识别图像格式。请尝试常见格式，如 JPEG 或 PNG。",
    "ja": "⚠️ 画像の形式を特定できませんでした。JPEGやPNGなどの一般的な形式を試してください。",
    "ko": "⚠️ 이미지 형식을 식별할 수 없습니다. JPEG 또는 PNG 같은 일반 형식을 사용해 주세요.",
    "pt-BR": "⚠️ Não foi possível identificar o formato da imagem. Tente um formato comum, como JPEG ou PNG.",
    "it": "⚠️ Impossibile identificare il formato dell’immagine. Si prega di provare un formato comune come JPEG o PNG.",
    "ar": "⚠️ لم يتم التعرف على تنسيق الصورة. يرجى تجربة تنسيق شائع مثل JPEG أو PNG.",
    "hi": "⚠️ छवि फ़ॉर्मेट पहचानने में असमर्थ। कृपया JPEG या PNG जैसे सामान्य फॉर्मेट में पुनः प्रयास करें।",
    "tr": "⚠️ Resim formatı tanınamadı. Lütfen JPEG veya PNG gibi yaygın bir formatı deneyin.",
    "nl": "⚠️ Kon het afbeeldingsformaat niet identificeren. Probeer een gangbaar formaat zoals JPEG of PNG.",
    "pl": "⚠️ Nie można rozpoznać formatu obrazu. Proszę spróbować popularnego formatu, np. JPEG lub PNG.",
    "sv": "⚠️ Kunde inte identifiera bildformatet. Försök med ett vanligt format som JPEG eller PNG.",
    "fi": "⚠️ Ei voitu tunnistaa kuvatiedoston muotoa. Kokeile yleistä muotoa kuten JPEG tai PNG.",
    "no": "⚠️ Kunne ikke identifisere bildeformat. Vennligst prøv et vanlig format som JPEG eller PNG.",
    "da": "⚠️ Kunne ikke identificere billedformatet. Prøv et almindeligt format som JPEG eller PNG.",
    "cs": "⚠️ Nepodařilo se rozpoznat formát obrázku. Zkuste běžný formát jako JPEG nebo PNG.",
    "hu": "⚠️ Nem sikerült azonosítani a kép formátumát. Próbálj meg egy általános formátumot, mint a JPEG vagy PNG.",
    "ro": "⚠️ Nu s‑a putut identifica formatul imaginii. Vă rugăm să încercați un format comun precum JPEG sau PNG.",
    "el": "⚠️ Δεν ήταν δυνατή η αναγνώριση της μορφής εικόνας. Δοκιμάστε μια κοινή μορφή όπως JPEG ή PNG.",
    "he": "⚠️ לא ניתן לזהות את פורמט התמונה. אנא נסה פורמט נפוץ כמו JPEG או PNG.",
    "th": "⚠️ ไม่สามารถระบุรูปแบบภาพได้ โปรดลองใช้รูปแบบทั่วไป เช่น JPEG หรือ PNG",
    "vi": "⚠️ Không thể xác định định dạng hình ảnh. Vui lòng thử định dạng phổ biến như JPEG hoặc PNG.",
    "id": "⚠️ Tidak dapat mengidentifikasi format gambar. Silakan coba format umum seperti JPEG atau PNG.",
    "ms": "⚠️ Tidak dapat mengenal pasti format imej. Sila cuba format biasa seperti JPEG atau PNG.",
    "uk": "⚠️ Не вдалося визначити формат зображення. Будь ласка, спробуйте поширений формат, як-от JPEG або PNG.",
    "uz": "⚠️ Rasm formatini aniqlab bo‘lmadi. Iltimos, JPEG yoki PNG kabi keng tarqalgan formatni urinib ko‘ring.",
    "zh-TW": "⚠️ 無法識別影像格式。請嘗試常見格式，如 JPEG 或 PNG。",
    "pt-PT": "⚠️ Não foi possível identificar o formato da imagem. Por favor, tente um formato comum como JPEG ou PNG."
    },
    "unexpected_image_error": {
    "en": "⚠️ An unexpected error occurred while analyzing the image.",
    "es": "⚠️ Ocurrió un error inesperado al analizar la imagen.",
    "fr": "⚠️ Une erreur inattendue s'est produite lors de l'analyse de l'image.",
    "kk": "⚠️ Суретті талдау кезінде күтпеген қате пайда болды.",
    "de": "⚠️ Beim Analysieren des Bildes ist ein unerwarteter Fehler aufgetreten.",
    "ru": "⚠️ При анализе изображения произошла непредвиденная ошибка.",
    "zh-CN": "⚠️ 分析图像时发生意外错误。",
    "ja": "⚠️ 画像の解析中に予期せぬエラーが発生しました。",
    "ko": "⚠️ 이미지를 분석하는 동안 예기치 않은 오류가 발생했습니다.",
    "pt-BR": "⚠️ Ocorreu um erro inesperado ao analisar a imagem.",
    "it": "⚠️ Si è verificato un errore imprevisto durante l'analisi dell'immagine.",
    "ar": "⚠️ حدث خطأ غير متوقع أثناء تحليل الصورة.",
    "hi": "⚠️ छवि का विश्लेषण करते समय एक अप्रत्याशित त्रुटि हुई।",
    "tr": "⚠️ Görsel analiz edilirken beklenmeyen bir hata oluştu.",
    "nl": "⚠️ Er is een onverwachte fout opgetreden bij het analyseren van de afbeelding.",
    "pl": "⚠️ Wystąpił nieoczekiwany błąd podczas analizy obrazu.",
    "sv": "⚠️ Ett oväntat fel uppstod vid analys av bilden.",
    "fi": "⚠️ Yllätyksellinen virhe esiintyi kuvan analysoinnissa.",
    "no": "⚠️ En uventet feil oppstod under analyse av bildet.",
    "da": "⚠️ En uventet fejl opstod under analysen af billedet.",
    "cs": "⚠️ Při analýze obrázku došlo k neočekávané chybě.",
    "hu": "⚠️ Kép elemzése közben váratlan hiba történt.",
    "ro": "⚠️ A apărut o eroare neașteptată în timpul analizei imaginii.",
    "el": "⚠️ Παρουσιάστηκε ένα απρόσμενο σφάλμα κατά την ανάλυση της εικόνας.",
    "he": "⚠️ ארעה שגיאה לא צפויה בעת ניתוח התמונה.",
    "th": "⚠️ เกิดข้อผิดพลาดที่ไม่คาดคิดขณะวิเคราะห์ภาพ",
    "vi": "⚠️ Đã xảy ra lỗi không mong muốn khi phân tích hình ảnh.",
    "id": "⚠️ Terjadi kesalahan tak terduga saat menganalisis gambar.",
    "ms": "⚠️ Ralat tak dijangka berlaku semasa menganalisis imej.",
    "uk": "⚠️ Під час аналізу зображення сталася непередбачена помилка.",
    "uz": "⚠️ Rasmni tahlil qilishda kutilmagan xato yuz berdi.",
    "zh-TW": "⚠️ 分析影像時發生意外錯誤。",
    "pt-PT": "⚠️ Ocorreu um erro inesperado ao analisar a imagem."
    },
    "download_failed_error": {
      "en": "⚠️ Sorry, I couldn't download the file '{file_name}'. Please try again or check the file.",
      "es": "⚠️ Lo siento, no pude descargar el archivo '{file_name}'. Inténtalo de nuevo o verifica el archivo.",
      "fr": "⚠️ Désolé, je n'ai pas pu télécharger le fichier '{file_name}'. Veuillez réessayer ou vérifier le fichier.",
      "kk": "⚠️ Кешіріңіз, '{file_name}' файлын жүктей алмадым. Қайта көріңіз немесе файлды тексеріңіз.",
      "de": "⚠️ Entschuldigung, ich konnte die Datei '{file_name}' nicht herunterladen. Bitte versuchen Sie es erneut oder überprüfen Sie die Datei.",
      "ru": "⚠️ Извините, не удалось скачать файл '{file_name}'. Пожалуйста, попробуйте ещё раз или проверьте файл.",
      "zh-CN": "⚠️ 抱歉，我无法下载文件“{file_name}”。请重试或检查文件。",
      "ja": "⚠️ 申し訳ありませんが、ファイル「{file_name}」をダウンロードできませんでした。もう一度お試しいただくか、ファイルをご確認ください。",
      "ko": "⚠️ 죄송합니다. 파일 '{file_name}'을(를) 다운로드할 수 없습니다. 다시 시도하거나 파일을 확인하세요.",
      "pt-BR": "⚠️ Desculpe, não consegui baixar o arquivo '{file_name}'. Tente novamente ou verifique o arquivo.",
      "it": "⚠️ Mi dispiace, non sono riuscito a scaricare il file '{file_name}'. Riprova o controlla il file.",
      "ar": "⚠️ عذرًا، لم أتمكن من تنزيل الملف '{file_name}'. يرجى المحاولة مرة أخرى أو التحقق من الملف.",
      "hi": "⚠️ क्षमा करें, मैं फ़ाइल '{file_name}' डाउनलोड नहीं कर सका। कृपया पुनः प्रयास करें या फ़ाइल की जाँच करें।",
      "tr": "⚠️ Üzgünüm, '{file_name}' dosyasını indiremedim. Lütfen tekrar deneyin veya dosyayı kontrol edin.",
      "nl": "⚠️ Sorry, ik kon het bestand '{file_name}' niet downloaden. Probeer het opnieuw of controleer het bestand.",
      "pl": "⚠️ Przepraszam, nie udało mi się pobrać pliku '{file_name}'. Spróbuj ponownie lub sprawdź plik.",
      "sv": "⚠️ Tyvärr kunde jag inte ladda ner filen '{file_name}'. Försök igen eller kontrollera filen.",
      "fi": "⚠️ Pahoittelut, en voinut ladata tiedostoa '{file_name}'. Yritä uudelleen tai tarkista tiedosto.",
      "no": "⚠️ Beklager, jeg kunne ikke laste ned filen '{file_name}'. Prøv igjen eller sjekk filen.",
      "da": "⚠️ Beklager, jeg kunne ikke downloade filen '{file_name}'. Prøv igen eller tjek filen.",
      "cs": "⚠️ Promiňte, nepodařilo se mi stáhnout soubor '{file_name}'. Zkuste to prosím znovu nebo zkontrolujte soubor.",
      "hu": "⚠️ Sajnálom, nem tudtam letölteni a(z) '{file_name}' fájlt. Próbáld újra vagy ellenőrizd a fájlt.",
      "ro": "⚠️ Ne pare rău, nu am putut descărca fișierul '{file_name}'. Încercați din nou sau verificați fișierul.",
      "el": "⚠️ Συγγνώμη, δεν μπόρεσα να κατεβάσω το αρχείο '{file_name}'. Δοκιμάστε ξανά ή ελέγξτε το αρχείο.",
      "he": "⚠️ מצטער, לא הצלחתי להוריד את הקובץ '{file_name}'. נסה שוב או בדוק את הקובץ.",
      "th": "⚠️ ขอโทษค่ะ ไม่สามารถดาวน์โหลดไฟล์ '{file_name}' ได้ กรุณาลองใหม่หรือตรวจสอบไฟล์",
      "vi": "⚠️ Rất tiếc, tôi không thể tải tệp '{file_name}'. Vui lòng thử lại hoặc kiểm tra tệp.",
      "id": "⚠️ Maaf, saya tidak dapat mengunduh file '{file_name}'. Silakan coba lagi atau periksa file-nya.",
      "ms": "⚠️ Maaf, saya tidak dapat memuat turun fail '{file_name}'. Sila cuba lagi atau semak fail itu.",
      "uk": "⚠️ Вибачте, не вдалося завантажити файл '{file_name}'. Спробуйте ще раз або перевірте файл.",
      "uz": "⚠️ Kechirasiz, '{file_name}' faylini yuklab olib bo‘lmadi. Iltimos, qaytadan urinib ko‘ring yoki faylni tekshiring.",
      "zh-TW": "⚠️ 抱歉，我無法下載檔案「{file_name}」。請再試一次或檢查檔案。",
      "pt-PT": "⚠️ Lamento, não consegui descarregar o ficheiro '{file_name}'. Por favor, tente novamente ou verifique o ficheiro."
    },
    "unsupported_document_type": {
        "en": "⚠️ Sorry, I can't process this document type: {file_type}. I can handle PDF, DOCX, and TXT files.",
        "es": "⚠️ Lo siento, no puedo procesar este tipo de documento: {file_type}. Puedo manejar archivos PDF, DOCX y TXT.",
        "fr": "⚠️ Désolé, je ne peux pas traiter ce type de document : {file_type}. Je peux gérer les fichiers PDF, DOCX et TXT.",
        "kk": "⚠️ Кешіріңіз, мен {file_type} құжатын өңдей алмаймын. Мен PDF, DOCX және TXT файлдарын өңдей аламын.",
        "de": "⚠️ Entschuldigung, ich kann diesen Dokumenttyp nicht verarbeiten: {file_type}. Ich kann PDF-, DOCX- und TXT-Dateien verarbeiten.",
        "ru": "⚠️ Извините, я не могу обработать тип документа: {file_type}. Я могу обрабатывать PDF, DOCX и TXT файлы.",
        "zh-CN": "⚠️ 抱歉，我无法处理此文档类型：{file_type}。我可以处理 PDF、DOCX 和 TXT 文件。",
        "ja": "⚠️ 申し訳ありませんが、このドキュメントタイプは処理できません: {file_type}。PDF、DOCX、TXT ファイルを処理できます。",
        "ko": "⚠️ 죄송합니다. 이 문서 유형은 처리할 수 없습니다: {file_type}. PDF, DOCX, TXT 파일을 처리할 수 있습니다.",
        "pt-BR": "⚠️ Desculpe, não consigo processar este tipo de documento: {file_type}. Posso lidar com arquivos PDF, DOCX e TXT.",
        "it": "⚠️ Mi dispiace, non posso elaborare questo tipo di documento: {file_type}. Posso gestire file PDF, DOCX e TXT.",
        "ar": "⚠️ عذرًا، لا يمكنني معالجة هذا النوع من المستندات: {file_type}. يمكنني معالجة ملفات PDF و DOCX و TXT.",
        "hi": "⚠️ क्षमा करें, मैं इस दस्तावेज़ प्रकार को संसाधित नहीं कर सकता: {file_type}। मैं PDF, DOCX और TXT फ़ाइलों को संसाधित कर सकता हूँ।",
        "tr": "⚠️ Üzgünüm, bu belge türünü işleyemiyorum: {file_type}. PDF, DOCX ve TXT dosyalarını işleyebilirim.",
        "nl": "⚠️ Sorry, ik kan dit documenttype niet verwerken: {file_type}. Ik kan PDF-, DOCX- en TXT-bestanden verwerken.",
        "pl": "⚠️ Przepraszam, nie mogę przetworzyć tego typu dokumentu: {file_type}. Obsługuję pliki PDF, DOCX i TXT.",
        "sv": "⚠️ Tyvärr, jag kan inte bearbeta denna dokumenttyp: {file_type}. Jag kan hantera PDF-, DOCX- och TXT-filer.",
        "fi": "⚠️ Valitettavasti en voi käsitellä tätä asiakirjatyyppiä: {file_type}. Voin käsitellä PDF-, DOCX- ja TXT-tiedostoja.",
        "no": "⚠️ Beklager, jeg kan ikke behandle denne dokumenttypen: {file_type}. Jeg kan håndtere PDF-, DOCX- og TXT-filer.",
        "da": "⚠️ Beklager, jeg kan ikke behandle denne dokumenttype: {file_type}. Jeg kan håndtere PDF-, DOCX- og TXT-filer.",
        "cs": "⚠️ Omlouvám se, tento typ dokumentu nemohu zpracovat: {file_type}. Mohu pracovat se soubory PDF, DOCX a TXT.",
        "hu": "⚠️ Sajnálom, nem tudom feldolgozni ezt a dokumentumtípust: {file_type}. Kezelek PDF, DOCX és TXT fájlokat.",
        "ro": "⚠️ Ne pare rău, nu pot procesa acest tip de document: {file_type}. Pot procesa fișiere PDF, DOCX și TXT.",
        "el": "⚠️ Συγγνώμη, δεν μπορώ να επεξεργαστώ αυτόν τον τύπο εγγράφου: {file_type}. Μπορώ να επεξεργαστώ αρχεία PDF, DOCX και TXT.",
        "he": "⚠️ מצטער, איני יכול לעבד סוג מסמך זה: {file_type}. אני יכול לטפל בקבצי PDF, DOCX ו-TXT.",
        "th": "⚠️ ขอโทษค่ะ ฉันไม่สามารถประมวลผลประเภทเอกสารนี้ได้: {file_type} ฉันสามารถจัดการไฟล์ PDF, DOCX และ TXT ได้",
        "vi": "⚠️ Rất tiếc, tôi không thể xử lý loại tài liệu này: {file_type}. Tôi có thể xử lý các tệp PDF, DOCX và TXT.",
        "id": "⚠️ Maaf, saya tidak dapat memproses jenis dokumen ini: {file_type}. Saya dapat menangani file PDF, DOCX, dan TXT.",
        "ms": "⚠️ Maaf, saya tidak dapat memproses jenis dokumen ini: {file_type}. Saya boleh mengendalikan fail PDF, DOCX dan TXT.",
        "uk": "⚠️ Вибачте, я не можу обробити цей тип документа: {file_type}. Я можу працювати з файлами PDF, DOCX і TXT.",
        "uz": "⚠️ Kechirasiz, ushbu hujjat turini qayta ishlay olmayman: {file_type}. Men PDF, DOCX va TXT fayllarini qayta ishlashim mumkin.",
        "zh-TW": "⚠️ 抱歉，我無法處理此文件類型：{file_type}。我可以處理 PDF、DOCX 和 TXT 文件。",
        "pt-PT": "⚠️ Lamento, não consigo processar este tipo de documento: {file_type}. Consigo lidar com ficheiros PDF, DOCX e TXT."
    },
    "no_text_in_document": {
        "en": "ℹ️ I couldn't find any text to extract from the document: {file_name}.",
        "es": "ℹ️ No pude encontrar texto para extraer del documento: {file_name}.",
        "fr": "ℹ️ Je n'ai trouvé aucun texte à extraire du document : {file_name}.",
        "kk": "ℹ️ Құжаттан мәтін табылмады: {file_name}.",
        "de": "ℹ️ Ich konnte keinen Text im Dokument finden: {file_name}.",
        "ru": "ℹ️ Не удалось найти текст в документе: {file_name}.",
        "zh-CN": "ℹ️ 无法从文档中提取任何文本: {file_name}。",
        "ja": "ℹ️ ドキュメントから抽出できるテキストが見つかりませんでした: {file_name}。",
        "ko": "ℹ️ 문서에서 추출할 텍스트를 찾을 수 없습니다: {file_name}.",
        "pt-BR": "ℹ️ Não consegui encontrar texto para extrair do documento: {file_name}.",
        "it": "ℹ️ Nessun testo trovato da estrarre dal documento: {file_name}.",
        "ar": "ℹ️ لم أتمكن من العثور على نص لاستخراجه من المستند: {file_name}.",
        "hi": "ℹ️ दस्तावेज़ से कोई भी टेक्स्ट निकालने के लिए नहीं मिला: {file_name}।",
        "tr": "ℹ️ Belgede çıkarılacak metin bulunamadı: {file_name}.",
        "nl": "ℹ️ Geen tekst gevonden om uit het document te extraheren: {file_name}.",
        "pl": "ℹ️ Nie znaleziono tekstu do wyodrębnienia z dokumentu: {file_name}.",
        "sv": "ℹ️ Kunde inte hitta någon text att extrahera från dokumentet: {file_name}.",
        "fi": "ℹ️ En löytänyt asiakirjasta tekstiä, jota voisi poimia: {file_name}.",
        "no": "ℹ️ Fant ingen tekst å hente ut fra dokumentet: {file_name}.",
        "da": "ℹ️ Kunne ikke finde nogen tekst at udtrække fra dokumentet: {file_name}.",
        "cs": "ℹ️ Nepodařilo se najít žádný text k extrakci z dokumentu: {file_name}.",
        "hu": "ℹ️ Nem találtam szöveget a dokumentumban: {file_name}.",
        "ro": "ℹ️ Nu am găsit niciun text de extras din document: {file_name}.",
        "el": "ℹ️ Δεν βρέθηκε κείμενο για εξαγωγή από το έγγραφο: {file_name}.",
        "he": "ℹ️ לא נמצא טקסט לחילוץ מהמסמך: {file_name}.",
        "th": "ℹ️ ไม่พบข้อความที่สามารถดึงออกจากเอกสาร: {file_name}.",
        "vi": "ℹ️ Không tìm thấy văn bản nào để trích xuất từ tài liệu: {file_name}.",
        "id": "ℹ️ Tidak menemukan teks untuk diekstrak dari dokumen: {file_name}.",
        "ms": "ℹ️ Tidak menemui teks untuk diekstrak daripada dokumen: {file_name}.",
        "uk": "ℹ️ Не вдалося знайти текст для вилучення з документа: {file_name}.",
        "uz": "ℹ️ Hujjatdan chiqariladigan matn topilmadi: {file_name}.",
        "zh-TW": "ℹ️ 找不到可從文件中提取的文字: {file_name}。",
        "pt-PT": "ℹ️ Não foi possível encontrar texto para extrair do documento: {file_name}."
      },
    "extracted_text_snippet_info": {
        "en": "Extracted text from '{file_name}' (approx. {chars_count} characters shown):",
        "es": "Texto extraído de '{file_name}' (aproximadamente {chars_count} caracteres mostrados):",
        "fr": "Texte extrait de '{file_name}' (environ {chars_count} caractères affichés):",
        "kk": "'{file_name}' құжатынан алынған мәтін (шамамен {chars_count} таңба көрсетілген):",
        "de": "Extrahierter Text aus '{file_name}' (ca. {chars_count} Zeichen angezeigt):",
        "ru": "Извлечённый текст из '{file_name}' (показано приблизительно {chars_count} символов):",
        "zh-CN": "从 '{file_name}' 中提取的文本（显示约 {chars_count} 个字符）：",
        "ja": "'{file_name}' から抽出されたテキスト（約 {chars_count} 文字を表示）：",
        "ko": "'{file_name}'에서 추출한 텍스트 (약 {chars_count}자 표시됨):",
        "pt-BR": "Texto extraído de '{file_name}' (aproximadamente {chars_count} caracteres exibidos):",
        "it": "Testo estratto da '{file_name}' (circa {chars_count} caratteri mostrati):",
        "ar": "النص المستخرج من '{file_name}' (تم عرض حوالي {chars_count} حرفًا):",
        "hi": "'{file_name}' से निकाला गया पाठ (लगभग {chars_count} वर्ण दिखाए गए):",
        "tr": "'{file_name}' dosyasından çıkarılan metin (yaklaşık {chars_count} karakter gösterildi):",
        "nl": "Geëxtraheerde tekst uit '{file_name}' (ongeveer {chars_count} tekens weergegeven):",
        "pl": "Wydobyty tekst z '{file_name}' (około {chars_count} znaków pokazanych):",
        "sv": "Extraherad text från '{file_name}' (ungefär {chars_count} tecken visade):",
        "fi": "Poimittu teksti tiedostosta '{file_name}' (noin {chars_count} merkkiä näytetty):",
        "no": "Ekstrahert tekst fra '{file_name}' (ca. {chars_count} tegn vist):",
        "da": "Udtrukket tekst fra '{file_name}' (ca. {chars_count} tegn vist):",
        "cs": "Extrahovaný text z '{file_name}' (zobrazeno přibližně {chars_count} znaků):",
        "hu": "Kinyert szöveg a(z) '{file_name}' fájlból (kb. {chars_count} karakter megjelenítve):",
        "ro": "Text extras din '{file_name}' (aproximativ {chars_count} caractere afișate):",
        "el": "Εξαγόμενο κείμενο από το '{file_name}' (περίπου {chars_count} χαρακτήρες εμφανίζονται):",
        "he": "טקסט שחולץ מתוך '{file_name}' (כ- {chars_count} תווים מוצגים):",
        "th": "ข้อความที่ดึงมาจาก '{file_name}' (แสดงประมาณ {chars_count} ตัวอักษร):",
        "vi": "Văn bản được trích xuất từ '{file_name}' (khoảng {chars_count} ký tự được hiển thị):",
        "id": "Teks yang diekstrak dari '{file_name}' (sekitar {chars_count} karakter ditampilkan):",
        "ms": "Teks yang diekstrak daripada '{file_name}' (lebih kurang {chars_count} aksara dipaparkan):",
        "uk": "Витягнутий текст з '{file_name}' (приблизно {chars_count} символів показано):",
        "uz": "'{file_name}' faylidan ajratib olingan matn (taxminan {chars_count} ta belgi ko‘rsatilgan):",
        "zh-TW": "從 '{file_name}' 中擷取的文字（顯示約 {chars_count} 個字元）：",
        "pt-PT": "Texto extraído de '{file_name}' (cerca de {chars_count} caracteres mostrados):"
    },
    "asking_ai_analysis": {
        "en": "Asking AI for analysis... 🤖",
        "es": "Solicitando análisis a la IA... 🤖",
        "fr": "Demande d'analyse à l'IA... 🤖",
        "kk": "AI-ден талдау сұралуда... 🤖",
        "de": "Frage die KI nach einer Analyse... 🤖",
        "ru": "Запрос анализа у ИИ... 🤖",
        "zh-CN": "请求 AI 进行分析... 🤖",
        "ja": "AI に分析を依頼中... 🤖",
        "ko": "AI에게 분석 요청 중... 🤖",
        "pt-BR": "Solicitando análise à IA... 🤖",
        "it": "Richiesta analisi all'IA... 🤖",
        "ar": "طلب التحليل من الذكاء الاصطناعي... 🤖",
        "hi": "AI से विश्लेषण के लिए पूछ रहे हैं... 🤖",
        "tr": "Yapay zekadan analiz isteniyor... 🤖",
        "nl": "Vraag AI om analyse... 🤖",
        "pl": "Prośba o analizę przez AI... 🤖",
        "sv": "Ber AI om analys... 🤖",
        "fi": "Pyydetään tekoälyltä analyysiä... 🤖",
        "no": "Ber AI om analyse... 🤖",
        "da": "Beder AI om analyse... 🤖",
        "cs": "Žádost o analýzu od AI... 🤖",
        "hu": "Elemzést kérünk az MI-től... 🤖",
        "ro": "Cerere de analiză AI... 🤖",
        "el": "Αίτηση για ανάλυση από την ΤΝ... 🤖",
        "he": "מבקש ניתוח מה-AI... 🤖",
        "th": "ขอการวิเคราะห์จาก AI... 🤖",
        "vi": "Yêu cầu AI phân tích... 🤖",
        "id": "Meminta analisis dari AI... 🤖",
        "ms": "Meminta analisis dari AI... 🤖",
        "uk": "Запит на аналіз у ШІ... 🤖",
        "uz": "AI’dan tahlil so‘ralmoqda... 🤖",
        "zh-TW": "請求 AI 進行分析... 🤖",
        "pt-PT": "A pedir análise à IA... 🤖"
    },
    "gemini_document_analysis_prompt": {
        "en": "The user has uploaded a document named '{file_name}'. Here is the text content extracted from it. Please act as an AI Study Helper: analyze this text, explain key concepts, summarize it, or answer potential questions a student might have about it. Prioritize correctness and clarity.\n\nExtracted Text:\n---\n{extracted_content}\n---",
        "es": "El usuario ha subido un documento llamado '{file_name}'. Aquí está el contenido de texto extraído de él. Por favor, actúa como un Ayudante de Estudio AI: analiza este texto, explica conceptos clave, resúmelo o responde preguntas potenciales que un estudiante podría tener al respecto. Prioriza la corrección y la claridad.\n\nTexto Extraído:\n---\n{extracted_content}\n---",
        "fr": "L'utilisateur a téléchargé un document nommé '{file_name}'. Voici le contenu textuel qui en a été extrait. Veuillez agir en tant qu'Assistant d'Étude IA : analysez ce texte, expliquez les concepts clés, résumez-le ou répondez aux questions potentielles qu'un étudiant pourrait avoir à ce sujet. Donnez la priorité à l'exactitude et à la clarté.\n\nTexte Extrait :\n---\n{extracted_content}\n---",
        "kk": "Пайдаланушы '{file_name}' атты құжатты жүктеді. Міне, одан алынған мәтін мазмұны. AI Оқу Жәрдемшісі ретінде әрекет етіңіз: осы мәтінді талдаңыз, негізгі ұғымдарды түсіндіріңіз, оны қысқаша мазмұндаңыз немесе студенттің ол туралы болуы мүмкін ықтимал сұрақтарына жауап беріңіз. Дұрыстық пен түсініктілікке басымдық беріңіз.\n\nАлынған мәтін:\n---\n{extracted_content}\n---",
        "de": "Der Benutzer hat ein Dokument namens '{file_name}' hochgeladen. Hier ist der daraus extrahierte Textinhalt. Bitte agiere als KI-Lernassistent: Analysiere diesen Text, erkläre Schlüsselkonzepte, fasse ihn zusammen oder beantworte potenzielle Fragen, die ein Student dazu haben könnte. Priorisiere Korrektheit und Klarheit.\n\nExtrahierter Text:\n---\n{extracted_content}\n---",
        "ru": "Пользователь загрузил документ с именем '{file_name}'. Вот извлеченное из него текстовое содержимое. Пожалуйста, выступите в роли Помощника по учебе с ИИ: проанализируйте этот текст, объясните ключевые понятия, резюмируйте его или ответьте на потенциальные вопросы, которые могут возникнуть у студента по этому поводу. Приоритет – правильность и ясность.\n\nИзвлеченный текст:\n---\n{extracted_content}\n---",
        "zh-CN": "用户上传了一个名为“{file_name}”的文档。这是从中提取的文本内容。请扮演 AI 学习助手的角色：分析此文本，解释关键概念，对其进行总结，或回答学生可能对此提出的潜在问题。请优先考虑正确性和清晰度。\n\n提取文本：\n---\n{extracted_content}\n---",
        "ja": "ユーザーが「{file_name}」という名前のドキュメントをアップロードしました。これがそこから抽出されたテキストコンテンツです。AI学習アシスタントとして行動してください：このテキストを分析し、主要な概念を説明し、要約し、または学生がそれについて持つ可能性のある潜在的な質問に答えてください。正確さと明確さを優先してください。\n\n抽出されたテキスト：\n---\n{extracted_content}\n---",
        "ko": "사용자가 '{file_name}'라는 이름의 문서를 업로드했습니다. 다음은 문서에서 추출한 텍스트 내용입니다. AI 학습 도우미 역할을 해주세요: 이 텍스트를 분석하고, 주요 개념을 설명하고, 요약하거나, 학생이 가질 수 있는 잠재적인 질문에 답해주세요. 정확성과 명확성을 우선시해주세요.\n\n추출된 텍스트:\n---\n{extracted_content}\n---",
        "pt-BR": "O usuário carregou um documento chamado '{file_name}'. Aqui está o conteúdo textual extraído dele. Por favor, atue como um Assistente de Estudos de IA: analise este texto, explique conceitos-chave, resuma-o ou responda a perguntas potenciais que um estudante possa ter sobre ele. Priorize a correção e a clareza.\n\nTexto Extraído:\n---\n{extracted_content}\n---",
        "it": "L'utente ha caricato un documento denominato '{file_name}'. Ecco il contenuto testuale estratto da esso. Ti preghiamo di agire come Assistente di Studio AI: analizza questo testo, spiega i concetti chiave, riassumilo o rispondi a potenziali domande che uno studente potrebbe avere al riguardo. Dai priorità alla correttezza e alla chiarezza.\n\nTesto Estratto:\n---\n{extracted_content}\n---",
        "ar": "قام المستخدم بتحميل مستند باسم '{file_name}'. هذا هو محتوى النص المستخرج منه. يرجى التصرف كمساعد دراسة ذكاء اصطناعي: قم بتحليل هذا النص، وشرح المفاهيم الأساسية، وتلخيصه، أو الإجابة على الأسئلة المحتملة التي قد تكون لدى الطالب حوله. أعط الأولوية للصحة والوضوح.\n\nالنص المستخرج:\n---\n{extracted_content}\n---",
        "hi": "उपयोगकर्ता ने '{file_name}' नामक एक दस्तावेज़ अपलोड किया है। इससे निकाला गया पाठ यहाँ है। कृपया एक एआई अध्ययन सहायक के रूप में कार्य करें: इस पाठ का विश्लेषण करें, मुख्य अवधारणाओं को समझाएं, इसे सारांशित करें, या एक छात्र के इसके बारे में संभावित प्रश्नों का उत्तर दें। शुद्धता और स्पष्टता को प्राथमिकता दें।\n\nनिकाला गया पाठ:\n---\n{extracted_content}\n---",
        "tr": "Kullanıcı '{file_name}' adlı bir belge yükledi. İşte bundan çıkarılan metin içeriği. Lütfen bir AI Çalışma Yardımcısı olarak hareket edin: bu metni analiz edin, anahtar kavramları açıklayın, özetleyin veya bir öğrencinin bununla ilgili olası sorularını yanıtlayın. Doğruluğa ve netliğe öncelik verin.\n\nÇıkarılan Metin:\n---\n{extracted_content}\n---",
        "nl": "De gebruiker heeft een document geüpload met de naam '{file_name}'. Hier is de tekstinhoud die eruit is gehaald. Handel als een AI Studiehulp: analyseer deze tekst, leg sleutelconcepten uit, vat het samen of beantwoord potentiële vragen die een student hierover zou kunnen hebben. Geef prioriteit aan correctheid en duidelijkheid.\n\nGeëxtraheerde Tekst:\n---\n{extracted_content}\n---",
        "pl": "Użytkownik przesłał dokument o nazwie „{file_name}”. Oto wyodrębniona z niego treść tekstowa. Proszę działać jako Asystent Nauki AI: przeanalizuj ten tekst, wyjaśnij kluczowe pojęcia, streść go lub odpowiedz na potencjalne pytania, jakie student może mieć na jego temat. Priorytetem jest poprawność i jasność.\n\nWyodrębniony Tekst:\n---\n{extracted_content}\n---",
        "sv": "Användaren har laddat upp ett dokument med namnet '{file_name}'. Här är textinnehållet som extraherats från det. Vänligen agera som en AI-studiehjälp: analysera denna text, förklara nyckelbegrepp, sammanfatta den eller svara på potentiella frågor en student kan ha om den. Prioritera korrekthet och tydlighet.\n\nExtraherad text:\n---\n{extracted_content}\n---",
        "fi": "Käyttäjä latasi asiakirjan nimeltä '{file_name}'. Tässä on siitä poimittu tekstisisältö. Toimi tekoälyopiskeluavustajana: analysoi tämä teksti, selitä avainkäsitteet, tiivistä se tai vastaa mahdollisiin kysymyksiin, joita opiskelijalla voi olla siitä. Priorisoi oikeellisuus ja selkeys.\n\nPoimittu teksti:\n---\n{extracted_content}\n---",
        "no": "Brukeren har lastet opp et dokument med navnet '{file_name}'. Her er tekstinnholdet som er hentet ut fra det. Vennligst opptre som en AI-studiehjelper: analyser denne teksten, forklar nøkkelbegreper, oppsummer den eller svar på potensielle spørsmål en student måtte ha om den. Prioriter korrekthet og klarhet.\n\nUthentet tekst:\n---\n{extracted_content}\n---",
        "da": "Brugeren har uploadet et dokument ved navn '{file_name}'. Her er tekstindholdet, der er udtrukket fra det. Vær venlig at fungere som en AI-studiehjælper: analyser denne tekst, forklar nøglebegreber, opsummer den eller besvar potentielle spørgsmål, en studerende måtte have om den. Prioriter korrekthed og klarhed.\n\nUdtrukket tekst:\n---\n{extracted_content}\n---",
        "cs": "Uživatel nahrál dokument s názvem '{file_name}'. Zde je textový obsah z něj extrahovaný. Prosím, jednejte jako AI studijní pomocník: analyzujte tento text, vysvětlete klíčové pojmy, shrňte jej nebo odpovězte na potenciální otázky, které by k němu student mohl mít. Upřednostněte správnost a srozumitelnost.\n\nExtrahovaný text:\n---\n{extracted_content}\n---",
        "hu": "A felhasználó feltöltött egy '{file_name}' nevű dokumentumot. Itt van a belőle kinyert szöveges tartalom. Kérjük, működjön AI tanulási segédként: elemezze ezt a szöveget, magyarázza el a kulcsfogalmakat, foglalja össze, vagy válaszoljon a diákok lehetséges kérdéseire. Helyezze előtérbe a helyességet és az egyértelműséget.\n\nKinyert szöveg:\n---\n{extracted_content}\n---",
        "ro": "Utilizatorul a încărcat un document numit '{file_name}'. Iată conținutul text extras din acesta. Vă rugăm să acționați ca un Asistent de Studiu AI: analizați acest text, explicați conceptele cheie, rezumați-l sau răspundeți la întrebările potențiale pe care un student le-ar putea avea despre acesta. Prioritizați corectitudinea și claritatea.\n\nText Extras:\n---\n{extracted_content}\n---",
        "el": "Ο χρήστης ανέβασε ένα έγγραφο με το όνομα '{file_name}'. Αυτό είναι το περιεχόμενο κειμένου που εξήχθη από αυτό. Παρακαλώ ενεργήστε ως Βοηθός Μελέτης AI: αναλύστε αυτό το κείμενο, εξηγήστε βασικές έννοιες, συνοψίστε το ή απαντήστε σε πιθανές ερωτήσεις που μπορεί να έχει ένας φοιτητής σχετικά με αυτό. Δώστε προτεραιότητα στην ορθότητα και τη σαφήνεια.\n\nΕξαγόμενο Κείμενο:\n---\n{extracted_content}\n---",
        "he": "המשתמש העלה מסמך בשם '{file_name}'. הנה תוכן הטקסט שחולץ ממנו. אנא פעל כעוזר לימוד AI: נתח טקסט זה, הסבר מושגי מפתח, סכם אותו או ענה על שאלות פוטנציאליות שעשויות להיות לסטודנט לגביו. תעדף נכונות ובהירות.\n\nטקסט שחולץ:\n---\n{extracted_content}\n---",
        "th": "ผู้ใช้ได้อัปโหลดเอกสารชื่อ '{file_name}' นี่คือเนื้อหาข้อความที่คัดลอกมาจากเอกสารนั้น โปรดทำหน้าที่เป็นผู้ช่วยการเรียนรู้ AI: วิเคราะห์ข้อความนี้ อธิบายแนวคิดหลัก สรุป หรือตอบคำถามที่นักเรียนอาจมีเกี่ยวกับข้อความนี้ โปรดให้ความสำคัญกับความถูกต้องและความชัดเจน\n\nข้อความที่คัดลอกมา:\n---\n{extracted_content}\n---",
        "vi": "Người dùng đã tải lên một tài liệu có tên '{file_name}'. Đây là nội dung văn bản được trích xuất từ đó. Vui lòng hoạt động như một Trợ lý Học tập AI: phân tích văn bản này, giải thích các khái niệm chính, tóm tắt nó hoặc trả lời các câu hỏi tiềm năng mà một sinh viên có thể có về nó. Ưu tiên tính đúng đắn và rõ ràng.\n\nNội dung Văn bản Được Trích xuất:\n---\n{extracted_content}\n---",
        "id": "Pengguna telah mengunggah dokumen bernama '{file_name}'. Berikut adalah konten teks yang diekstrak darinya. Harap bertindak sebagai Asisten Belajar AI: analisis teks ini, jelaskan konsep-konsep kunci, rangkum, atau jawab pertanyaan potensial yang mungkin dimiliki siswa tentangnya. Prioritaskan kebenaran dan kejelasan.\n\nTeks yang Diekstrak:\n---\n{extracted_content}\n---",
        "ms": "Pengguna telah memuat naik dokumen bernama '{file_name}'. Berikut ialah kandungan teks yang diekstrak daripadanya. Sila bertindak sebagai Pembantu Pembelajaran AI: analisis teks ini, terangkan konsep utama, ringkaskannya, atau jawab soalan berpotensi yang mungkin ada pada pelajar mengenainya. Utamakan ketepatan dan kejelasan.\n\nTeks Diekstrak:\n---\n{extracted_content}\n---",
        "uk": "Користувач завантажив документ під назвою '{file_name}'. Ось витягнутий з нього текстовий вміст. Будь ласка, виступіть у ролі Помічника з навчання зі ШІ: проаналізуйте цей текст, поясніть ключові поняття, узагальніть його або дайте відповіді на потенційні запитання, які можуть виникнути у студента щодо нього. Пріоритет – правильність та чіткість.\n\nВитягнутий текст:\n---\n{extracted_content}\n---",
        "uz": "Foydalanuvchi '{file_name}' nomli hujjatni yukladi. Undan olingan matn mazmuni quyida keltirilgan. Iltimos, AI O'quv Yordamchisi sifatida harakat qiling: ushbu matnni tahlil qiling, asosiy tushunchalarni tushuntiring, uni qisqacha bayon qiling yoki talabaning u haqida bo'lishi mumkin bo'lgan savollariga javob bering. To'g'rilik va aniqlikka ustuvorlik bering.\n\nOlingan matn:\n---\n{extracted_content}\n---",
        "zh-TW": "使用者上傳了一個名為「{file_name}」的文件。這是從中提取的文本內容。請扮演 AI 學習助手的角色：分析此文本，解釋關鍵概念，對其進行總結，或回答學生可能對此提出的潛在問題。請優先考慮正確性和清晰度。\n\n提取文本：\n---\n{extracted_content}\n---",
        "pt-PT": "O utilizador carregou um documento chamado '{file_name}'. Eis o conteúdo de texto extraído dele. Por favor, aja como um Assistente de Estudo de IA: analise este texto, explique conceitos-chave, resuma-o ou responda a perguntas potenciais que um estudante possa ter sobre ele. Priorize a correção e a clareza.\n\nTexto Extraído:\n---\n{extracted_content}\n---"
    },
    "document_processing_error": {
        "en": "⚠️ An error occurred while processing the document: {file_name}.",
        "es": "⚠️ Ocurrió un error al procesar el documento: {file_name}.",
        "fr": "⚠️ Une erreur s'est produite lors du traitement du document : {file_name}.",
        "kk": "⚠️ {file_name} құжатын өңдеу кезінде қате орын алды.",
        "de": "⚠️ Beim Verarbeiten des Dokuments ist ein Fehler aufgetreten: {file_name}.",
        "ru": "⚠️ Произошла ошибка при обработке документа: {file_name}.",
        "zh-CN": "⚠️ 处理文档时发生错误：{file_name}。",
        "ja": "⚠️ ドキュメントの処理中にエラーが発生しました：{file_name}。",
        "ko": "⚠️ 문서를 처리하는 동안 오류가 발생했습니다: {file_name}。",
        "pt-BR": "⚠️ Ocorreu um erro ao processar o documento: {file_name}.",
        "it": "⚠️ Si è verificato un errore durante l'elaborazione del documento: {file_name}.",
        "ar": "⚠️ حدث خطأ أثناء معالجة المستند: {file_name}.",
        "hi": "⚠️ दस्तावेज़ को संसाधित करते समय एक त्रुटि हुई: {file_name}।",
        "tr": "⚠️ Belge işlenirken bir hata oluştu: {file_name}.",
        "nl": "⚠️ Er is een fout opgetreden bij het verwerken van het document: {file_name}.",
        "pl": "⚠️ Wystąpił błąd podczas przetwarzania dokumentu: {file_name}.",
        "sv": "⚠️ Ett fel uppstod vid bearbetning av dokumentet: {file_name}.",
        "fi": "⚠️ Virhe asiakirjan käsittelyssä: {file_name}.",
        "no": "⚠️ Det oppstod en feil under behandling av dokumentet: {file_name}.",
        "da": "⚠️ Der opstod en fejl under behandling af dokumentet: {file_name}.",
        "cs": "⚠️ Při zpracování dokumentu došlo k chybě: {file_name}.",
        "hu": "⚠️ Hiba történt a dokumentum feldolgozása közben: {file_name}.",
        "ro": "⚠️ A apărut o eroare la procesarea documentului: {file_name}.",
        "el": "⚠️ Παρουσιάστηκε σφάλμα κατά την επεξεργασία του εγγράφου: {file_name}.",
        "he": "⚠️ אירעה שגיאה בעת עיבוד המסמך: {file_name}.",
        "th": "⚠️ เกิดข้อผิดพลาดขณะประมวลผลเอกสาร: {file_name}",
        "vi": "⚠️ Đã xảy ra lỗi khi xử lý tài liệu: {file_name}.",
        "id": "⚠️ Terjadi kesalahan saat memproses dokumen: {file_name}.",
        "ms": "⚠️ Ralat berlaku semasa memproses dokumen: {file_name}.",
        "uk": "⚠️ Сталася помилка під час обробки документа: {file_name}.",
        "uz": "⚠️ Hujjatni qayta ishlashda xatolik yuz berdi: {file_name}.",
        "zh-TW": "⚠️ 處理文件時發生錯誤：{file_name}。",
        "pt-PT": "⚠️ Ocorreu um erro ao processar o documento: {file_name}."
    },
    "error_displaying_response_part":{
        "en": "⚠️ Error: A part of the response could not be displayed correctly.",
        "es": "⚠️ Error: Una parte de la respuesta no se pudo mostrar correctamente.",
        "fr": "⚠️ Erreur : Une partie de la réponse n'a pas pu être affichée correctement.",
        "kk": "⚠️ Қате: Жауаптың бір бөлігі дұрыс көрсетілмеді.",
        "de": "⚠️ Fehler: Ein Teil der Antwort konnte nicht korrekt angezeigt werden.",
        "ru": "⚠️ Ошибка: Часть ответа не может быть отображена корректно.",
        "zh-CN": "⚠️ 错误：部分响应无法正确显示。",
        "ja": "⚠️ エラー：応答の一部を正しく表示できませんでした。",
        "ko": "⚠️ 오류: 응답의 일부를 올바르게 표시할 수 없습니다.",
        "pt-BR": "⚠️ Erro: Uma parte da resposta não pôde ser exibida corretamente.",
        "it": "⚠️ Errore: Una parte della risposta non è stata visualizzata correttamente.",
        "ar": "⚠️ خطأ: تعذر عرض جزء من الرد بشكل صحيح.",
        "hi": "⚠️ त्रुटि: प्रतिक्रिया का एक हिस्सा सही ढंग से प्रदर्शित नहीं किया जा सका।",
        "tr": "⚠️ Hata: Yanıtın bir bölümü doğru görüntülenemedi.",
        "nl": "⚠️ Fout: Een deel van het antwoord kon niet correct worden weergegeven.",
        "pl": "⚠️ Błąd: Część odpowiedzi nie mogła zostać poprawnie wyświetlona.",
        "sv": "⚠️ Fel: En del av svaret kunde inte visas korrekt.",
        "fi": "⚠️ Virhe: Vastausta ei voitu näyttää osittain oikein.",
        "no": "⚠️ Feil: En del av svaret kunne ikke vises riktig.",
        "da": "⚠️ Fejl: En del af svaret kunne ikke vises korrekt.",
        "cs": "⚠️ Chyba: Část odpovědi se nepodařilo správně zobrazit.",
        "hu": "⚠️ Hiba: A válasz egy része nem jeleníthető meg helyesen.",
        "ro": "⚠️ Eroare: O parte a răspunsului nu a putut fi afișată corect.",
        "el": "⚠️ Σφάλμα: Ένα μέρος της απάντησης δεν ήταν δυνατό να εμφανιστεί σωστά.",
        "he": "⚠️ שגיאה: לא ניתן היה להציג חלק מהתגובה כראוי.",
        "th": "⚠️ ข้อผิดพลาด: ไม่สามารถแสดงส่วนหนึ่งของคำตอบได้อย่างถูกต้อง",
        "vi": "⚠️ Lỗi: Một phần của phản hồi không thể hiển thị chính xác.",
        "id": "⚠️ Kesalahan: Sebagian respons tidak dapat ditampilkan dengan benar.",
        "ms": "⚠️ Ralat: Sebahagian daripada respons tidak dapat dipaparkan dengan betul.",
        "uk": "⚠️ Помилка: Частину відповіді не вдалося відобразити коректно.",
        "uz": "⚠️ Xato: Javobning bir qismi to‘g‘ri ko‘rsatilmadi.",
        "zh-TW": "⚠️ 錯誤：部分回應無法正確顯示。",
        "pt-PT": "⚠️ Erro: Uma parte da resposta não pôde ser apresentada corretamente."
    },
    "gemini_no_vision_response": {
        "en": "🤷 I couldn't generate a response for the image.",
        "es": "🤷 No pude generar una respuesta para la imagen.",
        "fr": "🤷 Je n'ai pas pu générer de réponse pour l'image.",
        "kk": "🤷 Мен суретке жауап бере алмадым.",
        "de": "🤷 Ich konnte keine Antwort für das Bild generieren.",
        "ru": "🤷 Не удалось сгенерировать ответ для изображения.",
        "zh-CN": "🤷 我无法为该图像生成响应。",
        "ja": "🤷 画像に対する応答を生成できませんでした。",
        "ko": "🤷 이미지에 대한 응답을 생성할 수 없었습니다.",
        "pt-BR": "🤷 Não consegui gerar uma resposta para a imagem.",
        "it": "🤷 Non sono riuscito a generare una risposta per l'immagine.",
        "ar": "🤷 لم أتمكن من إنشاء رد للصورة.",
        "hi": "🤷 मैं छवि के लिए प्रतिक्रिया उत्पन्न नहीं कर सका।",
        "tr": "🤷 Görüntü için bir yanıt oluşturamadım.",
        "nl": "🤷 Ik kon geen antwoord genereren voor de afbeelding.",
        "pl": "🤷 Nie udało mi się wygenerować odpowiedzi dla obrazu.",
        "sv": "🤷 Jag kunde inte generera ett svar för bilden.",
        "fi": "🤷 En voinut luoda vastausta kuvalle.",
        "no": "🤷 Jeg kunne ikke generere et svar for bildet.",
        "da": "🤷 Jeg kunne ikke generere et svar for billedet.",
        "cs": "🤷 Pro obrázek se mi nepodařilo vygenerovat odpověď.",
        "hu": "🤷 Nem sikerült választ generálnom a képhez.",
        "ro": "🤷 Nu am putut genera un răspuns pentru imagine.",
        "el": "🤷 Δεν μπόρεσα να δημιουργήσω απάντηση για την εικόνα.",
        "he": "🤷 לא הצלחתי ליצור תגובה לתמונה.",
        "th": "🤷 ฉันไม่สามารถสร้างคำตอบสำหรับภาพนี้ได้",
        "vi": "🤷 Tôi không thể tạo phản hồi cho hình ảnh.",
        "id": "🤷 Saya tidak dapat membuat respons untuk gambar tersebut.",
        "ms": "🤷 Saya tidak dapat menjana respons untuk imej tersebut.",
        "uk": "🤷 Не вдалося згенерувати відповідь для зображення.",
        "uz": "🤷 Rasm uchun javob yaratib bo‘lmadi.",
        "zh-TW": "🤷 我無法為該圖片產生回應。",
        "pt-PT": "🤷 Não consegui gerar uma resposta para a imagem."
    },
    "gemini_no_response_document": {
         "en": "🤷 I couldn't generate an analysis for the document content.",
         "es": "🤷 No pude generar un análisis para el contenido del documento.",
         "fr": "🤷 Je n'ai pas pu générer d'analyse pour le contenu du document.",
         "kk": "🤷 Мен құжат мазмұнына талдау жасай алмадым.",
         "de": "🤷 Ich konnte keine Analyse für den Dokumentinhalt generieren.",
         "ru": "🤷 Не удалось сгенерировать анализ содержимого документа.",
         "zh-CN": "🤷 我无法为文档内容生成分析。",
         "ja": "🤷 ドキュメントの内容の分析を生成できませんでした。",
         "ko": "🤷 문서 내용에 대한 분석을 생성할 수 없었습니다.",
         "pt-BR": "🤷 Não consegui gerar uma análise para o conteúdo do documento.",
         "it": "🤷 Non sono riuscito a generare un'analisi per il contenuto del documento.",
         "ar": "🤷 لم أتمكن من إنشاء تحليل لمحتوى المستند.",
         "hi": "🤷 मैं दस्तावेज़ सामग्री के लिए विश्लेषण उत्पन्न नहीं कर सका।",
         "tr": "🤷 Belge içeriği için bir analiz oluşturamadım.",
         "nl": "🤷 Ik kon geen analyse genereren voor de documentinhoud.",
         "pl": "🤷 Nie udało mi się wygenerować analizy zawartości dokumentu.",
         "sv": "🤷 Jag kunde inte generera en analys för dokumentinnehållet.",
         "fi": "🤷 En voinut luoda analyysiä asiakirjan sisällölle.",
         "no": "🤷 Jeg kunne ikke generere en analyse for dokumentinnholdet.",
         "da": "🤷 Jeg kunne ikke generere en analyse for dokumentets indhold.",
         "cs": "🤷 Pro obsah dokumentu se mi nepodařilo vygenerovat analýzu.",
         "hu": "🤷 Nem sikerült elemzést készítenem a dokumentum tartalmához.",
         "ro": "🤷 Nu am putut genera o analiză pentru conținutul documentului.",
         "el": "🤷 Δεν μπόρεσα να δημιουργήσω ανάλυση για το περιεχόμενο του εγγράφου.",
         "he": "🤷 לא הצלחתי ליצור ניתוח לתוכן המסמך.",
         "th": "🤷 ฉันไม่สามารถสร้างการวิเคราะห์สำหรับเนื้อหาเอกสารได้",
         "vi": "🤷 Tôi không thể tạo phân tích cho nội dung tài liệu.",
         "id": "🤷 Saya tidak dapat membuat analisis untuk konten dokumen.",
         "ms": "🤷 Saya tidak dapat menjana analisis untuk kandungan dokumen tersebut.",
         "uk": "🤷 Не вдалося згенерувати аналіз вмісту документа.",
         "uz": "🤷 Hujjat mazmuni uchun tahlil yaratib bo‘lmadi.",
         "zh-TW": "🤷 我無法為文件內容產生分析。",
         "pt-PT": "🤷 Não consegui gerar uma análise para o conteúdo do documento."
    },
    "analysis_complete": {
        "en": "✅ Analysis complete.",
        "es": "✅ Análisis completo.",
        "fr": "✅ Analyse terminée.",
        "kk": "✅ Талдау аяқталды.",
        "de": "✅ Analyse abgeschlossen.",
        "ru": "✅ Анализ завершен.",
        "zh-CN": "✅ 分析完成。",
        "ja": "✅ 分析完了。",
        "ko": "✅ 분석 완료.",
        "pt-BR": "✅ Análise concluída.",
        "it": "✅ Analisi completata.",
        "ar": "✅ اكتمل التحليل.",
        "hi": "✅ विश्लेषण पूर्ण हुआ।",
        "tr": "✅ Analiz tamamlandı.",
        "nl": "✅ Analyse voltooid.",
        "pl": "✅ Analiza zakończona.",
        "sv": "✅ Analys slutförd.",
        "fi": "✅ Analyysi valmis.",
        "no": "✅ Analyse fullført.",
        "da": "✅ Analyse afsluttet.",
        "cs": "✅ Analýza dokončena.",
        "hu": "✅ Elemzés kész.",
        "ro": "✅ Analiză finalizată.",
        "el": "✅ Η ανάλυση ολοκληρώθηκε.",
        "he": "✅ הניתוח הושלם.",
        "th": "✅ การวิเคราะห์เสร็จสมบูรณ์",
        "vi": "✅ Phân tích hoàn tất.",
        "id": "✅ Analisis selesai.",
        "ms": "✅ Analisis selesai.",
        "uk": "✅ Аналіз завершено.",
        "uz": "✅ Tahlil yakunlandi.",
        "zh-TW": "✅ 分析完成。",
        "pt-PT": "✅ Análise concluída."
    },
    "continuing_analysis":{
        "en": "...continuing analysis...",
        "es": "...continuando análisis...",
        "fr": "...poursuite de l'analyse...",
        "kk": "...талдауды жалғастыру...",
        "de": "...Analyse wird fortgesetzt...",
        "ru": "...продолжаю анализ...",
        "zh-CN": "...继续分析...",
        "ja": "...分析を続行中...",
        "ko": "...분석 계속 중...",
        "pt-BR": "...continuando análise...",
        "it": "...continuando l'analisi...",
        "ar": "...متابعة التحليل...",
        "hi": "...विश्लेषण जारी है...",
        "tr": "...analiz devam ediyor...",
        "nl": "...analyse wordt voortgezet...",
        "pl": "...kontynuacja analizy...",
        "sv": "...fortsätter analysen...",
        "fi": "...jatketaan analyysiä...",
        "no": "...fortsetter analysen...",
        "da": "...fortsætter analyse...",
        "cs": "...pokračování v analýze...",
        "hu": "...elemzés folytatása...",
        "ro": "...continuând analiza...",
        "el": "...συνέχεια ανάλυσης...",
        "he": "...ממשיך בניתוח...",
        "th": "...กำลังวิเคราะห์ต่อ...",
        "vi": "...tiếp tục phân tích...",
        "id": "...melanjutkan analisis...",
        "ms": "...meneruskan analisis...",
        "uk": "...продовжую аналіз...",
        "uz": "...tahlil davom etmoqda...",
        "zh-TW": "...繼續分析...",
        "pt-PT": "...a continuar a análise..."
    }
    # Add more message keys as needed
}


def get_template(message_key: str, lang_code: str, default_val: str = None, **kwargs) -> str:
    """
    Fetches a localized template and formats it with provided kwargs.
    Falls back to DEFAULT_LOC_LANG if the specific lang_code or message_key is not found.
    If default_val is provided and the key/lang is not found, default_val is used.
    """
    if message_key not in TEMPLATES:
        return default_val if default_val is not None else f"[MISSING TEMPLATE KEY: {message_key}]"

    # Try to get the message for the specific language
    message_for_lang = TEMPLATES[message_key].get(lang_code)

    if message_for_lang is None:
        # Fallback to default language if specific language translation is missing
        message_for_lang = TEMPLATES[message_key].get(DEFAULT_LOC_LANG)
        if message_for_lang is None:
            # Super fallback: if even default lang is missing for this key
            available_translations = list(TEMPLATES[message_key].values())
            if available_translations:
                message_for_lang = available_translations[0]  # Use first available
            else:  # No translations at all for this key
                return default_val if default_val is not None else f"[NO TRANSLATIONS FOR KEY: {message_key}]"

    # If the fetched template is None (e.g. key exists but lang entry is explicitly None, though unlikely)
    if message_for_lang is None:
        return default_val if default_val is not None else f"[EMPTY TEMPLATE for {message_key} in {lang_code}]"

    try:
        return message_for_lang.format(**kwargs)
    except KeyError as e:
        # One of the format placeholders was missing in kwargs
        # Log this error, as it's a developer issue with calling get_template
        # import logging # Add at top of file if not already there
        # logger = logging.getLogger(__name__) # Or your specific logger
        # logger.error(f"Localization formatting error for key '{message_key}', lang '{lang_code}'. Missing placeholder: {e}. Kwargs: {kwargs}. Template: '{message_for_lang}'")
        # Return a user-friendly error or the unformatted template with an error message
        return default_val if default_val is not None else f"[FORMATTING ERROR for {message_key}: Missing {e}]"
    except Exception as e:
        # import logging
        # logger = logging.getLogger(__name__)
        # logger.error(f"Unexpected localization formatting error for key '{message_key}', lang '{lang_code}': {e}. Template: '{message_for_lang}'")
        return default_val if default_val is not None else f"[UNEXPECTED FORMATTING ERROR for {message_key}]"

# --- END OF FILE bot/localization.py ---