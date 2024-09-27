from get_keys import TELEGRAM_BOT_TOKEN, USERNAME_API_AI, KEY_API_AI, VALUE_KEY_API_AI, USER_DB, PASSWORD_DB, ADMIN_ID
from config import DOWNLOADS_FOLDER, AI_DEFAULT, AI_DEFAULT_MODEL_GEMINI, AI_DEFAULT_MODEL_OPENAI, VOICE_THE_ANSWER, VOICE_FOLDER, AUDIO_FOLDER, GIFT, DEFAULT_DALL_E, AI_DRAW, AI_VOICE, AI_AUDIO, DIALOG, DIALOG_SUM, IMG_SIZE, N_NUMBER, VOICE, VOICE_SPEED, IMG_SIZE, N_NUMBER, IMG_QUALITY, IMG_STYLE, AI_DEFAULT_MODEL_GET_AUDIO, AI_DEFAULT_MODEL_GET_VOICE, LANGUAGE


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
from general_functions import escape_special_chars, random_name_2X, day_utcnow
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
    text = data["language"] if data.get("language") is not None else LANGUAGE
    ai = data["ai"] if data.get("ai") is not None else AI_DEFAULT
    dialog = data["dialog"] if data.get("dialog") is not None else DIALOG
    dialog = str(dialog)


    menu_en = f'''

<b>⚙️ SETTINGS:</b>
<b>{text.upper()}</b> : language /en or /ru
<b>{ai.upper()}</b> : AI /openai or /gemini
<b>{dialog.upper()}</b> : dialogue /di_on or /di_off
    Return an audio response with a text response /yes or /no - YES.
    Summarize the story /yes or /no - YES.
    Notifications /yes or /no - Yes.
    You can fine-tune each position or just leave it as default.

    <b>📝 Text CHAT:</b>

    OpenAI:
    /4_o_mini - bot about info
    /4_turbo - bot about info

    Gemini:
    /4_o_mini - bot about info
    /4_turbo - bot about info

    <b>🌇 Creating an IMAGE:</b>

    Dall-e settings:
    /set_dall_3 - set Dall-e 3
    /set_dall_2 - set Dall-e 2
    /setabouttext - change bot about info
    /setuserpic - change bot profile photo
    /setcommands - change the list of commands
    /deletebot - delete a bot

    Midjourney:
    /my_vote_for_mid - vote for the implementation, already 45 ❤️

    <b>🗣 Voice calls to AI:</b>

    OpenAI:
    /setcommands - change the list of commands
    /deletebot - delete a bot

    <b>🎧 Audio from AI:</b>

    OpenAI:
    /setcommands - change the list of commands
    /deletebot - delete a bot

    <b>💳 Balance and payment:</b>
    /deletebot - delete a bot
    /deletebot - delete a bot

    <b>🗞 Reports and statistics:</b>
    /deletebot - delete a bot
    /deletebot - delete a bot

    '''

    menu_ru = f'''

<b>⚙️ Настройки:</b>
<b>{text.upper()}</b> : язык /en или /ru
<b>{ai.upper()}</b> : ИИ /openai или /gemini
<b>{dialog.upper()}</b> : диалог /di_on или /di_off
    Dialogue with AI with memory /yes or /no - YES.
    Return an audio response with a text response /yes or /no - YES.
    Summarize the story /yes or /no - YES.
    Notifications /yes or /no - Yes.
    You can fine-tune each position or just leave it as default.

    <b>📝 Text CHAT:</b>

    OpenAI:
    /4_o_mini - bot about info
    /4_turbo - bot about info

    Gemini:
    /4_o_mini - bot about info
    /4_turbo - bot about info

    <b>🌇 Creating an IMAGE:</b>

    Dall-e settings:
    /set_dall_3 - set Dall-e 3
    /set_dall_2 - set Dall-e 2
    /setabouttext - change bot about info
    /setuserpic - change bot profile photo
    /setcommands - change the list of commands
    /deletebot - delete a bot

    Midjourney:
    /my_vote_for_mid - vote for the implementation, already 45 ❤️

    <b>🗣 Voice calls to AI:</b>

    OpenAI:
    /setcommands - change the list of commands
    /deletebot - delete a bot

    <b>🎧 Audio from AI:</b>

    OpenAI:
    /setcommands - change the list of commands
    /deletebot - delete a bot

    <b>💳 Balance and payment:</b>
    /deletebot - delete a bot
    /deletebot - delete a bot

    <b>🗞 Reports and statistics:</b>
    /deletebot - delete a bot
    /deletebot - delete a bot

    '''


    if data.get("language") == "ru":
        await message.answer(f"{menu_ru}", parse_mode="HTML")
    elif data.get("language") == "en":
        await message.answer(f"{menu_en}", parse_mode="HTML")

    # menu_message_id = menu_message.message_id
    # menu_chat_id = message.chat.id

    # link_to_menu_message = f"https://t.me/c/{menu_chat_id}/{menu_message_id}"

    # print(link_to_menu_message)


@dp.message(Command('help'))
async def start(message: types.Message):

    help = '''
    help
    '''

    await message.reply(f"{help}", parse_mode="Markdown")




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
    if data_from_db.get("voice_answer"):
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
    if data_from_db.get("dialog"):
        dialog = data_from_db.get("dialog")

    # Get language:
    if data_from_db.get("language"):
        language = data_from_db.get("language")

    # Get dialog_sum:
    if data_from_db.get("dialog_sum"):
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





