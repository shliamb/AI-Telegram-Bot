from get_keys import TELEGRAM_BOT_TOKEN, USERNAME_API_AI, KEY_API_AI, VALUE_KEY_API_AI, USER_DB, PASSWORD_DB, ADMIN_ID
from config import DOWNLOADS_FOLDER, AI_DEFAULT, AI_DEFAULT_MODEL_GEMINI, AI_DEFAULT_MODEL_OPENAI, VOICE_THE_ANSWER, VOICE_FOLDER, AUDIO_FOLDER, GIFT, DEFAULT_DALL_E, AI_DRAW, AI_VOICE, AI_AUDIO, DIALOG, DIALOG_SUM, IMG_SIZE, N_NUMBER, VOICE, VOICE_SPEED, IMG_SIZE, N_NUMBER, IMG_QUALITY, IMG_STYLE, AI_DEFAULT_MODEL_GET_AUDIO, AI_DEFAULT_MODEL_GET_VOICE, LANGUAGE, NOTIFICATIONS


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
from aiogram.types import (Message, BotCommand, LabeledPrice, ContentType, InputFile, Document, PhotoSize, \
        ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton)
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
from mod_dall_e import mod_openai_dall_e
from general_functions import escape_special_chars, random_name_2X, day_utcnow, bool_to_str
from worker_db import add_user, read_user, update_user
from texts import start_ru, start_en




bot = Bot(TELEGRAM_BOT_TOKEN, parse_mode="markdown") # Initialize Bot instance with a default parse mode which will be passed to all API calls
dp = Dispatcher() # All handlers should be attached to the Router (or Dispatcher)




# To Do:
# Сделать в меню отдельный блок объявлений или новосте, так же кнопку отказа от уведомлений.
#






#########
# Get User_ID
def user_id(action) -> int:
    return action.from_user.id

# Show Typing bot
async def typing(action) -> None:
    await bot.send_chat_action(action.chat.id, action='typing')




#### Push /start ####
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await typing(message)


    # MENU
    bot_commands = [
        BotCommand(command="/reset", description="RESET"),
        BotCommand(command="/menu", description="MENU"),
        BotCommand(command="/prices", description="PRICES"),
        BotCommand(command="/help", description="HELP"),
    ]
    await bot.set_my_commands(bot_commands)


    id = user_id(message)
    name = message.from_user.username
    full_name = message.from_user.full_name
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    # Choosing a name user
    about = name if name else (first_name if first_name else (last_name if last_name else "User"))

    is_user_to_db = await read_user(id)

    if is_user_to_db:
        await message.answer(f"🇺🇸 *EN:* Hi {about}! You are already initiated into the bot. You can start using it.\n\n🇷🇺 *RU:* Привет {about}! Вы уже инициированы в боте. Можете приступить к пользованию.", parse_mode="Markdown")
        return
    
    date = {
        "user_id": id,
        "name": name,
        "full_name": full_name,
        "first_name": first_name,
        "last_name": last_name,
        "money": GIFT,
        "last_visit": await day_utcnow(),
    }

    confirm = await add_user(date)

    if confirm:
        await message.answer(f"🇺🇸 *EN:* Hello, {about}! {start_en}\n\n🇷🇺 *RU:* Здравствуйте, {about}! {start_ru}", parse_mode="Markdown")
        return confirm
    
    return






#### WORK MENU ####

# RESET
@dp.message(Command('reset'))
async def start(message: types.Message):

    await message.reply(f"I reset the history. You're clean)", parse_mode="Markdown")
    #await bot.answer_callback_query(callback_query.id)



