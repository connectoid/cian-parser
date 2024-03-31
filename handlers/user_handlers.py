from aiogram import Bot, Dispatcher, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart, Text, StateFilter
from aiogram.types import (CallbackQuery, Message, ReplyKeyboardRemove, 
                           LabeledPrice, PreCheckoutQuery, ContentType)
from aiogram.types.message import ContentType
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.filters.state import State, StatesGroup

from environs import Env

from keyboards.commands_menu import set_commands_menu
from keyboards.bottom_url_keyboard import get_cian_url_keyboard, get_bottom_keyboard
from keyboards.main_menu import get_main_menu, get_profile_menu

from database.orm import add_user, get_prefs, set_prefs

from services.parsing import parse
from services.tools import (check_city, check_date_gte, check_date_lt, check_int_answer,
                            check_is_hotel_answer, get_city_id)

env: Env = Env()
env.read_env()
token = env('token')

router = Router()
bot = Bot(token=token, parse_mode='HTML')

class FSMAddCategory(StatesGroup):
    add_city = State()
    add_rooms_count = State()
    add_beds_count = State()
    add_min_price = State()
    add_date_gte = State()
    add_date_lt = State()
    add_is_hotel = State()


def format_offer_message(offer):
    text = (
                f"{offer['title']}\n"
                f"<b>Цена:</b> {offer['price']} руб.\n"
                f"<b>Адрес:</b> <i>{offer['address']}</i>\n"
                f"<b>Телефон:</b> <i>+7{offer['phone']}</i>\n"
                f"<i>{offer['description']}</i>\n"
                f"<b>ID объявления:</b> {offer['offer_id']}\n"
                f"<b>Фото:</b> {offer['photo_mini']}\n"
            )
    return text


@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Вы вышли из режима изменения нстроек\n\n')
    await state.clear()


@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text='Отменять нечего. Вы вне диалога изменение настроек\n\n')


@router.message(CommandStart())
async def process_start_command(message: Message):
    fname = message.from_user.first_name
    lname = message.from_user.last_name
    tg_id = message.from_user.id
    add_user(tg_id)
    await message.answer(
    text=f'Здравствуйте {fname} {lname}! Вы запустили бот для парсинга недвижимости на сайте cian.ru',
    reply_markup=get_main_menu())


@router.message(Text(text='Назад'))
async def process_start_command(message: Message):
    await message.answer(
        text=f' ',
        reply_markup=get_main_menu())


@router.message(Text(text='❔ Помощь'))
async def process_start_command(message: Message):
    await message.answer(
        text=f'Здесь будет текст справочной информации по работе с ботом.',
        reply_markup=get_main_menu())


@router.message(Text(text='Настройки поиска'))
async def process_profile_prefs(message: Message):
    tg_id = message.from_user.id
    prefs, prefs_text = get_prefs(tg_id)
    print(prefs_text)
    await message.answer(
        text=prefs_text,
        reply_markup=get_bottom_keyboard())



@router.message(Text(text='Проверить сейчас'))
async def process_check_offers(message: Message):
    tg_id = message.from_user.id
    prefs, prefs_text = get_prefs(tg_id)
    offers = parse(tg_id, prefs)
    if offers:
        for offer in offers:
            print('Sending TG message')
            text = format_offer_message(offer)
            await message.answer(
                text=text,
                parse_mode='HTML',
                reply_markup=get_cian_url_keyboard(offer['url']))
    else:
        await message.answer(text='Новых предложений пока нет')


@router.callback_query(Text(text='change_prefs'), StateFilter(default_state))
async def process_fillform_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Пожалуйста, введите город транслитом (например kostroma).\n'
                         'Если хотите прервать изменение настроек, введите команду /cancel')
    await state.set_state(FSMAddCategory.add_city)


