# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from app import dp, bot, storage

from aiogram.dispatcher.storage import FSMContext

from utils import get_week_info, get_pair, main, rate_limit
from messages import MESSAGES
from keyboards import get_keyboard_start


@dp.message_handler(commands='start')
async def start_command(message: types.Message):
    first_name = message.chat.first_name
    full_name = message.from_user.full_name
    await message.reply(f'Привет, студент!')
    await message.answer(MESSAGES['start'], reply_markup=get_keyboard_start())


@dp.message_handler(commands='help')
async def help_command(message: types.Message):
    await message.answer(MESSAGES['help'])


@rate_limit(limit=1800)
@dp.message_handler(commands='schedule')
@dp.message_handler(lambda message: message.text=="Расписание на текущую неделю")
async def get_schedule(message: types.Message):
    main()
    with open('result.txt', 'r', encoding='utf8') as file:
        schedule = file.read()
        await message.answer(schedule)


@dp.message_handler()
async def echo_message(message: types.Message):
    await message.reply('Сам ' + message.text)

