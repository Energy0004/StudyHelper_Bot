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
    "help_text_body": {
        "en": (
            "I'm your _StudyHelper_Bot_! Send me any message related to your studies.\n"
            "I try to remember our recent conversation and respond in your preferred language (set with `/language`).\n\n"
            "*Available commands:*\n"
            "`/start` - Ask to clear our chat history and see a welcome message.\n"
            "`/help` - Show this help message.\n"
            "`/language` - Choose your preferred language for my responses."
        ),
        "es": (
            "¡Soy tu _StudyHelper_Bot_! Envíame cualquier mensaje relacionado con tus estudios.\n"
            "Intento recordar nuestra conversación reciente y responder en tu idioma preferido (configurado con `/language`).\n\n"
            "*Comandos disponibles:*\n"
            "`/start` - Pide borrar nuestro historial de chat y ver un mensaje de bienvenida.\n"
            "`/help` - Muestra este mensaje de ayuda.\n"
            "`/language` - Elige tu idioma preferido para mis respuestas."
        ),
        "fr": (
            "Je suis votre _StudyHelper_Bot_ ! Envoyez-moi tout message concernant vos études.\n"
            "J'essaie de me souvenir de notre conversation récente et de répondre dans votre langue préférée (définie avec `/language`).\n\n"
            "*Commandes disponibles :*\n"
            "`/start` - Demandez à effacer notre historique de discussion et voir un message de bienvenue.\n"
            "`/help` - Affiche ce message d'aide.\n"
            "`/language` - Choisissez votre langue préférée pour mes réponses."
        ),
        "de": (
            "Ich bin dein _StudyHelper_Bot_! Schick mir jede Nachricht, die mit deinem Studium zu tun hat.\n"
            "Ich versuche, mich an unser letztes Gespräch zu erinnern und in deiner bevorzugten Sprache zu antworten (mit `/language` eingestellt).\n\n"
            "*Verfügbare Befehle:*\n"
            "`/start` - Fordere das Löschen unseres Chatverlaufs und eine Begrüßungsnachricht an.\n"
            "`/help` - Zeige diese Hilfenachricht.\n"
            "`/language` - Wähle deine bevorzugte Sprache für meine Antworten."
        ),
        "ru": (
            "Я ваш _StudyHelper_Bot_! Отправляйте мне любые сообщения, связанные с учебой.\n"
            "Я стараюсь помнить наш недавний разговор и отвечать на вашем предпочтительном языке (устанавливается командой `/language`).\n\n"
            "*Доступные команды:*\n"
            "`/start` - Запрос на очистку истории чата и приветственное сообщение.\n"
            "`/help` - Показать это сообщение помощи.\n"
            "`/language` - Выберите предпочитаемый язык для моих ответов."
        ),
        "zh-CN": (
            "我是你的 _StudyHelper_Bot_！发送任何与你学习相关的信息给我。\n"
            "我会尝试记住我们最近的对话，并用你偏好的语言回复（通过 `/language` 设置）。\n\n"
            "*可用命令：*\n"
            "`/start` - 请求清除聊天记录并显示欢迎信息。\n"
            "`/help` - 显示此帮助信息。\n"
            "`/language` - 选择我回复时使用的语言。"
        ),
        "kk": (
            "Мен сіздің _StudyHelper_Bot_ болып табыламын! Оқуыңызға қатысты кез келген хабарламаны жіберіңіз.\n"
            "Мен соңғы сұхбатымызды есте сақтауға және сіздің таңдаған тіліңізде жауап беруге тырысамын (`/language` арқылы орнатылады).\n\n"
            "*Қолжетімді пәрмендер:*\n"
            "`/start` - Сұхбат тарихын тазартуды сұрау және сәлемдесу хабарламасын көру.\n"
            "`/help` - Осы көмек хабарламасын көрсету.\n"
            "`/language` - Менің жауаптарым үшін қалаған тіліңізді таңдаңыз."
        ),
        "ja": (
            "私はあなたの_StudyHelper_Bot_です！勉強に関するメッセージを送ってください。\n"
            "最近の会話を覚えており、あなたの希望する言語（`/language`で設定）で返信します。\n\n"
            "*利用可能なコマンド:*\n"
            "`/start` - チャット履歴をクリアしてウェルカムメッセージを表示します。\n"
            "`/help` - このヘルプメッセージを表示します。\n"
            "`/language` - 返信に使う言語を選択します。"
        ),
        "ko": (
            "저는 당신의 _StudyHelper_Bot_입니다! 공부와 관련된 메시지를 보내주세요.\n"
            "최근 대화를 기억하며, 선호하는 언어(`/language`로 설정)로 답변합니다.\n\n"
            "*사용 가능한 명령어:*\n"
            "`/start` - 대화 기록을 삭제하고 환영 메시지를 봅니다.\n"
            "`/help` - 이 도움말 메시지를 표시합니다.\n"
            "`/language` - 답변에 사용할 언어를 선택하세요."
        ),
        "pt-BR": (
            "Eu sou seu _StudyHelper_Bot_! Envie qualquer mensagem relacionada aos seus estudos.\n"
            "Eu tento lembrar nossa conversa recente e responder no seu idioma preferido (configurado com `/language`).\n\n"
            "*Comandos disponíveis:*\n"
            "`/start` - Peça para limpar o histórico do chat e ver uma mensagem de boas-vindas.\n"
            "`/help` - Mostrar esta mensagem de ajuda.\n"
            "`/language` - Escolha seu idioma preferido para minhas respostas."
        ),
        "it": (
            "Sono il tuo _StudyHelper_Bot_! Inviami qualsiasi messaggio relativo ai tuoi studi.\n"
            "Cerco di ricordare la nostra conversazione recente e rispondere nella lingua preferita (impostata con `/language`).\n\n"
            "*Comandi disponibili:*\n"
            "`/start` - Richiedi di cancellare la cronologia chat e visualizzare un messaggio di benvenuto.\n"
            "`/help` - Mostra questo messaggio di aiuto.\n"
            "`/language` - Scegli la lingua preferita per le mie risposte."
        ),
        "ar": (
            "أنا بوت _StudyHelper_Bot_ الخاص بك! أرسل لي أي رسالة تتعلق بدراستك.\n"
            "أحاول تذكر محادثتنا الأخيرة والرد بلغتك المفضلة (تُحدد باستخدام `/language`).\n\n"
            "*الأوامر المتاحة:*\n"
            "`/start` - اطلب مسح سجل الدردشة ورؤية رسالة ترحيب.\n"
            "`/help` - عرض رسالة المساعدة هذه.\n"
            "`/language` - اختر لغتك المفضلة لردودي."
        ),
        "hi": (
            "मैं आपका _StudyHelper_Bot_ हूँ! मुझे अपनी पढ़ाई से संबंधित कोई भी संदेश भेजें।\n"
            "मैं हमारी हाल की बातचीत याद रखने की कोशिश करता हूँ और आपकी पसंदीदा भाषा में जवाब देता हूँ (`/language` से सेट)।\n\n"
            "*उपलब्ध कमांड:*\n"
            "`/start` - चैट इतिहास साफ़ करने और स्वागत संदेश देखने के लिए कहें।\n"
            "`/help` - यह सहायता संदेश दिखाएँ।\n"
            "`/language` - मेरी प्रतिक्रियाओं के लिए अपनी पसंदीदा भाषा चुनें।"
        ),
        "tr": (
            "Ben senin _StudyHelper_Bot_'unum! Bana çalışmalarınla ilgili herhangi bir mesaj gönder.\n"
            "Son sohbetimizi hatırlamaya çalışır ve tercih ettiğin dilde cevap veririm (`/language` ile ayarlanır).\n\n"
            "*Mevcut komutlar:*\n"
            "`/start` - Sohbet geçmişimizi temizlemeyi ve bir karşılama mesajı görmeyi iste.\n"
            "`/help` - Bu yardım mesajını göster.\n"
            "`/language` - Yanıtlarım için tercih ettiğin dili seç."
        ),
        "nl": (
            "Ik ben je _StudyHelper_Bot_! Stuur me een bericht over je studie.\n"
            "Ik probeer ons recente gesprek te onthouden en te antwoorden in je voorkeurstaal (ingesteld met `/language`).\n\n"
            "*Beschikbare commando's:*\n"
            "`/start` - Vraag om onze chatgeschiedenis te wissen en een welkomstbericht te zien.\n"
            "`/help` - Toon dit helpbericht.\n"
            "`/language` - Kies je voorkeurs taal voor mijn antwoorden."
        ),
        "pl": (
            "Jestem twoim _StudyHelper_Bot_! Wyślij mi dowolną wiadomość związaną z nauką.\n"
            "Staram się pamiętać naszą ostatnią rozmowę i odpowiadać w twoim preferowanym języku (ustawiane przez `/language`).\n\n"
            "*Dostępne polecenia:*\n"
            "`/start` - Poproś o wyczyszczenie historii czatu i wyświetlenie powitalnej wiadomości.\n"
            "`/help` - Pokaż tę wiadomość pomocy.\n"
            "`/language` - Wybierz preferowany język moich odpowiedzi."
        ),
        "sv": (
            "Jag är din _StudyHelper_Bot_! Skicka mig ett meddelande om dina studier.\n"
            "Jag försöker komma ihåg vår senaste konversation och svara på ditt föredragna språk (inställt med `/language`).\n\n"
            "*Tillgängliga kommandon:*\n"
            "`/start` - Be om att rensa vår chatt-historik och visa ett välkomstmeddelande.\n"
            "`/help` - Visa detta hjälpmeddelande.\n"
            "`/language` - Välj ditt föredragna språk för mina svar."
        ),
        "fi": (
            "Olen _StudyHelper_Bot_! Lähetä minulle mitä tahansa opintoihisi liittyvää viestiä.\n"
            "Yritän muistaa viimeisimmän keskustelumme ja vastata valitsemallasi kielellä (`/language`).\n\n"
            "*Saatavilla olevat komennot:*\n"
            "`/start` - Pyydä tyhjentämään keskusteluhistoria ja näkemään tervetuloviesti.\n"
            "`/help` - Näytä tämä ohjeviesti.\n"
            "`/language` - Valitse vastausteni kieli."
        ),
        "no": (
            "Jeg er din _StudyHelper_Bot_! Send meg en melding relatert til studiene dine.\n"
            "Jeg prøver å huske vår siste samtale og svare på ditt foretrukne språk (innstilt med `/language`).\n\n"
            "*Tilgjengelige kommandoer:*\n"
            "`/start` - Be om å tømme chatthistorikken og se en velkomstmelding.\n"
            "`/help` - Vis denne hjelpeteksten.\n"
            "`/language` - Velg ditt foretrukne språk for mine svar."
        ),
        "da": (
            "Jeg er din _StudyHelper_Bot_! Send mig en besked relateret til dine studier.\n"
            "Jeg prøver at huske vores seneste samtale og svare på dit foretrukne sprog (indstillet med `/language`).\n\n"
            "*Tilgængelige kommandoer:*\n"
            "`/start` - Bed om at rydde chat historikken og se en velkomstbesked.\n"
            "`/help` - Vis denne hjælpetekst.\n"
            "`/language` - Vælg dit foretrukne sprog for mine svar."
        ),
        "cs": (
            "Jsem váš _StudyHelper_Bot_! Pošlete mi jakoukoli zprávu týkající se vašich studií.\n"
            "Snažím se pamatovat na naši nedávnou konverzaci a odpovídat ve vámi preferovaném jazyce (nastaveném příkazem `/language`).\n\n"
            "*Dostupné příkazy:*\n"
            "`/start` - Požádejte o vymazání historie chatu a zobrazení uvítací zprávy.\n"
            "`/help` - Zobrazit tuto nápovědu.\n"
            "`/language` - Vyberte preferovaný jazyk pro mé odpovědi."
        ),
        "hu": (
            "Én vagyok a te _StudyHelper_Bot_-od! Küldj nekem bármilyen tanulmányokkal kapcsolatos üzenetet.\n"
            "Megpróbálom megjegyezni a legutóbbi beszélgetésünket és a preferált nyelveden válaszolni (`/language`-vel beállítható).\n\n"
            "*Elérhető parancsok:*\n"
            "`/start` - Kérd a csevegési előzmények törlését és egy üdvözlő üzenet megjelenítését.\n"
            "`/help` - Mutasd ezt a súgóüzenetet.\n"
            "`/language` - Válaszd ki a válaszaim nyelvét."
        ),
        "ro": (
            "Sunt _StudyHelper_Bot_-ul tău! Trimite-mi orice mesaj legat de studiile tale.\n"
            "Încerc să îmi amintesc conversația recentă și să răspund în limba ta preferată (setată cu `/language`).\n\n"
            "*Comenzi disponibile:*\n"
            "`/start` - Cere să se șteargă istoricul conversației și să vezi un mesaj de bun venit.\n"
            "`/help` - Arată acest mesaj de ajutor.\n"
            "`/language` - Alege limba preferată pentru răspunsurile mele."
        ),
        "el": (
            "Είμαι ο _StudyHelper_Bot_ σου! Στείλε μου οποιοδήποτε μήνυμα σχετικό με τις σπουδές σου.\n"
            "Προσπαθώ να θυμάμαι την πρόσφατη συνομιλία μας και να απαντώ στη γλώσσα που προτιμάς (ορίζεται με `/language`).\n\n"
            "*Διαθέσιμες εντολές:*\n"
            "`/start` - Ζήτα να διαγραφεί το ιστορικό συνομιλιών και να δεις ένα μήνυμα καλωσορίσματος.\n"
            "`/help` - Εμφάνιση αυτού του μηνύματος βοήθειας.\n"
            "`/language` - Επέλεξε την προτιμώμενη γλώσσα για τις απαντήσεις μου."
        ),
        "he": (
            "אני ה_StudyHelper_Bot_ שלך! שלח לי כל הודעה שקשורה ללימודים שלך.\n"
            "אני מנסה לזכור את השיחה האחרונה שלנו ולהגיב בשפה המועדפת עליך (נבחרת באמצעות `/language`).\n\n"
            "*פקודות זמינות:*\n"
            "`/start` - בקש לנקות את היסטוריית הצ׳אט ולקבל הודעת ברכה.\n"
            "`/help` - הצג הודעת עזרה זו.\n"
            "`/language` - בחר את שפת התשובות שלי."
        ),
        "th": (
            "ฉันคือ _StudyHelper_Bot_ ของคุณ! ส่งข้อความที่เกี่ยวกับการเรียนของคุณมาได้เลย\n"
            "ฉันพยายามจำบทสนทนาล่าสุดและตอบกลับเป็นภาษาที่คุณเลือกไว้ (`/language`).\n\n"
            "*คำสั่งที่ใช้ได้:*\n"
            "`/start` - ขอเคลียร์ประวัติแชทและดูข้อความต้อนรับ\n"
            "`/help` - แสดงข้อความช่วยเหลือนี้\n"
            "`/language` - เลือกภาษาที่ต้องการให้ฉันตอบกลับ"
        ),
        "vi": (
            "Tôi là _StudyHelper_Bot_ của bạn! Gửi cho tôi bất kỳ tin nhắn nào liên quan đến việc học của bạn.\n"
            "Tôi cố gắng ghi nhớ cuộc trò chuyện gần đây và trả lời bằng ngôn ngữ bạn chọn (đặt bằng `/language`).\n\n"
            "*Các lệnh có sẵn:*\n"
            "`/start` - Yêu cầu xóa lịch sử trò chuyện và xem tin nhắn chào mừng.\n"
            "`/help` - Hiển thị tin nhắn trợ giúp này.\n"
            "`/language` - Chọn ngôn ngữ ưu tiên để tôi trả lời."
        ),
        "id": (
            "Saya _StudyHelper_Bot_ Anda! Kirimkan pesan apa pun yang berhubungan dengan studi Anda.\n"
            "Saya mencoba mengingat percakapan terbaru dan merespons dalam bahasa pilihan Anda (diatur dengan `/language`).\n\n"
            "*Perintah yang tersedia:*\n"
            "`/start` - Minta untuk menghapus riwayat chat dan melihat pesan sambutan.\n"
            "`/help` - Tampilkan pesan bantuan ini.\n"
            "`/language` - Pilih bahasa pilihan Anda untuk respons saya."
        ),
        "ms": (
            "Saya adalah _StudyHelper_Bot_ anda! Hantar apa-apa mesej berkaitan dengan pembelajaran anda.\n"
            "Saya cuba mengingati perbualan terkini dan membalas dalam bahasa pilihan anda (ditetapkan dengan `/language`).\n\n"
            "*Perintah tersedia:*\n"
            "`/start` - Minta untuk membersihkan sejarah chat dan lihat mesej alu-aluan.\n"
            "`/help` - Tunjukkan mesej bantuan ini.\n"
            "`/language` - Pilih bahasa pilihan anda untuk balasan saya."
        ),
        "uk": (
            "Я ваш _StudyHelper_Bot_! Надсилайте мені будь-які повідомлення, що стосуються ваших навчань.\n"
            "Я намагаюся пам’ятати нашу недавню розмову і відповідати вашою обраною мовою (встановлюється командою `/language`).\n\n"
            "*Доступні команди:*\n"
            "`/start` - Попросити очистити історію чату і побачити привітальне повідомлення.\n"
            "`/help` - Показати це повідомлення допомоги.\n"
            "`/language` - Оберіть бажану мову для моїх відповідей."
        ),
        "uz": (
            "Men sizning _StudyHelper_Bot_ man! O'qishingizga oid har qanday xabarni menga yuboring.\n"
            "So‘nggi suhbatimizni eslab qolishga harakat qilaman va javoblarni siz tanlagan tilingizda beraman (`/language` yordamida sozlanadi).\n\n"
            "*Mavjud buyruqlar:*\n"
            "`/start` - Suhbat tariximizni tozalash va xush kelibsiz xabarini ko‘rishni so‘rashingiz mumkin.\n"
            "`/help` - Ushbu yordam xabarini ko‘rsatish.\n"
            "`/language` - Javoblarim uchun afzal tilingizni tanlang."
        ),
        "zh-TW": (
            "我是你的_StudyHelper_Bot_！發送任何與你的學習相關的訊息給我。\n"
            "我會嘗試記住我們最近的對話，並用你設定的語言回覆（通過 `/language` 設定）。\n\n"
            "*可用指令：*\n"
            "`/start` - 請求清除我們的聊天記錄並查看歡迎訊息。\n"
            "`/help` - 顯示此幫助訊息。\n"
            "`/language` - 選擇你希望我使用的回覆語言。"
        ),
        "pt-PT": (
            "Sou o teu _StudyHelper_Bot_! Envia-me qualquer mensagem relacionada com os teus estudos.\n"
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
    # Add more message keys as needed
}


def get_template(message_key: str, lang_code: str, **kwargs) -> str:
    """
    Fetches a localized template and formats it with provided kwargs.
    Falls back to DEFAULT_LOC_LANG if the specific lang_code or message_key is not found.
    """
    if message_key not in TEMPLATES:
        # Fallback for missing message_key: return the key itself or a generic error
        return f"[MISSING TEMPLATE: {message_key}]"

    # Try to get the message for the specific language
    message_for_lang = TEMPLATES[message_key].get(lang_code)

    if message_for_lang is None:
        # Fallback to default language if specific language translation is missing
        message_for_lang = TEMPLATES[message_key].get(DEFAULT_LOC_LANG)
        if message_for_lang is None:
            # Super fallback: if even default lang is missing for this key (should not happen if structured well)
            # Return the first available translation for that key or an error string
            available_translations = list(TEMPLATES[message_key].values())
            if available_translations:
                message_for_lang = available_translations[0]
            else:
                return f"[NO TRANSLATIONS FOR KEY: {message_key}]"

    try:
        return message_for_lang.format(**kwargs)
    except KeyError as e:
        # One of the format placeholders was missing in kwargs
        return f"[FORMATTING ERROR for {message_key} in {lang_code}: Missing key {e}] {message_for_lang}"
    except Exception as e:
        return f"[UNEXPECTED FORMATTING ERROR for {message_key} in {lang_code}: {e}] {message_for_lang}"

# --- END OF FILE bot/localization.py ---