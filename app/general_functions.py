from worker_db import add_statistics, read_user, update_user
from config import PRICE, TIME_CORRECTION, PATH_LOGS
from setup_config_logger import setup_logger
logger_bot = setup_logger('bot', f'{PATH_LOGS}bot.log')
from datetime import datetime, timezone, timedelta
import random
import string
import tiktoken
import os
# import re
import base64
import aiofiles
import asyncio
from mutagen import File
from io import BytesIO




# Encode the image base64:
async def encode_file(file_path):
  async with aiofiles.open(file_path, "rb") as file:
    content = await file.read()
    return base64.b64encode(content).decode('utf-8')

# Random name to file:
def random_name() -> str:
    random_num = str(random.randint(11, 98))
    random_letters = string.ascii_lowercase + string.ascii_uppercase
    text = random.choice(random_letters) + random_num
    return text

# Run Random name:
def random_name_2X() -> str:
    name = f"{random_name()}-{random_name()}"
    return name

# Combined escaping of special characters:
def escape_special_chars(text: str) -> str:
    if not text:
       print("Error: There is no content in the model's response.")
       return

    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text

# GET DAY AND TIME:
async def day_utcnow(time_zone=None):
    if not time_zone:
       time_zone = TIME_CORRECTION
    utc_zone = timezone.utc
    a = datetime.now(timezone.utc).replace(tzinfo=utc_zone)
    a = a + timedelta(hours=time_zone)
    day_str = a.strftime("%Y-%m-%d %H:%M:%S")
    day = datetime.strptime(day_str, '%Y-%m-%d %H:%M:%S')
    #logging.info("info: Getting the day and time from the server")
    return day or None

# UNFORMAT TIME:
async def unformat_date(date) -> dict:
    day = str(date.strftime("%Y-%m-%d"))
    time = str(date.strftime("%H.%M"))
    return {"day": day, "time": time}

# in BOOL out STR TEXT UPPER:
def bool_to_str(bools: bool, lang: str) -> str:
    if bools == True:
        if lang == "ru":
            text = "Включено"
        elif lang == "en":
            text = "On"
    elif bools == False:
        if lang == "ru":
            text = "Выключено"
        elif lang == "en":
            text = "Off"
    return text.upper()

# Calculation of the cost of used tokens:
async def calculation(data: dict, input_data: str) -> bool:
    one_price, use_model, data_stat = None, None, {}
    
    try:
        for key, value in PRICE.items():
            if input_data == "text" and key == data.get("model_language"):
                one_price = value / 1000000 # Price 1 token to USD
                use_model = data.get("model_language")
                total_price = one_price * data.get("used_tokens")
                data_stat["tokens"] = data.get("used_tokens")
                break
            elif input_data == "gen_img" and key == data.get("model_draw"):
                one_price = value
                use_model = data.get("model_draw")
                total_price = one_price * data.get("n_number")
                data_stat["img"] = data.get("n_number")
                break
            elif input_data == "voice_to_text" and key == data.get("model_voice_to_text"):
                one_price = value # Price 1 min
                use_model = data.get("model_voice_to_text")
                total_price = one_price * data.get("min")
                data_stat["min"] = data.get("min")
                break
            elif input_data == "text_to_voice" and key == data.get("model_text_to_voice"):
                one_price = value / 1000000 # Price 1 charaster to USD
                use_model = data.get("model_text_to_voice")
                total_price = one_price * data.get("used_tokens")
                data_stat["tokens"] = data.get("used_tokens")
                break

        # Collecting data
        data_stat["user_id"] = data.get("user_id")
        data_stat["date"] = await day_utcnow()
        data_stat["model"] = use_model
        data_stat["price_1"] = one_price
        data_stat["price"] = total_price

        # Save statistic data to DB:
        if not await add_statistics(data_stat):
            logger_bot.error("Error: add_statistics")

        # Getting user data
        user_data = await read_user(data.get("user_id"))
        new_money = user_data.get("money") - total_price
        data_money = {"money": new_money, "user_id": data.get("user_id"), "last_visit": await day_utcnow()}

        # The balance was changed taking into account the expense
        if not await update_user(data_money):
            logger_bot.error("Error: update_user")

        return True
    
    except Exception as error:
        logger_bot.error("Error:", error)
        return False

# Counts the number of tokens from the text:
def tiktroken(user_content) -> int:
    # Statistic *** Ебанный костыль, пока что не знаю как подругому сделать ****   Available encodings: ['gpt2', 'r50k_base', 'p50k_base', 'p50k_edit', 'cl100k_base', 'o200k_base']
    enc = tiktoken.get_encoding("gpt2")
    tokens = enc.encode(user_content)
    used_tokens = len(tokens)
    return used_tokens

# Set right model OpenAI Dall-e:
def set_model_dalle(data: dict) -> str:
    quality = data.get("quality")
    size = data.get("size")
    model = data.get("model_draw")

    if data.get("ai_draw") == "openai":
        # Choosing a price list
        if model and model == "dall-e-3":
            if quality and quality == "hd":
                if size and size == "1024x1024":
                    model = "dall-e-3-hd-1024"
                elif size and size == "1792x1024" or size and size == "1024x1792":
                    model = "dall-e-3-hd-1792"
                else:
                    model = "dall-e-3-hd-1024"
            elif quality and quality == "standard":
                if size and size == "1024x1024":
                    model = "dall-e-3-1024"
                elif size and size == "1792x1024" or size and size == "1024x1792":
                    model = "dall-e-3-1792"
                else:
                    model = "dall-e-3-1024"
            else:
                model = "dall-e-3-1024"

        elif model and model == "dall-e-2":
            if size and size == "1024x1024":
                model = "dall-e-2-1024"
            elif size and size == "512x512":
                model = "dall-e-2-512"
            elif size and size == "256x256":
                model = "dall-e-2-256"
            else:
                model = "dall-e-2-1024"
        else:
            model = "dall-e-3-1024"
        return model

# Get activ use pay method:
def get_use_met_all(n) -> str:
    if n.get("use_sbp_transfer") is True:
        use = "use_sbp_transfer"
    elif n.get("use_mastercard") is True:
        use = "use_mastercard"
    elif n.get("use_visa") is True:
        use = "use_visa"
    elif n.get("use_mircard") is True:
        use = "use_mircard"
    elif n.get("use_cripto") is True:
        use = "use_cripto"
    elif n.get("use_sms") is True:
        use = "use_sms"
    elif n.get("use_stars") is True:
        use = "use_stars"
    elif n.get("use_telegram") is True:
        use = "use_telegram"
    elif n.get("use_digital") is True:
        use = "use_digital"
    else:
        use = "not use"
    return use

# Async save file:
async def write_file(file, file_path):
    async with aiofiles.open(file_path, "wb") as buffer:
        while content := await file.read(1024):  # Читаем файл порциями по 1024 байта
            await buffer.write(content)
            return

# Remove File OS Async
async def remove_file_os(file_path):
    loop = asyncio.get_running_loop()
    
    if await loop.run_in_executor(None, os.path.exists, file_path):
        await loop.run_in_executor(None, os.remove, file_path)
        logger_bot.info(f"The {file_path} file was successfully deleted.")
        return True
    else:
        logger_bot.error(f"The {file_path} file does not exist.")
        return False










