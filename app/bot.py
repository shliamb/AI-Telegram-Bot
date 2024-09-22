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



#### GET CHAT to AI:
async def mod_tex(ai, data, message, voice_answer):

    await typing(message)

    if ai == "gemini":
        answer = await mod_gemini_chat(data)
    elif ai == "openai":
        answer = await mod_openai_chat(data)

    if not answer:
        return
    
    # Attempts to give a response to the user:
    await try_answer_bot(message, answer, voice_answer)


# Attempts to give a response to the user:
async def try_answer_bot(message, answer, voice_answer):
    await typing(message)

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
        logging.error(f"The file is empty or missing - {voice_answer_file_path}")


#### IMG + TEXT ####
class Form_text_img(StatesGroup):
    no_caption = State()

# PHOTO input:
async def mod_photo(ai, data, message, voice_answer, state: FSMContext):

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

    if data.get("user_content") is None:
        await message.reply("🇺🇸 *EN:* Ask a question in the caption of the picture.\n🇷🇺 *RU:* Задайте вопрос в подписи картинки.", parse_mode="Markdown")
        return

    if ai == "gemini":
        answer = await mod_gemini_chat(data)
    elif ai == "openai":
        answer = await mod_openai_chat(data)

    if not answer:
        return
    
    # Attempts to give a response to the user:
    await try_answer_bot(message, answer, voice_answer)


    # class Form_text_img(StatesGroup):
    # no_caption = State()



# DOCUMENTS input:
async def mod_documents(ai, data, message, voice_answer, state: FSMContext):

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

        if data.get("user_content") is None:
            await message.reply("🇺🇸 *EN:* Ask a question in the caption of the picture.\n🇷🇺 *RU:* Задайте вопрос в подписи картинки.", parse_mode="Markdown")
            return

    #### DOC ####
    elif extension.lower() == "doc":
        await message.reply("Серьезно...?", parse_mode="markdown")
        return

    else:
        await message.answer(f"The bot does not support this file yet, sorry - {name_file}", parse_mode="Markdown")
        logging.error(f"The bot does not support this file yet, sorry - {name_file}")
        return

    if ai == "gemini":
        answer = await mod_gemini_chat(data)
    elif ai == "openai":
        answer = await mod_openai_chat(data)

    if not answer:
        return
    
    # Attempts to give a response to the user:
    await try_answer_bot(message, answer, voice_answer)

# "docx", "odt", "rtf", "txt", "xls", "xlsx", "ods", "ppt", "pptx", "odp", "pdf", "html", "htm", "csv", "md", "xml", "json", "doc"





#### AUDIO input:

# Две кнопки, одна - перевод на анг, другая - транскрипция!!!
async def mod_text_to_audio(ai, data, message):

    audio = message.audio
    file_id = audio.file_id
    little = random_name_2X()
    audio_file_name = f"audio-{little}-{audio.file_id}.mp3"
    file = await bot.get_file(file_id)
    file_path = f'{AUDIO_FOLDER}{audio_file_name}'
    await bot.download_file(file.file_path, file_path)
    # await message.reply("Аудиофайл сохранен!")
    # if not answer:
    #     return
    
    # # Attempts to give a response to the user:
    # await try_answer_bot(message, answer, voice_answer)




#### VOICE input:
async def mod_voice_to_text(ai, data, message, voice_answer):

    voice = message.voice
    file_id = voice.file_id
    little = random_name_2X()
    voice_file_name = f"voice-{little}-{voice.file_id}.ogg"
    file = await bot.get_file(file_id)
    file_path = f'{VOICE_FOLDER}{voice_file_name}'
    await bot.download_file(file.file_path, file_path)

    if file_path:
        data["file_path"] = file_path
    if voice_file_name:
        data["name_file"] = voice_file_name

    # Convert Voice to Text
    convert_answer = await get_text_openai(data)
    if convert_answer is None:
        return

    data = {"user_content": convert_answer,}
    answer = await mod_tex(ai, data, message, voice_answer)

    if not answer:
        return
    
    # Attempts to give a response to the user:
    await try_answer_bot(message, answer, voice_answer)
 



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
    ai = data_state.get("ai")
    all_data = data_state.get("all_data")
    voice_answer = data_state.get("voice_answer")
    message = data_state.get("message")


    if callback_query.data == 'draw':
        await bot.send_message(callback_query.from_user.id, "🇺🇸 *EN:* The image is already being generated, expect it.\n🇷🇺 *RU:* Изображение уже генерируется, ожидайте.")

        # Generation image:
        if ai == "openai":
            answer = await mod_openai_dall_e(all_data)
        elif ai == "gemini":
            answer = await mod_openai_dall_e(all_data) # Sorry)))

        # Response to the user:
        await bot.send_message(callback_query.from_user.id, answer)


    elif callback_query.data == 'not_draw':

        # await bot.send_message(callback_query.from_user.id, "🇺🇸 *EN:* Waiting for the response to be generated.\n🇷🇺 *RU:* Ожидание генерации ответа.")
        sent_message = await bot.send_message(callback_query.from_user.id, "🇺🇸 *EN:* The response is already being generated, expect.\n🇷🇺 *RU:* Ответ уже генерируется, ожидайте.", parse_mode='Markdown')

        answer = await mod_tex(ai, all_data, message, voice_answer)

        if not answer:
            return
        
        # Response to the user:
        await try_answer_bot(message, answer, voice_answer)

        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=sent_message.message_id) # Должен удалять сообщение выше, но чет не пашет

    await bot.answer_callback_query(callback_query.id)
    await state.clear()






