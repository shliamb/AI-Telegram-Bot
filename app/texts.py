

start_ru = '''

Добро пожаловать в телеграм-бот, созданный для работы с передовыми искусственными интеллектами, такими как OpenAI, Google, Anthropic и многими другими. Здесь вы можете задавать вопросы как текстом, так и голосом, прикреплять изображения а также попросить создать уникальные изображения. Кроме того,  ИИ может отвечать вам голосовыми сообщениями.

Мы рады помочь вам!

'''


start_en = '''

Welcome to Telegram bot, created to work with advanced artificial intelligences such as Open AI, Google, Anthropic and many others. Here you can ask questions in both text and voice, attach images, and ask to create unique images. In addition, the AI can respond to you with voice messages.

We are happy to help you!

'''


system_content = '''

System content в OpenAI ChatGPT — это предварительно заданные инструкции или контекст, которые помогают модели понять, как она должна взаимодействовать с пользователем. Это может включать указания о тоне общения, стиле ответов и других аспектах, чтобы обеспечить более целенаправленный и релевантный опыт для пользователя.

'''


prices_ru = '''

Языковая модель OpenAI 1млн токенов в USD:
    'o1-preview': 150,
    'o1-preview-2024-09-12': 150,
    'o1-mini': 30,
    'o1-mini-2024-09-12': 30,
    'chatgpt-4o-latest': 40,
    'gpt-4o': 40,
    'gpt-4o-2024-05-13': 40,
    'gpt-4o-2024-08-06': 25,
    'gpt-4o-mini': 1.5,
    'gpt-4o-mini-2024-07-18': 1.5,
    'gpt-4-turbo-2024-04-09': 80,

Языковая модель от Google 1млн в USD:
    'gemini-1.5-pro-latest': 93.75,
    'gemini-1.5-flash-latest': 1.125,

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
    'o1-preview': 150,
    'o1-preview-2024-09-12': 150,
    'o1-mini': 30,
    'o1-mini-2024-09-12': 30,
    'chatgpt-4o-latest': 40,
    'gpt-4o': 40,
    'gpt-4o-2024-05-13': 40,
    'gpt-4o-2024-08-06': 25,
    'gpt-4o-mini': 1.5, # no vision
    'gpt-4o-mini-2024-07-18': 1.5, # no vision
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