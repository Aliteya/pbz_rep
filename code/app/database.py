from .config import settings
import psycopg2
from psycopg2 import sql
# from sqlalchemy import MetaData, Table, Index, Column, ForeignKey, String, Integer, DateTime
# import asyncpg

DATABASE_URL = settings.get_db_url()



def connect_db():
    return psycopg2.connect(DATABASE_URL)

conn = connect_db()
# metadata = MetaData()

# owner = Table('Владелец', metadata,
#             Column('owner_id', Integer(), primary_key=True),
#             Column('type_of_owner', String(15), nullable=False),
#             Column('name', String(30), nullable=False),
#             Column('owners_fullname', String(80), nullable=False),
#             Column('contact', String(13), nullable=False)
#             )

# object = Table('Место_проведения_досуга', metadata,
#             Column('object_id', Integer(), primary_key=True),
#             Column('owner_id', ForeignKey("Владелец.owner_id")),
#             Column('type', String(20), nullable=False),
#             Column('address',String(80), nullable=False),
#             Column('name', String(30), nullable=False),
#             Column('number_of_places', Integer(), nullable=False)
#             )

# popularity = Table('Популярность', metadata,
#             Column('popularity_id', Integer(), primary_key=True),
#             Column('object_id', ForeignKey("Место_проведения_досуга.object_id")),
#             Column('event_date', DateTime(), nullable=False),
#             Column('number_of_visitors', Integer(), nullable=False)
#             )

# event = Table('Мероприятие', metadata,
#               Column('event_id', Integer(), primary_key=True),
#               Column('object_id', ForeignKey("Место_проведения_досуга.object_id")),
#               Column('fut_event_date', DateTime(), nullable=False),
#               Column('event_name', String(90), nullable=False),
#               Column('event_type', String(30), nullable=False)
#             )

# date = Table('Дата_открытия', metadata,
#             Column('date_id', Integer(), primary_key=True),
#             Column('object_id', ForeignKey("Место_проведения_досуга.object_id")),
#             Column('opening_date', DateTime(), nullable=False),
#             Column('closing_date', DateTime()),
#             Index('idx_opening_date','opening_date')
#             )


