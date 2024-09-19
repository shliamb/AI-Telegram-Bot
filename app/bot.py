from get_keys import TELEGRAM_BOT_TOKEN, USERNAME_API_AI, KEY_API_AI, VALUE_KEY_API_AI, USER_DB, PASWORD_DB, ADMIN_ID
from config import DOWNLOADS_FOLDER, AI_DEFAULT, AI_DEFAULT_MODEL_GEMINI, AI_DEFAULT_MODEL_OPENAI, VOICE_THE_ANSWER, VOICE_FOLDER, AUDIO_FOLDER


import logging
# in terminal:
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# in file:
# logging.getLogger('aiogram').propagate = False # Блокировка логирование aiogram до его импорта
# logging.basicConfig(level=logging.INFO, filename='./log/bot.log', filemode='a', format='%(levelname)s - %(asctime)s - %(name)s - %(message)s',) # При деплое активировать логирование в файл
import re
import random
import os
import asyncio
import requests
from io import StringIO, BytesIO
import uuid
from pathlib import Path # Работа с файловыми путями 
# from datetime import datetime, timezone, timedelta
# import time
# import sys
import csv
# import datetime
# Aiogram
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold
from aiogram.filters import CommandStart, Command, Filter
from aiogram.types import (Message, BotCommand, LabeledPrice, ContentType,
                            InputFile, Document, PhotoSize, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# Service
# from worker_db import get_user_by_id, get_user_by_username, update_user, adding_user, get_all_data_user_by_username, get_last_statistics
# from general_functions import day_utcnow, unformat_date
# from config import money_to_start, my_app_key, time_correction, min_pay
from mod_gemini import mod_gemini_chat
from mod_openai import mod_openai_chat
from mod_get_voice_in_text_openai import get_voice_openai
from mod_get_text_in_voice_openai import get_text_openai
from general_functions import escape_special_chars, random_name_2X





bot = Bot(TELEGRAM_BOT_TOKEN, parse_mode="markdown") # Initialize Bot instance with a default parse mode which will be passed to all API calls
dp = Dispatcher() # All handlers should be attached to the Router (or Dispatcher)




#########
# Get User_ID
def user_id(action) -> int:
    return action.from_user.id

# Show Typing bot
async def typing(action) -> None:
    await bot.send_chat_action(action.chat.id, action='typing')
    # await asyncio.sleep(5)


#### Push /start ####
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await typing(message)

    id = user_id(message)
    name = message.from_user.username
    full_name = message.from_user.full_name
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    # Choosing a name user
    about = name if name else (first_name if first_name else (last_name if last_name else "User"))

    await message.answer(f"hi <strong>{about}</strong>! Get high", parse_mode="HTML")








# TEXT
async def mod_tex(ai, data):
    if ai == "gemini":
        answer = await mod_gemini_chat(data)
    elif ai == "openai":
        answer = await mod_openai_chat(data)
    return answer


# Attempts to give a response to the user:
async def try_answer_bot(message, answer, voice_answer):
    try:
        await message.reply(answer, parse_mode="MarkdownV2")
    except:
        try:
            await message.reply(answer, parse_mode="HTML")
        except:
            escape_text = escape_special_chars(answer)
            await message.reply(escape_text)
    
    if voice_answer is False:
        return
    
    if len(answer) >= 4096:
        await message.reply("🇺🇸 *EN:* Text max 4096 characters.\n🇷🇺 *RU:* Текст max 4096 символа.", parse_mode="markdown") # MarkdownV2
        return
    
    data_audio = {
        "user_content": answer,
        #...
    }

    voice_answer_file_path = await get_voice_openai(data_audio)

    if os.path.exists(voice_answer_file_path) and os.path.getsize(voice_answer_file_path) > 0:
        await bot.send_document(chat_id=message.from_user.id, document=types.input_file.FSInputFile(voice_answer_file_path))
    else:
        print(f"The file is empty or missing - {voice_answer_file_path}")


# Set State
class Form_img_text(StatesGroup):
    first_stage = State()
    #second_stage = State()



# PHOTO + DOC + Text
@dp.message(Form_img_text.first_stage, F.content_type.in_({'text'}))
async def mod_photo_text(message: Message, state: FSMContext):
    # Из прошлого State
    data = await state.get_data()
    ai = data.get('ai')
    voice_answer = data.get('voice_answer')

    if message.text:
        data["user_content"] = message.text

    if ai == "gemini":
        answer = await mod_gemini_chat(data)
    elif ai == "openai":
        answer = await mod_openai_chat(data)
    if answer:
        # Attempts to give a response to the user:
        await try_answer_bot(message, answer, voice_answer) 

    await state.clear()



# PHOTO + DOC + Caption
async def mod_photo_caption(ai, data):
    if ai == "gemini":
        answer = await mod_gemini_chat(data)
    elif ai == "openai":
        answer = await mod_openai_chat(data)
    return answer



#### Addressing AI:
@dp.message(F.content_type.in_({'text', 'document', 'photo', 'audio', 'voice', })) # 'location' 'contact' 'video_note'  'video'  'sticker'
async def second_function(message: types.Message, state: FSMContext):

    ai = AI_DEFAULT
    if ai == "openai":
        model = AI_DEFAULT_MODEL_OPENAI
    elif ai == "gemini":
        model = AI_DEFAULT_MODEL_GEMINI
    
    voice_answer = VOICE_THE_ANSWER


    file_path, question, received_object, user_content, photo_file_name, name_file, caption, system_content = (None,) * 8

    await typing(message)
    id = user_id(message)
    caption = message.caption  # Получаем caption изображения

    #### TEXT:
    if message.content_type == 'text':
        received_object = "text"
        question = message.text

    #### DOCUMENTS:
    elif message.content_type == 'document': # Любые форматы, а потому внутри нужна логика проверки
        received_object = "document"
        file_id = message.document.file_id
        little = random_name_2X()
        name_file = little + "-" + message.document.file_name

        # Get extension:
        match = re.search(r'\.([^.]+)$', name_file)

        if match:
            extension = match.group(1)  # Получаем расширение без точки
        else:
            logging.error(f"Dont support file - {name_file}")
            return
        
        # Installation is not supported temporarily:
        set_extension = {"doc", "docx", "odt", "rtf", "txt", "xls", "xlsx", "ods", "ppt", "pptx", "odp", "pdf", "html", "htm", "csv", "md", "xml", "json"}

        if extension in set_extension:
            await message.answer(f"The bot does not support this file - {name_file}", parse_mode="markdown")
            logging.error(f"Dont support file - {name_file}")
            return

        file_path = f'{DOWNLOADS_FOLDER}{name_file}'
        file = await bot.get_file(file_id)
        await bot.download_file(file.file_path, file_path)
        # await message.reply("Документ сохранен!")


    #### PHOTO:
    elif message.content_type == 'photo': # Telegram always saves in jpg in compress
        received_object = "photo"
        photo = message.photo[-1]  # Используем самый большой размер фотографии
        file_id = photo.file_id
        file = await bot.get_file(file_id)
        little = random_name_2X()
        photo_file_name = f"photo-{little}-{message.photo[-1].file_id}.jpg"
        file_path = f'{DOWNLOADS_FOLDER}{photo_file_name}'
        await bot.download_file(file.file_path, file_path)
        # await message.reply("Фотография сохранена!")


    #### AUDIO:
    elif message.content_type == 'audio':
        received_object = "audio"
        audio = message.audio
        file_id = audio.file_id
        little = random_name_2X()
        audio_file_name = f"audio-{little}-{audio.file_id}.mp3"
        file = await bot.get_file(file_id)
        file_path = f'{AUDIO_FOLDER}{audio_file_name}'
        await bot.download_file(file.file_path, file_path)
        # await message.reply("Аудиофайл сохранен!")


    #### VOICE:
    elif message.content_type == 'voice':
        received_object = "voice"
        voice = message.voice
        file_id = voice.file_id
        little = random_name_2X()
        voice_file_name = f"voice-{little}-{voice.file_id}.ogg"
        file = await bot.get_file(file_id)
        file_path = f'{VOICE_FOLDER}{voice_file_name}'
        await bot.download_file(file.file_path, file_path)
        # await message.reply("Голосовое сообщение сохранено!")

    #### None, why not?)
    if received_object is None:
        await message.reply("Dont support file")
        logging.error(f"Dont support file")
        return

    # Проверка в базе данных выбор пользователя - выбрана openai или Gemini или др., \
    # затем конкретно какая из версий, если нет этого то по умолчанию.
    #system_content = "отвечай по русски" # Удалить нахер когда апи поправлю... твою мать...
    # voice_answer ?
    # ai
    # model
    # system_content


    data = {
        "ai": ai,
    }

    if model:
        data["model"] = model
    if system_content:
        data["system_content"] = system_content


    # if PHOTO and some DOCUMENTS like a image:
    if received_object == "document" or received_object == "photo":

        if file_path:
            data["file_path"] = file_path
        if name_file:
            data["name_file"] = name_file
        elif photo_file_name:
            data["name_file"] = photo_file_name
        if voice_answer:
            data["voice_answer"] = voice_answer
        if caption:
            data["user_content"] = caption
            answer = await mod_photo_caption(ai, data)
            if answer is None:
                return
            # Attempts to give a response to the user:
            await try_answer_bot(message, answer, voice_answer) 
            return
        
        await state.update_data(data=data) # Прикрепление в state данных
        await message.reply("🇺🇸 *EN:* Question about the attached image:\n🇷🇺 *RU:* Вопрос по прикрепленному изображению:", parse_mode="markdown")
        await state.set_state(Form_img_text.first_stage) # Ожидание следующего шага



    # if only TEXT:
    elif received_object == "text":

        if question:
            data["user_content"] = question

        answer = await mod_tex(ai, data)

        if answer is None:
            return
        
        # Attempts to give a response to the user:
        await try_answer_bot(message, answer, voice_answer) 

        await state.clear()



    # if VOICE:
    elif received_object == "voice":
        if ai == "gemini":
            answer = await get_text_openai(data) # Поменять когда будет и Гугль, но пока он тильки на енглишь
        elif ai == "openai":
            answer = await get_text_openai(data)
        #return answer








# # PHOTO + DOC + Text
# async def mod_photo_text(ai, data):
#     if ai == "gemini":
#         answer = await mod_gemini_chat(data)
#     elif ai == "openai":
#         answer = await mod_openai_chat(data)
#     return answer


# # TEXT
# async def mod_tex(ai, data):
#     if ai == "gemini":
#         answer = await mod_gemini_chat(data)
#     elif ai == "openai":
#         answer = await mod_openai_chat(data)
#     return answer


# AUDIO


















# main def polling
async def main_bot() -> None:
    await dp.start_polling(bot, skip_updates=False) # skip_updates=False обрабатывать каждое сообщение с серверов Telegram, важно для принятия платежей


# Start polling
if __name__ == "__main__":
    try:
        asyncio.run(main_bot())
    except Exception as e:
        logging.error(f"An error occurred: {e}.")
        print(f"An error occurred: {e}.")