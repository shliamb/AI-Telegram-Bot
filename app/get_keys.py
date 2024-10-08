import os
from dotenv import load_dotenv
load_dotenv()


TELEGRAM_BOT_TOKEN = os.environ.get('telegram_bot_token')
USERNAME_API_AI = str(os.environ.get('username_api_ai'))
KEY_API_AI = str(os.environ.get('key_api_ai'))
VALUE_KEY_API_AI = str(os.environ.get('value_key_api_ai'))
USER_DB = os.environ.get('user_db')
PASSWORD_DB = os.environ.get('password_db')
ADMIN_ID = int(os.environ.get('admin_id'))
DB_NAME = os.environ.get('db_name')
