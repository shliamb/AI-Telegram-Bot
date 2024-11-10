

#### BASIC CONFIG ####

# System:
NAME_BOT = "Multimodal AI bot"
URL = "http://137.184.87.156:8000"
TIME_CORRECTION = +3 # Moscow
MIN_PAY = 1 # $ Minimum pay
RUBTOUSD = 100 # The internal exchange rate
GIFT = 0.1 # $ The amount on the account at the beginning
VOICE_THE_ANSWER = True # False or True
HISTORY_LINE_LIMIT = 30 # The number of rows in the history table that will be used
MAX_SIMBOLS = 500 # Maximum number of characters of text to compress  
DIALOG = True # History dialog
DIALOG_SUM = False # AI compress history dialog
LANGUAGE = "en"
NOTIFICATIONS = True
DIALOG_SUM = False
BACKUP_PATH = "./backup_db/"

# Language models:
AI_DEFAULT = "gemini" # gemini or openai, anthropic in future
AI_DEFAULT_MODEL_GEMINI = "gemini-1.5-flash-latest"
AI_DEFAULT_MODEL_OPENAI = "gpt-4o-mini"

# Gen Audio models:
AI_TEXT_TO_VOICE = "openai" # in - Text, Out - Voice 
AI_DEFAULT_MODEL_TEXT_TO_VOICE = "tts-1" # tts-1-hd           AI_DEFAULT_MODEL_GET_AUDIO
VOICE = "nova" # alloy, echo, fable, onyx, nova, and shimmer
VOICE_SPEED = 1.0 # 0.25 to 4.0

# Transcription voice models:
AI_VOICE_TO_TEXT = "openai"  # in - voice, out - text   
AI_DEFAULT_MODEL_VOICE_TO_TEXT = "whisper-1" # no choes  model_voice_to_text

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

# Delete files:
DEL_DOWNLOADS = True
DEL_UPLOADS = True
DEL_AUDIO = True
DEL_VOICE = True

#
# Как это работает:
# Активирую нужный пункт, в /admin добавляю новый метод оплаты - method_pay, выбираю его в select_method_pay
# под названием активированного пункта тут.
#
# Place of use pay method:
USE_SBP_TRANSFER = False
USE_MASTERCARD = True
USE_VISA = False
USE_MIRCARD = True
USE_CRIPTO = False
USE_SMS = False
USE_STARS = False
USE_TELEGRAM = False
USE_DIGITAL = False


# Prices per 1M tokens models:
NULL_TOKEN = 0
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

    'babbage-002': 0.8, # For summarizing texts, the clean price is 0.8 ???

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
    #'gemini-1.0-pro': 4, # Не срабатывает, так как не поддерживает системные инструкции, json режим, выполнение кода, лучше не пользоваться ею
    # 'text-embedding-004': 0, # Free  хз пока что как ее пользовать
    # 'aqa': 0,
    }