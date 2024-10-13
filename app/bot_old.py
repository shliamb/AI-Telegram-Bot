from get_keys import TELEGRAM_BOT_TOKEN_OLD
import asyncio
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Aiogram
from aiogram import Bot, Dispatcher, types, F


bot = Bot(TELEGRAM_BOT_TOKEN_OLD, parse_mode="markdown") 
dp = Dispatcher()

# Show Typing bot
async def typing(action) -> None:
    await bot.send_chat_action(action.chat.id, action='typing')

#### MAIN HENDLER INCOMING
@dp.message(F.content_type.in_({'text'}))
async def second_function(message: types.Message):
    await typing(message)
    await bot.send_message(message.chat.id, "<b>EN:</b> The bot has been updated and is now here - @sliamb_ai_bot \n\n<b>RU:</b> Бот обновился и теперь находится тут - @sliamb_ai_bot ", parse_mode="HTML")
    return


# main def polling
async def main_bot() -> None:
    await dp.start_polling(bot, skip_updates=False)


# Start polling
if __name__ == "__main__":
    try:
        asyncio.run(main_bot())
    except Exception as e:
        logging.error(f"An error occurred: {e}.")
        print(f"An error occurred: {e}.")