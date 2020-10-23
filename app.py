# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# ATPb-20-1   @ATPb20bot    schedule
# бот сообщает расписание для группы АТПб-20-1 Иркутского политеха(ИСТУ)

import os
import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor


from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


if __name__ == '__main__':
    from handlers import dp
    import middlewares
    middlewares.setup(dp)
    executor.start_polling(dp, skip_updates=True)
