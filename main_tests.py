import unittest
from main import app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Contact
from datetime import date
from schemas import ContactCreateUpdate, ContactResponse



class TestMain(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_read_root(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Hello, world!"})


class TestModels(unittest.TestCase):

    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        SessionLocal = sessionmaker(bind=engine)
        self.db = SessionLocal()

        Base.metadata.create_all(bind=engine)

    def tearDown(self):
        self.db.close()

    def test_contact_model(self):
        contact = Contact(
            id=1,
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone_number="123456789",
            birth_date=date(1990, 1, 1),
            additional_data="Additional information"
        )

        self.db.add(contact)
        self.db.commit()

        db_contact = self.db.query(Contact).filter(Contact.id == 1).first()

        self.assertEqual(db_contact.id, 1)
        self.assertEqual(db_contact.first_name, "John")
        self.assertEqual(db_contact.last_name, "Doe")
        self.assertEqual(db_contact.email, "john@example.com")
        self.assertEqual(db_contact.phone_number, "123456789")
        self.assertEqual(db_contact.birth_date, date(1990, 1, 1))
        self.assertEqual(db_contact.additional_data, "Additional information")


class TestSchemas(unittest.TestCase):

    def test_contact_create_update_schema(self):
        contact_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "phone_number": "123456789",
            "birth_date": date(1990, 1, 1),
            "additional_data": "Additional information"
        }
        contact_schema = ContactCreateUpdate(**contact_data)

        self.assertEqual(contact_schema.first_name, "John")
        self.assertEqual(contact_schema.last_name, "Doe")
        self.assertEqual(contact_schema.email, "john@example.com")
        self.assertEqual(contact_schema.phone_number, "123456789")
        self.assertEqual(contact_schema.birth_date, date(1990, 1, 1))
        self.assertEqual(contact_schema.additional_data, "Additional information")

    def test_contact_response_schema(self):
        contact_data = {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "phone_number": "123456789",
            "birth_date": date(1990, 1, 1),
            "additional_data": "Additional information"
        }
        contact_schema = ContactResponse(**contact_data)

        self.assertEqual(contact_schema.id, 1)
        self.assertEqual(contact_schema.first_name, "John")
        self.assertEqual(contact_schema.last_name, "Doe")
        self.assertEqual(contact_schema.email, "john@example.com")
        self.assertEqual(contact_schema.phone_number, "123456789")
        self.assertEqual(contact_schema.birth_date, date(1990, 1, 1))
        self.assertEqual(contact_schema.additional_data, "Additional information")


if __name__ == '__main__':
    unittest.main()
