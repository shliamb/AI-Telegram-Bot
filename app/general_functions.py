from worker_db import add_statistics, read_user, update_user
from config import PRICE
from datetime import datetime, timezone, timedelta
from config import TIME_CORRECTION
import logging
import random
import string
import tiktoken
import os
import re
import base64
import aiofiles
import asyncio
from mutagen import File
from io import BytesIO






# Encode the image
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

def random_name_2X() -> str:
    name = f"{random_name()}-{random_name()}"
    return name

# Combined escaping of special characters:
def escape_special_chars(text):
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
    logging.info("info: Getting the day and time from the server")
    return day or None

# UNFORMAT TIME:
async def unformat_date(date):
    day_now = str(date.strftime("%Y-%m-%d"))
    time_now = float(date.strftime("%H.%M"))
    return day_now, time_now

# in BOOL out STR TEXT UPPER:
def bool_to_str(bools, lang):
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


# Calculation of the cost of used tokens
async def calculation(data, input_data):
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
        confirm = await add_statistics(data_stat)
        if not confirm:
            print("Error: add_statistics")

        # Getting user data
        user_data = await read_user(data.get("user_id"))
        new_money = user_data.get("money") - total_price
        data_money = {"money": new_money, "user_id": data.get("user_id"),}

        # The balance was changed taking into account the expense
        confirm = await update_user(data_money)
        if not confirm:
            print("Error: update_user")

        return True
    
    except Exception as error:
        print("Error:", error)
        return False



# We consider tokens from the text to be average and I'm not sure what is correct
def tiktroken(user_content):
    # Statistic *** Ебанный костыль, пока что не знаю как подругому сделать ****   Available encodings: ['gpt2', 'r50k_base', 'p50k_base', 'p50k_edit', 'cl100k_base', 'o200k_base']
    enc = tiktoken.get_encoding("gpt2")
    tokens = enc.encode(user_content)
    used_tokens = len(tokens)
    return used_tokens



# Set model OpenAI Dall-e
def set_model_dalle(data):

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













# # Async calculating the length of an audio file:
# async def read_audio_file(file_path: str) -> float: # mp3 (ID3v1 и ID3v2), flac, ogg Vorbis, acc (and M4A), wav, wma (limited support), aiff
#     async with aiofiles.open(file_path, 'rb') as f:
#         content = await f.read()
#         audio_file = BytesIO(content)
        
#         # Загружаем аудиофайл с помощью mutagen
#         audio = File(audio_file)
        
#         if audio is None or audio.info is None:
#             print("The audio file could not be uploaded.")
#             logging.error("The audio file could not be uploaded.")
#         else:
#             # print(audio.pprint())
#             duration = audio.info.length  # Получаем длину в секундах
#             if duration:
#                 length_sound = float(f"{duration:.2f}")
#                 return length_sound


# Remove File OS
# async def remove_file_os(file_path):
#     if os.path.exists(file_path):
#         os.remove(file_path)
#         #print(f"The {file_path} file was successfully deleted.")
#         logging.info(f"The {file_path} file was successfully deleted.")
#         return True
#     else:
#         #print(f"The {file_path} file does not exist.")
#         logging.error(f"The {file_path} file does not exist.")
#         return False

# # Remove File OS Async
# async def remove_file_os(file_path):
#     loop = asyncio.get_running_loop()
    
#     if await loop.run_in_executor(None, os.path.exists, file_path):
#         await loop.run_in_executor(None, os.remove, file_path)
#         logging.info(f"The {file_path} file was successfully deleted.")
#         return True
#     else:
#         logging.error(f"The {file_path} file does not exist.")
#         return False
    

# # Cleaner model AI
# async def cleaner_model(name_model):
#     pattern = r"(dall-e-\d)"
#     match = re.search(pattern, name_model)
#     if match:
#         match = match.group(1)
#     return match



  

# # Async save file
# async def write_file(file, file_path):
#     async with aiofiles.open(file_path, "wb") as buffer:
#         while content := await file.read(1024):  # Читаем файл порциями по 1024 байта
#             await buffer.write(content)
#             return




