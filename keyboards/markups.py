from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


def start_keyboard():
    markup = ReplyKeyboardMarkup(row_width=2)

    genBtn = KeyboardButton(text='Создать новый документ')

    markup.insert(genBtn)

    return markup


def photo_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)

    successBtn = InlineKeyboardButton(text='Подтвердить', callback_data='success')
    reloadBtn = InlineKeyboardButton(text='Обновить', callback_data='reload')

    markup.insert(successBtn).insert(reloadBtn)

    return markup