@router.message(StateFilter(FSMAddCategory.add_city))
async def process_city_sent(message: Message, state: FSMContext):
    if check_city(message.text):
        await state.update_data(city=message.text)
        await message.answer(text='Спасибо!\n\nТеперь введите количество комнат.')
        await state.set_state(FSMAddCategory.add_rooms_count)
    else:
        await message.answer(text='Город не найден. Проверьте правильность написания города и введите еще раз\n'
                             'Если хотите прервать изменение настроек, введите команду /cancel')


@router.message(StateFilter(FSMAddCategory.add_rooms_count))
async def process_rooms_count_sent(message: Message, state: FSMContext):
    if check_int_answer(message.text):
        await state.update_data(rooms_count=message.text)
        await message.answer(text='Спасибо!\n\nТеперь введите количество гостей.')
        await state.set_state(FSMAddCategory.add_beds_count)
    else:
        await message.answer(text='Вы ввели не число, попробуйте еще раз.\n'
                             'Если хотите прервать изменение настроек, введите команду /cancel')
        

@router.message(StateFilter(FSMAddCategory.add_beds_count))
async def process_beds_count_sent(message: Message, state: FSMContext):
    if check_int_answer(message.text):
        await state.update_data(beds_count=message.text)
        await message.answer(text='Спасибо!\n\nТеперь введите минимальную цену.')
        await state.set_state(FSMAddCategory.add_min_price)
    else:
        await message.answer(text='Вы ввели не число, попробуйте еще раз.\n'
                             'Если хотите прервать изменение настроек, введите команду /cancel')


@router.message(StateFilter(FSMAddCategory.add_min_price))
async def process_min_price_sent(message: Message, state: FSMContext):
    if check_int_answer(message.text):
        await state.update_data(min_price=message.text)
        await message.answer(text='Спасибо!\n\nТеперь введите дату заезда в формате 01.01.2024')
        await state.set_state(FSMAddCategory.add_date_gte)
    else:
        await message.answer(text='Вы ввели не число, попробуйте еще раз.\n'
                             'Если хотите прервать изменение настроек, введите команду /cancel')


@router.message(StateFilter(FSMAddCategory.add_date_gte))
async def process_date_gte_sent(message: Message, state: FSMContext):
    if check_date_gte(message.text):
        await state.update_data(date_gte=message.text)
        await message.answer(text='Спасибо!\n\nТеперь введите дату выезда в формате 01.01.2024')
        await state.set_state(FSMAddCategory.add_date_lt)
    else:
        await message.answer(text='Вы неправильно ввели дату, попробуйте еще раз.\n'
                             'Если хотите прервать изменение настроек, введите команду /cancel')


@router.message(StateFilter(FSMAddCategory.add_date_lt))
async def process_date_lt_sent(message: Message, state: FSMContext):
    if check_date_lt(message.text):
        await state.update_data(date_lt=message.text)
        await message.answer(text='Спасибо!\n\nТеперь укажите, искать ли только отели? (0 - Нет, 1 - Да)')
        await state.set_state(FSMAddCategory.add_is_hotel)
    else:
        await message.answer(text='Вы неправильно ввели дату, попробуйте еще раз.\n'
                             'Если хотите прервать изменение настроек, введите команду /cancel')


@router.message(StateFilter(FSMAddCategory.add_is_hotel))
async def process_is_hotels_sent(message: Message, state: FSMContext):
    if check_is_hotel_answer(message.text):
        if int(message.text) == 1:
            await state.update_data(is_hotel=True)
        else:
            await state.update_data(is_hotel=False)
        user_data = await state.get_data()
        tg_id = message.from_user.id
        set_prefs(tg_id, user_data)
        print(user_data)
        await state.clear()
        await message.answer(text='Спасибо!\n\nНастройки добавлены',
                             reply_markup=get_main_menu())
    else:
        await message.answer(text='Вы неправильно указали признак поиска только отелей.\n'
                             'Если хотите прервать изменение настроек, введите команду /cancel')