# MENU
@dp.message(Command('menu'))
async def main_menu(message: types.Message):

    id = user_id(message)


    data = await read_user(id)


    # print(data)
    language = data["language"] if data.get("language") is not None else LANGUAGE
    ai = data["ai"] if data.get("ai") is not None else AI_DEFAULT
    dialog = data["dialog"] if data.get("dialog") is not None else DIALOG
    dialog = bool_to_str(dialog, language)
    notifications = data["notifications"] if data.get("notifications") is not None else NOTIFICATIONS
    notifications = bool_to_str(notifications, language)
    dialog_sum = data["dialog_sum"] if data.get("dialog_sum") is not None else DIALOG_SUM
    dialog_sum = bool_to_str(dialog_sum, language)
    voice_answer = data["voice_answer"] if data.get("voice_answer") is not None else VOICE_THE_ANSWER
    voice_answer = bool_to_str(voice_answer, language)
    if ai == "openai":
        def_model_language = AI_DEFAULT_MODEL_OPENAI
    elif ai == "gemini":
        def_model_language = AI_DEFAULT_MODEL_GEMINI
    model_language = data["model_language"] if data.get("model_language") is not None else def_model_language
    ai_draw = data["ai_draw"] if data.get("ai_draw") is not None else AI_DRAW
    model_draw = data["model_draw"] if data.get("model_draw") is not None else DEFAULT_DALL_E
    img_size = data["img_size"] if data.get("img_size") is not None else IMG_SIZE
    img_quality = data["img_quality"] if data.get("img_quality") is not None else IMG_QUALITY
    img_style = data["img_style"] if data.get("img_style") is not None else IMG_STYLE
    ai_voice = data["ai_voice"] if data.get("ai_voice") is not None else AI_VOICE
    model_voice = data["model_voice"] if data.get("model_voice") is not None else AI_DEFAULT_MODEL_GET_VOICE
    ai_audio = data["ai_audio"] if data.get("ai_audio") is not None else AI_AUDIO
    model_audio = data["model_audio"] if data.get("model_audio") is not None else AI_DEFAULT_MODEL_GET_AUDIO
    voice = data["voice"] if data.get("voice") is not None else VOICE
    voice_speed = data["voice_speed"] if data.get("voice_speed") is not None else VOICE_SPEED
    money = data.get("money")
    system_content = True if data.get("system_content") is not None else False
    system_content = bool_to_str(system_content, language)


    menu_ru = f'''

<b>⚙️ Настройки:</b>


<b>Язык: {language.upper()}</b>
   - /en — Английский
   - /ru — Русский

<b>Уведомления: {notifications}</b>
   - /notif_on — Вкл уведомления
   - /notif_off — Выкл уведомления

<b>История диалога: {dialog}</b>
   - /dialog_on — Вкл диалог
   - /dialog_off — Выкл диалог

<b>Сжатие истории: {dialog_sum}</b>
   - /sum_on — Вкл сжатие диалога
   - /sum_off — Вык сжатие диалога

<b>Аудио ответ: {voice_answer}</b>
   - /audio_on — Вкл аудио ответ
   - /audio_off — Выкл аудио ответ

<b>ИИ: {ai.upper()} - {model_language.upper()}</b>
   <b>Выбрать модель от OpenAI:</b>
      1. /gpt_4o_mini - 1.5$ 1m ток
      2. /gpt_4o - 40$ 1m ток
      3. /gpt_4o_2024_05_13 - 40$ 1m ток
      4. /gpt_4o_2024_08_06 - 25$ 1m ток
      5. /gpt_4_turbo - 80$ 1m ток
      6. /chatgpt_4o_latest - 40$ 1m ток
   <b>Выбрать модель от Google:</b>
      1. /gemini_1_5_flash - 1.125$ 1m ток
      2. /gemini_1_0_pro - 4$ 1m ток
      3. /gemini_1_5_pro - 93.75$ 1m ток
   
<b>Генерация изо.: {ai_draw.upper()} - {model_draw.upper()}</b>
   <b>Выбрать модель от OpenAI:</b>
      1. /dall_e_3
      2. /dall_e_2
   <b>Выбрать модель от Midjourney:</b>
      1. /midjourney
   <b>OpenAI размер изо: {img_size.upper()}</b>
      1. /1792x1024
      2. /1024x1792
      3. /1024x1024
   <b>OpenAI качество изо: {img_quality.upper()}</b>
      1. /standard
      2. /hd
   <b>OpenAI стиль изо: {img_style.upper()}</b>
      1. /vivid
      2. /natural

<b>Распоз. голоса: {ai_voice.upper()} - {model_voice.upper()}</b>
   <b>OpenAI выбрать модель:</b>
      1. /whisper_1

<b>Генерация голоса: {ai_audio.upper()} - {model_audio.upper()}</b>
   <b>Выбрать модель от OpenAI:</b>
      1. /tts_1
      2. /tts_1_hd - hd и дороже
   <b>Стиль голоса: {voice.upper()}</b>
      1. /nova - женский голос
      2. /alloy
      3. /echo
      4. /fable
      5. /onyx
      6. /shimmer
   <b>Скорость голоса: {voice_speed}</b>
      1. /speed_0_75 - 0.75
      2. /speed_1 - 1.0
      3. /speed_1_25 - 1.25

<b>Инструкции для ИИ: {system_content}</b>
   - /system_content — добавить
   - /get_sys_content - посмотреть

<b>Баланс счета: {money} $</b>
   - /add_money — пополнить

<b>Скачать отчеты:</b>
   - /get_stat — статистика 

<b>😋 Новые возможности:</b>
   - можно передать изображение и обсудить его с ИИ,
   - можно передать голосовое сообщение, ИИ ответит,
   - можно попросить нарисовать, ИИ нарисует.

    '''




    menu_en = f'''

<b>⚙️ Settings:</b>


<b>Language: {language.upper()}</b>
   - /en — English
   - /ru — Russian

<b>Notifications: {notifications}</b>
   - /notif_on — On notifications
   - /notif_off — Off notifications

<b>History of dialogue: {dialog}</b>
   - /dialog_on — On the dialog
   - /dialog_off — Off the dialog

<b>History Compression: {dialog_sum}</b>
   - /sum_on — On compression
   - /sum_off — Off compression

<b>Audio response: {voice_answer}</b>
   - /audio_on — On audio response
   - /audio_off — Off audio response

<b>AI: {ai.upper()} - {model_language.upper()}</b>
   <b>Choose a model from OpenAI:</b>
      1. /gpt_4o_mini - 1.5$ 1m tok
      2. /gpt_4o - 40$ 1m tok
      3. /gpt_4o_2024_05_13 - 40$ 1m tok
      4. /gpt_4o_2024_08_06 - 25$ 1m tok
      5. /gpt_4_turbo - 80$ 1m tok
      6. /chatgpt_4o_latest - 40$ 1m tok
   <b>Choose a model from Google:</b>
      1. /gemini_1_5_flash - 1.125$ 1m tok
      2. /gemini_1_0_pro - 4$ 1m tok
      3. /gemini_1_5_pro - 93.75$ 1m tok
   
<b>Image generation: {ai_draw.upper()} - {model_draw.upper()}</b>
   <b>Choose a model from OpenAI:</b>
      1. /dall_e_3
      2. /dall_e_2
   <b>Choose a model from Midjourney:</b>
      1. /midjourney
   <b>OpenAI img size: {img_size.upper()}</b>
      1. /1792x1024
      2. /1024x1792
      3. /1024x1024
   <b>OpenAI img quality: {img_quality.upper()}</b>
      1. /standard
      2. /hd
   <b>OpenAI img style: {img_style.upper()}</b>
      1. /vivid
      2. /natural

<b>Voice recognition: {ai_voice.upper()} - {model_voice.upper()}</b>
   <b>OpenAI choose a model:</b>
      1. /whisper_1

<b>Voice generation: {ai_audio.upper()} - {model_audio.upper()}</b>
   <b>Choose a model from OpenAI:</b>
      1. /tts_1
      2. /tts_1_hd 
   <b>Voice style: {voice.upper()}</b>
      1. /nova - a woman's voice
      2. /alloy
      3. /echo
      4. /fable
      5. /onyx
      6. /shimmer
   <b>The speed of the voice: {voice_speed}</b>
      1. /speed_0_25 - 0.25
      2. /speed_1 - 1.0
      3. /speed_1_25 - 1.25

<b>System content: {system_content}</b>
   - /system_content — add text
   - /get_sys_content - watch

<b>Download reports:</b>
   - /get_stat — statistics 

<b>😋 New features:</b>
   - you can transfer the image and discuss it with the AI,
   - You can send a voice message And it will respond,
   - You can ask him to draw, And he will draw.

    '''

    if language == "ru":
        await message.answer(f"{menu_ru}", parse_mode="HTML")
    elif language == "en":
        await message.answer(f"{menu_en}", parse_mode="HTML")








