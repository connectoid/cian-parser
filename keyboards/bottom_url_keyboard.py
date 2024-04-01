from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Создаем объекты инлайн-кнопок

def get_cian_url_keyboard(url):

    url_button_1 = InlineKeyboardButton(
        text='Перейти на Циан',
        url=url
    )
    url_button_2 = InlineKeyboardButton(
        text='Документация Telegram Bot API',
        url='https://core.telegram.org/bots/api'
    )

    # Создаем объект инлайн-клавиатуры
    cian_url_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[url_button_1]]
    )
    return cian_url_keyboard


def get_bottom_keyboard(autocheck):

    button_1 = InlineKeyboardButton(
        text='Изменить настройки',
        callback_data='change_prefs'
    )
    if autocheck:
        button_2 = InlineKeyboardButton(
            text=f'Выключить автопроверку',
            callback_data='change_autocheck'
        )
    else:
        button_2 = InlineKeyboardButton(
            text=f'Включить автопроверку',
            callback_data='change_autocheck'
        )


    # Создаем объект инлайн-клавиатуры
    bottom_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_1],
                         [button_2]]
    )
    return bottom_keyboard