

#### BASIC CONFIG ####

# System:
URL = "http://137.184.87.156:8000"
TIME_CORRECTION = +3 # Moscow
MIN_PAY = 1 # $ Minimum pay
RUBTOUSD = 100 # The internal exchange rate
GIFT = 0.1 # $ The amount on the account at the beginning
VOICE_THE_ANSWER = True # False or True
DIALOG = True # History dialog
DIALOG_SUM = True # AI compress history dialog
LANGUAGE = "en"

# Language models:
AI_DEFAULT = "gemini" # gemini or openai, anthropic in future
AI_DEFAULT_MODEL_GEMINI = "gemini-1.5-flash-latest" #  gemini-1.5-flash-latest or gpt-4o-mini-2024-07-18
AI_DEFAULT_MODEL_OPENAI = "gpt-4o-mini-2024-07-18"

# Gen Audio models:
AI_AUDIO = "openai"
AI_DEFAULT_MODEL_GET_AUDIO = "tts-1" # tts-1-hd
VOICE = "nova" # alloy, echo, fable, onyx, nova, and shimmer
VOICE_SPEED = 1.0 # 0.25 to 4.0

# Transcription voice models:
AI_VOICE = "openai"
AI_DEFAULT_MODEL_GET_VOICE = "whisper-1" # no choes

# Gen Img models:
AI_DRAW = "openai" # or midjourney
DEFAULT_DALL_E = "dall-e-3"
IMG_SIZE = "1024x1024" # 
N_NUMBER = 1
IMG_QUALITY = "standard" # standard or hd
IMG_STYLE = "vivid" # vivid ore natural

# Gen Video models:
AI_GEN_VIDEO = None

# Folders:
DOWNLOADS_FOLDER = "./downloads/"
UPLOADS_FOLDER = "./uploads/"
AUDIO_FOLDER = "./audio/"
VOICE_FOLDER = "./voice/"


# Prices per 1M tokens models:
PRICE = {
    # OpenAI to 1M tokes:
    # New:
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