# Language:
@dp.message(Command('en'))
async def en(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "language": "en"
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)

@dp.message(Command('ru'))
async def ru(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "language": "ru"
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)

# Notifications:
@dp.message(Command('notif_on'))
async def notif_on(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "notifications": True,
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)

@dp.message(Command('notif_off'))
async def notif_off(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "notifications": False,
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)

# History:
@dp.message(Command('dialog_on'))
async def dialog_on(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "dialog": True,
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)

@dp.message(Command('dialog_off'))
async def dialog_off(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "dialog": False,
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)


# History Compression:
@dp.message(Command('sum_on'))
async def sum_on(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "dialog_sum": True,
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)

@dp.message(Command('sum_off'))
async def sum_off(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "dialog_sum": False,
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)


# Audio response:
@dp.message(Command('audio_on'))
async def audio_on(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "voice_answer": True,
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)

@dp.message(Command('audio_off'))
async def audio_off(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "voice_answer": False,
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)



# OpenAI models:
@dp.message(Command('gpt_4o_mini'))
async def gpt_4o_mini(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "openai",
        "model_language": "gpt-4o-mini",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)

@dp.message(Command('gpt_4o'))
async def gpt_4o(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "openai",
        "model_language": "gpt-4o",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)

@dp.message(Command('gpt_4o_2024_05_13'))
async def gpt_4o_2024_05_13(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "openai",
        "model_language": "gpt-4o-2024-05-13",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)

