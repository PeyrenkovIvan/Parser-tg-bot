import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import aiofiles

logging.basicConfig(filename='bot.txt', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

TOKEN = '8154800660:AAFcBE5Qvk4dr71ZUPA68tlSX4QcMMlHJ7M'
FILE_PATH = 'parsed_data.txt'
MAX_MESSAGE_LENGTH = 4096

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Bot started and will send data from the file every 60 seconds.")
    logging.info(f"Command /start received from user {message.from_user.id}")

    while True:
        try:
            async with aiofiles.open(FILE_PATH, mode='r', encoding='utf-8') as file:
                content = await file.read()
                logging.info("Data successfully read from file.")
            
            if content:
                for chunk in [content[i:i + MAX_MESSAGE_LENGTH] for i in range(0, len(content), MAX_MESSAGE_LENGTH)]:
                    await message.answer(chunk)
                logging.info(f"Data sent to user {message.from_user.id}")
            else:
                await message.answer("The file is empty.")
                logging.info(f"The file is empty. Message sent to user {message.from_user.id}")
        except FileNotFoundError:
            await message.answer(f"File '{FILE_PATH}' not found.")
            logging.error(f"File '{FILE_PATH}' not found.")
            break
        except Exception as e:
            logging.error(f"Error sending data to user {message.from_user.id}: {e}")
        await asyncio.sleep(60*10)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("Bot launched and polling started.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
