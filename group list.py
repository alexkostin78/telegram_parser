#!/usr/bin/env python
# coding: utf-8

# ### Список доступных групп

from telethon import TelegramClient
import asyncio
import nest_asyncio


# #### Константы


# Укажите свои данные
API_ID = '1111111111'
API_HASH = '77777777777777777777'
PHONE_NUMBER = '79221234567'


client = TelegramClient('session_name', API_ID, API_HASH)


# #### Функции


# Функция получения списка доступных групп:

async def get_available_groups():
    # Подключение к Telegram
    await client.start(PHONE_NUMBER)

    # Получение списка диалогов
    dialogs = await client.get_dialogs()

    # Фильтрация групп (и каналов)    
    groups = [(dialog.name, dialog.id) for dialog in dialogs if dialog.is_group or dialog.is_channel]

    # Отключение клиента
    await client.disconnect()

    return groups


# #### Main


# Запуск функции
nest_asyncio.apply()

groups = asyncio.run(get_available_groups())
print("Доступные группы:")  #  и каналы
for name, group_id in groups:
    print(f"Имя: {name}, ID: {group_id}")