@dp.message(Command('gpt_4o_2024_08_06'))
async def gpt_4o_2024_08_06(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "openai",
        "model_language": "gpt-4o-2024-08-06",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)

@dp.message(Command('gpt_4_turbo'))
async def gpt_4_turbo(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "openai",
        "model_language": "gpt-4-turbo-2024-04-09",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)

@dp.message(Command('chatgpt_4o_latest'))
async def chatgpt_4o_latest(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "openai",
        "model_language": "chatgpt-4o-latest",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)


# Google models:
@dp.message(Command('gemini_1_5_flash'))
async def gemini_1_5_flash(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "gemini",
        "model_language": "gemini-1.5-flash-latest",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)

@dp.message(Command('gemini_1_0_pro'))
async def gemini_1_0_pro_latest(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "gemini",
        "model_language": "gemini-1.0-pro-latest",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)

@dp.message(Command('gemini_1_5_pro'))
async def gemini_1_5_pro_latest(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "gemini",
        "model_language": "gemini-1.5-pro-latest",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)



# Image generation:
@dp.message(Command('dall_e_3'))
async def dall_e_3(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai_draw": "openai",
        "model_draw": "dall-e-3",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)

@dp.message(Command('dall_e_2'))
async def dall_e_2(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai_draw": "openai",
        "model_draw": "dall-e-2",
        "img_size": "1024x1024",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)

@dp.message(Command('midjourney'))
async def midjourney(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai_draw": "openai",
        "model_draw": "dall-e-3",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)

@dp.message(Command('1792x1024'))
async def dall_e_3_1792x1024(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai_draw": "openai",
        "model_draw": "dall-e-3",
        "img_size": "1792x1024",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)

@dp.message(Command('1024x1792'))
async def dall_e_3_1024x1792(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai_draw": "openai",
        "model_draw": "dall-e-3",
        "img_size": "1024x1792",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)

@dp.message(Command('1024x1024'))
async def dall_e_3_1024x1024(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai_draw": "openai",
        "model_draw": "dall-e-3",
        "img_size": "1024x1024",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)

@dp.message(Command('standard'))
async def dall_e_3_standard(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai_draw": "openai",
        "model_draw": "dall-e-3",
        "img_quality": "standard",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)

@dp.message(Command('hd'))
async def dall_e_3_hd(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai_draw": "openai",
        "model_draw": "dall-e-3",
        "img_quality": "hd",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)

@dp.message(Command('vivid'))
async def dall_e_3_vivid(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai_draw": "openai",
        "model_draw": "dall-e-3",
        "img_style": "vivid",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)

@dp.message(Command('natural'))
async def dall_e_3_natural(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai_draw": "openai",
        "model_draw": "dall-e-3",
        "img_style": "natural",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)


# Voice recognition:
@dp.message(Command('whisper_1'))
async def whisper_1(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai_audio": "openai",
        "model_audio": "whisper-1",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)


# Voice generation:
@dp.message(Command('tts_1'))
async def tts_1(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai_voice": "openai",
        "model_voice": "tts-1",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)

@dp.message(Command('tts_1_hd'))
async def tts_1_hd(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai_voice": "openai",
        "model_voice": "tts-1-hd",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)

@dp.message(Command('nova'))
async def nova(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "voice": "nova",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)


@dp.message(Command('alloy'))
async def alloy(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "voice": "alloy",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)

@dp.message(Command('echo'))
async def echo(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "voice": "echo",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)


@dp.message(Command('fable'))
async def fable(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "voice": "fable",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)


@dp.message(Command('onyx'))
async def onyx(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "voice": "onyx",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)

@dp.message(Command('shimmer'))
async def shimmer(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "voice": "shimmer",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)


@dp.message(Command('speed_0_75'))
async def speed_0_75(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "voice_speed": 0.75,
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)

@dp.message(Command('speed_1'))
async def speed_1(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "voice_speed": 1.0,
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)


@dp.message(Command('speed_1_25'))
async def speed_1_25(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "voice_speed": 1.25,
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)



# Set system content:
class Form_system(StatesGroup):
    content = State()

