from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from environs import Env

from .models import Base, User, Flat

env: Env = Env()
env.read_env()

db_name = env('db_name')
db_host = env('db_host')
db_user = env('db_user')
db_password = env('db_password')

database_url = f'postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}'

engine = create_engine(database_url, echo=False, pool_size=20, max_overflow=0)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def add_new_user(tg_id):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    if user is None:
        new_user = User(
            tg_id=tg_id,
            autocheck_enable=False,
            city='Moskva',
            rooms_count=1,
            beds_count=1,
            min_price=3000,
            date_gte='01.06.2024',
            date_lt='08.06.2024',
            is_hotel=False,
        )
        session.add(new_user)
        session.commit()
        return True
    return False


def switch_autocheck(tg_id):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    user.autocheck_enable = not user.autocheck_enable
    session.add(user)
    session.commit()


def get_autocheck_status(tg_id):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    return user.autocheck_enable


def add_flat(tg_id, offer):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    flat = session.query(Flat).filter(Flat.owner == user.id, Flat.offer_id == offer['offer_id']).first()
    if flat is None:
        new_flat = Flat(
            offer_id = offer['offer_id'],
            url = offer['url'],
            added_datetime = offer['added_datetime'],
            address = offer['address'],
            phone = offer['phone'],
            price = offer['price'],
            area = offer['area'],
            rooms_count = offer['rooms_count'],
            floor = offer['floor'],
            floor_count = offer['floor_count'],
            photo_mini = offer['photo_mini'],
            photos = offer['photos'],
            owner = user.id
        )
        session.add(new_flat)
        session.commit()
        return True
    return False


def get_prefs(tg_id):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    prefs = {}
    prefs['city'] = user.city
    prefs['rooms_count'] = user.rooms_count
    prefs['beds_count'] = user.beds_count
    prefs['min_price'] = user.min_price
    prefs['date_gte'] = user.date_gte
    prefs['date_lt'] = user.date_lt
    prefs['is_hotel'] = user.is_hotel

    return prefs


def get_prefs_text(tg_id):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    if user.is_hotel:
        is_hotel = 'Да'
    else:
        is_hotel = 'Нет'

    prefs_text = (
        f'<b>Город:</b> {user.city}\n'
        f'<b>Кол-во комнат:</b> {user.rooms_count}\n'
        f'<b>Кол-во гостей:</b> {user.beds_count}\n'
        f'<b>Мин. цена:</b> {user.min_price}\n'
        f'<b>Дата заезда:</b> {user.date_gte}\n'
        f'<b>Дата выезда:</b> {user.date_lt}\n'
        f'<b>Искать отели:</b> {is_hotel}\n'
    )
    return prefs_text


def set_prefs(tg_id, prefs):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    user.city = prefs['city']
    user.rooms_count = prefs['rooms_count']
    user.beds_count = prefs['beds_count']
    user.min_price = prefs['min_price']
    user.date_gte = prefs['date_gte']
    user.date_lt = prefs['date_lt']
    user.is_hotel = prefs['is_hotel']
    session.add(user)
    session.commit()