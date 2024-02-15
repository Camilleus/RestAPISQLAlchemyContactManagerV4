import unittest
from unittest.mock import patch, MagicMock
from databases import Database
from sqlalchemy.orm import sessionmaker
from dbs import database, engine, Base, init_db, get_db
from faker import Faker
from sqlalchemy import create_engine, Column, Integer, String, Date, Text, MetaData, Table
from data_faker import create_fake_contact, seed_fake_data
from data_sender import import_data_to_mysql


class TestDB(unittest.TestCase):

    @patch("dbs.create_engine")
    @patch("dbs.Base.metadata.create_all")
    def test_init_db(self, mock_create_all, mock_create_engine):
        init_db()
        mock_create_engine.assert_called_once_with(database)
        mock_create_all.assert_called_once_with(bind=engine)

    @patch("dbs.SessionLocal")
    def test_get_db(self, mock_session_local):
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        with get_db() as db:
            self.assertEqual(db, mock_session)
        mock_session_local.assert_called_once()
        mock_session.close.assert_called_once()


class TestDataFaker(unittest.TestCase):

    @patch("data_faker.engine.connect")
    @patch("data_faker.fake.first_name")
    @patch("data_faker.fake.last_name")
    @patch("data_faker.fake.email")
    @patch("data_faker.fake.phone_number")
    @patch("data_faker.fake.date_of_birth")
    @patch("data_faker.fake.text")
    def test_create_fake_contact(self, mock_text, mock_date_of_birth, mock_phone_number, mock_email, mock_last_name,
                                 mock_first_name, mock_connect):
        mock_text.return_value = "Lorem ipsum dolor sit amet"
        mock_date_of_birth.return_value = "1990-01-01"
        mock_phone_number.return_value = "123456789"
        mock_email.return_value = "test@example.com"
        mock_last_name.return_value = "Doe"
        mock_first_name.return_value = "John"

        expected_contact = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "test@example.com",
            "phone_number": "123456789",
            "birth_date": "1990-01-01",
            "additional_data": "Lorem ipsum dolor sit amet"
        }

        self.assertEqual(create_fake_contact(), expected_contact)

    @patch("data_faker.engine.connect")
    @patch("data_faker.contacts.insert")
    @patch("data_faker.create_fake_contact")
    def test_seed_fake_data(self, mock_create_fake_contact, mock_insert, mock_connect):
        mock_create_fake_contact.return_value = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "test@example.com",
            "phone_number": "123456789",
            "birth_date": "1990-01-01",
            "additional_data": "Lorem ipsum dolor sit amet"
        }

        seed_fake_data()
        mock_insert.assert_called()
        mock_connect.assert_called()


class TestDataSender(unittest.TestCase):

    @patch("data_sender.mysql.connector.connect")
    @patch("data_sender.open")
    @patch("data_sender.mysql.connector.cursor")
    def test_import_data_to_mysql(self, mock_cursor, mock_open, mock_connect):
        mock_cursor_instance = MagicMock()
        mock_cursor.return_value.__enter__.return_value = mock_cursor_instance

        mock_connect_instance = MagicMock()
        mock_connect.return_value = mock_connect_instance

        mock_open_instance = MagicMock()
        mock_open.return_value.__enter__.return_value.read.return_value = "CREATE TABLE test_table (id INT); INSERT INTO test_table VALUES (1);"
        mock_open.return_value = mock_open_instance

        import_data_to_mysql()

        mock_connect.assert_called_with(
            host="localhost",
            user="Camilleus",
            password="fghg1234",
            database="konigcontacts"
        )

        mock_cursor_instance.execute.assert_called_with("CREATE TABLE test_table (id INT)")
        mock_cursor_instance.execute.assert_called_with("INSERT INTO test_table VALUES (1)")
        mock_connect_instance.commit.assert_called()
        mock_cursor_instance.close.assert_called()
        mock_connect_instance.close.assert_called()

        
if __name__ == '__main__':
    unittest.main()