@dp.message(Command('system_content'))
async def system_content(message: types.Message, state: FSMContext):
    id = user_id(message)
    await message.reply("🇺🇸 *EN:* Set instructions that will help the AI understand how to interact with you.:\n\n🇷🇺 *RU:* Задайте инструкции которые помогут ИИ понять, как нужно взаимодействовать с вами:", parse_mode="Markdown")
    await state.set_state(Form_system.content)

@dp.message(Form_system.content)
async def system_content_get_text(message: types.Message, state: FSMContext):
    id = user_id(message)
    data = {
        "user_id": id,
        "system_content": message.text,
    }
    confirm = await update_user(data)

    if confirm:
        await message.reply("🇺🇸 *EN:* The system instruction has been saved.\n\n🇷🇺 *RU:* Системная инструкция сохранена.", parse_mode="Markdown")

    await state.clear()







@dp.message(Command('get_sys_content'))
async def get_sys_content(message: types.Message):
    id = user_id(message)
    data = await read_user(id)
    system_content = data["system_content"] if data.get("system_content") is not None else "is Empty"
    await message.answer(system_content, parse_mode="HTML")



@dp.message(Command('get_stat'))
async def get_stat(message: types.Message):
    id = user_id(message)
    # data = {
    #     "user_id": id,
    #     "voice_speed": 1.25,
    # }
    # confirm = await update_user(data)
    # if confirm:
    #     await main_menu(message)



























@dp.message(Command('openai'))
async def openai(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "openai"
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)

@dp.message(Command('gemini'))
async def gemini(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "gemini"
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message)














@dp.message(Command('help'))
async def start(message: types.Message):
    help = '''
    help
    '''
    await message.reply(f"{help}", parse_mode="Markdown")
















############ AI ###############
###############################

# Attempts to give a response to the user:
async def try_answer_bot(message, answer, data):
    await typing(message)

    try:
        await message.reply(answer, parse_mode="MarkdownV2")
    except:
        try:
            await message.reply(answer, parse_mode="HTML")
        except:
            escape_text = escape_special_chars(answer)
            await message.reply(escape_text)
    
    if data.get("voice_answer") is False:
        return
    
    if len(answer) >= 4096:
        await message.reply("🇺🇸 *EN:* To translate text into audio, it must be less than 4096 characters.\n\n🇷🇺 *RU:* Для перевода текста в аудио, должно быть меньше 4096 символов.", parse_mode="markdown") # MarkdownV2
        return
    

    data["user_content"] = answer

    voice_answer_file_path = await get_voice_openai(data)

    if os.path.exists(voice_answer_file_path) and os.path.getsize(voice_answer_file_path) > 0:
        await bot.send_document(chat_id=message.from_user.id, document=types.input_file.FSInputFile(voice_answer_file_path))
    else:
        print(f"The file is empty or missing - {voice_answer_file_path}")
        logging.error(f"The file is empty or missing - {voice_answer_file_path}")

    data = {}


#### GET CHAT to AI:
async def mod_tex(data, message):

    await typing(message)

    if data.get("ai") == "gemini":
        answer = await mod_gemini_chat(data)
    elif data.get("ai") == "openai":
        answer = await mod_openai_chat(data)

    if not answer:
        return
    
    # Attempts to give a response to the user:
    await try_answer_bot(message, answer, data)



#### IMG + TEXT ####
class Form_text_img(StatesGroup):
    no_caption = State()


# Add a separate description of the image:
@dp.message(Form_text_img.no_caption, F.content_type.in_({'text'}))
async def add_text_to_photo(message: Message, state: FSMContext):
    answer = None
    # Из прошлого State
    data_state = await state.get_data()
    all_data = data_state.get('all_data')

    all_data["user_content"] = message.text

    if all_data.get('ai') == "gemini":
        answer = await mod_gemini_chat(all_data)
    elif all_data.get('ai') == "openai":
        answer = await mod_openai_chat(all_data)

    if not answer:
        return

    all_data["file_path"] = None
    all_data["name_file"] = None

    # Attempts to give a response to the user:
    await try_answer_bot(message, answer, all_data)
    await state.clear()



