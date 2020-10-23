# -*- coding: utf-8 -*-
# !/usr/bin/env python3

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


def get_keyboard_start():
    button1 = KeyboardButton('Расписание на текущую неделю')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button1)
    return keyboard
