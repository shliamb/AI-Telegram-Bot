from get_keys import TELEGRAM_BOT_TOKEN, ADMIN_ID
from config import DOWNLOAD, AI_DEFAULT, AI_DEFAULT_MODEL_GEMINI, AI_DEFAULT_MODEL_OPENAI, VOICE_THE_ANSWER, VOICE_FOLDER, GIFT, DEFAULT_DALL_E, AI_DRAW, AI_VOICE_TO_TEXT, AI_TEXT_TO_VOICE, DIALOG, DIALOG_SUM, IMG_SIZE, N_NUMBER, VOICE, VOICE_SPEED, IMG_SIZE, N_NUMBER, IMG_QUALITY, IMG_STYLE, AI_DEFAULT_MODEL_TEXT_TO_VOICE, AI_DEFAULT_MODEL_VOICE_TO_TEXT, LANGUAGE, NOTIFICATIONS, USE_SBP_TRANSFER, USE_MASTERCARD, USE_VISA, USE_MIRCARD, USE_CRIPTO, USE_SMS, USE_STARS, USE_TELEGRAM, USE_DIGITAL, RUBTOUSD, DEL_VOICE, DEL_DOWNLOADS, DEL_AUDIO, BACKUP_DB, NAME_BOT, NULL_TOKEN, MAX_SIMBOLS, AI_DEFAULT_MODEL_CLAUDE, AI_DEFAULT_MODEL_DEEPSEEK, AI_DEFAULT_MODEL_GROK, MAX_LEN, MIN_PAY, PATH_JSON_USERS, PATH_LOGS, MAX_SIZE_DOC, EXTENS_DOC_SUPPORT
 #, DEFAULT_MODEL_ASSIST_OA
# logging.getLogger('aiogram').propagate = False # Блокировка логирование aiogram до его импорта
from setup_config_logger import setup_logger
logger_bot = setup_logger('bot', f'{PATH_LOGS}bot.log')
import re
import random
import os
import asyncio
import json
#import requests
from io import StringIO, BytesIO
#import uuid
from pathlib import Path # Работа с файловыми путями 
# from datetime import datetime, timezone, timedelta
# import time
# import sys
import csv
import docx
import PyPDF2
from openpyxl import load_workbook  # для Excel (.xlsx)
import pandas as pd  # для Excel и CSV
import io
# import datetime
# Aiogram
from aiogram import Bot, Dispatcher, types, F#, Router
# from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold
from aiogram.filters import CommandStart, Command #, Filter
from aiogram.types import Message, BotCommand, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton #, ReplyKeyboardMarkup, KeyboardButton, LabeledPrice, ContentType, InputFile, Document, PhotoSize
from aiogram.fsm.context import FSMContext
#from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# Service
from mod_claude import mod_claude_chat
from mod_gemini import mod_gemini_chat
from mod_openai import mod_openai_chat
from mod_deepseek import mod_deepseek_chat
from mod_grok import mod_grok_chat
from mod_get_voice_in_text_openai import get_voice_openai
from mod_get_text_in_voice_openai import get_text_openai
from mod_dall_e import mod_openai_dall_e
from general_functions import escape_special_chars, random_name_2X, day_utcnow, bool_to_str, calculation, tiktroken, set_model_dalle, get_use_met_all, remove_file_os
from worker_db import add_user, read_user, update_user, read_statistics, read_all_users, add_methods_pay, read_all_methods_pay, update_methods_pay, read_one_methods_pay_by_use, deleted_one_methods_pay, read_all_payments, add_payments, read_discussion, add_discussion, clear_discussion_by_id, fast_delete_statistics_tab, drop_all_tables_and_reset_schema #, read_admin_data, add_data_admin, update_admin_data, assist_admin_db_users
from texts import start_ru, start_en
from backupdb import backup_db
from restore_db import restore_db
from create_tables import create_tables_in_db
from restore_loyal_users import restore_loyal_users_to_db
from get_json_old_users import get_json_old_users_to_db
# from oa_assist import AssistOpenAI




bot = Bot(TELEGRAM_BOT_TOKEN, parse_mode="markdown") # Initialize Bot instance with a default parse mode which will be passed to all API calls
dp = Dispatcher() # All handlers should be attached to the Router (or Dispatcher)






#########
# Get User_ID
def user_id(action) -> int:
    return action.from_user.id

# Show Typing bot
async def typing(action) -> None:
    await bot.send_chat_action(action.chat.id, action='typing')

# Forced Start:
async def forced_start(message: types.Message):
    language_code = message.from_user.language_code
    if language_code == "ru":
        await message.answer("Обновлен бот. Для продолжения нажмите /start.  ", parse_mode="HTML")
    else:
        await message.answer("Updated the bot. To continue, press /start", parse_mode="HTML")






# START:
class Form_start(StatesGroup):
    language = State()

# Select English in to start:
@dp.callback_query(Form_start.language, lambda c: c.data and c.data.startswith('select_en'))
async def select_en_in_start(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user_data = user_data.get("user_date")
    id = user_data.get("user_id")
    about = user_data.get("name") if user_data.get("name") else (user_data.get("first_name") if user_data.get("first_name") else (user_data.get("last_name") if user_data.get("last_name") else "User"))
    language = "en"

    # Read user data:
    is_user_to_db = await read_user(id)

    if is_user_to_db:
        await bot.send_message(callback_query.from_user.id, f"Hi {about}! You are already initiated into the bot. You can start using it.")
        await bot.answer_callback_query(callback_query.id)
        await state.clear()
    else:
        date = {
            "user_id": id,
            "name": user_data.get("name"),
            "full_name": user_data.get("full_name"),
            "first_name": user_data.get("first_name"),
            "last_name": user_data.get("last_name"),
            "money": GIFT,
            "last_visit": await day_utcnow(),
            "language": language,
        }

        confirm = await add_user(date)

        if confirm:
            await bot.send_message(callback_query.from_user.id, f"Hello, {about}! {start_en}")
            logger_bot.info(f"New registration - {id}.")
            await bot.answer_callback_query(callback_query.id)
            await state.clear()




# Select Russian in to start:
@dp.callback_query(Form_start.language, lambda c: c.data and c.data.startswith('select_ru'))
async def select_ru_in_start(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user_data = user_data.get("user_date")
    id = user_data.get("user_id")
    about = user_data.get("name") if user_data.get("name") else (user_data.get("first_name") if user_data.get("first_name") else (user_data.get("last_name") if user_data.get("last_name") else "User"))
    language = "ru"

    # Read user data:
    is_user_to_db = await read_user(id)

    if is_user_to_db:
        await bot.send_message(callback_query.from_user.id, f"Привет {about}! Вы уже инициированы в боте. Можете приступить к использованию.")
        await bot.answer_callback_query(callback_query.id)
        await state.clear()
    else:
        date = {
            "user_id": id,
            "name": user_data.get("name"),
            "full_name": user_data.get("full_name"),
            "first_name": user_data.get("first_name"),
            "last_name": user_data.get("last_name"),
            "money": GIFT,
            "last_visit": await day_utcnow(),
            "language": language,
        }

        confirm = await add_user(date)

        if confirm:
            await bot.send_message(callback_query.from_user.id, f"Здравствуйте, {about}! {start_ru}")
            logger_bot.info(f"New registration - {id}.")
            await bot.answer_callback_query(callback_query.id)
            await state.clear()



#### Push /start ####
@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext):
    await typing(message)

    if message.from_user.is_bot:
        await message.answer("🚔 Sorry, the bot only works with humans.")
        return

    # MENU
    bot_commands = [
        BotCommand(command="/reset", description="CLEAR MEMORY"), # clear memory
        BotCommand(command="/menu", description="MENU"),
        BotCommand(command="/gen_draw", description="GEN DRAW"), # genDraw
        # BotCommand(command="/prices", description="PRICES"),
        BotCommand(command="/help", description="GUIDE"),
    ]
    await bot.set_my_commands(bot_commands)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇺🇸 ENGLISH", callback_data=f"select_en")],
            [InlineKeyboardButton(text="🇷🇺 RUSSIAN", callback_data=f"select_ru")],
        ]
    )

    user_date = {
        "user_id": user_id(message),
        "name": message.from_user.username,
        "full_name": message.from_user.full_name,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
    }

    await state.update_data(user_date=user_date)
    await bot.send_message(message.chat.id, "*EN:* Select a language:\n*RU:* Выберите язык:", parse_mode="Markdown", reply_markup=keyboard) 
    await state.set_state(Form_start.language)





#### WORK MENU ####

# RESET clear memory
@dp.message(Command('reset'))
async def reset_history(message: types.Message):
    id = user_id(message)
    data = await read_user(id)
    if not data:
        await forced_start(message)
        return

    language = data.get("language")

    confirm = await clear_discussion_by_id(id)

    if not confirm:
        logger_bot.error("Error: The dialog history has not been cleared.")

    if language == "ru":
        await message.answer("🗑 История диалога очищена.", parse_mode="HTML")
    else:
        await message.answer("🗑 The dialog history has been cleared.", parse_mode="HTML")