# PHOTO input:
async def mod_photo(data, message, state: FSMContext):

    await typing(message)

    # Telegram always saves in jpg in compress
    photo = message.photo[-1]  # Используем самый большой размер фотографии
    file_id = photo.file_id
    file = await bot.get_file(file_id)
    little = random_name_2X()
    photo_file_name = f"photo-{little}-{message.photo[-1].file_id}.jpg"
    file_path = f'{DOWNLOADS_FOLDER}{photo_file_name}'
    await bot.download_file(file.file_path, file_path)

    data["file_path"] = file_path
    data["name_file"] = photo_file_name

    if data.get("user_content"):

        if data.get("ai") == "gemini":
            answer = await mod_gemini_chat(data)
        elif data.get("ai") == "openai":
            answer = await mod_openai_chat(data)

        if not answer:
            return
        
        # Attempts to give a response to the user:
        await try_answer_bot(message, answer, data)
        await state.clear()
    

    elif data.get("user_content") is None:
        await state.update_data(all_data=data)
        await message.reply("🇺🇸 *EN:* Question about the attached image:\n\n🇷🇺 *RU:* Вопрос по прикрепленному изображению:", parse_mode="Markdown")
        await state.set_state(Form_text_img.no_caption)





# DOCUMENTS input:
async def mod_documents(data, message, state: FSMContext):

    await typing(message)

    # Get id and name file:
    file_id = message.document.file_id
    little = random_name_2X()
    name_file = little + "-" + message.document.file_name

    # Get extension:
    match = re.search(r'\.([^.]+)$', name_file)
    if not match:
        logging.error(f"File dont have extension - {name_file}")
    extension = match.group(1)  # Получаем расширение без точки


    #### IMAGE ####
    if extension.lower() == "jpg" or extension.lower() == "png":

        file_path = f'{DOWNLOADS_FOLDER}{name_file}'
        file = await bot.get_file(file_id)
        await bot.download_file(file.file_path, file_path)

        data["file_path"] = file_path
        data["name_file"] = name_file

        if data.get("user_content"):

            if data.get("ai") == "gemini":
                answer = await mod_gemini_chat(data)
            elif data.get("ai") == "openai":
                answer = await mod_openai_chat(data)

            if not answer:
                return
            
            data["file_path"] = None
            data["name_file"] = None
            
            # Attempts to give a response to the user:
            await try_answer_bot(message, answer, data)
            await state.clear()

        elif data.get("user_content") is None:
            await state.update_data(all_data=data)
            await message.reply("🇺🇸 *EN:* Question about the attached image:\n\n🇷🇺 *RU:* Вопрос по прикрепленному изображению:", parse_mode="Markdown")
            await state.set_state(Form_text_img.no_caption)

    #### DOC ####
    elif extension.lower() == "doc":
        await message.reply("Серьезно...?", parse_mode="markdown")
        return

    else:
        await message.answer(f"The bot does not support this file yet, sorry - {name_file}", parse_mode="Markdown")
        logging.error(f"The bot does not support this file yet, sorry - {name_file}")
        return

# "docx", "odt", "rtf", "txt", "xls", "xlsx", "ods", "ppt", "pptx", "odp", "pdf", "html", "htm", "csv", "md", "xml", "json", "doc"





#### AUDIO input: Есть сомнения в востребованности данной функции, позже подумаю еще..

# Две кнопки, одна - перевод на анг, другая - транскрипция!!!
# async def mod_text_to_audio(ai, data, message):

    # audio = message.audio
    # file_id = audio.file_id
    # little = random_name_2X()
    # audio_file_name = f"audio-{little}-{audio.file_id}.mp3"
    # file = await bot.get_file(file_id)
    # file_path = f'{AUDIO_FOLDER}{audio_file_name}'
    # await bot.download_file(file.file_path, file_path)
    # await message.reply("Аудиофайл сохранен!")
    # if not answer:
    #     return
    
    # # Attempts to give a response to the user:
    # await try_answer_bot(message, answer, voice_answer)




#### VOICE input:
async def mod_voice_to_text(data, message):

    voice = message.voice
    file_id = voice.file_id
    little = random_name_2X()
    voice_file_name = f"voice-{little}-{voice.file_id}.ogg"
    file = await bot.get_file(file_id)
    file_path = f'{VOICE_FOLDER}{voice_file_name}'
    await bot.download_file(file.file_path, file_path)

    data["file_path"] = file_path
    data["name_file"] = voice_file_name

    if data.get("ai_voice") == "openai":
        convert_answer = await get_text_openai(data)
    # elif data.get("ai_voice") == "gemini":
    #     convert_answer = await get_text_openai(data)

    if convert_answer is None:
        return

    data["user_content"] = convert_answer
    data["file_path"] = None
    data["name_file"] = None

    answer = await mod_tex(data, message)

    if not answer:
        return
    
    # Attempts to give a response to the user:
    await try_answer_bot(message, answer, data)
 



#### DRAW ####
# Set State
class Form_draw(StatesGroup):
    draw = State()

