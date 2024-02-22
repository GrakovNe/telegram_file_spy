import asyncio
import os
import logging
from telegram import Bot
from telegram.ext import Application

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Ваши настройки
bot_token = '6996614206:AAFaVIYUYP5cUsd3nLeFmVJg4pnQDF2nFcY'
chat_id = '93179449'
directory_to_watch = '/Users/grakovne/Desktop/file_spy/'
scan_interval = 10  # Интервал сканирования в секундах

def get_files(directory):
    """Возвращает список путей ко всем файлам в директории и поддиректориях."""
    files_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            files_list.append(os.path.join(root, file))
    return set(files_list)

async def scan_and_notify(bot):
    previous_scan = get_files(directory_to_watch)

    while True:
        current_scan = get_files(directory_to_watch)
        new_files = current_scan - previous_scan
        if new_files:
            for file_path in new_files:
                logging.info(f"Отправка файла: {file_path}")
                try:
                    with open(file_path, 'rb') as file:
                        await bot.send_document(chat_id=chat_id, document=file)
                except Exception as e:
                    logging.error(f"Ошибка отправки файла: {e}")
        else:
            logging.info("Новых файлов нет")
        previous_scan = current_scan
        await asyncio.sleep(scan_interval)

async def main():
    bot = Bot(token=bot_token)
    await scan_and_notify(bot)

if __name__ == "__main__":
    asyncio.run(main())