# MENU
@dp.message(Command('menu'))
async def main_menu(message: types.Message, submenu="main"):

    id = user_id(message)
    logger_bot.info(f"Push menu -  {id}.")

    data = await read_user(id)
    if not data:
        await forced_start(message)
        return

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
    elif ai == "claude":
        def_model_language = AI_DEFAULT_MODEL_CLAUDE
    elif ai == "deepseek":
        def_model_language = AI_DEFAULT_MODEL_DEEPSEEK
    elif ai == "grok":
        def_model_language = AI_DEFAULT_MODEL_GROK
        
    model_language = data["model_language"] if data.get("model_language") is not None else def_model_language
    ai_draw = data["ai_draw"] if data.get("ai_draw") is not None else AI_DRAW
    model_draw = data["model_draw"] if data.get("model_draw") is not None else DEFAULT_DALL_E
    img_size = data["img_size"] if data.get("img_size") is not None else IMG_SIZE
    img_quality = data["img_quality"] if data.get("img_quality") is not None else IMG_QUALITY
    img_style = data["img_style"] if data.get("img_style") is not None else IMG_STYLE
    ai_voice_to_text = data["ai_voice_to_text"] if data.get("ai_voice_to_text") is not None else AI_VOICE_TO_TEXT
    model_voice_to_text = data["model_voice_to_text"] if data.get("model_voice_to_text") is not None else AI_DEFAULT_MODEL_VOICE_TO_TEXT
    ai_text_to_voice = data["ai_text_to_voice"] if data.get("ai_text_to_voice") is not None else AI_TEXT_TO_VOICE
    model_text_to_voice = data["model_text_to_voice"] if data.get("model_text_to_voice") is not None else AI_DEFAULT_MODEL_TEXT_TO_VOICE
    voice = data["voice"] if data.get("voice") is not None else VOICE
    voice_speed = data["voice_speed"] if data.get("voice_speed") is not None else VOICE_SPEED
    money = round(data.get("money"), 4)
    system_content = True if data.get("system_content") is not None else False
    system_content = bool_to_str(system_content, language)



    img_menu_ru = (
        f"<b>🎛 НАСТРОЙКИ ГЕН. ИЗО.:</b>\n\n"
        f"<b>ГЕНЕРАЦИЯ КАРТИНОК ИИ: {ai_draw.upper()}</b>\n"
        f"<b>МОДЕЛЬ СЕЙЧАС: {model_draw.upper()}</b>\n\n"
        f"<b>Модели openai:</b>\n"
        f"        {'/dall_e_2' if model_draw == 'dall-e-3' else '/dall_e_3'}\n\n"
        f"<b>Размер изо: {img_size.upper()}</b>\n"
        f"        /1792x1024\n"
        f"        /1024x1792\n"
        f"        /1024x1024\n\n"
        f"<b>Качество изо: {img_quality.upper()}</b>\n"
        f"        /standard\n"
        f"        /hd\n\n"
        f"<b>Стиль изо: {img_style.upper()}</b>\n"
        f"        /vivid\n"
        f"        /natural\n\n"
        f"<b>Цены на одно изображение:</b>\n"
        f"        dall-e-3-1024 - 0.048$\n"
        f"        dall-e-3-1792 - 0.096$\n"
        f"        dall-e-3-hd-1024 - 0.096$\n"
        f"        dall-e-3-hd-1792 - 0.144$\n"
        f"        dall-e-2-1024 - 0.024$\n"
        f"        dall-e-2-512 - 0.0216$\n"
        f"        dall-e-2-256 - 0.0192$\n\n\n"
        f"/menu - вернуться назад\n"
    )



    img_menu_en = (
        f"<b>🎛 IMAGE GEN. SETTINGS:</b>\n\n"
        f"<b>IMAGE GENERATION AI: {ai_draw.upper()}</b>\n"
        f"<b>MODEL NOW: {model_draw.upper()}</b>\n\n"
        f"<b>Models openai:</b>\n"
        f"        {'/dall_e_2' if model_draw == 'dall-e-3' else '/dall_e_3'}\n\n"
        f"<b>Img size: {img_size.upper()}</b>\n"
        f"        /1792x1024\n"
        f"        /1024x1792\n"
        f"        /1024x1024\n\n"
        f"<b>Img quality: {img_quality.upper()}</b>\n"
        f"        /standard\n"
        f"        /hd\n\n"
        f"<b>Img style: {img_style.upper()}</b>\n"
        f"        /vivid\n"
        f"        /natural\n\n"
        f"<b>Prices per image:</b>\n"
        f"        dall-e-3-1024 - 0.048$\n"
        f"        dall-e-3-1792 - 0.096$\n"
        f"        dall-e-3-hd-1024 - 0.096$\n"
        f"        dall-e-3-hd-1792 - 0.144$\n"
        f"        dall-e-2-1024 - 0.024$\n"
        f"        dall-e-2-512 - 0.0216$\n"
        f"        dall-e-2-256 - 0.0192$\n\n\n"
        f"/menu - Go back\n"
    )


    voice_menu_ru = (
        f"<b>🎛 НАСТРОЙКИ ГОЛОСА:</b>\n\n"
        f"<b>РАСПОЗ. ГОЛОСА ИИ: {ai_voice_to_text.upper()}</b>\n"
        f"<b>МОДЕЛЬ: {model_voice_to_text.upper()}</b>\n\n"
        f"<b>Модели openai: {model_voice_to_text.upper()}</b>\n"
        f"<b>        /whisper_1 - 0.0072$ / минута</b>\n\n\n"
        f"<b>ГЕНЕРАЦИЯ ГОЛОСА ИИ: {ai_text_to_voice.upper()}</b>\n"
        f"<b>МОДЕЛЬ: {model_text_to_voice.upper()}:</b>\n\n"
        f"<b>Модель openai: {model_text_to_voice.upper()}</b>\n"
        f"        /tts_1 - 18$ / 1M символ\n"
        f"        /tts_1_hd - 36$ / 1M символ\n"
        f"        /4o_mini_tts - 15.12$ / 1M символ\n\n"
        f"<b>Стиль голоса:  {voice.upper()}</b>\n"
        f"        /nova - женский голос\n"
        f"        /alloy\n"
        f"        /echo\n"
        f"        /fable\n"
        f"        /onyx\n"
        f"        /shimmer\n\n"
        f"<b>Скорость голоса: {voice_speed}</b>\n"
        f"        /speed_0_75 - 0.75\n"
        f"        /speed_1 - 1.0\n"
        f"        /speed_1_25 - 1.25\n\n\n"
        f"/menu - вернуться назад\n"
    )




    voice_menu_en = (
        f"<b>🎛 VOICE SETTINGS:</b>\n\n"
        f"<b>VOICE RECOGNITION AI: {ai_voice_to_text.upper()}</b>\n"
        f"<b>MODEL NOW: {model_voice_to_text.upper()}</b>\n\n"
        f"<b>Models openai: {model_voice_to_text.upper()}</b>\n"
        f"<b>        /whisper_1 - 0.0072$ / minute</b>\n\n\n"
        f"<b>VOICE GENERATION AI: {ai_text_to_voice.upper()}</b>\n"
        f"<b>MODEL NOW: {model_text_to_voice.upper()}:</b>\n\n"
        f"<b>Model from OpenAI: {model_text_to_voice.upper()}</b>\n"
        f"        /tts_1 - 18$ / 1M characters\n"
        f"        /tts_1_hd - 36$ / 1M characters\n"
        f"        /4o_mini_tts - 15.12$ / 1M characters\n\n"
        f"<b>Voice style: {voice.upper()}</b>\n"
        f"        /nova - a woman's voice\n"
        f"        /alloy\n"
        f"        /echo\n"
        f"        /fable\n"
        f"        /onyx\n"
        f"        /shimmer\n\n"
        f"<b>The speed of the voice: {voice_speed}</b>\n"
        f"        /speed_0_75 - 0.75\n"
        f"        /speed_1 - 1.0\n"
        f"        /speed_1_25 - 1.25\n\n\n"
        f"/menu - Go back\n"
    )




    menu_ru = (
        f"<b>🎛 НАСТРОЙКИ:</b>\n\n"
        f"<b>🇷🇺 ЯЗЫК: {language.upper()}</b>\n"
        f"        На англ. – /en\n\n" # 🇺🇸
        f"<b>🔅 УВЕДОМЛЕНИЯ: {notifications}</b>\n"
        f"        {'Выкл. увед. - /notOFF' if notifications == 'ВКЛЮЧЕНО' else 'Вкл. увед. - /notON'}\n\n"
        f"<b>📖 ИСТОРИЯ ДИАЛОГА: {dialog}</b>\n"
        f"        {'Выкл. диалог - /diOFF' if dialog == 'ВКЛЮЧЕНО' else 'Вкл. диалог - /diON'}\n\n"
        f"<b>🗜 СЖАТИЕ ИСТОРИИ: {dialog_sum}</b>\n"
        f"        {'Выкл. сжатие диалога - /sumOFF' if dialog_sum == 'ВКЛЮЧЕНО' else 'Вкл. сжатие диалога - /sumON'}\n\n"
        f"<b>🎙 АУДИО ОТВЕТА: {voice_answer}</b>\n"
        f"        {'Выкл. аудио ответ - /audOFF' if voice_answer == 'ВКЛЮЧЕНО' else 'Вкл. аудио ответ - /audON'}\n\n"
        f"<b>🔖 ИНСТРУКЦИИ ДЛЯ ИИ: {system_content}</b>\n"
        f"        Добавить - /addSYS\n"
        f"        Посмотреть - /getSYS\n\n"
        f"<b>💳 БАЛАНС СЧЕТА: {money} $</b>\n"
        f"        Пополнить - /pay\n\n"
        f"<b>💵 ФИН. ОТЧЕТ:</b>\n"
        f"        Скачать в .CSV - /getStat\n\n\n"
        f"<b>🚩 ЯЗЫКОВАЯ ИИ: {ai.upper()}</b>\n"
        f"<b>МОДЕЛЬ: {model_language.upper()}</b>\n"
        f"(Наценка на токены 20% от их ориг. стоимости)\n\n"
        f"<b>💡 Модели OpenAI 1м ток:</b>\n"
        f"        /gpt_5_4_pro 🎉 - 252$\n" # gpt-5.4-pro
        f"        /gpt_5_4 🎉 - 21$\n" # gpt-5.4
        f"        /gpt_5 - 13.5$\n" # gpt-5-chat-latest
        f"        /gpt_5_mini - 2.7$\n" # gpt-5-mini
        f"        /gpt_5_nano - 0.54$\n\n" # gpt-5-nano
        #f"        /o1_pro - 900$\n"
        #f"        /o3_pro - 120$\n"
        #f"        /o3 - 12$\n\n"
        #f"        /chatgpt_4o 🔥 - 24$\n\n"
        f"<b>💡 Модели Google 1м ток:</b>\n"
        f"        /gemini_3_1_pro 🎉 - 16.8$\n" # gemini-3.1-pro-preview
        f"        /gemini_3_1_flash_lite 🎉 - 2.1$\n\n" # gemini-3.1-flash-lite-preview
        #f"        /gemini_3_pro 🎉 - 16.8$\n"  # gemini-3-pro-preview
        #f"        /gemini_2_5_pro 🔥 - 13.5$\n"
        #f"        /gemini_2_5_flash - 3.36$\n\n"
        #f"        /gemini_2_5_flash_lite - 0.6$\n\n"
        f"<b>💡 Модели Anthropic 1м ток:</b>\n"
        f"        /claude_4_6_opus 🎉 - 36$\n"
        f"        /claude_4_1_opus - 108$\n"
        #f"        /claude_4_opus - 108$\n"
        f"        /claude_4_6_sonnet 🎉 - 21.6$\n"
        f"        /claude_4_5_sonnet - 21.6$\n\n"
        #f"        /claude_4_sonnet - 21.6$\n\n"
        f"<b>💡 Модели Grok 1м ток:</b>\n"
        f"        /grok_4_1_reason 🎉 - 0.84$\n"
        f"        /grok_4_1_no_reason 🎉 - 0.84$\n"
        f"        /grok_4 - 21.6$\n\n"
        #f"        /grok_3 - 21.6$\n"
        #f"        /grok_3_mini - 0.96$\n\n"
        f"<b>💡 Модели DeepSeek 1м ток:</b>\n"
        f"        /deepseek_reasoner R1 - 3.288$\n"
        f"        /deepseek_chat 🔥 - 1.644$\n\n\n"
        f"<b>🎚 ДОПОЛНИТЕЛЬНО:</b>\n"
        f"        Параметры ген. изо. - /imgMenu\n"
        f"        Параметры голоса - /voiceMenu\n"

    )



    menu_en = (
        f"<b>🎛 SETTINGS:</b>\n\n"
        f"<b>🇺🇸 LANGUAGE: {language.upper()}</b>\n"
        f"        Russian – /ru\n\n"
        f"<b>🔅 NOTIFICATIONS: {notifications}</b>\n"
        f"        {'Enab. notif. - /notON' if notifications == 'OFF' else 'Dis. notif. - /notOFF'}\n\n"
        f"<b>📖 HISTORY OF DIALOGUE: {dialog}</b>\n"
        f"        {'Enab. history - /diON' if dialog == 'OFF' else 'Dis. history - /diOFF'}\n\n"
        f"<b>🗜 HISTORY COMPRESSION: {dialog_sum}</b>\n"
        f"        {'Dis. compres. - /sumOFF' if dialog_sum == 'ON' else 'Enab. compres. - /sumON'}\n\n"
        f"<b>🎙 AUDIO RESPONSE: {voice_answer}</b>\n"
        f"        {'Dis. audio res. - /audOFF' if voice_answer == 'ON' else 'Enab. audio res. - /audON'}\n\n"
        f"<b>🔖 SYSTEM CONTENT AI: {system_content}</b>\n"
        f"        Add - /addSYS\n"
        f"        View text - /getSYS\n\n"
        f"<b>💳 ACCOUNT BALANS: {money} $</b>\n"
        f"        Pay - /pay\n\n"
        f"<b>💵 FINANCIAL REPORTS:</b>\n"
        f"        Download in .CSV - /getStat\n\n\n"
        f"<b>🚩 LANGUAGE AI: {ai.upper()}</b>\n"
        f"<b>MODEL: {model_language.upper()}</b>\n"
        f"(The token markup is 20% of their original cost)\n\n"
        f"<b>💡 Models OpenAI 1m tok:</b>\n"
        f"        /gpt_5_4_pro 🎉 - 252$\n" # gpt-5.4-pro
        f"        /gpt_5_4 🎉 - 21$\n" # gpt-5.4
        f"        /gpt_5 - 13.5$\n" # gpt-5-chat-latest
        f"        /gpt_5_mini - 2.7$\n" # gpt-5-mini
        f"        /gpt_5_nano - 0.54$\n\n" # gpt-5-nano
        #f"        /o1_pro - 900$\n"
        #f"        /o3_pro - 120$\n"
        #f"        /o3 - 12$\n\n"
        #f"        /chatgpt_4o 🔥 - 24$\n\n"
        f"<b>💡 Models Google 1m tok:</b>\n"
        f"        /gemini_3_1_pro 🎉 - 16.8$\n" # gemini-3.1-pro-preview
        f"        /gemini_3_1_flash_lite 🎉 - 2.1$\n\n" # gemini-3.1-flash-lite-preview
        #f"        /gemini_3_pro 🎉 - 16.8$\n"  # gemini-3-pro-preview
        #f"        /gemini_2_5_pro 🔥 - 13.5$\n"
        #f"        /gemini_2_5_flash - 3.36$\n\n"
        #f"        /gemini_2_5_flash_lite - 0.6$\n\n"
        f"<b>💡 Models Anthropic 1m tok:</b>\n"
        f"        /claude_4_6_opus 🎉 - 36$\n"
        f"        /claude_4_1_opus - 108$\n"
        #f"        /claude_4_opus - 108$\n"
        f"        /claude_4_6_sonnet 🎉 - 21.6$\n"
        f"        /claude_4_5_sonnet - 21.6$\n\n"
        #f"        /claude_4_sonnet - 21.6$\n\n"
        f"<b>💡 Models Grok 1m tok:</b>\n"
        f"        /grok_4_1_reason 🎉 - 0.84$\n"
        f"        /grok_4_1_no_reason 🎉 - 0.84$\n"
        f"        /grok_4 - 21.6$\n\n"
        #f"        /grok_3 - 21.6$\n"
        #f"        /grok_3_mini - 0.96$\n\n"
        f"<b>💡 Models DeepSeek 1m tok:</b>\n"
        f"        /deepseek_reasoner R1 - 3.288$\n"
        f"        /deepseek_chat 🔥 - 1.644$\n\n\n"
        f"<b>🎚 ADDITIONALLY:</b>\n"
        f"        Image gen. param. - /imgMenu\n"
        f"        Voice param. - /voiceMenu\n"

    )



    if language == "ru" and submenu == "main":
        await message.answer(f"{menu_ru}", parse_mode="HTML")
    elif language == "en" and submenu == "main":
        await message.answer(f"{menu_en}", parse_mode="HTML")

    if language == "ru" and submenu == "voice_menu":
        await message.answer(f"{voice_menu_ru}", parse_mode="HTML")
    elif language == "en" and submenu == "voice_menu":
        await message.answer(f"{voice_menu_en}", parse_mode="HTML")

    if language == "ru" and submenu == "img_menu":
        await message.answer(f"{img_menu_ru}", parse_mode="HTML")
    elif language == "en" and submenu == "img_menu":
        await message.answer(f"{img_menu_en}", parse_mode="HTML")








# SUB MENU IMG:
@dp.message(Command('imgMenu'))
async def en(message: types.Message):
    await main_menu(message, "img_menu")

# SUB MENU VOICE:
@dp.message(Command('voiceMenu'))
async def en(message: types.Message):
    await main_menu(message, "voice_menu")

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
        await main_menu(message, "main")