# Confirmations to draw:
@dp.callback_query(Form_draw.draw, lambda c: c.data in ["draw", "not_draw"])
async def process_callback_draw(callback_query: types.CallbackQuery, state: FSMContext):

    chat_id = callback_query.message.chat.id
    await bot.send_chat_action(chat_id, action='typing')

    # Deleted keyboard and message:
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)     # await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=None)

    data_state = await state.get_data()
    message = data_state.get("message")
    all_data = data_state.get("all_data")

    if callback_query.data == 'draw':
        await bot.send_message(callback_query.from_user.id, "🇺🇸 *EN:* The image is already being generated, expect it.\n\n🇷🇺 *RU:* Изображение уже генерируется, ожидайте.")

        # Generation image:
        if all_data.get("ai_draw") == "openai":
            answer = await mod_openai_dall_e(all_data)
        # elif all_data.get("ai_draw") == "gemini":
        #     answer = await mod_openai_dall_e(all_data) # Sorry)))

        # Response to the user:
        await bot.send_message(callback_query.from_user.id, answer)


    elif callback_query.data == 'not_draw':

        # await bot.send_message(callback_query.from_user.id, "🇺🇸 *EN:* Waiting for the response to be generated.\n🇷🇺 *RU:* Ожидание генерации ответа.")
        sent_message = await bot.send_message(callback_query.from_user.id, "🇺🇸 *EN:* The response is already being generated, expect.\n\n🇷🇺 *RU:* Ответ уже генерируется, ожидайте.", parse_mode='Markdown')

        answer = await mod_tex(all_data, message)

        if not answer:
            return
        
        # Response to the user:
        await try_answer_bot(message, answer, all_data)

        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=sent_message.message_id) # Должен удалять сообщение выше, но чет не пашет

    await bot.answer_callback_query(callback_query.id)
    await state.clear()






# Drawing Dall-e 3:
async def mod_gen_img(data, message, state: FSMContext):

    await state.update_data(all_data=data, message=message)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🖼 Yes / Да", callback_data="draw")],
            [InlineKeyboardButton(text="❌ No / Нет", callback_data="not_draw")],
        ]
    )

    await bot.send_message(message.chat.id, "🇺🇸 *EN:* Generate an image?\n\n🇷🇺 *RU:* Сгенерировать изображение?", parse_mode="Markdown", reply_markup=keyboard) 

    await state.set_state(Form_draw.draw)





# Check request drawing:
async def check_request_drawing(question):
    typecontent = None

    draw_words = {  # добавить еще на каждое слово его слово-формы.. так лень, капец.. позже..)
        "draw", "sketch", "illustrate", "depict", "paint", "render", "нарисуй", "нарисуйте", "нарисовал", "нарисовала", "нарисовало", "нарисовать",  \
        "рисунок", "изобрази", "схема", "нарисовали", "рисуешь", "иллюстрация", "набросок", "макет", "дизайн", "чертеж",
    }
    question_words = set(question.lower().split())
    if draw_words & question_words:
        typecontent = "draw"
    
    return typecontent





