#!/usr/bin/env python
# coding: utf-8

# ### Парсер информации из телеграмм группы.


from telethon import TelegramClient, events
from telethon.tl.types import InputMessagesFilterDocument, InputMessagesFilterPhotos, InputMessagesFilterVideo, InputMessagesFilterGif, InputMessagesFilterPhotoVideo
from datetime import datetime, timedelta
import os
import sys

import asyncio
import nest_asyncio


# #### Константы


# Данные телеграмм аккаунта
API_ID = '11111111111'
API_HASH = '7777777777777777777777777777'
PHONE_NUMBER = '79221234567'

GROUP_ID = "-10000000000000"

# END_DATE = datetime(2023, 11, 8)  # Укажите дату, ДО которой загружать файлы
END_DATE = datetime.now()  # До сегодняшней даты
START_DATE = END_DATE - timedelta(days=7) # None, если скачивать все до указанной даты
FILES_LIMIT = 10 # None - для скачивания всей истории. Лимит одинаков для всех видов файлов. 
MIN_MESSAGE_LEN = 50  # Минимальная длина сообщения, при которой осуществляется загрузка сообщения

DEL_SESSION = False

EXPORT_PATH = "/media/user/Disk_F/tmp_data/04_parcer"


# Запуск клиента
client = TelegramClient('session_name', API_ID, API_HASH)


# #### Функции
# > https://docs-python.ru/packages/telegram-klient-telethon-python/metody-obekta-telegramclient/#TelegramClient.get_messages <br>
# https://docs.telethon.dev/en/stable/modules/client.html <br>
# https://tl.telethon.dev/types/messages_filter.html


# Функция сохранения текста в файл
def write_txt(input_file, text):
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(text)

# Функция добавления даты к имени файла
def name_with_date(full_old_name:str, message_date:datetime):
    fname, ext = os.path.splitext(os.path.basename(full_old_name))
    file_date = message_date.strftime('%Y-%m-%d')
    new_file_name = f"{file_date}_{fname}{ext}"
    full_new_file_name = os.path.join(EXPORT_PATH, new_file_name)
    return full_new_file_name
    

#  Функция для загрузки файлов:
async def download_files(chat_id, start_date, end_date):    
    # Создание директории для сохранения файлов
    if not os.path.exists(EXPORT_PATH):
        os.makedirs(EXPORT_PATH)

    # Подключение к Telegram
    await client.start(PHONE_NUMBER)

    # Получение указанных типов документов из сообщений с указанного момента времени 
    # InputMessagesFilterDocument, InputMessagesFilterPhotos, InputMessagesFilterVideo, InputMessagesFilterGif, InputMessagesFilterPhotoVideo    
    filters = [InputMessagesFilterDocument, InputMessagesFilterPhotos, InputMessagesFilterVideo, InputMessagesFilterGif]   
    for filter in filters:
        messages = await client.get_messages(chat_id, limit=FILES_LIMIT, offset_date=end_date, filter=filter)
        # Вывод шапки:
        if filter == InputMessagesFilterDocument:
            print("Документы:")
        elif filter == InputMessagesFilterPhotos:
            print("Фото:")
        elif filter == InputMessagesFilterVideo:
            print("Видео:")
        elif filter == InputMessagesFilterGif:
            print("GIF:") 
        
        # Загрузка медиа файлов
        for message in messages:
            if message.media:
                if start_date is None:
                    file_path = await client.download_media(message.media, EXPORT_PATH)
                    new_file_name = name_with_date(file_path, message.date)
                    print(f'Загружено: {new_file_name}')
                else:
                    if datetime.astimezone(message.date) >= datetime.astimezone(start_date):                                        
                        file_path = await client.download_media(message.media, EXPORT_PATH)
                        new_file_name = name_with_date(file_path, message.date)
                        print(f'Загружено: {new_file_name}')
            

    # Получаем текстовые сообщения
    print("Текстовые сообщения:")
    messages = await client.get_messages(chat_id, limit=FILES_LIMIT, offset_date=end_date)
    # Загрузка файлов
    for message in messages:
        if message.text:
            texts = message.text
            if len(texts) > MIN_MESSAGE_LEN:
                if start_date is None:      
                    new_file_name = name_with_date(f"{message.id}.txt", message.date)
                    write_txt(new_file_name, texts)
                    print(f'Загружено: {new_file_name}')
                    
                else:
                    if datetime.astimezone(message.date) >= datetime.astimezone(start_date):                                        
                        new_file_name = name_with_date(f"{message.id}.txt", message.date)
                        write_txt(new_file_name, texts)
                        print(f'Загружено: {new_file_name}')

    # Отключение клиента
    await client.disconnect()


# #### Main

nest_asyncio.apply()

# Запуск функции
asyncio.run(download_files(int(GROUP_ID), START_DATE, END_DATE))

print("[+] Готово!")

