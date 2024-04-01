import asyncio

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
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.base import STATE_RUNNING, STATE_STOPPED

from keyboards.commands_menu import set_commands_menu
from keyboards.bottom_url_keyboard import get_cian_url_keyboard, get_bottom_keyboard
from keyboards.main_menu import get_main_menu, get_profile_menu

from database.orm import (add_user, get_prefs, get_prefs_text, set_prefs, get_autocheck_status,
                          switch_autocheck)

from services.parsing import parse
from services.tools import (check_city, check_date_gte, check_date_lt, check_int_answer,
                            check_is_hotel_answer, get_city_id)

env: Env = Env()
env.read_env()
token = env('token')

router = Router()
bot = Bot(token=token, parse_mode='HTML')
scheduler = AsyncIOScheduler()
# scheduler.start()


REQUEST_INTERVAL = 60

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


async def start_polling(message: Message, tg_id):
    scheduler.add_job(
            func=process_check_offers_silent,
            trigger='interval',
            seconds=REQUEST_INTERVAL,
            args=(message, tg_id, ),
            id=f'process_check_offers_silent_{tg_id}'
        )
    if not scheduler.running:
        scheduler.start()


async def stop_polling(message: Message, tg_id):
    scheduler.remove_job(f'process_check_offers_silent_{tg_id}')
    if not scheduler.running:
        scheduler.start()



@router.message(Command(commands='showjobs'))
async def process_show_jobs_command(message: Message):
    jobs = scheduler.get_jobs()
    print(jobs)


@router.message(Command(commands='startjobs'))
async def process_start_jobs_command(message: Message):
    if not scheduler.running:
        scheduler.start()


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
    await add_user(tg_id)
    # await start_polling(message, tg_id)
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
    autocheck_status = get_autocheck_status(tg_id)
    prefs_text = get_prefs_text(tg_id)
    await message.answer(
        text=prefs_text,
        reply_markup=get_bottom_keyboard(autocheck=autocheck_status))


@router.callback_query(Text(text='change_autocheck'), StateFilter(default_state))
async def process_fillform_command(callback: CallbackQuery, state: FSMContext):
    tg_id = callback.from_user.id
    switch_autocheck(tg_id)
    autocheck_status = get_autocheck_status(tg_id)
    if autocheck_status:
        text = 'Автопроверка ВКЛЮЧЕНА'
        await start_polling(callback.message, tg_id)
    else:
        text = 'Автопроверка ВЫКЛЮЧЕНА'
        await stop_polling(callback.message, tg_id)
    await callback.answer(text=text)
    await callback.message.edit_reply_markup(
        reply_markup=get_bottom_keyboard(autocheck=autocheck_status))
    await callback.answer()


async def process_check_offers_silent(message: Message, tg_id):
    # tg_id = message.from_user.id
    prefs = get_prefs(tg_id)
    offers = parse(tg_id, prefs)
    if offers:
        for offer in offers:
            text = format_offer_message(offer)
            await message.answer(
                text=text,
                parse_mode='HTML',
                reply_markup=get_cian_url_keyboard(offer['url']))


@router.message(Text(text='Проверить сейчас'))
async def process_check_offers(message: Message):
    tg_id = message.from_user.id
    prefs = get_prefs(tg_id)
    offers = parse(tg_id, prefs)
    if offers:
        for offer in offers:
            print(f'Sending TG message to user {tg_id}')
            text = format_offer_message(offer)
            await message.answer(
                text=text,
                parse_mode='HTML',
                reply_markup=get_cian_url_keyboard(offer['url']))
    else:
        await message.answer(text='Новых предложений пока нет')


@router.callback_query(Text(text='change_prefs'), StateFilter(default_state))
async def process_fillform_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Пожалуйста, введите город.\n'
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
        await message.answer(text='Спасибо!\n\nТеперь введите максимальную цену.')
        await state.set_state(FSMAddCategory.add_min_price)
    else:
        await message.answer(text='Вы ввели не число, попробуйте еще раз.\n'
                             'Если хотите прервать изменение настроек, введите команду /cancel')


@router.message(StateFilter(FSMAddCategory.add_min_price))
async def process_min_price_sent(message: Message, state: FSMContext):
    if check_int_answer(message.text):
        await state.update_data(min_price=message.text)
        await message.answer(text='Спасибо!\n\nТеперь введите дату заезда в формате ДД.ММ.ГГГГ, '
                                'например 01.09.2024')
        await state.set_state(FSMAddCategory.add_date_gte)
    else:
        await message.answer(text='Вы ввели не число, попробуйте еще раз.\n'
                             'Если хотите прервать изменение настроек, введите команду /cancel')


@router.message(StateFilter(FSMAddCategory.add_date_gte))
async def process_date_gte_sent(message: Message, state: FSMContext):
    if check_date_gte(message.text):
        await state.update_data(date_gte=message.text)
        await message.answer(text='Спасибо!\n\nТеперь введите количество дней проживания или '
                                'дату выезда в формате ДД.ММ.ГГГГ, '
                                'например 01.09.2024')
        await state.set_state(FSMAddCategory.add_date_lt)
    else:
        await message.answer(text='Вы ввели дату в неправильном формате, несуществующую дату '
                                    'или дату раньше завтрашнего дня, попробуйте еще раз.\n'
                                    'Если хотите прервать изменение настроек, введите команду /cancel')


@router.message(StateFilter(FSMAddCategory.add_date_lt))
async def process_date_lt_sent(message: Message, state: FSMContext):
    user_data = await state.get_data()
    date_gte = user_data['date_gte']
    date_lt = check_date_lt(message.text, date_gte)
    if date_lt:
        await state.update_data(date_lt=date_lt)
        await message.answer(text='Спасибо!\n\nТеперь укажите, искать ли отели или только квартиры? '
                                    '(0 - Только квартиры, 1 - Квартиры и отели)')
        await state.set_state(FSMAddCategory.add_is_hotel)
    else:
        await message.answer(text='Вы ввели дату в неправильном формате, несуществующую дату '
                                    'или дату раньше следующего дня с даты заезда, попробуйте еще раз.\n'
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
        await state.clear()
        await message.answer(text='Спасибо!\n\nНастройки добавлены',
                             reply_markup=get_main_menu())
    else:
        await message.answer(text='Вы неправильно указали признак поиска только отелей.\n'
                             'Если хотите прервать изменение настроек, введите команду /cancel')