# Drawing Dall-e 3:
async def mod_gen_img(ai, data, message, voice_answer, state: FSMContext):

    await state.update_data(ai=ai, all_data=data, message=message, voice_answer=voice_answer)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🖼 Yes / Да", callback_data="draw")],
            [InlineKeyboardButton(text="❌ No / Нет", callback_data="not_draw")],
        ]
    )

    await bot.send_message(message.chat.id, "🇺🇸 *EN:* Generate an image?\n🇷🇺 *RU:* Сгенерировать изображение?", parse_mode="Markdown", reply_markup=keyboard) 

    await state.set_state(Form_draw.draw)





# Check request drawing:
async def check_request_drawing(question):
    typecontent = None

    draw_words = {  # добавить еще на каждое слово его слово-формы..
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

    # SYS
    file_path, question, received_object, photo_file_name, name_file, caption, system_content, model_voice = (None,) * 8
    caption, question, typecontent = message.caption, message.text, message.content_type
    ai, voice_answer = AI_DEFAULT, VOICE_THE_ANSWER
    await typing(message)
    id = user_id(message)
    
    # Getting a model depending on the selected AI:
    default_model_ai = {
        "openai": AI_DEFAULT_MODEL_OPENAI,
        "gemini": AI_DEFAULT_MODEL_GEMINI, # ...
    }

    model = default_model_ai[ai]


    # Getting the user's system data from the database:

    # Проверка в базе данных выбор пользователя - выбрана openai или Gemini или др., \
    # затем конкретно какая из версий, если нет этого то по умолчанию.
    # system_content = "отвечай по русски" или еще чего
    # voice_answer !
    # model_voice
    # ai
    # model

    #await state.update_data(ass="one") !!!!!!! delete

    # Checking the text for a drawing request:
    if typecontent == "text":
        drawing_request = await check_request_drawing(question)
        typecontent = drawing_request or typecontent

    # Data collection to API:
    data = {"ai": ai,}
    # All:
    data["model"] = model
    data["system_content"] = system_content
    data["user_content"] = caption or question
    data["voice_answer"] = voice_answer
    # Voice:
    data["model_voice"] = model_voice
    # data["response_format"] = response_format
    # data["language"] = language
    # data["prompt"] = prompt


    # Each type does its job
    input_content_type = {
        "text": mod_tex,
        "draw": mod_gen_img,
        "document": mod_documents,
        "photo": mod_photo,
        "audio": mod_text_to_audio,
        "voice": mod_voice_to_text,
    }

    if typecontent not in input_content_type:
        #await message.reply("Not support type file, sorry.")
        logging.error(f"Not support type file, sorry.")
        return

    arguments = {
        'ai': ai,
        'data': data,
        'message': message,
        'voice_answer': voice_answer
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















#     await state.update_data(data=data) # Прикрепление в state данных
#     await message.reply("🇺🇸 *EN:* Question about the attached image:\n🇷🇺 *RU:* Вопрос по прикрепленному изображению:", parse_mode="markdown")
#     await state.set_state(Form_img_text.first_stage) # Ожидание следующего шага



# # Set State
# class Form_img_text(StatesGroup):
#     first_stage = State()
#     #second_stage = State()



# # PHOTO + DOC + Text
# @dp.message(Form_img_text.first_stage, F.content_type.in_({'text'}))
# async def mod_photo_text(message: Message, state: FSMContext):
#     # Из прошлого State
#     data = await state.get_data()
#     ai = data.get('ai')
#     voice_answer = data.get('voice_answer')

#     if message.text:
#         data["user_content"] = message.text

#     if ai == "gemini":
#         answer = await mod_gemini_chat(data)
#     elif ai == "openai":
#         answer = await mod_openai_chat(data)
#     if answer:
#         # Attempts to give a response to the user:
#         await try_answer_bot(message, answer, voice_answer) 

#     await state.clear()





    # # if PHOTO and some DOCUMENTS like a image:
    # if received_object == "document" or received_object == "photo":

    #     if file_path:
    #         data["file_path"] = file_path
    #     if name_file:
    #         data["name_file"] = name_file
    #     elif photo_file_name:
    #         data["name_file"] = photo_file_name
    #     if voice_answer:
    #         data["voice_answer"] = voice_answer
    #     if caption:
    #         data["user_content"] = caption
    #         answer = await mod_photo_caption(ai, data)
    #         if answer is None:
    #             return
    #         # Attempts to give a response to the user:
    #         await try_answer_bot(message, answer, voice_answer) 
    #         return
        
    #     await state.update_data(data=data) # Прикрепление в state данных
    #     await message.reply("🇺🇸 *EN:* Question about the attached image:\n🇷🇺 *RU:* Вопрос по прикрепленному изображению:", parse_mode="markdown")
    #     await state.set_state(Form_img_text.first_stage) # Ожидание следующего шага



    # # if only TEXT:
    # elif received_object == "text":

    #     if question:
    #         data["user_content"] = question

    #     answer = await mod_tex(ai, data)

    #     if answer is None:
    #         return
        
    #     # Attempts to give a response to the user:
    #     await try_answer_bot(message, answer, voice_answer) 

    #await state.clear()



      # #### PHOTO:
    # elif message.content_type == 'photo': # Telegram always saves in jpg in compress
    #     received_object = "photo"
    #     photo = message.photo[-1]  # Используем самый большой размер фотографии
    #     file_id = photo.file_id
    #     file = await bot.get_file(file_id)
    #     little = random_name_2X()
    #     photo_file_name = f"photo-{little}-{message.photo[-1].file_id}.jpg"
    #     file_path = f'{DOWNLOADS_FOLDER}{photo_file_name}'
    #     await bot.download_file(file.file_path, file_path)
    #     # await message.reply("Фотография сохранена!")



    # # Set State
# class Form_img_text(StatesGroup):
#     first_stage = State()
#     #second_stage = State()



# # PHOTO + DOC + Text
# @dp.message(Form_img_text.first_stage, F.content_type.in_({'text'}))
# async def mod_photo_text(message: Message, state: FSMContext):
#     # Из прошлого State
#     data = await state.get_data()
#     ai = data.get('ai')
#     voice_answer = data.get('voice_answer')

#     if message.text:
#         data["user_content"] = message.text

#     if ai == "gemini":
#         answer = await mod_gemini_chat(data)
#     elif ai == "openai":
#         answer = await mod_openai_chat(data)
#     if answer:
#         # Attempts to give a response to the user:
#         await try_answer_bot(message, answer, voice_answer) 

#     await state.clear()



    # #### DOCUMENTS:
    # if message.content_type == 'document': # Любые форматы, а потому внутри нужна логика проверки
    #     received_object = "document"
    #     file_id = message.document.file_id
    #     little = random_name_2X()
    #     name_file = little + "-" + message.document.file_name

    #     # Get extension:
    #     match = re.search(r'\.([^.]+)$', name_file)

    #     if match:
    #         extension = match.group(1)  # Получаем расширение без точки
    #     else:
    #         logging.error(f"Dont support file - {name_file}")
    #         return
        
    #     # Installation is not supported temporarily:
    #     set_extension = {"doc", "docx", "odt", "rtf", "txt", "xls", "xlsx", "ods", "ppt", "pptx", "odp", "pdf", "html", "htm", "csv", "md", "xml", "json"}

    #     if extension in set_extension:
    #         await message.answer(f"The bot does not support this file - {name_file}", parse_mode="markdown")
    #         logging.error(f"Dont support file - {name_file}")
    #         return

    #     file_path = f'{DOWNLOADS_FOLDER}{name_file}'
    #     file = await bot.get_file(file_id)
    #     await bot.download_file(file.file_path, file_path)
    #     # await message.reply("Документ сохранен!")





      # kb = [
    #     [
    #         types.KeyboardButton(text="Да"),
    #         types.KeyboardButton(text="Нет")
    #     ],
    # ]
    # keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    
    # await message.reply("🇺🇸 *EN:* Generate an image?\n🇷🇺 *RU:* Сгенерировать изображение?", reply_markup=keyboard)




    # keyboard = ReplyKeyboardMarkup(
    #     inline_keyboard=[
    #         [KeyboardButton(text="🖼 Yes / Да")], 
    #         [KeyboardButton(text="❌ No / Нет")], 
    #     ]
    # )

    # await bot.send_message(message.chat.id, "🇺🇸 *EN:* Generate an image?\n🇷🇺 *RU:* Сгенерировать изображение?", parse_mode="MarkdownV2", reply_markup=keyboard)




    #keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    # markup = ReplyKeyboardMarkup(
    #     keyboard=[
    #         ['Кнопка 1', 'Кнопка 2'],
    #         ['Кнопка 3']
    #     ],
    #     resize_keyboard=True
    # )


    # button = KeyboardButton("Присвоить значение")
    # markup.add(button)

    # Пример правильного использования
    # markup = ReplyKeyboardMarkup(
    #     keyboard=[
    #         [KeyboardButton(text='Кнопка 1'), KeyboardButton(text='Кнопка 2')],
    #         [KeyboardButton(text='Кнопка 3')]
    #     ],
    #     resize_keyboard=True
    # )

    # button = KeyboardButton("Присвоить значение")
    # markup.add(button)



# Ждем ответа от пользователя в рамках этой же функции
# @dp.message(lambda m: m.text in ["Да", "Нет"])
# async def process_choice(message: types.Message):
#     user_choice = message.text  # Присваиваем значение переменной
#     await message.answer(f"Вы выбрали: {user_choice}")
#     # Удаляем клавиатуру
#     await message.reply("Клавиатура удалена.", reply_markup=types.ReplyKeyboardRemove())