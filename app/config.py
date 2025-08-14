#### BASIC CONFIG (set it up manually): ####
HOST = "app_postgres" # app_postgres localhost
DOCKER = True # True or False
TIME_CORRECTION = + 3
URL = "http://167.99.210.245:8000"
########

# Folders:
PATH_LOGS = "/log/" if DOCKER else "./log/"
PATH_CAPTCHA_1 = "/img_captcha_1/" if DOCKER else "./img_captcha_1/"
DOWNLOAD = "/downloads/" if DOCKER else "./downloads/"
BACKUP_DB = "/backup_db/" if DOCKER else "./backup_db/"
PATH_JSON_USERS = "/json/" if DOCKER else "./json/"
UPLOADS_FOLDER = "/uploads/" if DOCKER else "./uploads/"
AUDIO_FOLDER = "/audio/" if DOCKER else "./audio/"
VOICE_FOLDER = "/voice/" if DOCKER else "./voice/"

# System:
NAME_BOT = "Main AI: [ ChatGPT, Gemini, Claude, DeepSeek ]"
MIN_PAY = 1 # $ Minimum pay
RUBTOUSD = 100 # The internal exchange rate
LIMIT_STAT = 500 # CSV file last 500
GIFT = 0.1 # $ The amount on the account at the beginning
VOICE_THE_ANSWER = False # False or True
HISTORY_LINE_LIMIT = 15 # The number of rows in the history table that will be used   ----- 10 25 30 50 !!! Сделать в настройках изменяемые..
MAX_SIMBOLS = 500 # Maximum number of characters of text to compress  
DIALOG = True # History dialog
DIALOG_SUM = False # AI compress history dialog
LANGUAGE = "en"
NOTIFICATIONS = True
MAX_LEN = 4000 #4096
MAX_SIZE_DOC = 3 # Возможный максимум передоваемого файла в mb
EXTENS_DOC_SUPPORT = ["docx", "pdf", "md", "txt", "json"]

# Language models:
AI_DEFAULT = "gemini" # gemini, openai, anthropic, deepseek, grok
AI_DEFAULT_MODEL_GEMINI = "gemini-2.5-flash"
AI_DEFAULT_MODEL_OPENAI = "o3"
AI_DEFAULT_MODEL_CLAUDE = "claude-3-5-haiku-latest"
AI_DEFAULT_MODEL_DEEPSEEK = "deepseek-chat"
AI_DEFAULT_MODEL_GROK = "grok-3-mini-latest"

# Gen Audio models:
AI_TEXT_TO_VOICE = "openai" # in - Text, Out - Voice 
AI_DEFAULT_MODEL_TEXT_TO_VOICE = "gpt-4o-mini-tts" # tts-1-hd gpt-4o-mini-tts           AI_DEFAULT_MODEL_GET_AUDIO
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


# # Assistent OpenAI END-POINT:
# LIST_ASSIST_OA = "/api/oa-assist-list/"
# DEL_ASSIST_OA = "/api/oa-assist-del/"
# DEL_THREAD_OA = "/api/oa-thread-del/"
# RETRIEVE_OA = "/api/oa-assist-retrieve/"
# RETUEN_RESULT_OA = "/api/oa-return-result-assist/"
# RUN_ASSIST_CUSTOM_0525 = "/api/oa-assist-custom-0525/"

# DEFAULT_MODEL_ASSIST_OA = "gpt-4o"


