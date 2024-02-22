import asyncio
import os
import logging
from telegram import Bot
import configparser

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Чтение конфигурации
config = configparser.ConfigParser()
config.read('config.properties')
bot_token = config.get('DEFAULT', 'bot_token')
chat_ids = config.get('DEFAULT', 'chat_ids').split(',')
directory_to_watch = config.get('DEFAULT', 'directory_to_watch')
scan_interval = config.getint('DEFAULT', 'scan_interval')
file_extensions = tuple(config.get('DEFAULT', 'file_extensions').split(','))

def get_files(directory, extensions):
    """Returns a set of file paths in the directory and subdirectories filtered by extensions."""
    files_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extensions):
                files_list.append(os.path.join(root, file))
    return set(files_list)

async def scan_and_notify(bot):
    previous_scan = get_files(directory_to_watch, file_extensions)

    while True:
        current_scan = get_files(directory_to_watch, file_extensions)
        new_files = current_scan - previous_scan
        if new_files:
            for file_path in new_files:
                logging.info(f"Sending file: {file_path}")
                for chat_id in chat_ids:
                    try:
                        with open(file_path, 'rb') as file:
                            await bot.send_document(chat_id=chat_id, document=file)
                    except Exception as e:
                        logging.error(f"Error sending file: {e}")
        else:
            logging.info("No new files")
        previous_scan = current_scan
        await asyncio.sleep(scan_interval)

async def main():
    bot = Bot(token=bot_token)
    await scan_and_notify(bot)

if __name__ == "__main__":
    asyncio.run(main())
