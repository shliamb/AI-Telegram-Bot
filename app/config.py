

#### CONFIG ####
URL = "http://137.184.87.156:8000"
TIME_CORRECTION = +3 # Moscow
MIN_PAY = 1 # Minimum pay
VOICE_THE_ANSWER = True # False or True
AI_DEFAULT = "openai" # gemini or openai
AI_DEFAULT_MODEL_GEMINI = "gemini-1.5-flash-latest" #  gemini-1.5-flash-latest or gpt-4o-mini-2024-07-18
AI_DEFAULT_MODEL_OPENAI = "gpt-4o-mini-2024-07-18"
AI_DEFAULT_MODEL_GET_AUDIO = "tts-1"
AI_DEFAULT_MODEL_GET_TRANSCRIPTION = "whisper-1"


# Folders:
DOWNLOADS_FOLDER = "./downloads/"
UPLOADS_FOLDER = "./uploads/"
AUDIO_FOLDER = "./audio/"
VOICE_FOLDER = "./voice/"


# Prices per 1M tokens:
PRICE = {
    # OpenAI to 1M tokes:
    'chatgpt-4o-latest': 40,
    'gpt-4o': 40,
    'gpt-4o-2024-05-13': 40,
    'gpt-4o-2024-08-06': 25,
    'gpt-4o-mini': 1.5, # no vision
    'gpt-4o-mini-2024-07-18': 1.5, # no vision
    'gpt-4-turbo-2024-04-09': 80,

    # New:
    'o1-preview': 150,
    'o1-preview-2024-09-12': 150,

    'o1-mini': 30,
    'o1-mini-2024-09-12': 30,

    # Images to one img:
    'dall-e-3-1024': 0.08,
    'dall-e-3-1792': 0.16,

    'dall-e-3-hd-1024': 0.16,
    'dall-e-3-hd-1792': 0.24,

    'dall-e-2-1024': 0.04,
    'dall-e-2-512': 0.036,
    'dall-e-2-256': 0.032,

    # Audio to 1M characters:
    'tts-1': 30, # / 1M characters
    'tts-1-hd': 60, # / 1M characters
    'whisper-1': 0.012, # minute (rounded to the nearest second)

    # Google Gemini to 1M tokens:
    'gemini-1.5-pro-latest': 93.75,
    'gemini-1.5-flash-latest': 1.125,
    'gemini-1.0-pro-latest': 4,
    # 'text-embedding-004': 0, # Free  хз пока что как ее пользовать
    # 'aqa': 0,
    }