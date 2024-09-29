from datetime import datetime, timezone, timedelta
from config import TIME_CORRECTION
import logging
import random
import string
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
















# # Calculation of the cost of used tokens
# async def calculation(username, model_version, used_tokens, input_data):
#     one_tok_price = None
    
#     for key, value in price.items():
#         if key == model_version:
#             if input_data == "text":
#                 one_tok_price = value / 1000000 # Price 1 token to USD
#                 break
#             elif input_data == "img":
#                 one_tok_price = value
#                 break
#             elif input_data == "audio":
#                 one_tok_price = value # Price 1 min
#                 break
        
#     if one_tok_price == None:
#         print(f"The model {model_version} was not found in the price list")
#         logging.error(f"The model {model_version} was not found in the price list")
#         one_tok_price = 0.000095 # Sorry..

#     total_price = one_tok_price * used_tokens

#     # Collecting data
#     data_stat = {
#         "username_table_stat": username,
#         "time": await day_utcnow(),
#         "use_model": model_version,
#         "sesion_token": used_tokens,
#         "price_1_tok": one_tok_price,
#         "total_price": total_price,
#     }

#     # Save statistic data to DB:
#     await add_statistic(data_stat)

#     # Getting user data
#     user_data = await get_user_by_username(username)
#     new_money = user_data.money - total_price
#     data_money = {"money": new_money}

#     # The balance was changed taking into account the expense
#     await update_user_by_username(username, data_money)

#     return total_price


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


