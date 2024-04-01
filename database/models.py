from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, Float, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
 

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, nullable=False)
    flats = relationship('Flat', backref='flats', lazy=True)
    autocheck_enable = Column(Boolean, default=False)
    city = Column(String, nullable=False)
    rooms_count = Column(Integer)
    beds_count = Column(Integer, nullable = False)
    min_price = Column(Integer, nullable = False)
    date_gte = Column(String, default='01.06.2024', nullable=False)
    date_lt = Column(String, default='08.06.2024', nullable=False)
    is_hotel = Column(Boolean, default=False)
    flats = relationship('Flat', backref='flats', lazy=True)


    def __repr__(self):
        return self.tg_id


class Flat(Base):
    __tablename__ = 'flat'
    id = Column(Integer, primary_key=True)
    offer_id = Column(Integer)
    url = Column(String)
    added_datetime = Column(String)
    address = Column(String)
    phone = Column(String)
    price = Column(Integer)
    area = Column(Float)
    rooms_count = Column(Integer)
    floor = Column(Integer)
    floor_count = Column(Integer)
    photo_mini = Column(String)
    photos = Column(String)
    owner = Column(Integer, ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return self.offer_id