@dp.message(Command('ru'))
async def ru(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "language": "ru"
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")

# Notifications:
@dp.message(Command('notON'))
async def notif_on(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "notifications": True,
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")

@dp.message(Command('notOFF'))
async def notif_off(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "notifications": False,
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")

# History:
@dp.message(Command('diON'))
async def dialog_on(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "dialog": True,
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")

@dp.message(Command('diOFF'))
async def dialog_off(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "dialog": False,
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


# History Compression:
@dp.message(Command('sumON'))
async def sum_on(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "dialog_sum": True,
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")

@dp.message(Command('sumOFF'))
async def sum_off(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "dialog_sum": False,
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


# Audio response:
@dp.message(Command('audON'))
async def audio_on(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "voice_answer": True,
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")

@dp.message(Command('audOFF'))
async def audio_off(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "voice_answer": False,
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")



# OpenAI models:
@dp.message(Command('gpt_5'))
async def gpt_5(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "openai",
        "model_language": "gpt-5",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")

@dp.message(Command('gpt_5_1'))
async def gpt_5_1(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "openai",
        "model_language": "gpt-5.1-2025-11-13",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


@dp.message(Command('gpt_5_4_pro'))
async def gpt_5_4_pro(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "openai",
        "model_language": "gpt-5.4-pro",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


@dp.message(Command('gpt_5_4'))
async def gpt_5_4(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "openai",
        "model_language": "gpt-5.4",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


@dp.message(Command('gpt_5_pro'))
async def gpt_5_pro(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "openai",
        "model_language": "gpt-5-pro-2025-10-06",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")

@dp.message(Command('gpt_5_mini'))
async def gpt_5_mini(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "openai",
        "model_language": "gpt-5-mini",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")

@dp.message(Command('gpt_5_nano'))
async def gpt_5_nano(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "openai",
        "model_language": "gpt-5-nano",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")








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
        await main_menu(message, "main")

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
        await main_menu(message, "main")

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
        await main_menu(message, "main")

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
        await main_menu(message, "main")

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
        await main_menu(message, "main")

@dp.message(Command('chatgpt_4o'))
async def chatgpt_4o_latest(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "openai",
        "model_language": "chatgpt-4o-latest",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")

# o1:

'''
- no image,
- no system content,
- context window of 128,000 tokens, 
- The maximum output token limits are:
    o1-preview: Up to 32,768 tokens
    o1-mini: Up to 65,536 tokens
'''


@dp.message(Command('o1_preview'))
async def o1(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "openai",
        "model_language": "o1-preview",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


@dp.message(Command('o1_mini'))
async def o3_mini(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "openai",
        "model_language": "o1-mini",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


@dp.message(Command('gpt_4_1'))
async def gpt_4_1(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "openai",
        "model_language": "gpt-4.1",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


@dp.message(Command('gpt_4_1_mini'))
async def gpt_4_1_mini(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "openai",
        "model_language": "gpt-4.1-mini",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


@dp.message(Command('gpt_4_1_nano'))
async def gpt_4_1_nano(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "openai",
        "model_language": "gpt-4.1-nano",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")



@dp.message(Command('gpt_4_5_preview'))
async def gpt_4_5_preview(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "openai",
        "model_language": "gpt-4.5-preview",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


@dp.message(Command('o3_mini'))
async def o3_mini(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "openai",
        "model_language": "o3-mini",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


@dp.message(Command('o3'))
async def o3(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "openai",
        "model_language": "o3",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")





@dp.message(Command('o3_pro'))
async def o3_pro(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "openai",
        "model_language": "o3-pro",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")



@dp.message(Command('o4_mini'))
async def o4_mini(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "openai",
        "model_language": "o4-mini",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")





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
        await main_menu(message, "main")

# @dp.message(Command('gemini_1_0_pro'))
# async def gemini_1_0_pro_latest(message: types.Message):
#     id = user_id(message)
#     data = {
#         "user_id": id,
#         "ai": "gemini",
#         "model_language": "gemini-1.0-pro",
#     }
#     confirm = await update_user(data)
#     if confirm:
#         await main_menu(message, "main")

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
        await main_menu(message, "main")

@dp.message(Command('gemini_1_5_flash_8b'))
async def gemini_1_5_flash_8b(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "gemini",
        "model_language": "gemini-1.5-flash-8b",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")

@dp.message(Command('gemini_2_0_flash'))
async def gemini_2_0_flash_exp(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "gemini",
        "model_language": "gemini-2.0-flash",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


@dp.message(Command('gemini_2_5_pro'))
async def gemini_2_5_pro_preview_03_25(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "gemini",
        "model_language": "gemini-2.5-pro" #gemini-2.5-pro-preview-05-06",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


@dp.message(Command('gemini_3_1_flash_lite'))
async def gemini_3_1_flash_lite(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "gemini",
        "model_language": "gemini-3.1-flash-lite-preview"
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


@dp.message(Command('gemini_3_1_pro'))
async def gemini_3_1_pro(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "gemini",
        "model_language": "gemini-3.1-pro-preview"
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


@dp.message(Command('gemini_3_pro'))
async def gemini_3_pro(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "gemini",
        "model_language": "gemini-3-pro-preview"
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


@dp.message(Command('gemini_2_5_flash'))
async def gemini_2_5_flash(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "gemini",
        "model_language": "gemini-2.5-flash",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


@dp.message(Command('gemini_2_5_flash_lite'))
async def gemini_2_5_flash_lite(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "gemini",
        "model_language": "gemini-2.5-flash-lite-preview-06-17",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


@dp.message(Command('gemini_2_0_flash_lite'))
async def gemini_2_0_flash_lite_001(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "gemini",
        "model_language": "gemini-2.0-flash-lite",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")










# Grok models:


@dp.message(Command('grok_4_1_reason'))
async def grok_4_1_reason(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "grok",
        "model_language": "grok-4-1-fast-reasoning",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


@dp.message(Command('grok_4_1_no_reason'))
async def grok_4_1_no_reason(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "grok",
        "model_language": "grok-4-1-fast-non-reasoning",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")



@dp.message(Command('grok_4'))
async def grok_4(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "grok",
        "model_language": "grok-4-0709",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")

@dp.message(Command('grok_vision_beta'))
async def grok_vision_beta(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "grok",
        "model_language": "grok-vision-beta",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")

@dp.message(Command('grok_2_vision_latest'))
async def grok_2_vision_latest(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "grok",
        "model_language": "grok-2-vision-latest",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


@dp.message(Command('grok_2_latest'))
async def grok_2_latest(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "grok",
        "model_language": "grok-2-latest",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


@dp.message(Command('grok_beta'))
async def grok_beta(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "grok",
        "model_language": "grok-beta",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


@dp.message(Command('grok_3_mini_fast_latest'))
async def grok_3_mini_fast_latest(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "grok",
        "model_language": "grok-3-mini-fast-latest",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


@dp.message(Command('grok_3_mini'))
async def grok_3_mini_latest(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "grok",
        "model_language": "grok-3-mini-latest",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


@dp.message(Command('grok_3_fast_latest'))
async def grok_3_fast_latest(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "grok",
        "model_language": "grok-3-fast-latest",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


@dp.message(Command('grok_3'))
async def grok_3_latest(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "grok",
        "model_language": "grok-3-latest",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")










# DeepSeek models:
@dp.message(Command('deepseek_reasoner'))
async def deepseek_reasoner(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "deepseek",
        "model_language": "deepseek-reasoner",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")

@dp.message(Command('deepseek_chat'))
async def deepseek_chat(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "deepseek",
        "model_language": "deepseek-chat",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")







# Anthropic models:

@dp.message(Command('claude_4_6_opus'))
async def claude_4_6_opus (message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "claude",
        "model_language": "claude-opus-4-6",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


@dp.message(Command('claude_4_1_opus'))
async def claude_4_1_opus(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "claude",
        "model_language": "claude-opus-4-1-20250805",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")

@dp.message(Command('claude_4_opus'))
async def claude_4_opus(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "claude",
        "model_language": "claude-opus-4-20250514",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")

@dp.message(Command('claude_4_sonnet'))
async def claude_4_sonnet(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "claude",
        "model_language": "claude-sonnet-4-20250514",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


@dp.message(Command('claude_4_5_sonnet'))
async def claude_4_5_sonnet(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "claude",
        "model_language": "claude-sonnet-4-5-20250929",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


@dp.message(Command('claude_4_6_sonnet'))
async def claude_4_6_sonnet(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "claude",
        "model_language": "claude-sonnet-4-6",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


@dp.message(Command('claude_3_5_sonnet'))
async def claude_3_5_sonnet(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "claude",
        "model_language": "claude-3-5-sonnet-latest",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")

@dp.message(Command('claude_3_5_haiku'))
async def claude_3_5_haiku(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "claude",
        "model_language": "claude-3-5-haiku-latest",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")

@dp.message(Command('claude_3_opus'))
async def claude_3_opus(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "claude",
        "model_language": "claude-3-opus-latest",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")

@dp.message(Command('claude_3_sonnet'))
async def claude_3_sonnet(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "claude",
        "model_language": "claude-3-sonnet-20240229",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")

@dp.message(Command('claude_3_haiku'))
async def claude_3_haiku(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "claude",
        "model_language": "claude-3-haiku-20240307",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")


@dp.message(Command('claude_3_7_sonnet'))
async def claude_3_7_sonnet_latest(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai": "claude",
        "model_language": "claude-3-7-sonnet-latest",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "main")












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
        await main_menu(message, "img_menu")

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
        await main_menu(message, "img_menu")

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
        await main_menu(message, "img_menu")

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
        await main_menu(message, "img_menu")

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
        await main_menu(message, "img_menu")

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
        await main_menu(message, "img_menu")

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
        await main_menu(message, "img_menu")

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
        await main_menu(message, "img_menu")

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
        await main_menu(message, "img_menu")

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
        await main_menu(message, "img_menu")


# Voice recognition:
@dp.message(Command('whisper_1'))
async def whisper_1(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai_voice_to_text": "openai",
        "model_voice_to_text": "whisper-1",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "voice_menu")


# Voice generation:
@dp.message(Command('tts_1'))
async def tts_1(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai_text_to_voice": "openai",
        "model_text_to_voice": "tts-1",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "voice_menu")

@dp.message(Command('tts_1_hd'))
async def tts_1_hd(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai_text_to_voice": "openai",
        "model_text_to_voice": "tts-1-hd",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "voice_menu")



@dp.message(Command('4o_mini_tts'))
async def for_o_mini_tts(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "ai_text_to_voice": "openai",
        "model_text_to_voice": "gpt-4o-mini-tts",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "voice_menu")


@dp.message(Command('nova'))
async def nova(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "voice": "nova",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "voice_menu")


@dp.message(Command('alloy'))
async def alloy(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "voice": "alloy",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "voice_menu")

@dp.message(Command('echo'))
async def echo(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "voice": "echo",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "voice_menu")


@dp.message(Command('fable'))
async def fable(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "voice": "fable",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "voice_menu")


@dp.message(Command('onyx'))
async def onyx(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "voice": "onyx",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "voice_menu")

@dp.message(Command('shimmer'))
async def shimmer(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "voice": "shimmer",
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "voice_menu")


@dp.message(Command('speed_0_75'))
async def speed_0_75(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "voice_speed": 0.75,
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "voice_menu")

@dp.message(Command('speed_1'))
async def speed_1(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "voice_speed": 1.0,
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "voice_menu")


@dp.message(Command('speed_1_25'))
async def speed_1_25(message: types.Message):
    id = user_id(message)
    data = {
        "user_id": id,
        "voice_speed": 1.25,
    }
    confirm = await update_user(data)
    if confirm:
        await main_menu(message, "voice_menu")






# Set system content:
class Form_system(StatesGroup):
    content = State()

@dp.message(Command('addSYS'))
async def system_content(message: types.Message, state: FSMContext):
    id = user_id(message)    
    is_user_to_db = await read_user(id)
    language = is_user_to_db.get("language")
    await state.update_data(language=language)

    if is_user_to_db:
        if language == "ru":
            await message.reply(f"Задайте инструкции которые помогут ИИ понять, как нужно взаимодействовать с вами:", parse_mode="Markdown")
        else:
            await message.reply(f"Set instructions that will help the AI understand how to interact with you:", parse_mode="Markdown")
    
    await state.set_state(Form_system.content)

@dp.message(Form_system.content)
async def system_content_get_text(message: types.Message, state: FSMContext):
    id = user_id(message)
    state_data = await state.get_data()
    language = state_data.get("language")

    data = {
        "user_id": id,
        "system_content": message.text,
    }
    confirm = await update_user(data)

    if confirm:
        if language == "ru":
            await message.reply(f"Системная инструкция сохранена.", parse_mode="Markdown")
        else:
            await message.reply(f"The system instruction has been saved.", parse_mode="Markdown")

    await state.clear()

@dp.message(Command('getSYS'))
async def get_sys_content(message: types.Message):
    id = user_id(message)
    data = await read_user(id)
    system_content = data["system_content"] if data.get("system_content") is not None else "is Empty"
    await message.answer(system_content, parse_mode="HTML")





# User statistic:
@dp.message(Command('getStat'))
async def get_stat(message: types.Message):
    id = user_id(message)
    all_data = await read_statistics(id)
    is_user_to_db = await read_user(id)
    language = is_user_to_db.get("language")

    if not all_data:
        if language == "ru":
            await message.answer("У вас еще нет статистики.", parse_mode="HTML")
        else:
            await message.answer("You don't have statistics yet.", parse_mode="HTML")
        return

    all_static = []

    all_static.append(["№", "User id", "Date", "Use model AI", "Tokens", "Minutes Audio", "Image", "Price for one", "Full session consumption"])
    
    for data in all_data:
        all_static.append([data.get("id"), data.get("user_id"), data.get("date"), data.get("model"), data.get("tokens"), data.get("min"), data.get("img"), data.get("price_1"), data.get("price")])

    # Create csv file
    output = StringIO()
    writer = csv.writer(output)
    for row in all_static:
        writer.writerow(row)
    csv_data = output.getvalue()
    output.close()

    # csv file to download
    file_name = f"User-statistic-{random_name_2X()}.csv"
    buffered_input_file = types.input_file.BufferedInputFile(file=csv_data.encode(), filename=file_name)
    try:
        await bot.send_document(chat_id=message.chat.id, document=buffered_input_file)
    except:
        logger_bot.error(f"Error sending documentb User stat")




# # MENU: PRICES:
# @dp.message(Command('prices'))
# async def get_prices(message: types.Message):

#     id = user_id(message)
#     user_data = await read_user(id)
#     language = user_data.get("language")

#     if language == "ru":
#         await message.answer(prices_ru, parse_mode="HTML")
#     else:
#         await message.answer(prices_en, parse_mode="HTML")


















#### Transfer money: ####
####################


# 6 Обработчик подтверждения
@dp.callback_query(lambda c: c.data and c.data.startswith('admin_conf'))
async def confirm_callback(callback_query: types.CallbackQuery):

    data = callback_query.data.split(':')

    if not data:
        logger_bot.error("Error: dont get data - data_button.")
        await bot.send_message(callback_query.from_user.id, "Error: dont get data - data_button.")
        return
    
    id = int(data[1])
    amount = float(data[2])
    use = str(data[3])
    data_user = await read_user(id)
    language = data_user.get("language")
    admin_id = ADMIN_ID
    mes_id = id
    new_money = data_user.get("money") + (float(amount))
    new_paid = data_user.get("paid") + 1

    updated_data = {"user_id": id, "money": new_money, "paid": new_paid, "block": False}
    confirm_save = await update_user(updated_data)

    logger_bot.info(f"Adding funds to your account - {id}.")

    pay_data = {
        "date": await day_utcnow(),
        "title_method_pay": use,
        "sum": float(amount),
        "user_id": id
        }
    
    confirm_pay_stat =  await add_payments(pay_data)
    if not confirm_pay_stat:
        logger_bot.error("Error: Dont save payments.")

    one_method = await read_one_methods_pay_by_use(use)
    if one_method:
        old_coint = one_method.get("counts")
        if old_coint == None:
            old_coint = 0
        metod_id = one_method.get("id")
        counts = old_coint + 1
        method_data = {"id": metod_id, "counts": counts}
        confirm_update_met =  await update_methods_pay(method_data)
        if not confirm_update_met:
            logger_bot.error("Error: Dont update counts pay method.")

    if confirm_save is True:
        # Admin:
        await bot.send_message(admin_id, f"Счет клиента {id} пополнен, общий:  {new_money} $.")
        
        # User:
        if language == "ru":
            await bot.send_message(mes_id, f"Ваш счет пополнен. На балансе - {new_money}$. Поздравляем!")
        else:
            await bot.send_message(mes_id, f"Your account has been topped up. On the balance sheet - {new_money}$. Congratulations!")

        await bot.answer_callback_query(callback_query.id)
        return
    else:
        await bot.send_message(admin_id, "Error: A replenishment error occurred.")
        await bot.answer_callback_query(callback_query.id)
        return




# 5 Вызов у админа кнопки подтверждения
async def confirm_my_button(data_button):

    id = data_button.get("id")
    amount = data_button.get("amount")
    admin_id = data_button.get("admin_id")
    mes_id = data_button.get("mes_id")
    url = f"<a href='tg://user?id={id}'>{id}</a>"
    language = data_button.get("language")
    use = data_button.get("use")

    if use == "use_sbp_transfer" or use == "use_mircard":
        amount = float(amount) / float(RUBTOUSD)
    else:
        amount = float(amount)

    # Кнопка подтверждения
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👛 Confirmation", callback_data=f"admin_conf:{id}:{amount}:{use}")], 
        ]
    )
    await bot.send_message(admin_id, f"Пользователь: <a href='tg://user?id={id}'>{id}</a>, хочет пополнить счет на: {amount}$, вариант оплаты - '{use}'", parse_mode="HTML", reply_markup=keyboard)
    return



class Form_my_pay(StatesGroup):
    text = State()
    add_summ = State()
    confirm_summ = State()
    #admin_confirm = State()

# 1 Select method pay:
@dp.message(Command("pay"))
async def add_money(message: types.Message, state: FSMContext):

    id = user_id(message)
    data_user = await read_user(id)
    language = data_user.get("language")

    answer = ""

    intro_ru = '''
Выбор способа оплаты: 
'''
    intro_en = '''
Choosing a payment method:
'''

    if USE_SBP_TRANSFER and await read_one_methods_pay_by_use("use_sbp_transfer"):
        if language == "ru":
            answer = answer + "\n/sbp_ru - перевод RUB по СБП"
        else:
            answer = answer + "\n/sbp_ru - transfer RUB by SBP"

    if USE_MASTERCARD and await read_one_methods_pay_by_use("use_mastercard"):
        if language == "ru":
            answer = answer + "\n/mastercard - перевод USD Mastercard"
        else:
            answer = answer + "\n/mastercard - transfer USD Mastercard"

    if USE_VISA and await read_one_methods_pay_by_use("use_visa"):
        if language == "ru":
            answer = answer + "\n/use_visa - перевод USD Visa"
        else:
            answer = answer + "\n/use_visa - transfer USD Visa card"

    if USE_MIRCARD and await read_one_methods_pay_by_use("use_mircard"):
        if language == "ru":
            answer = answer + "\n/mir_ru - перевод RUB на карту"
        else:
            answer = answer + "\n/mir_ru - transfer RUB to a card"

    if USE_CRIPTO and await read_one_methods_pay_by_use("use_cripto"):
        if language == "ru":
            answer = answer + "/use_cripto"
        else:
            answer = answer + "/use_cripto"

    if USE_SMS and await read_one_methods_pay_by_use("use_sms"):
        if language == "ru":
            answer = answer + "/use_sms"
        else:
            answer = answer + "/use_sms"

    if USE_STARS and await read_one_methods_pay_by_use("use_stars"):
        if language == "ru":
            answer = answer + "/use_stars"
        else:
            answer = answer + "/use_stars"

    if USE_TELEGRAM and await read_one_methods_pay_by_use("use_telegram"):
        if language == "ru":
            answer = answer + "/use_telegram"
        else:
            answer = answer + "/use_telegram"

    if USE_DIGITAL and await read_one_methods_pay_by_use("use_digital"):
        if language == "ru":
            answer = answer + "/use_digital"
        else:
            answer = answer + "/use_digital"

    if answer == "":
        logger_bot.error("Error: not default method pay.")
        if language == "ru":
            await message.reply("Нет способов оплаты, извините.", parse_mode="HTML")
        else:
            await message.reply("There are no payment methods, sorry.", parse_mode="HTML")
        await state.clear()
        return

    if language == "ru":
        answer = intro_ru + answer
    else:
        answer = intro_en + answer

    await message.reply(answer, parse_mode="HTML")
    await state.update_data(language=language)
    await state.set_state(Form_my_pay.text)



# 2
@dp.message(Form_my_pay.text)
async def sbp_ru(message: types.Message, state: FSMContext):

    state_data = await state.get_data()
    language = state_data.get("language")

    if message.text == "/sbp_ru":
        use="use_sbp_transfer"
    if message.text == "/mastercard":
        use="use_mastercard"
    if message.text == "/use_visa":
        use="use_visa"
    if message.text == "/mir_ru":
        use="use_mircard"
    if message.text == "/use_cripto":
        use="use_cripto"
    if message.text == "/use_sms":
        use="use_sms"
    if message.text == "/use_stars":
        use="use_stars"
    if message.text == "/use_telegram":
        use="use_telegram"
    if message.text == "/use_digital":
        use="use_digital"

    if use == "use_sbp_transfer" or use == "use_mircard":
        if language == "ru":
            await message.reply(f"Введите сумму в RUB:\nДля отмены введите 0.\n\n<b>Обратите внимание</b>, что на счет поступит сумма в USD по внутреннему курсу 1USD = {RUBTOUSD}RUB", parse_mode="HTML")
        else:
            await message.reply(f"Enter the amount in RUB:\nTo cancel, enter 0.\n\n<b>Please note</b> that the amount in USD will be credited to the account at the internal rate of 1USD = {RUBTOUSD}RUB", parse_mode="HTML")
    else:
        if language == "ru":
            await message.reply(f"Введите сумму в USD:\nДля отмены введите 0.", parse_mode="HTML")
        else:
            await message.reply(f"Enter the amount in USD:\nTo cancel, enter 0.", parse_mode="HTML")

    await state.update_data(language=language, use=use)
    await state.set_state(Form_my_pay.add_summ)


# 3
@dp.message(Form_my_pay.add_summ)
async def sbp_ru_input(message: types.Message, state: FSMContext):

    state_data = await state.get_data()
    language = state_data.get("language")
    use = state_data.get("use")

    try:
        amount = float(message.text)
    except:
        logger_bot.error(f"This not float input.")
        await message.reply("This not float input.", parse_mode="Markdown") 
        return

    if float(message.text) == 0.0:
        if language == "ru":
            await message.reply("Пополнение отменено.", parse_mode="HTML")
        else:
            await message.reply("The deposit has been canceled.", parse_mode="HTML")
        await state.clear()
        return

    if use == "use_sbp_transfer" and amount < 100 or use == "use_mircard" and amount < 100:
        if language == "ru":
            await message.reply("Минимальная сумма 100 RUB.", parse_mode="HTML")
        else:
            await message.reply("The minimum amount is 100 RUB.", parse_mode="HTML")
        return
    elif amount < 1:
        if language == "ru":
            await message.reply("Минимальная сумма 1 USD.", parse_mode="HTML")
        else:
            await message.reply("The minimum amount is 1 USD.", parse_mode="HTML")
        return

    data = await read_one_methods_pay_by_use(use)

    if language == "ru":
        answer = data.get("method_pay_ru")
    else:
        answer = data.get("method_pay_en")

    await message.reply(answer, parse_mode="HTML")

    if language == "ru":
        await message.reply("После успешного перевода, введите 'Готово' или 'Отмена' - для отмены.", parse_mode="HTML")
    else:
        await message.reply("After successful transfer, enter 'Done' or 'Cancel' to cancel.", parse_mode="HTML")

    await state.update_data(language=language, amount=amount, use=use)
    await state.set_state(Form_my_pay.confirm_summ)


# 4
@dp.message(Form_my_pay.confirm_summ)
async def sbp_ru_confirm(message: types.Message, state: FSMContext):

    state_data = await state.get_data()
    language = state_data.get("language")
    amount = state_data.get("amount")
    text = message.text
    use = state_data.get("use")


    if text.lower() == "отмена" or text.lower() == "cancel":
        if language == "ru":
            await message.reply("Пополнение отменено.", parse_mode="HTML")
        else:
            await message.reply("The deposit has been canceled.", parse_mode="HTML")
        await state.clear()
        return

    elif text.lower() == "готово" or text.lower() == "done":
        if language == "ru":
            await message.reply("После проверки платежа, ваш счет пополнится и придет уведомление.", parse_mode="HTML")
        else:
            await message.reply("After checking the payment, your account will be replenished and a notification will be sent.", parse_mode="HTML")
        
        # End state:
        await state.clear()

        mes_id = message.chat.id
        id = user_id(message)
        admin_id = ADMIN_ID
        url = f"tg://user?id={id}"

        data_button = {
            "id": id,
            "amount": amount,
            "admin_id": admin_id,
            "mes_id": mes_id,
            "url": url,
            "language": language,
            "use": use
        }

        # Send message to ADMIN:
        await confirm_my_button(data_button)
        return
    
    else:
        if language == "ru":
            await message.reply("После успешного перевода, введите 'Готово' или 'Отмена' - для отмены.", parse_mode="HTML")
        else:
            await message.reply("After successful transfer, enter 'Done' or 'Cancel' to cancel.", parse_mode="HTML")

#####




















@dp.message(Command('help'))
async def start(message: types.Message):

    id = user_id(message)
    data = await read_user(id)
    if not data:
        await forced_start(message)
        return
    language = data.get("language")

    text_button = "📝 Сообщение разработчику" if language == "ru" else "📝 Message to the developer"

    keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=text_button, callback_data=f"send_message")], 
            ]
        )

    if language == "ru":
        await bot.send_message(message.chat.id, f"{start_ru}", parse_mode="HTML", reply_markup=keyboard)
    elif language == "en":
        await bot.send_message(message.chat.id, f"{start_en}", parse_mode="HTML", reply_markup=keyboard)


class Form_send(StatesGroup):
    send_admin = State()

@dp.callback_query(lambda c: c.data and c.data.startswith('send_message'))
async def send_to_admin(callback_query: types.CallbackQuery, state: FSMContext):
    id = user_id(callback_query)
    data = await read_user(id)
    language = data.get("language")
    block = data.get("block")

    if block:
        logger_bot.error(f"This dude - {id} is trying to write blocked.")
        if language == "ru":
            await bot.send_message(callback_query.from_user.id, "У вас больше нет попыток написать.", parse_mode="HTML")
        elif language == "en":
            await bot.send_message(callback_query.from_user.id, "You don't have any more attempts to write.", parse_mode="HTML")
        await bot.answer_callback_query(callback_query.id)
        return

    if language == "ru":
        await bot.send_message(callback_query.from_user.id, "Напишите сообщение:", parse_mode="HTML")
    elif language == "en":
        await bot.send_message(callback_query.from_user.id, "Write a message:", parse_mode="HTML")

    await bot.answer_callback_query(callback_query.id)
    await state.set_state(Form_send.send_admin)



@dp.message(Form_send.send_admin)
async def in_text_send_admin(message: types.Message, state: FSMContext):
    id = user_id(message)
    data = await read_user(id)
    language = data.get("language")

    mes_id = message.chat.id
    admin_id = ADMIN_ID
    url = f"tg://user?id={id}"
    
    if message.text:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🤯 Blocking", callback_data=f"block_now:{id}")], 
            ]
        )
        escape_text = escape_special_chars(message.text)
        await bot.send_message(admin_id, f"Пользователь: <a href='{url}'>{id}</a>, написал вам сообщение из бота {NAME_BOT}:", parse_mode="HTML")
        await bot.send_message(admin_id, escape_text, parse_mode="HTML", reply_markup=keyboard)

    if language == "ru":
        await bot.send_message(message.chat.id, "Ваше сообщение отправлено.", parse_mode="HTML")
    elif language == "en":
        await bot.send_message(message.chat.id, "Your message has been sent.", parse_mode="HTML")

    await state.clear()


# Block user:
@dp.callback_query(lambda c: c.data and c.data.startswith('block_now'))
async def blocking_dude(callback_query: types.CallbackQuery):

    data = callback_query.data.split(':')

    if not data:
        logger_bot.error("Error: dont get data - data_button.")
        await bot.send_message(callback_query.from_user.id, "Error: dont get data - data_button.")
        return

    id = int(data[1])
    logger_bot.info(id)

    updated_data = {"user_id": id, "block": True}
    confirm_save = await update_user(updated_data)
    logger_bot.info(f"The user is blocked - {id}.")

    if confirm_save is True:
        # to Admin:
        await bot.send_message(ADMIN_ID, f"Пользователь - {id} успешно заблокирован. Поздравляю бля!")
    
    await bot.answer_callback_query(callback_query.id)
####















#### ADMIN MENU ####
####################

# ADMIN: Get menu:
@dp.message(Command('admin'))
async def admin_menu(message: types.Message):
    id = user_id(message)


    if id != ADMIN_ID:
        logger_bot.error(f"This {id} shit made an attempt to enter to Admin Panel.")
        return

    # Get method default:
    #data_pay = await read_one_methods_pay_by_use(i)
    #use_pay = data_pay.get("title_method_pay")

    # try:
    #     admin_data = await read_admin_data(id)
    #     if not admin_data:
    #         admin_data = {
    #             "user_id": id, 
    #             "operating_mode": False, 
    #             "model_assist": DEFAULT_MODEL_ASSIST_OA
    #         }
    #         if not await add_data_admin(admin_data):
    #             logger_bot.error("Admin_data write error 13")

    #     mode = "is enabled" if admin_data.get("operating_mode") else "is disabled"
    # except:
    #     logger_bot.error("In Table Db dont have admin data")
    #     mode = "is disabled"

    # print(f"AGENT MODE IS: {mode}")

    # <b>👽 AGENT: {mode.upper()}</b>
    # /agent - push to on/off
    # /clear_ag


    admin_menu_text = (
        f"<b>🎛 ADMIN MENU:</b>\n\n"
        f"<b>📊 STATISTICS:</b>\n"
        f"        Info Users – /allUs\n"
        f"        Info Payers – /allPay\n\n"
        f"<b>📝 LOGS:</b>\n"
        f"        Get logs – /logs\n\n"
        f"<b>🗳 BACKUP & RESTORE:</b>\n"
        f"        Backup DB – /bupDb\n"
        f"        Restore DB – /resDb\n"
        f"        Create Tab DB – /crTabDb\n"
        f"        Down users – /dnlUsers\n"
        f"        Restore Users – /resUs\n\n"
        f"<b>💳 METHODS PAY:</b>\n"
        f"        Add Metod – /addMe\n"
        f"        Select Met – /selMet\n"
        f"        Delete Met – /delMe\n\n"
        f"<b>🗑 CLEAR:</b>\n"
        f"        Stat Tab DB – /dStat\n"
        f"        All Tabs DB – /allDel\n"
        f"        Logs – /dLogs\n\n"
        f"<b>📩 SENDING NEWS:</b>\n"
        f"        Mailing – /sendN\n\n"
        f"<b>🧪 SPECIAL:</b>\n"
        f"        Paranoi mode – /blok!\n"
    )

    await message.answer(admin_menu_text, parse_mode="HTML")





# Create Tables in DB:
@dp.message(Command('crTabDb'))
async def create_tebles_in_db_admin(message: types.Message):
    id = user_id(message)

    if id != ADMIN_ID:
        logger_bot.error(f"This {id} shit made an attempt to enter to Admin Panel.")
        return

    if create_tables_in_db(): # Синхронная
        await bot.send_message(message.chat.id, "Tables in the DB were created successfully.")
    else:
        await bot.send_message(message.chat.id, "Error creating DB tables. Check logs for details.")





# Fast Delete Table Statistic in DB:
@dp.message(Command('dStat'))
async def fast_delete_statistic_table_in_db_admin(message: types.Message):
    id = user_id(message)

    if id != ADMIN_ID:
        logger_bot.error(f"This {id} shit made an attempt to enter to Admin Panel.")
        return

    if await fast_delete_statistics_tab():
        await bot.send_message(message.chat.id, "The Statistical table has been successfully deleted.")
    else:
        await bot.send_message(message.chat.id, "Error deleting the Statistical Table.")




# Fast Delete All Tables in DB:
@dp.message(Command('allDel'))
async def delete_all_tables_in_db_admin(message: types.Message):
    id = user_id(message)

    if id != ADMIN_ID:
        logger_bot.error(f"This {id} shit made an attempt to enter to Admin Panel.")
        return

    if await drop_all_tables_and_reset_schema():
        await bot.send_message(message.chat.id, "All tables have been deleted successfully.")
    else:
        await bot.send_message(message.chat.id, "Error deleting all tables.")






# Get_on_json_old_users:
@dp.message(Command('dnlUsers'))
async def get_on_json_old_users(message: types.Message):
    id = user_id(message)

    if id != ADMIN_ID:
        logger_bot.error(f"This {id} shit made an attempt to enter to Admin Panel.")
        return

    name_file = await get_json_old_users_to_db()
    if not name_file:
        await message.answer(f"No users found with money > {MIN_PAY}$ or one more pay")
        return

    if os.path.exists(name_file) and os.path.getsize(name_file) > 0:
        await bot.send_document(message.chat.id, document=types.input_file.FSInputFile(name_file))
    else:
        await bot.send_message(message.chat.id, "File (name_file) is empty or missing.")  









# Admin Restore Users to DB in Json
class Restore_json(StatesGroup):
    load_json = State()

# Resore OLD users to DB:
@dp.message(Command('resUs'))
async def restore_old_users_admin(message: types.Message, state: FSMContext):
    await typing(message)
    id = user_id(message)

    if id != ADMIN_ID:
        logger_bot.error(f"This {id} shit made an attempt to enter to Admin Panel.")
        return

    await bot.send_message(message.chat.id, "Attach and send the necessary json file for recovery Users to DB.", parse_mode="Markdown", reply_markup=ReplyKeyboardRemove()) 
    await state.set_state(Restore_json.load_json)


@dp.message(Restore_json.load_json)
async def load_json_users_to_db(message: Message, state: FSMContext):
    await typing(message)
    id = user_id(message)
    
    if not isinstance(message.document, types.Document):
        await message.answer("It's not a documents")
        return

    file_extension = message.document.file_name.split('.')[-1]
    allowed_extensions = ['json']

    if file_extension not in allowed_extensions:
        await message.answer("You have sent a non-json extension file.")
        return 

    file_name = f"uploaded-json-restore-users.json"
    file_path = f"{PATH_JSON_USERS}{file_name}"
    await bot.download(message.document, file_path)

    await bot.session.close()
    await dp.storage.close()


    res_update_db = await restore_loyal_users_to_db(file_path)

    if res_update_db:
        await message.answer(f"Results of adding regular Users to DB:\n{res_update_db}")
    else:
        await message.answer(f"Error of adding regular Users to DB:\n{res_update_db}")

    await state.clear()






# # ADMIN AI:
# @dp.message(Command('agent'))
# async def switch_ask_agent(message: types.Message):
#     id = user_id(message)

#     if id != ADMIN_ID:
#         logger_bot.error(f"This {id} shit made an attempt to enter to Admin Panel.")
#         return


#     admin_data = await read_admin_data(id)
#     operating_mode = admin_data.get("operating_mode")

#     if operating_mode:
#         answer_bot = "Агент отключен"
#         admin_data = {"user_id": id, "operating_mode": False}
#         if not await update_admin_data(admin_data):
#             print("Admin_data write error 543")
#     else:
#         answer_bot = "Агент активирован"
#         admin_data = {"user_id": id, "operating_mode": True}
#         if not await update_admin_data(admin_data):
#             print("Admin_data write error 546")

#     await admin_menu(message)
#     await message.reply(answer_bot, parse_mode="markdown")




# # Clear Agent Admin:
# @dp.message(Command('clear_ag'))
# async def clear_agent_admin(message: types.Message):
#     id = user_id(message)

#     if id != ADMIN_ID:
#         logging.error(f"This {id} shit made an attempt to enter to Admin Panel.")
#         return

#     admin_data = await read_admin_data(id)
#     assistant_id = admin_data.get("assistant_id")
#     thread_id = admin_data.get("thread_id")

#     assist = AssistOpenAI()

#     # Delete assistant
#     if assistant_id:
#         try:
#             res = await assist.del_assist_oa(assistant_id)
#             if not res or res.get("deleted"):
#                 if not await update_admin_data({"user_id": id, "assistant_id": None}):
#                     logging.error("DB error while clearing assistant_id")
#                 await message.reply("Assistant removed", parse_mode="markdown")
#             else:
#                 await message.reply("Something went wrong... please try again", parse_mode="markdown")
#         except Exception as e:
#             logging.error(f"Assistant delete error: {e}")
#             await message.reply("Failed to remove Assistant", parse_mode="markdown")
#     else:
#         await message.reply("Assistant already missing", parse_mode="markdown")

#     await asyncio.sleep(1)

    # # Delete thread
    # if thread_id:
    #     try:
    #         res = await assist.del_thread_oa(thread_id)
    #         if not res or res.get("deleted"):
    #             if not await update_admin_data({"user_id": id, "thread_id": None}):
    #                 logging.error("DB error while clearing thread_id")
    #             await message.reply("Thread removed", parse_mode="markdown")
    #         else:
    #             await message.reply("Something went wrong... please try again", parse_mode="markdown")
    #     except Exception as e:
    #         logging.error(f"Thread delete error: {e}")
    #         await message.reply("Failed to remove Thread", parse_mode="markdown")
    # else:
    #     await message.reply("Thread already missing", parse_mode="markdown")











# ADMIN: Get stat by users:
@dp.message(Command('allUs'))
async def get_info_by_users(message: types.Message):
    id = user_id(message)

    if id != ADMIN_ID:
        logger_bot.error(f"This {id} shit made an attempt to enter to Admin Panel.")
        return

    all_data = await read_all_users()
    all_static, i = [], 1
    all_static.append(["№", "User id", "Name", "Full Name", "First Name", "Last Name", "Block", "Last Visit", "Time Zone", "Language", "Paid", "Money $", "Notifications", "Dialog", "Dialog Summarization", "Voise answer", "Ai", "Model Language", "Ai draw", "Model Draw", "System Content"])
    for data in all_data:
        all_static.append([i, data.get("user_id"), data.get("name"), data.get("full_name"), data.get("first_name"), data.get("last_name"), data.get("block"), data.get("last_visit"), data.get("time_zone"), data.get("language"), data.get("paid"), data.get("money"), data.get("notifications"), data.get("dialog"), data.get("dialog_sum"), data.get("voice_answer"), data.get("system_content")])
        i += 1

    # Create csv file
    output = StringIO()
    writer = csv.writer(output)
    for row in all_static:
        writer.writerow(row)
    csv_data = output.getvalue()
    output.close()

    # csv file to download
    file_name = f"Users-admin-{random_name_2X()}.csv"
    buffered_input_file = types.input_file.BufferedInputFile(file=csv_data.encode(), filename=file_name)
    try:
        await bot.send_document(chat_id=message.chat.id, document=buffered_input_file)
    except:
        logger_bot.error(f"Error sending documentb User stat")







# ADMIN: SEND NEWS USER's:

class News(StatesGroup):
    news_ru = State()
    news_en = State()
    confirm_send_news = State()

@dp.message(Command('sendN'))
async def sending_news(message: types.Message, state: FSMContext):
    id = user_id(message)

    if id != ADMIN_ID:
        logger_bot.error(f"This {id} shit made an attempt to enter to Admin Panel.")
        return

    await message.answer("News message on RU:", parse_mode="HTML")
    await state.set_state(News.news_ru)

@dp.message(News.news_ru)
async def text_news_ru(message: types.Message, state: FSMContext):
    text_news_ru = message.text
    await state.update_data(text_news_ru=text_news_ru)
    await message.answer("News message on EN:", parse_mode="HTML")
    await state.set_state(News.news_en)

@dp.message(News.news_en)
async def text_news_en(message: types.Message, state: FSMContext):
    text_news_en = message.text
    await state.update_data(text_news_en=text_news_en)
    await message.answer("Type 'Yes' or 'No':", parse_mode="HTML")
    await state.set_state(News.confirm_send_news)

@dp.message(News.confirm_send_news)
async def confirm_send_news(message: types.Message, state: FSMContext):

    if message.text.lower() == "no":
        await message.answer("Canceling.", parse_mode="HTML")
        await state.clear()

    elif message.text.lower() == "yes":
        admin_id = ADMIN_ID
        all_users_data = await read_all_users()
        state_data = await state.get_data()
        text_news_ru = state_data.get("text_news_ru")
        text_news_en = state_data.get("text_news_en")

        #logging.error(all_users_data)
        for user in all_users_data:
            user_id = user.get("user_id")
            language = user.get("language")
            notifications = user.get("notifications")

            if notifications == True or notifications == None:

                try:
                    if language == "ru":
                        await bot.send_message(user_id, text_news_ru, parse_mode="HTML")
                    else:
                        await bot.send_message(user_id, text_news_en, parse_mode="HTML")

                    await bot.send_message(admin_id, f"The message was sent successfully to the user <a href='tg://user?id={user_id}'>{user_id}</a>", parse_mode="HTML")
                except:
                    await bot.send_message(admin_id, f"Error: sending a message to the user <a href='tg://user?id={user_id}'>{user_id}</a>.", parse_mode="HTML")

                aw_time = random.uniform(1, 3)
                await asyncio.sleep(aw_time)
                await bot.send_message(admin_id, f"wating {round(aw_time, 2)}", parse_mode="HTML")

            else:
                await bot.send_message(admin_id, f"The user has disabled notifications. <a href='tg://user?id={user_id}'>{user_id}</a>.", parse_mode="HTML")

        await bot.send_message(admin_id, f"The newsletter is completed.", parse_mode="HTML")
        await state.clear()

    else:
        await message.answer("I don't understand, say it again.", parse_mode="HTML")






# Admin submenu download log
# @dp.message(Command("logs"))
# async def get_logs_bot(message: types.Message):
#     await typing(message)
#     id = user_id(message)

#     if id != ADMIN_ID:
#         logger_bot.error(f"This {id} shit made an attempt to enter to Admin Panel.")
#         return

#     data_folder = Path(PATH_LOGS)
#     empts = True
#     for entry in data_folder.iterdir():
#         if entry.is_file() and entry.stat().st_size > 0:  # Проверяем, что файл не пустой
#             file_path = str(entry.absolute())  # Получаем абсолютный путь
#             try:
#                 await bot.send_document(
#                     chat_id=message.from_user.id,
#                     document=types.input_file.FSInputFile(file_path)
#                 )
#                 empts = False
#                 await asyncio.sleep(0.5)
#             except Exception as e:
#                 logger_bot.error(f"Error sending file log: {file_path}: {e}")
#     if empts:
#         await bot.send_message(message.chat.id, "There are no logging files or they are empty")


@dp.message(Command("logs"))
async def get_logs_bot(message: types.Message):
    await typing(message)
    if user_id(message) != ADMIN_ID:
        logger_bot.error(f"{user_id(message)} tried to enter Admin Panel")
        return

    log_dir = Path(PATH_LOGS)
    sent_any = False

    async def send_as_utf8(path: Path):
        # читаем файл
        raw = path.read_bytes()
        try:
            text = raw.decode('utf-8')
        except UnicodeDecodeError:
            text = raw.decode('cp1251', errors='replace')

        # кладём в буфер
        buf = BytesIO(text.encode('utf-8'))
        buf.name = path.stem + '_utf8.txt'   # чтоб iOS показал превью

        await bot.send_document(
            chat_id=message.from_user.id,
            document=types.input_file.BufferedInputFile(buf.getvalue(), filename=buf.name)
        )

    for entry in log_dir.iterdir():
        if entry.is_file() and entry.stat().st_size:
            try:
                await send_as_utf8(entry)
                sent_any = True
                await asyncio.sleep(0.5)
            except Exception as e:
                logger_bot.error(f"cant send {entry}: {e}")

    if not sent_any:
        await bot.send_message(message.chat.id,
                               "There are no logging files or they are empty")




# Admin clear logs /dLogs
@dp.message(Command("dLogs"))
async def admin_clear_logs(message: types.Message):
    await typing(message)
    id = user_id(message)

    if id != ADMIN_ID:
        logger_bot.error(f"This {id} shit made an attempt to enter to Admin Panel.")
        return


    data_folder = Path(PATH_LOGS)
    for entry in data_folder.iterdir():
        if entry.is_file() and entry.stat().st_size > 0:  # Проверяем, что файл не пустой
            file_path = str(entry.absolute())  # Получаем абсолютный путь
            try:
                with open(file_path, 'w'):
                    pass
                await bot.send_message(message.chat.id, f"The '{file_path}' file has been clearing.")
                await asyncio.sleep(0.5)
            except Exception as e:
                logger_bot.error(f"Error clearing file log: {file_path}: {e}")






# ADMIN: Get Info a Payments:
@dp.message(Command('allPay'))
async def get_info_a_payments_users(message: types.Message):
    id = user_id(message)

    if id != ADMIN_ID:
        logger_bot.error(f"This {id} shit made an attempt to enter to Admin Panel.")
        return

    data_payments = await read_all_payments()

    if not data_payments:
        await message.reply("No payment was found.", parse_mode="Markdown")
        return
    

    all_static = []
    all_static.append(["№", "Date", "Title Method Pay", "$", "user_id"])
    for data in data_payments:
        all_static.append([data.get("id"), data.get("date"), data.get("title_method_pay"), data.get("sum"), data.get("user_id")])

    # Create csv file
    output = StringIO()
    writer = csv.writer(output)
    for row in all_static:
        writer.writerow(row)
    csv_data = output.getvalue()
    output.close()

    # csv file to download
    file_name = f"Info_a_payments-{random_name_2X()}.csv"
    buffered_input_file = types.input_file.BufferedInputFile(file=csv_data.encode(), filename=file_name)
    try:
        await bot.send_document(chat_id=message.chat.id, document=buffered_input_file)
    except:
        logger_bot.error(f"Error sending documentb User stat")








# ADMIN: Add method pay:
class Form_method_pay(StatesGroup):
    title_pay = State()
    text_pay_ru = State()
    text_pay_en = State()

@dp.message(Command('addMe'))
async def add_metod_pay(message: types.Message, state: FSMContext):
    id = user_id(message)

    if id != ADMIN_ID:
        logger_bot.error(f"This {id} shit made an attempt to enter to Admin Panel.")
        return

    await message.reply("The name of the payment method is short (title method):", parse_mode="Markdown") 
    await state.set_state(Form_method_pay.title_pay)

@dp.message(Form_method_pay.title_pay)
async def add_metod_pay_input_title(message: types.Message, state: FSMContext):
    id = user_id(message)

    if id != ADMIN_ID:
        logger_bot.error(f"This {id} shit made an attempt to enter to Admin Panel.")
        return

    await state.update_data(title=message.text)
    await message.reply("The terms of the payment method are detailed for users RU version:", parse_mode="Markdown") 
    await state.set_state(Form_method_pay.text_pay_ru)

@dp.message(Form_method_pay.text_pay_ru)
async def add_metod_pay_input_text_ru(message: types.Message, state: FSMContext):
    id = user_id(message)

    if id != ADMIN_ID:
        logger_bot.error(f"This {id} shit made an attempt to enter to Admin Panel.")
        return

    await state.update_data(text_ru=message.text)

    await message.reply("The terms of the payment method are detailed for users EN version:", parse_mode="Markdown") 
    await state.set_state(Form_method_pay.text_pay_en)

@dp.message(Form_method_pay.text_pay_en)
async def add_metod_pay_input_text_en(message: types.Message, state: FSMContext):
    id = user_id(message)

    if id != ADMIN_ID:
        logger_bot.error(f"This {id} shit made an attempt to enter to Admin Panel.")
        return

    st_data = await state.get_data()
    text_ru = st_data.get("text_ru")
    text_en = message.text

    pay_data = {
        "date": await day_utcnow(),
        "title_method_pay": st_data.get("title"),
        "method_pay_ru": text_ru,
        "method_pay_en": text_en,
    }

    confirm = await add_methods_pay(pay_data)

    if confirm:
        await message.reply("The payment method has been successfully added.", parse_mode="Markdown") 
    await state.clear()
####




# ADMIN: DELETE method pay:
class Form_delete_method(StatesGroup):
    num = State()


@dp.message(Command('delMe'))
async def select_when_deleted_metod_pay(message: types.Message, state: FSMContext):
    id = user_id(message)

    if id != ADMIN_ID:
        logger_bot.error(f"This {id} shit made an attempt to enter to Admin Panel.")
        return

    # Get metods pay data:
    all_metods = await read_all_methods_pay()

    if not all_metods:
        logger_bot.error("Error: Dont have metods pay.")
        await message.reply("*Error*: Dont have metods pay.", parse_mode="Markdown") 
        return

    # Show metods:
    count = []
    methods = ""

    for n in all_metods:
        use = get_use_met_all(n)
        id = str(n.get("id"))
        title = n.get("title_method_pay")
        methods = methods + "\n" + id + " - " + title + " - " + use
        count.append(id)

    await message.reply(f"{methods}\n\nSelect the number corresponding to the name of the method you want to delete. Make sure that it is not in use:", parse_mode="HTML") 
    await state.update_data(count=count)
    await state.set_state(Form_delete_method.num)

    
@dp.message(Form_delete_method.num)
async def delete_metod_pay(message: types.Message, state: FSMContext):
    data = await state.get_data()
    count = data.get("count")

    if message.text == "None":
        await message.reply("a pass!", parse_mode="Markdown") 
        await state.clear()
        return

    try:
        int_value = int(message.text)
    except:
        logger_bot.error(f"This not integer id method pay.")
        await message.reply("This not integer id method pay.", parse_mode="Markdown") 
        return
    
    if message.text not in count:
        logger_bot.error(f"There is no such position.")
        await message.reply(f"There is no item - {int_value}.", parse_mode="Markdown") 
        return

    confirm = await deleted_one_methods_pay(int_value)
    if not confirm:
        logger_bot.error("Error: Not deleted_methods_pay.")
        return

    await message.reply(f"The payment method has been deleted.", parse_mode="HTML")
    await state.clear()



# ADMIN: SELECT method pay:
class Form_change_method(StatesGroup):
    start = State()
    num = State()


@dp.message(Command('selMet'))
async def start_metod_pay(message: types.Message, state: FSMContext):
    id = user_id(message)

    if id != ADMIN_ID:
        logger_bot.error(f"This {id} shit made an attempt to enter to Admin Panel.")
        return
    
    await state.set_state(Form_change_method.start)
    await select_metod_pay(message, state) # Автоматически вызываем следующий обработчик


@dp.message(Form_change_method.start)
async def select_metod_pay(message: types.Message, state: FSMContext):

    try:
        st_data = await state.get_data()
        i = st_data.get("exi")
        place_of_use = st_data.get("place_of_use")
    except:
        logger_bot.error("Info: First change method pay.")

    if not i:
        i = 0
        place_of_use = []

        if USE_SBP_TRANSFER is not False:
            place_of_use.append("use_sbp_transfer")
        if USE_MASTERCARD is not False:
            place_of_use.append("use_mastercard")
        if USE_VISA is not False:
            place_of_use.append("use_visa")
        if USE_MIRCARD is not False:
            place_of_use.append("use_mircard")
        if USE_CRIPTO is not False:
            place_of_use.append("use_cripto")
        if USE_SMS is not False:
            place_of_use.append("use_sms")
        if USE_STARS is not False:
            place_of_use.append("use_stars")
        if USE_TELEGRAM is not False:
            place_of_use.append("use_telegram")
        if USE_DIGITAL is not False:
            place_of_use.append("use_digital")

    # Get metods pay data:
    all_metods = await read_all_methods_pay()

    if not all_metods:
        logger_bot.error("Error: Dont have metods pay.")
        await message.reply("*Error*: Dont have metods pay.", parse_mode="Markdown") 
        return

    # Show metods:
    count = []
    methods = ""


    for n in all_metods:
        use = get_use_met_all(n)
        id = str(n.get("id"))
        title = n.get("title_method_pay")
        methods = methods + "\n" + id + " - " + title + " - " + use
        count.append(id)

    place = place_of_use[i]    

    await message.reply(f"{methods}\n\nSelect the number corresponding to the name of the method that should be used by default in position number {place}:", parse_mode="HTML") 
    await state.update_data(exi=i, place_of_use=place_of_use, count=count)
    await state.set_state(Form_change_method.num)

@dp.message(Form_change_method.num)
async def add_metod_pay_input_title(message: types.Message, state: FSMContext):

    st_data = await state.get_data()
    i = st_data.get("exi")
    place_of_use = st_data.get("place_of_use")
    count= st_data.get("count")

    if message.text == "None":
        await message.reply("a pass!", parse_mode="Markdown") 
        await state.clear()
        return

    try:
        int_value = int(message.text)
    except:
        logger_bot.error(f"This not integer id method pay.")
        await message.reply("This not integer id method pay.", parse_mode="Markdown") 
        return

    if message.text not in count:
        logger_bot.error(f"There is no such position.")
        await message.reply(f"There is no item - {int_value}.", parse_mode="Markdown") 
        return
    
    try:
        pl_use = place_of_use[i]
    except:
        logger_bot.error("Error: Get place_of_use.")
        return

    # Unset default method pay:
    data = await read_one_methods_pay_by_use(pl_use)

    if data:
        pay_data = {
            "id": data.get("id"),
            f"{pl_use}": False,
        }
        confirm = await update_methods_pay(pay_data)
        if not confirm:
            logger_bot.error("Error: Not update_methods_pay.")
            return

    # Set default method pay:
    pay_data = {
        "id": int_value,
        f"{pl_use}": True,
    }
    confirm = await update_methods_pay(pay_data)
    if not confirm:
        logger_bot.error("Error: Not update_methods_pay.")
        return

    await message.reply(f"The default payment method in place use {pl_use} has been successfully installed - {int_value}", parse_mode="HTML")
    i += 1
    if i >= len(place_of_use):
        i = 0
        await message.reply("*The process is completed.*", parse_mode="Markdown")
        await state.clear()
    else:
        await state.update_data(exi=i)
        await state.set_state(Form_change_method.start)
        await select_metod_pay(message, state)



# ADMIN: Backup:
@dp.message(Command('bupDb'))
async def backup(message: types.Message):
    id = user_id(message)

    if id != ADMIN_ID:
        logger_bot.error(f"This {id} shit made an attempt to enter to Admin Panel.")
        return

    confirm = await backup_db() # Create Backup DB

    if confirm:
        await message.reply("The backup copy of the database was created successfully and is presented below. The 3 latest versions are saved in the working folder, the rest are deleted.", parse_mode="HTML")
    else:
        await message.reply("Error: Database backup error.", parse_mode="HTML")

    await asyncio.sleep(0.5)
    data_folder = Path(BACKUP_DB)
    files = [entry for entry in data_folder.iterdir() if entry.is_file()] # Получаем список всех файлов в директории
    sorted_files = sorted(files, key=lambda x: x.stat().st_mtime, reverse=True) # Сортируем список файлов по дате изменения (от новых к старым)
    for file_to_delete in sorted_files[3:]: # Оставляем последние 3 файла, удаляем остальные
        os.remove(file_to_delete)
    logger_bot.info("Remove all file DB, saved 3 latest files.")
    last_downloaded_file = sorted_files[0] if sorted_files else None   # Последний скачанный файл будет первым в отсортированном списке (новейшим) (адрес)
    logger_bot.info("Download last DB file.")

    await bot.send_document(chat_id=message.from_user.id, document=types.input_file.FSInputFile(last_downloaded_file))


#
# Admin Restore DB
#
# Нажимаю кнопку восстановления, прикрепляю свой файл db бинарный в .sql, он загружается в папку download_db.
# Далее скрипт останавливает все запросы и очищает память. Очищается полностью и даже разметка работающей базы 
# и полностью переписывается с закаченного файла. Он не удаляется из папки, не думаю что их будет много...
#
 
 # ADMIN: Restore DB:
class Restor_db(StatesGroup):
    load_db = State()
    #restor_db = State()

#Push button - restore
@dp.message(Command('resDb'))
async def restore_db_admin(message: types.Message, state: FSMContext):
    id = user_id(message)

    if id != ADMIN_ID:
        logger_bot.error(f"This {id} shit made an attempt to enter to Admin Panel.")
        return
    
    await bot.send_message(message.chat.id, "Attach and send the necessary copy of the database for recovery.", parse_mode="Markdown", reply_markup=ReplyKeyboardRemove()) 
    await state.set_state(Restor_db.load_db)

# Next step - download db and restore
@dp.message(Restor_db.load_db)
async def load_a_base(message: Message, state: FSMContext):

    if not isinstance(message.document, types.Document):
        await message.answer("The file you submitted is not a database. Try again.")
        return

    file_extension = message.document.file_name.split('.')[-1]
    allowed_extensions = ['sql']

    if file_extension not in allowed_extensions:
        await message.answer("The file you submitted is not sql . Try again.")
        return    

    # Name file
    formtime = random_name_2X()
    file_path = f"{BACKUP_DB}Uploaded-db-{formtime}.sql"
    await bot.download(message.document, file_path)
    await bot.session.close()
    await dp.storage.close()

    # Restore DB:
    confirm = await restore_db(file_path)

    if confirm:
        await message.answer("The database recovery was successful.")
    else:
        await message.answer("When restoring the database, something went wrong.")

    await state.clear()


####









############ AI ###############
###############################



# Сохранение текста в файл и передача
async def _save_text_to_file(message: types.Message, in_text: str, message_to_user: str) -> bool:
    text = f" {in_text} "
    file_bytes = text.encode("utf-8")
    buffered_file = types.input_file.BufferedInputFile(
        file=file_bytes,
        filename=f"output-{random_name_2X()}.txt"
    )
    try:
        await message.answer_document(
            document=buffered_file,
            caption=f"📄 {message_to_user}"
        )
        return True
    except Exception as e:
        logger_bot.error(f"Error sending document: {e}")
        return False




async def _try_send_message(message, text: str, language: str) -> None:
    """Пытается отправить сообщение с разными форматами."""

    try:
        await message.reply(text, parse_mode="markdown")
    except:
        try:
            await message.reply(text, parse_mode="HTML")  # escape_special_chars(part)
        except:
            # Если совсем не понравится API Telegram то в файл
            err_text = "Ответ содержит сложное форматирование, потому он прикреплен файлом" if language == "ru" else "This response uses rich formatting, so it has been sent as a file"
            logger_bot.error(f"Error: {err_text}")
            await _save_text_to_file(message, text, err_text)




# Attempts to give a response to the user:
async def try_answer_bot(message, answer, data):
    await typing(message)
    id = user_id(message)
    language = data.get("language")

    text = data.get("user_content")
    logger_bot.info(f"User: {id}, Say: {text}")


    # Messages to the administrator about a zero balance
    # If OpenAI is no money for account.
    if "Error: There is no money for OpenAI account" in answer and data.get("ai") == "openai":
        await bot.send_message(ADMIN_ID, f"The user {id} tried to make a request. Error: There is no money for OpenAI account.")

    # If DeepSeek is no money for account.
    if "Insufficient Balance" in answer and data.get("ai") == "deepseek":
        await bot.send_message(ADMIN_ID, f"The user {id} tried to make a request. Error: There is no money for DeepSeek account.")

    # # If Gemini is no money for account.
    # if "money" in answer and data.get("ai") == "gemini":
    #     await bot.send_message(ADMIN_ID, f"The user {id} tried to make a request. Error: There is no money for Gemini account.")

    # # If Anthropic is no money for account.
    # if "money" in answer and data.get("ai") == "anthropic":
    #     await bot.send_message(ADMIN_ID, f"The user {id} tried to make a request. Error: There is no money for Anthropic account.")

    # # If Grok is no money for account.
    # if "money" in answer and data.get("ai") == "grok":
    #     await bot.send_message(ADMIN_ID, f"The user {id} tried to make a request. Error: There is no money for Grok account.")
        


    # Разбиваем текст на части
    text_parts = [answer[i:i + MAX_LEN] for i in range(0, len(answer), MAX_LEN)] # Якобы API Telegram принимает в одном сообщении только 4096 символов, потому делим и частями, на всякий чуть меньше

    if len(text_parts) == 1:
        text = text_parts[0] if text_parts else ""
        await _try_send_message(message, text, language)
    else:
        i = 0
        # Отправляем сообщения по частям
        for part in text_parts:
            i += 1
            numb_part = f"{i} часть:\n\n" if language == "ru" else f"Part {i}:\n\n"
            part_message = numb_part + part
            await _try_send_message(message, part_message, language)





    # VOICE ANSWER:
    if data.get("voice_answer") and len(answer) < 4096:

        # Convert Text to Audio:
        data["user_content"] = answer
        voice_answer_file_path = await get_voice_openai(data)

        # Get tokens to Text input:
        token_in_text = tiktroken(answer)

        data["used_tokens"] = None
        data["used_tokens"] = token_in_text
        data["min"] = None
        
        # Calculation voice:
        confirm = await calculation(data, "text_to_voice")
        if not confirm:
            logger_bot.error("Error: calculation.")

        # Save file answer:
        if os.path.exists(voice_answer_file_path) and os.path.getsize(voice_answer_file_path) > 0:
            await bot.send_document(chat_id=message.from_user.id, document=types.input_file.FSInputFile(voice_answer_file_path))
        else:
            print(f"The file is empty or missing - {voice_answer_file_path}")
            logger_bot.error(f"The file is empty or missing - {voice_answer_file_path}")

        if DEL_AUDIO == True:
            await remove_file_os(voice_answer_file_path)


    # HISTORY:

    # Сheck button dialog user:
    dialog = data.get("dialog")
    if not dialog:
        data = {}
        return


    # Summirization answer:
    dialog_sum = data.get("dialog_sum")
    original_len = len(answer.encode("utf-8"))
    if dialog_sum and original_len > MAX_SIMBOLS:
        #print(f"\n\n\nReal answer: {answer}")
        print("ENABLED SUMM")

        prompt = '''
        Ты — вспомогательный ИИ. Твоя задача — предельно сжать входной текст, сохранив только критически важную информацию, пригодную для последующей генерации ответов.

        Цель — максимальное сокращение:

        - Сохраняй только основные факты, ключевые термины, числа, ссылки и выводы.  
        - Удаляй всё: пояснения, примеры, рассуждения, вводные конструкции, вежливость.  
        - Текст должен быть минимален, но логически понятен.  
        - Если в тексте есть код любого языка программирования — оставь его в неизменном виде.   
        - Игнорируй читаемость, если это помогает сократить.  
        - Не меняй язык входа. Никогда не переводить.  
        - Ничего не добавлять от себя. Никакой переформулировки.  

        Важно:

        - Результат только на оригинальном языке входа.  
        - Не обосновывай, не комментируй, не оформляй.  
        - Просто выдай результат без объяснений.
        '''



        zip_data = {
            "user_id": id,
            "user_content": answer,
            "system_content": prompt,
            "file_path": None,
            "name_file": None,
            "assist_content": None,
            "model_language": "gemini-2.0-flash-lite" # "gpt-4.1-nano" # "gemini-2.5-flash-preview-04-17" # gemini-2.0-flash-exp  gemini-1.5-flash-latest    gemini-2.0-flash-lite-001
        }
        
        # await asyncio.sleep(1)
        zip_answer = await mod_gemini_chat(zip_data) # Сука все на английский переводит, не слушается команд нормально
        #zip_answer = await mod_openai_chat(zip_data) # Как часы, но дороже сука

        print(zip_answer)
        if zip_answer:
            try: 
                answer = zip_answer.get("response")
                #logging.info(f"Summarizacion: {answer}")
                #print(f"\nSummarizacion: {answer}\n")
            except:
                answer = {'response': answer, "used_tokens": NULL_TOKEN}

            used_tokens = zip_answer.get("used_tokens")
            zip_data["used_tokens"] = used_tokens

            # Вывод в процентах уменьшение ответа в процентах
            compressed_len = len(answer.encode("utf-8"))
            reduction_percent = round(100 * (1 - compressed_len / original_len), 1)

            if language == "ru":
                await message.answer(f"📦 <b>Ответ сжат в историю на {reduction_percent}%:</b>", parse_mode="HTML")
            else:
                await message.answer(f"📦 <b>The answer is compressed into a {reduction_percent} story:</b>", parse_mode="Markdown")

            await _try_send_message(message, answer, language)

            # try:
            #     await message.answer(answer, parse_mode="Markdown")
            # except:
            #     try:
            #         await message.answer(answer, parse_mode="HTML")
            #     except:
            #         escape_text = escape_special_chars(answer)
            #         await message.answer(answer)



            # Помечаю для ИИ что ответ сжат:
            """ Каждый следующий ответ, становится все сжатие, пытаюсь таким образом решить проблему """
            answer = f"[!Don’t let the compressed version affect the style or conciseness of your answer!]\n[START COMPRESSED]\n{answer}\n[END COMPRESSED]"
            #print(f"\n{answer}\n")


        confirm = await calculation(zip_data, "text")
        if not confirm:
            print("Error: calculation dialog_sum.")
            logger_bot.error("Error: calculation dialog_sum.")



    # Save history:
    user_content = data.get("user_content")
    update_history = {
        "user_id": id,
        "date": await day_utcnow(),
        "user_say": user_content,
        "assist_say": answer,
    }

    if not await add_discussion(update_history):
        print("Error save history.")
        logger_bot.error("Error save history.")

    data = {}
    return


#### GET CHAT to AI:
async def mod_tex(data, message):

    await typing(message)
    id = user_id(message)
    history, assist_content = None, None

    # Building a story:
    dialog = data.get("dialog")
    if dialog:
        history = await read_discussion(id)

    if history:
        assist_content = []
        history.reverse()
        for chunk in history:
            # time_chunk = chunk.get("date")
            # date_time = await unformat_date(time_chunk)
            # dates = f"{date_time.get('day')} {date_time.get('time')}: "
            assist_content.append({"user": chunk.get("user_say")}) # dates + 
            assist_content.append({"assistant": chunk.get("assist_say")})

    # elif not history:
    #     logger_bot.info("Info: History is empty.")

    # Add to Data - assist_content:
    if assist_content:
        data["assist_content"] = assist_content


    # Select AI:
    get_ai = data.get("ai")
    if get_ai == "gemini":
        answer = await mod_gemini_chat(data)
    elif get_ai == "openai":
        answer = await mod_openai_chat(data)
    elif get_ai == "claude":
        answer = await mod_claude_chat(data)
    elif get_ai == "deepseek":
        answer = await mod_deepseek_chat(data)
    elif get_ai == "grok":
        answer = await mod_grok_chat(data)

    print(answer)

    if not answer:
        return False

    '''
    Когда заканчиваются деньги, OpenAI шлет просто str другой структуры
    '''
    if isinstance(answer, dict):
        response = answer.get("response") 
        used_tokens = answer.get("used_tokens")
    else:
        response = answer
        used_tokens = NULL_TOKEN

    data["used_tokens"] = used_tokens

    confirm = await calculation(data, "text")
    if not confirm:
        logger_bot.error("Error: calculation.")

    # Attempts to give a response to the user:
    await try_answer_bot(message, response, data)



#### IMG + TEXT ####
class Form_text_img(StatesGroup):
    no_caption = State()


# Add a separate description of the image:
@dp.message(Form_text_img.no_caption, F.content_type.in_({'text'}))
async def add_text_to_photo(message: Message, state: FSMContext):
    id = user_id(message)
    answer = None
    # Из прошлого State
    data_state = await state.get_data()
    all_data = data_state.get('all_data')

    all_data["user_content"] = message.text

    logger_bot.info(f"User: {id} sent a photo and Say: {message.text}")

    if all_data.get('ai') == "gemini":
        answer = await mod_gemini_chat(all_data)
    elif all_data.get('ai') == "openai":
        answer = await mod_openai_chat(all_data)
    else:
        answer = await mod_gemini_chat(all_data)
    # elif all_data.get("ai") == "claude":
    #     answer = await mod_claude_chat(all_data)
    # elif all_data.get("ai") == "deepseek":
    #     answer = await mod_deepseek_chat(all_data)
    # elif all_data.get("ai") == "grok":
    #     answer = await mod_grok_chat(all_data)

    if not answer:
        return

    all_data["file_path"] = None
    all_data["name_file"] = None


    text = answer.get("response")
    used_tokens = answer.get("used_tokens")
    all_data["used_tokens"] = None
    all_data["used_tokens"] = used_tokens

    confirm = await calculation(all_data, "text")
    if not confirm:
        logger_bot.error("Error: calculation.")

    # Attempts to give a response to the user:
    await try_answer_bot(message, text, all_data)
    await state.clear()



# PHOTO input:
async def mod_photo(data, message, state: FSMContext):

    await typing(message)
    answer = {}
    id = user_id(message)
    language = data.get("language")

    # Telegram always saves in jpg in compress
    photo = message.photo[-1]  # Используем самый большой размер фотографии
    file_id = photo.file_id
    little = random_name_2X()
    photo_file_name = f"photo-{little}-{message.photo[-1].file_id}.jpg"
    file_path = f'{DOWNLOAD}{photo_file_name}'
    try:
        file = await bot.get_file(file_id)
        await bot.download_file(file.file_path, file_path)
    except:
        logger_bot.error("Error: Couldn't get a photo.")
        await message.reply("Error: Couldn't get a photo.", parse_mode="Markdown")
        return

    data["file_path"] = file_path
    data["name_file"] = photo_file_name


    if data.get("user_content"):

        text = data.get("user_content")
        logger_bot.info(f"User: {id} sent a photo and Say: {text}")

        if data.get("ai") == "gemini":
            answer = await mod_gemini_chat(data)
        elif data.get("ai") == "openai":
            answer = await mod_openai_chat(data)
        else:
            answer = await mod_gemini_chat(data)
        # elif data.get("ai") == "claude":
        #     answer = await mod_claude_chat(data)
        # elif data.get("ai") == "deepseek":
        #     answer = await mod_deepseek_chat(data)
        # elif data.get("ai") == "grok":
        #     answer = await mod_grok_chat(data)

        if not answer:
            return

        if DEL_DOWNLOADS == True:
            await remove_file_os(file_path)

        text = answer.get("response")
        used_tokens = answer.get("used_tokens")
        data["used_tokens"] = None
        data["used_tokens"] = used_tokens

        confirm = await calculation(data, "text")
        if not confirm:
            logger_bot.error("Error: calculation.")


        # Attempts to give a response to the user:
        await try_answer_bot(message, text, data)
        await state.clear()
    

    elif not data.get("user_content"):
        await state.update_data(all_data=data)
        if language == "ru":
            await message.reply(f"Вопрос по прикрепленному изображению:", parse_mode="Markdown")
        elif language == "en" or language is None:
            await message.reply(f"Question about the attached image:", parse_mode="Markdown")
        await state.set_state(Form_text_img.no_caption)





# DOCUMENTS input:
async def mod_documents(data, message, state: FSMContext):

    await typing(message)
    id = user_id(message)
    language = data.get("language")

    # Get id and name file:
    file_id = message.document.file_id
    little = random_name_2X()
    name_file = little + "-" + message.document.file_name

    # Get extension:
    match = re.search(r'\.([^.]+)$', name_file)
    if not match:
        logger_bot.error(f"File dont have extension - {name_file}")
    extension = match.group(1)  # Получаем расширение без точки


    #### IMAGE ####
    if extension.lower() == "jpg" or extension.lower() == "png":

        file_path = f'{DOWNLOAD}{name_file}'

        try:
            file = await bot.get_file(file_id)
            await bot.download_file(file.file_path, file_path)
        except:
            logger_bot.error("Error: Couldn't get a picture.")
            await message.reply("Error: Couldn't get a picture.", parse_mode="Markdown")
            return


        data["file_path"] = file_path
        data["name_file"] = name_file

        if data.get("user_content"):

            text = data.get("user_content")
            logger_bot.info(f"User: {id} sent a photo.document and Say: {text}")

            if data.get("ai") == "openai":
                answer = await mod_openai_chat(data)
            elif data.get("ai") == "gemini":
                answer = await mod_gemini_chat(data)
            else:
                answer = await mod_gemini_chat(data)
            # elif data.get("ai") == "claude":
            #     answer = await mod_claude_chat(data)
            # elif data.get("ai") == "deepseek":
            #     answer = await mod_deepseek_chat(data)
            # elif data.get("ai") == "grok":
            #     answer = await mod_grok_chat(data)

            if not answer:
                return
            
            if DEL_DOWNLOADS == True:
                await remove_file_os(file_path)

            data["file_path"] = None
            data["name_file"] = None
            
            text = answer.get("response")
            used_tokens = answer.get("used_tokens")
            data["used_tokens"] = None
            data["used_tokens"] = used_tokens

            confirm = await calculation(data, "text")
            if not confirm:
                logger_bot.error("Error: calculation.")

            # Attempts to give a response to the user:
            await try_answer_bot(message, text, data)
            await state.clear()

        elif not data.get("user_content"):
            await state.update_data(all_data=data)
            if language == "ru":
                await message.reply(f"Вопрос по прикрепленному изображению:", parse_mode="Markdown")
            elif language == "en" or language is None:
                await message.reply(f"Question about the attached image:", parse_mode="Markdown")
            await state.set_state(Form_text_img.no_caption)

    # #### DOC ####
    # elif extension.lower() == "doc":
    #     await message.reply("Серьезно...?", parse_mode="markdown")
    #     return
    #
    # else:
    #     await message.answer(f"The bot does not support this file yet, sorry - {name_file}", parse_mode="Markdown")
    #     logger_bot.error(f"The bot does not support this file yet, sorry - {name_file}")
    #     return

# "docx", "odt", "rtf", "txt", "xls", "xlsx", "ods", "ppt", "pptx", "odp", "pdf", "html", "htm", "csv", "md", "xml", "json", "doc"







# @dp.message(Command('geen'))
# async def geen_say(message: types.Message):
#     id = user_id(message)

#     if id != ADMIN_ID:
#         logging.error(f"This {id} shit made an attempt to enter to Admin Panel.")
#         return


#     all_data = await assist_admin_db_users()
#     if not all_data:
#         print("Error get data of assist_admin_db_users (546)")


#     print(all_data)
    #await message.reply(all_data, parse_mode="markdown")
    # all_static, i = [], 1
    # all_static.append(["№", "User id", "Name", "Full Name", "First Name", "Last Name", "Block", "Last Visit", "Time Zone", "Language", "Paid", "Money $", "Notifications", "Dialog", "Dialog Summarization", "Voise answer", "Ai", "Model Language", "Ai draw", "Model Draw", "System Content"])
    # for data in all_data:
    #     all_static.append([i, data.get("user_id"), data.get("name"), data.get("full_name"), data.get("first_name"), data.get("last_name"), data.get("block"), data.get("last_visit"), data.get("time_zone"), data.get("language"), data.get("paid"), data.get("money"), data.get("notifications"), data.get("dialog"), data.get("dialog_sum"), data.get("voice_answer"), data.get("system_content")])
    #     i += 1



    # # Create csv file
    # output = StringIO()
    # writer = csv.writer(output)
    # for row in all_static:
    #     writer.writerow(row)
    # csv_data = output.getvalue()
    # output.close()


    # # csv file to download
    # file_name = f"Users-admin-{random_name_2X()}.csv"
    # buffered_input_file = types.input_file.BufferedInputFile(file=csv_data.encode(), filename=file_name)
    # try:
    #     await bot.send_document(chat_id=message.chat.id, document=buffered_input_file)
    # except:
    #     logging.error(f"Error sending documentb User stat")




#### Admin AI: ####
###################


# # Запрос Ассистенту OpenAI:
# async def admin_ai(question, message):
#     id = user_id(message)

#     admin_data = await read_admin_data(id)
#     if not admin_data:
#         return False
#     elif not admin_data.get("operating_mode"):
#         return False
    
#     assist = AssistOpenAI()
#     thread_id = admin_data.get("thread_id")
#     assistant_id = admin_data.get("assistant_id")
#     new_assist = not thread_id or not assistant_id # new_assist = True if not thread_id or not assistant_id else False
#     instructions = """
#     Ты — внутренний ассистент для управления и аналитики Telegram ИИ-бота.

#     1. Твои задачи:

#     Пояснять свое назначение и возможности.
#     Предоставлять статистику.
#     Анализировать данные.

#     2. Ограничения:
#     Не отвечаешь на вопросы не по теме.

#     Смена режима:
#     По запросу администратора можешь переключиться в обычный режим ИИ после подтверждения:
#     «Перейти в обычный режим ИИ? Подтвердите, пожалуйста.»

#     Получение данных из базы:
#     По запросу администратора можешь получить данные из базы данных после подтверждения:
#     «Загрузить данные из базы? Подтвердите, пожалуйста.»

#     """
#     model = admin_data.get("model_assist")
#     user_content = question 
#     tools = [
#         {
#             "type": "function",
#             "function": {
#                 "name": "close",
#                 "description": "выйти из режима и придумать короткий прощальный эпичный текст", 
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "text": {"type": "string"},
#                     },
#                     "required": ["text"]
#                 }
#             }
#         },
#         {
#             "type": "function",
#             "function": {
#                 "name": "statistic",
#                 "description": "получить статистику из базы данных телеграмм бота", 
#                 "parameters": {
#                     "type": "object",
#                     "properties": {}
#                 }
#             }
#         }
#     ]

#     # Создание и запуск Ассистента или создание или запуск:
#     asist_data = await assist.run_custom_assist_0525_oa(
#         thread_id, assistant_id, instructions, model, user_content, tools
#     )

#     if new_assist:
#         thread_id = asist_data.get("thread_id")
#         assistant_id = asist_data.get("assistant_id")
#         new_assist_data = {
#             "thread_id": thread_id,
#             "assistant_id": assistant_id,
#             "user_id": id
#         }

#         if not await update_admin_data(new_assist_data):
#             logging.error("Failed to update admin data (5404)")


#     # Получение id запущенного Асистента:
#     run_id = asist_data.get("run_id")
#     if not run_id:
#         logging.error("Error, note have run_id 4432")
#         await message.reply("Something went wrong... please try again", parse_mode="markdown")
#         return True




#     # Цикл ожидания ответа ассистента:
#     while True:
#         '''
#         Цикл для получения статуса выполнения (status) от OpenAI Assistant.
#         Ограничения API требуют сделать задержки между запросами, иначе блокируется.
        
#         Возможные статусы:
#         - queued (в очереди)
#         - in_progress (в процессе)
#         - requires_action (требуется действие)
#         - completed (завершено)
#         '''
#         response = await assist.get_retrieve_oa(thread_id, run_id)
#         if not response:
#             continue

#         status = response.get("status")

#         # print(f"Status from Assist OpenAI: {status}")
#         # logging.info(f"Status from Assist OpenAI: {status}")

#         # Обработка текстового ответа:
#         if status == "completed":
#             assistant_reply = response.get("message")
#             if assistant_reply:
#                 # TRY TRANSFER ANSWER TO TELERAM:
#                 try:
#                     await message.reply(assistant_reply, parse_mode="markdown")
#                 except:
#                     try:
#                         await message.reply(assistant_reply, parse_mode="HTML")
#                     except:
#                         escape_text = escape_special_chars(assistant_reply)
#                         await message.reply(escape_text)
#                 return True

#         # Если ассистент требует внешнее действие:
#         elif status == "requires_action":
#             tool_calls = response.get("tool_calls")
#             break
        
#         # Если нет статуса – считаем, что произошла ошибка:
#         elif status == None:
#             print("Error: Missing status in response from get_retrieve_oa()")
#             logging.error("Error: Missing status in response from get_retrieve_oa()")
#             return True

#         # Задержка для избежания ограничения по частоте:
#         await asyncio.sleep(2)



#     # Ассистент запускает команды:
#     tool_outputs = []

#     for tool_call in tool_calls:

#         # Extract function name and arguments from assistant's tool_call:
#         func_name = tool_call['function']['name']
#         arguments = json.loads(tool_call['function']['arguments'])

#         if func_name == "close":
#             # Update admin state (deactivate):
#             admin_data = {"user_id": id, "operating_mode": False}
#             if not await update_admin_data(admin_data):
#                 logging.error("Admin update failed (code 4543)")

#             # Get response text and send message (отправка текста пользователю)
#             response_text = arguments["text"]
#             await message.reply(response_text, parse_mode="markdown")


#         if func_name == "statistic":

#             response_text = await assist_admin_db_users()
#             if not response_text:
#                 logging.error("Error get data of assist_admin_db_users (546) or not have data")
#             else:
#                 await message.reply("Данные получены. Вы можете уточнить вопрос по данным..", parse_mode="markdown")


#         else:
#             # Unknown function handler (обработка неизвестной команды)
#             response_text = "Неизвестная функция (Unknown function)"

#         # Append result for assistant output return
#         tool_outputs.append({
#             "tool_call_id": tool_call["id"],  # id вызова инструмента
#             "output": response_text
#         })

#     # Send back full result to assistant (ответ ассистенту)
#     final_output = await assist.returning_result_assist_oa(thread_id, run_id, tool_outputs)

#     return True











# Проблема в том, что ты пытаешься отправить tool output (вывод инструмента) в run, у которого статус "expired" (истекший).

# Когда status = "expired", run больше не принимает никакие данные — он как бы завершен по времени или по таймауту. Запрос больше невалиден (invalid).

# Просто:

# - Либо создай новый run,
# - Либо следи за его статусом перед тем, как что-то слать (run['status'] должен быть "in_progress").




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


async def forget_history(question, message):
    forget_words = {"забудь", "forget"}
    question_words = set(re.sub(r'[^\w\s]', '', question.lower()).split())
    if forget_words & question_words:
        await reset_history(message)
        return True
    return False



#### VOICE input to TEXT and send AI:
async def mod_voice_to_text(data, message):

    id = user_id(message)
    language = data.get("language")

    voice = message.voice
    file_id = voice.file_id
    little = random_name_2X()
    voice_file_name = f"voice-{little}-{voice.file_id}.ogg"
    file_path = f'{VOICE_FOLDER}{voice_file_name}'
    try:
        file = await bot.get_file(file_id)
        await bot.download_file(file.file_path, file_path)
    except:
        logger_bot.error("Error: Voice transmission error.")
        await message.reply("Error: Voice transmission error.", parse_mode="Markdown")
        return

    data["file_path"] = file_path
    data["name_file"] = voice_file_name

    if data.get("ai_voice_to_text") == "openai":
        convert_answer = await get_text_openai(data)
    # elif data.get("ai_voice_to_text") == "gemini":
    #     convert_answer = await get_text_openai(data)

    print(f"\n{convert_answer}\n")
    
    if DEL_VOICE == True:
        await remove_file_os(file_path)

    if not convert_answer:
        logger_bot.error("Error: Convet voice to text.")
        await message.reply("Error: Convet voice to text.", parse_mode="Markdown")
        return

    question = convert_answer.get("response")

    data["user_content"] = question
    data["file_path"] = None
    data["name_file"] = None
    data["used_tokens"] = None
    data["min"] = convert_answer.get("minutes")

    if not await calculation(data, "voice_to_text"):
        logger_bot.error("Error: calculation tokens voice to text.")
        return

    data["min"] = None

    if language == "ru":
        await message.answer(f"📎 <b>Из вашего голосового:</b>\n", parse_mode="HTML")
    else:
        await message.answer(f"📎 <b>From your voicemail:</b>\n", parse_mode="HTML")
    for i in range(0, len(question), MAX_LEN):
        await message.answer(question[i:i+MAX_LEN], parse_mode="HTML")

    # Check forgot - забыть историю
    if await forget_history(question, message):
        return

#    # Check Admin AI
#     if await admin_ai(question, message):
#         return

    await mod_tex(data, message) # there is also a calculation of statistics

 



#### DRAW ####
# Set State
class Form_draw(StatesGroup):
    draw = State()


# Confirmations to draw:
@dp.message(Form_draw.draw)
async def process_draw(message: types.Message, state: FSMContext):

    id = user_id(message)
    data_state = await state.get_data()
    all_data = data_state.get("all_data")
    all_data["user_content"] = message.text
    language = all_data.get("language")

    logger_bot.info(f"User: {id} image generation and Say: {message.text}")

    if message.text.lower() == "no" or message.text.lower() == "нет":
        if language == "ru":
            await bot.send_message(message.chat.id, "❌ Генерация изображения отменена. ", parse_mode="Markdown") 
        elif language == "en" or language is None:
            await bot.send_message(message.chat.id, "❌ Image generation has been canceled. ", parse_mode="Markdown")
        return await state.clear()

    if language == "ru":
        await bot.send_message(message.chat.id, "Изображение уже генерируется, ожидайте.", parse_mode="Markdown") 
    elif language == "en" or language is None:
        await bot.send_message(message.chat.id, "The image is already being generated, expect it.", parse_mode="Markdown")

    # Generation image:
    if all_data.get("ai_draw") == "openai":
        answer = await mod_openai_dall_e(all_data)
    # elif all_data.get("ai_draw") == "gemini":
    #     answer = await mod_openai_dall_e(all_data) # Sorry)))

    if not answer:
        logger_bot.error("Error: Generation image.")
        return

    logger_bot.info(answer)
    # Response to the user:
    await bot.send_message(message.chat.id, answer.get("response"))

    # get model dall-e
    peps_model = set_model_dalle(all_data)

    # Statistic:
    all_data["file_path"] = None
    all_data["name_file"] = None
    all_data["used_tokens"] = None
    all_data["min"] = None
    all_data["model_draw"] = peps_model

    confirm = await calculation(all_data, "gen_img")

    if not confirm:
        logger_bot.error("Error: calculation tokens draw.")
        return

    await state.clear()






# Drawing:
async def mod_gen_img(data, message, state: FSMContext):

    await state.update_data(all_data=data, message=message)
    language = data.get("language")

    if language == "ru":
        await bot.send_message(message.chat.id, "🖼 Опишите желаемое изображение или 'Нет' для отмены: ", parse_mode="Markdown") 
    elif language == "en" or language is None:
        await bot.send_message(message.chat.id, "🖼 Describe the desired image or 'No' to cancel: ", parse_mode="Markdown")

    await state.set_state(Form_draw.draw)





# Check request drawing:
async def check_request_drawing(question):
    typecontent = None

    draw_words = {"/gen_draw"}
    question_words = set(question.lower().split())
    if draw_words & question_words:
        typecontent = "draw"

    return typecontent






# WHEN USER SEND FILE:
# Пользователь передает файл вместо текста docx, xlsx, md, txt, json, csv
async def get_data_doc_file(message: types.Message, language: str):
    text_content = ""
    caption = ""

    if message.caption:
        caption = message.caption

    if message.text:
        text_content = message.text
    elif message.document:
        file_size = MAX_SIZE_DOC * 1024 * 1024
        if message.document.file_size > file_size:
            error_text = f"⚠ Файл слишком большой (макс. {file_size} МБ)" if language == "ru" else f"⚠ The file is too large (max . {file_size} MB)"
            await message.answer(error_text, parse_mode="HTML")
            return "end"
        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path # В ОЗУ
        # Скачиваем файл
        downloaded_file = await bot.download_file(file_path)
        file_bytes = downloaded_file.read()

        # MD TXT
        if message.document.mime_type == "text/plain" or message.document.file_name.endswith(('.txt', '.md')):
            text_content = file_bytes.decode('utf-8')

        # DOCX:
        elif message.document.file_name.endswith('.docx'):
            doc = docx.Document(io.BytesIO(file_bytes))
            text_content = "\n".join([paragraph.text for paragraph in doc.paragraphs])

        # PDF:
        elif message.document.file_name.endswith('.pdf'):
            try:
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
                text_content = "\n".join([page.extract_text() for page in pdf_reader.pages])
            except Exception as e:
                error_text = f"❌ Ошибка чтения PDF: {e}" if language == "ru" else f"❌ PDF reading error: {e}"
                await message.answer(error_text, parse_mode="HTML")
                return "end"
        # JSON:
        elif message.document.file_name.endswith('.json'):
            try:
                json_data = json.loads(file_bytes.decode('utf-8'))  # Парсим JSON
                text_content = str(json_data)  # Преобразуем в строку для примера гавное ебаное, переделаю потом нормально...
                # Или работаем напрямую с json_data (dict/list)
            except json.JSONDecodeError as e:
                error_text = f"❌ Ошибка парсинга JSON: {e}" if language == "ru" else f"❌ JSON parsing error: {e}"
                await message.answer(error_text, parse_mode="HTML")
                return "end"

        # XLSX:
        elif message.document.file_name.endswith('.xlsx'):
            try:
                # Используем pandas для чтения Excel (можно и openpyxl)
                df = pd.read_excel(io.BytesIO(file_bytes))
                text_content = df.to_string(index=False)  # без индексов для краткости
            except Exception as e:
                await message.answer(f"❌ Ошибка чтения Excel: {e}")
                return "end"

        # CSV:
        elif message.document.file_name.endswith('.csv'):
            try:
                df = pd.read_csv(io.BytesIO(file_bytes))
                text_content = df.to_string(index=False)
            except Exception as e:
                await message.answer(f"❌ Ошибка чтения CSV: {e}")
                return "end"

    if caption and text_content:
        text_content = f":\n\n{text_content}"

    return f"{caption}{text_content}" if caption else text_content








#### MAIN HENDLER INCOMING
@dp.message(F.content_type.in_({'text', 'document', 'photo', 'audio', 'voice', })) # 'location' 'contact' 'video_note'  'video'  'sticker'
async def second_function(message: types.Message, state: FSMContext):

    if message.from_user.is_bot:
        await message.answer("🚔 Sorry, the bot only works with humans.")
        return



    #### DEFAULT VALUES:

    # Language models:
    default_model_ai = {
        "openai": AI_DEFAULT_MODEL_OPENAI,
        "gemini": AI_DEFAULT_MODEL_GEMINI,
        "claude": AI_DEFAULT_MODEL_CLAUDE,
        "deepseek": AI_DEFAULT_MODEL_DEEPSEEK,
        "grok": AI_DEFAULT_MODEL_GROK,
    }
    # Gen Img models:
    default_model_draw = {
        "openai": DEFAULT_DALL_E,
        #"midjourney": 
    }
    # Gen Audio models:
    default_model_audio = {
        "openai": AI_DEFAULT_MODEL_TEXT_TO_VOICE,
    }
    # Transcription voice models:
    default_model_voice = {
        "openai": AI_DEFAULT_MODEL_VOICE_TO_TEXT,
    }

    # SYS
    file_path, received_object, photo_file_name, name_file, system_content, model_voice_to_text, voice, language = (None,) * 8
    typecontent = message.content_type
    ai, ai_draw, ai_voice_to_text, ai_text_to_voice, voice_answer, dialog, img_size, n_number, dialog_sum, voice, voice_speed, img_quality, img_style = AI_DEFAULT, AI_DRAW, AI_VOICE_TO_TEXT, AI_TEXT_TO_VOICE, VOICE_THE_ANSWER, DIALOG, IMG_SIZE, N_NUMBER, DIALOG_SUM, VOICE, VOICE_SPEED, IMG_QUALITY, IMG_STYLE


    await typing(message)
    id = user_id(message)

    # Getting the user's system data from the database:
    data_from_db = await read_user(id)
    if not data_from_db:
        await forced_start(message)
        return

    language = data_from_db.get("language", "en")

    # Проверка входного на документ
    question = await get_data_doc_file(message, language)
    if question == "end":
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

    # Get ai_voice_to_text:
    if data_from_db.get("ai_voice_to_text"):
        ai_voice_to_text = data_from_db.get("ai_voice_to_text")

    # Get model draw ai:
    if data_from_db.get("model_voice_to_text"):
        model_voice_to_text = data_from_db.get("model_voice_to_text")
    else:
        model_voice_to_text = default_model_voice[ai_voice_to_text]

    # Get ai_text_to_voice:
    if data_from_db.get("ai_text_to_voice"):
        ai_text_to_voice = data_from_db.get("ai_text_to_voice")

    # Get model_text_to_voice:
    if data_from_db.get("model_text_to_voice"):
        model_text_to_voice = data_from_db.get("model_text_to_voice")
    else:
        model_text_to_voice = default_model_audio[ai_text_to_voice]

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

    # Get dialog_sum:
    if data_from_db.get("dialog_sum") is not None:
        dialog_sum = data_from_db.get("dialog_sum")

    if data_from_db.get("money") <= 0:
        if language == "ru":
            await message.reply(f"Недостаточно средств, пополните счет.", parse_mode="Markdown")
        else:
            await message.reply(f"There are not enough funds, top up your account.", parse_mode="Markdown")
        return

    if data_from_db.get("block") == True:
        if language == "ru":
            await message.reply(f"К счастью, ты заблокирован...", parse_mode="Markdown")
        else:
            await message.reply(f"Fortunately, you're blocked...", parse_mode="Markdown")
        return


    # Checking the text for a DRAWING request:
    if typecontent == "text":
        user_paid = data_from_db.get("paid")
        drawing_request = await check_request_drawing(question)
        typecontent = drawing_request or typecontent
        if typecontent == "draw" and user_paid == 0:
            await message.reply("😳 Доступно после пополнения счета" if language == "ru" else "😳 Available after adding funds to your account")
            logger_bot.error("Error: 😳 Доступно после пополнения счета")
            return





    # Checking the text for a CLEAR HISTORY:
    if typecontent == "text":
        if await forget_history(question, message):
            return

    # # Checking ADMIN AI:
    # if typecontent == "text" and id == ADMIN_ID:
    #     if await admin_ai(question, message):
    #         return

    # Data collection to API:
    data = {
        "user_id": id,
        "ai": ai,
        "model_language": model_language,

        "ai_draw": ai_draw,
        "model_draw": model_draw,

        "ai_voice_to_text": ai_voice_to_text,
        "model_voice_to_text": model_voice_to_text,

        "ai_text_to_voice": ai_text_to_voice,
        "model_text_to_voice": model_text_to_voice,

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
    data["user_content"] = question
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
        logger_bot.error(f"Not support type file, sorry.")
        return

    arguments = {
        'data': data,
        'message': message,
    }



    if typecontent == "document":
        match = re.search(r'\.([^.]+)$', message.document.file_name) # Получаю расширение из имени документа
        extension = match.group(1)
        if extension.lower() in EXTENS_DOC_SUPPORT:
            typecontent = "text"
            await input_content_type[typecontent](**arguments)
            return
        elif extension.lower() in ["jpg", "png"]:
            arguments["state"] = state  # state: FSMContext
            await input_content_type[typecontent](**arguments)
            return
        else:
            error_text = f"⚠ Поддерживаются только файлы: {str(EXTENS_DOC_SUPPORT)} + jpg + png" if language == "ru" else f"⚠ Only files are supported: {str(EXTENS_DOC_SUPPORT)} + jpg + png"
            await message.answer(error_text, parse_mode="HTML")
            return
    elif typecontent == "draw" or typecontent == "photo":
        arguments["state"] = state #state: FSMContext
        await input_content_type[typecontent](**arguments)
        return
    else:
        await input_content_type[typecontent](**arguments)
        return


####


  








# main def polling
async def main_bot() -> None:
    await dp.start_polling(bot, skip_updates=False) # skip_updates=False обрабатывать каждое сообщение с серверов Telegram, важно для принятия платежей


# Start polling
if __name__ == "__main__":
    try:
        asyncio.run(main_bot())
    except Exception as e:
        logger_bot.error(f"Error: An error occurred: {e}.")
        print(f"An error occurred: {e}.")