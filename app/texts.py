

start_ru = '''

Возможности Телеграмм Бота:

Задать вопрос ИИ:
- ИИ можно написать вопрос текстом,
- ИИ можно надиктовать вопрос голосовым сообщением,
- ИИ может увидеть прикрепленное изображение,
- Можно переключать языковые модели OpenAI, Google, Anthropic, Grok, DeepSeek прямо в разговоре, контекст разговора сохраниться,
- Для сброса истории диалога просто напишите - "забудь" или выберите в быстром меню /reset

Получить ответ ИИ:
- ИИ отвечает текстом,
- ИИ может отвечать текст + аудио,
- ИИ может сгенирировать изображение (Dall-e 3) /genDraw


Настройки:
- Выбор языка /en /ru
- Включение уведомлений бота /notON /notOFF
    Для того, что бы новости от бота не беспокоили вас, вы можете просто их отключить. В редких новостях, обычно, описываются новые возможности или добавление языковых моделей.
- Включение истории диалога /diON /diOFF
    ИИ помнит последние 15 итераций вопрос - ответ. Если вы отклдючите историю, каждый вопрос к ИИ будет первым в контексте для нее. Чем больше история, тем больше оплата за токены. Очистка памяти поможет вам с экономить.
- Включение сжатия истории /sumON /sumOFF
    Если эта функция включена, то каждый ответ от ИИ, проверяется на длину. Сообщение больше 500 символов, автоматически будет сжато без потери смысла самой дешевой языковой моделью и сохранено сжатым в историю, экономя ваши деньги. Вы же, получите полный ответ.
- Включение аудио ответа /audON /audOFF
    ИИ будет выдавать вам после текстового ответа аудиофайл, который вы можете прослушать. Иногда бывает удобнее и проще послушать, чем читать. В настройках ниже, вы можете так же выбрать голос озвучки, качество, скорость. 
- Задать системные инструкции ИИ /addSYS
    Системные инструкции помогают модели понять, как она должна взаимодействовать с пользователем. Пример: "Ты личный асистент по имени Алиса молодой девушки 17 лет по имени Лола. Ты даешь сжатые, но полные ответы на ее вопросы."
- Пополнить финансовый баланс счета /pay
    Для нового пользователя придусмотренна проверочная сумма на счете. Далее, вы можете пополнить счет для дальнейшей работы.
- Скачать CSV файл последних 50 трат /getStat

От разработчика: "Эта программа сейчас на стадии тестирования. Никаких гарантий, никаких обязательств, никакой ответственности – вообще ничего! Используя её, ты полностью соглашаешься с этим беспределом. Но, между нами, надеюсь, тебе понравится 😉"

'''


start_en = '''

Features of Telegram Bot:

Ask an AI question:
- AI can write a question in text,
- AI can dictate a question by voice message,
- The AI can see the attached image,
- You can switch the language models of OpenAI, Google, Anthropic, Grok, DeepSeek right in the conversation, the context of the conversation will be preserved,
- To reset the dialog history, simply write - "forget" or select /reset in the quick menu.

Get an AI response:
- The AI responds with text,
- AI can respond with text + audio,
- AI can generate an image (Dall-e 3) /genDraw


Settings:
- Language selection /en /ru
- Enabling bot notifications /notON /notOFF
    In order for the news from the bot not to bother you, you can simply turn it off. Rare news reports usually describe new features or the addition of language models.
- Enabling dialog history /diON /diOFF
    The AI remembers the last 15 iterations of the question and answer. If you tell the story, every question to the AI will be the first in the context for it. The longer the story, the higher the payment for tokens. Clearing your memory will help you save money.
- Enabling history compression /sumON /sumOFF
    If this feature is enabled, then each response from the AI is checked for length. A message with more than 500 characters will be automatically compressed without loss of meaning using the cheapest language model and saved compressed into history, saving you money. You will get a complete answer.
- Enabling audio response /audON /audOFF
    The AI will give you an audio file after the text response, which you can listen to. Sometimes it is more convenient and easier to listen than to read. In the settings below, you can also select the voiceover voice, quality, and speed. 
- Set system instructions and /addSYS
    The system instructions help the model understand how it should interact with the user. Example: "You are the personal assistant named Alice of a 17-year-old young girl named Lola. You give concise but complete answers to her questions."
- Top up your financial account balance /pay
    The verification amount on the account is provided for the new user. Next, you can add funds to your account for further work.
- Download the CSV file of the last 50 expenses /getStat

From the developer: "This program is currently under testing. No guarantees, no obligations, no responsibilities – nothing at all! By using it, you completely agree with this lawlessness. But just between you and me, I hope you like it. 😉"

'''


