import unittest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models import Contact, User, Token
from auth.auths import get_current_active_user
from api.apis import create_contact, get_all_contacts, get_contact, update_contact, delete_contact, get_birthdays_within_7_days
from config import SECRET_KEY, ALGORITHM, oauth2_scheme


class TestAPIs(unittest.TestCase):

    def setUp(self):
        self.mock_user = User(id=1, username="testuser", email="test@example.com")
        self.mock_db_session = MagicMock(spec=Session)
        self.mock_contact = Contact(id=1, first_name="John", last_name="Doe", email="john@example.com")

    def test_create_contact(self):
        contact_data = {"first_name": "John", "last_name": "Doe", "email": "john@example.com"}
        response = create_contact(contact_data, current_user=self.mock_user)
        self.assertIsInstance(response, dict)
        self.assertEqual(response["first_name"], "John")
        self.assertEqual(response["last_name"], "Doe")
        self.assertEqual(response["email"], "john@example.com")

    def test_get_all_contacts(self):
        self.mock_db_session.query.return_value.all.return_value = [self.mock_contact]
        contacts = get_all_contacts(db=self.mock_db_session)
        self.assertIsInstance(contacts, list)
        self.assertEqual(len(contacts), 1)
        self.assertIsInstance(contacts[0], Contact)

    def test_get_contact(self):
        self.mock_db_session.query.return_value.filter.return_value.first.return_value = self.mock_contact
        contact = get_contact(contact_id=1, db=self.mock_db_session, current_user=self.mock_user)
        self.assertIsInstance(contact, Contact)
        self.assertEqual(contact.id, 1)
        self.assertEqual(contact.first_name, "John")


class TestConfig(unittest.TestCase):

    @patch.dict('os.environ', {'SECRET_KEY': 'test_secret_key', 'ALGORITHM': 'test_algorithm'})
    def test_config_values(self):
        self.assertEqual(SECRET_KEY, 'test_secret_key')
        self.assertEqual(ALGORITHM, 'test_algorithm')

    def test_oauth2_scheme(self):
        self.assertIsInstance(oauth2_scheme, OAuth2PasswordBearer)
        

if __name__ == '__main__':
    unittest.main()