# Prices per 1M tokens models:
NULL_TOKEN = 0
PRICE = {
    # OpenAI to 1M tokes:
    'gpt-5': 13.5,
    'gpt-5-chat-latest': 13.5,
    'gpt-5-mini': 2.7,
    'gpt-5-nano': 0.54,

    'gpt-4.5-preview': 270,  # gpt-4.5-preview-2025-02-27
    'gpt-4.1': 12, # 1 million Contex gpt-4.1-2025-04-14
    'o3-pro': 120,  # o3-pro-2025-06-10   !!!!
    'o3': 12,  # o3-2025-04-16
    'o1-pro': 900, # o1-pro-2025-03-19
    'o1': 90, # o1-2024-12-17

    'chatgpt-4o-latest': 24,
    'gpt-4o-mini': 1.8,  # no vision

    # Hidden:
    'gpt-4.1-mini': 2.4, # gpt-4.1-mini-2025-04-14
    'gpt-4.1-nano': 0.6, # gpt-4.1-nano-2025-04-14
    'o1-preview': 90,
    'o4-mini': 6.6, # o4-mini-2025-04-16
    'o3-mini': 6.6, # 
    'o1-mini': 6.6,
    # 'gpt-4o-mini-search-preview': 0.9,
    # 'gpt-4o-search-preview': 15,
    # 'computer-use-preview': 18,
    'gpt-4o': 24,
    'gpt-4o-2024-05-13': 24,
    'gpt-4o-2024-08-06': 15,
    'gpt-4o-mini-2024-07-18': 1.8, # no vision
    'gpt-4-turbo-2024-04-09': 48,

    # Google Gemini to 1M tokens:
    'gemini-2.5-pro': 13.5, # Maximum input tokens 1,048,576
    'gemini-2.5-flash': 3.36, # $3.50  - Text output (thinking- response and reasoning) 3.36
    'gemini-2.5-flash-lite-preview-06-17': 0.6,
    # Hidden:
    'gemini-2.0-flash': 0.6, # 15,
    'gemini-2.0-flash-lite': 0.45,
    'gemini-1.5-pro-latest': 3.75, # 15, 
    'gemini-1.5-flash-latest': 0.225, # 0.8,
    'gemini-1.5-flash-8b': 0.5,

    # Ilon Mask Grok to 1M tokens:
    'grok-4-0709': 21.6, # 256 000
    'grok-3-latest': 21.6, # Contex 131072,
    'grok-3-mini-latest': 0.96, # Contex 131072,

    # Hidden:
    'grok-3-fast-latest': 21.6, # Contex 131072,
    'grok-3-mini-fast-latest': 5.52, # Contex 131072,
    'grok-vision-beta': 24, # Text, Image = 6, Contex 8192, 
    'grok-2-vision-latest': 14.4, # Text, Image = 2.4, Contex 32768, 
    'grok-2-latest': 14.4, # Only Text, Contex 131072, 
    'grok-beta': 24, # Only Text, Contex 131072, 

    # DeepSeek:
    'deepseek-reasoner': 3.288,
    'deepseek-chat': 1.644,

    # Antropic Claude to 1M tokens:  Context window - 200k, 
    # New:
    'claude-opus-4-1-20250805': 108,
    'claude-opus-4-20250514': 108, # claude-opus-4-20250514
    'claude-sonnet-4-20250514': 21.6, # claude-sonnet-4-20250514

    # Hidden:
    'claude-3-7-sonnet-latest': 21.6, # 200K context window Most intelligent model, with visible step‑by‑step reasoning claude-3-7-sonnet-20250219
    'claude-3-5-sonnet-latest': 21.6, # output 8192 tokens
    'claude-3-5-haiku-latest': 5.76, # no vision and output 8192 tokens
    'claude-3-opus-latest': 108, # 4096 tokens
    'claude-3-sonnet-20240229': 21.6, # 4096 tokens
    'claude-3-haiku-20240307': 1.8, # 200K context window


    # Images to one img:
    'gpt-image-1': 60,
    'dall-e-3-1024': 0.048,
    'dall-e-3-1792': 0.096,

    'dall-e-3-hd-1024': 0.096,
    'dall-e-3-hd-1792': 0.144,

    'dall-e-2-1024': 0.024,
    'dall-e-2-512': 0.0216,
    'dall-e-2-256': 0.0192,

    # Audio to 1M characters:
    'tts-1': 18, # / 1M characters
    'tts-1-hd': 36, # / 1M characters
    'gpt-4o-mini-tts': 15.12, # / 1M characters
    'whisper-1': 0.0072, # minute (rounded to the nearest second)

    }