from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)


def get_main_menu():
    button_1: KeyboardButton = KeyboardButton(text='Настройки поиска')
    button_2: KeyboardButton = KeyboardButton(text='Проверить сейчас')

    main_menu_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                        keyboard=[[button_1, button_2]],
                                        resize_keyboard=True)
    return main_menu_keyboard


def get_profile_menu():
    button_1: KeyboardButton = KeyboardButton(text='Изменить настройки')
    button_2: KeyboardButton = KeyboardButton(text='Назад')

    profile__menu_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                        keyboard=[[button_1, button_2]],
                                        resize_keyboard=True)
    return profile__menu_keyboard