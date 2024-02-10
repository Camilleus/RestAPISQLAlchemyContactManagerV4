from faker import Faker
from sqlalchemy import create_engine, Column, Integer, String, Date, Text, MetaData, Table
from sqlalchemy.orm import sessionmaker
import random

fake = Faker()

engine = create_engine("sqlite:///./contacts.db", echo=True)
Base = MetaData()

contacts = Table(
    'contacts',
    Base,
    Column('id', Integer, primary_key=True, index=True),
    Column('first_name', String, index=True),
    Column('last_name', String, index=True),
    Column('email', String, unique=True, index=True),
    Column('phone_number', String),
    Column('birth_date', Date),
    Column('additional_data', Text, nullable=True),
)

Base.create_all(engine)
Session = sessionmaker(bind=engine)

def create_fake_contact():
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "phone_number": fake.phone_number(),
        "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=90),
        "additional_data": fake.text()
    }

def seed_fake_data():
    contacts_data = [create_fake_contact() for _ in range(50)]

    with engine.connect() as conn:
        for contact in contacts_data:
            conn.execute(contacts.insert().values(contact))

if __name__ == "__main__":
    seed_fake_data()
    print("Fikcyjne dane zostały zapisane i zaimportowane do bazy.")