#### MAIN HENDLER INCOMING
@dp.message(F.content_type.in_({'text', 'document', 'photo', 'audio', 'voice', })) # 'location' 'contact' 'video_note'  'video'  'sticker'
async def second_function(message: types.Message, state: FSMContext):

    #### DEFAULT VALUES:

    # Language models:
    default_model_ai = {
        "openai": AI_DEFAULT_MODEL_OPENAI,
        "gemini": AI_DEFAULT_MODEL_GEMINI,
    }
    # Gen Img models:
    default_model_draw = {
        "openai": DEFAULT_DALL_E,
        #"midjourney": 
    }
    # Gen Audio models:
    default_model_audio = {
        "openai": AI_DEFAULT_MODEL_GET_AUDIO,
    }
    # Transcription voice models:
    default_model_voice = {
        "openai": AI_DEFAULT_MODEL_GET_VOICE,
    }

    # SYS
    file_path, question, received_object, photo_file_name, name_file, caption, system_content, model_voice, voice, language = (None,) * 10
    caption, question, typecontent = message.caption, message.text, message.content_type
    ai, ai_draw, ai_voice, ai_audio, voice_answer, dialog, img_size, n_number, dialog_sum, voice, voice_speed, img_quality, img_style = AI_DEFAULT, AI_DRAW, AI_VOICE, AI_AUDIO, VOICE_THE_ANSWER, DIALOG, IMG_SIZE, N_NUMBER, DIALOG_SUM, VOICE, VOICE_SPEED, IMG_QUALITY, IMG_STYLE

    await typing(message)
    id = user_id(message)

    # Getting the user's system data from the database:
    data_from_db = await read_user(id)

    if not data_from_db: # False or Data
        confirm = await command_start_handler(message) # Go to the regist user to the DB.
        return

    if data_from_db.get("money") <= 0:
        await message.reply("🇺🇸 *EN:* There are not enough funds, top up your account.\n\n🇷🇺 *RU:* Недостаточно средств, пополните счет.", parse_mode="Markdown")
        return

    if data_from_db.get("block") == True:
        await message.reply("🇺🇸 *EN:* Fortunately, you're blocked...\n\n🇷🇺 *RU:* К счастью, ты заблокирован...", parse_mode="Markdown")
        return

    # Get AI:
    if data_from_db.get("ai"):
        ai = data_from_db.get("ai")

    # Get model ai:
    if data_from_db.get("model_language"):
        model_language = data_from_db.get("model_language")
    else:
        model_language = default_model_ai[ai]

    # Get draw ai:
    if data_from_db.get("ai_draw"):
        ai_draw = data_from_db.get("ai_draw")

    # Get model draw ai:
    if data_from_db.get("model_draw"):
        model_draw = data_from_db.get("model_draw")
    else:
        model_draw = default_model_draw[ai_draw]

    # Get ai_voice:
    if data_from_db.get("ai_voice"):
        ai_voice = data_from_db.get("ai_voice")

    # Get model draw ai:
    if data_from_db.get("model_voice"):
        model_voice = data_from_db.get("model_voice")
    else:
        model_voice = default_model_voice[ai_voice]

    # Get ai_audio:
    if data_from_db.get("ai_audio"):
        ai_audio = data_from_db.get("ai_audio")

    # Get model_audio:
    if data_from_db.get("model_audio"):
        model_audio = data_from_db.get("model_audio")
    else:
        model_audio = default_model_audio[ai_audio]

    # Get system_content:
    if data_from_db.get("system_content"):
        system_content = data_from_db.get("system_content")

    # Get voice_answer:
    if data_from_db.get("voice_answer") is not None:
        voice_answer = data_from_db.get("voice_answer")

    # Get voice style:
    if data_from_db.get("voice"):
        voice = data_from_db.get("voice")

    # Get voice_speed:
    if data_from_db.get("voice_speed"):
        voice_speed = data_from_db.get("voice_speed")

    # Get img_quality:
    if data_from_db.get("img_quality"):
        img_quality = data_from_db.get("img_quality")

    # Get img_style:
    if data_from_db.get("img_style"):
        img_style = data_from_db.get("img_style")

    # Get img_size:
    if data_from_db.get("img_size"):
        img_size = data_from_db.get("img_size")

    # Get n_number:
    if data_from_db.get("n_number"):
        n_number = data_from_db.get("n_number")

    # Get dialog:
    if data_from_db.get("dialog") is not None:
        dialog = data_from_db.get("dialog")

    # Get language:
    if data_from_db.get("language"):
        language = data_from_db.get("language")

    # Get dialog_sum:
    if data_from_db.get("dialog_sum") is not None:
        dialog_sum = data_from_db.get("dialog_sum")


    # Checking the text for a drawing request:
    if typecontent == "text":
        drawing_request = await check_request_drawing(question)
        typecontent = drawing_request or typecontent

    # Data collection to API:
    data = {
        "ai": ai,
        "model_language": model_language,

        "ai_draw": ai_draw,
        "model_draw": model_draw,

        "ai_voice": ai_voice,
        "model_voice": model_voice,

        "ai_audio": ai_audio,
        "model_audio": model_audio,

        "voice_answer": voice_answer,
        "img_size": img_size,
        "n_number": n_number,
        "dialog": dialog,
        "dialog_sum": dialog_sum,
        "voice": voice,
        "voice_speed": voice_speed,
        "img_quality": img_quality,
        "img_style": img_style,
    }

    # Additionally:
    data["system_content"] = system_content
    data["user_content"] = caption or question
    data["language"] = language

    # Choosing a direction:
    input_content_type = {
        "text": mod_tex,
        "draw": mod_gen_img,
        "document": mod_documents,
        "photo": mod_photo,
        #"audio": mod_text_to_audio,
        "voice": mod_voice_to_text,
    }

    if typecontent not in input_content_type:
        logging.error(f"Not support type file, sorry.")
        return

    arguments = {
        'data': data,
        'message': message,
    }

    if typecontent == "draw" or typecontent == "photo" or typecontent == "document":
        arguments["state"] = state #state: FSMContext

    await input_content_type[typecontent](**arguments)
####


  































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