system_content = '''

System content в OpenAI ChatGPT — это предварительно заданные инструкции или контекст, которые помогают модели понять, как она должна взаимодействовать с пользователем. Это может включать указания о тоне общения, стиле ответов и других аспектах, чтобы обеспечить более целенаправленный и релевантный опыт для пользователя.

'''


prices_ru = '''

Языковая модель OpenAI 1млн токенов в USD:
    'o1-preview': 150,
    'o1-preview-2024-09-12': 150,
    'o3-mini': 11,
    'o3-mini-2025-01-31': 11,
    'chatgpt-4o-latest': 40,
    'gpt-4o': 40,
    'gpt-4o-2024-05-13': 40,
    'gpt-4o-2024-08-06': 25,
    'gpt-4o-mini': 2.5,
    'gpt-4o-mini-2024-07-18': 2.5,
    'gpt-4-turbo-2024-04-09': 80,

Языковая модель от Google 1млн в USD:
    'gemini-2.0-flash-exp': 25,
    'gemini-1.5-pro-latest': 25,
    'gemini-1.5-flash-latest': 1.2,
    'gemini-1.5-flash-8b': 0.8,

Языковая модель от Anthropic 1млн в USD:
    'claude-3-5-sonnet-latest': 36,
    'claude-3-5-haiku-latest': 12,
    'claude-3-opus-latest': 180,
    'claude-3-sonnet-20240229': 36,
    'claude-3-haiku-20240307': 3,

Генерация изображений за одну в USD:
    'dall-e-3-1024': 0.08,
    'dall-e-3-1792': 0.16,
    'dall-e-3-hd-1024': 0.16,
    'dall-e-3-hd-1792': 0.24,
    'dall-e-2-1024': 0.04,
    'dall-e-2-512': 0.036,
    'dall-e-2-256': 0.032,

Генерация голоса 1млн символов в USD:
    'tts-1': 30,
    'tts-1-hd': 60,

Транскрипция из аудио в текст мин. в USD:
    'whisper-1': 0.012,

/add_money — пополнить баланс

'''


prices_en = '''

OpenAI language model 1 million tokens in $:
    'chatgpt-4o-latest': 40,
    'gpt-4o': 40,
    'gpt-4o-2024-05-13': 40,
    'gpt-4o-2024-08-06': 25,
    'gpt-4o-mini': 2.5, # no vision
    'gpt-4o-mini-2024-07-18': 2.5, # no vision
    'gpt-4-turbo-2024-04-09': 80,

The language model from Google is 1 million in $:
    'gemini-2.0-flash-exp': 25,
    'gemini-1.5-pro-latest': 25,
    'gemini-1.5-flash-latest': 1.2,
    'gemini-1.5-flash-8b': 0.8,

The language model from Anthropic is 1 million in $:
    'claude-3-5-sonnet-latest': 36,
    'claude-3-5-haiku-latest': 12,
    'claude-3-opus-latest': 180,
    'claude-3-sonnet-20240229': 36,
    'claude-3-haiku-20240307': 3,

Generating images for one in $:
    'dall-e-3-1024': 0.08,
    'dall-e-3-1792': 0.16,
    'dall-e-3-hd-1024': 0.16,
    'dall-e-3-hd-1792': 0.24,
    'dall-e-2-1024': 0.04,
    'dall-e-2-512': 0.036,
    'dall-e-2-256': 0.032,

Voice generation of 1M characters in $:
    'tts-1': 30, 
    'tts-1-hd': 60,

Transcription from audio to text min. in $:
    'whisper-1': 0.012,

/add_money — replenish    

'''



# 🇺🇸 EN: 
# [OpenAI - ChatGPT, Google - Gemini, Anthropic - Claude]

# - The bot accepts images, voice messages, text,
# - The bot can respond with text, audio response, generate an image,
# - The ability to give AI system instructions separately,
# - Perfect dialogue history management and on-the-fly language model switching while maintaining the context of communication,
# - Quick response of the whole response model.



# 🇷🇺 RU:
# [OpenAI - ChatGPT, Google - Gemini, Anthropic - Claude]

# - Бот принимает изображения, голосовые сообщения, текст,
# - Бот может отвечать текстом, аудио ответом, сгенерировать изображение,
# - Возможность дать ИИ системные инструкции отдельно,
# - Идеальное ведение истории диалога и переключение на лету языковой модели с сохранением контекста общения,
# - Быстрый ответ модели всего ответа целиком.