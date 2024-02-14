import unittest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Contact, User, Token
from auth.auths import get_current_active_user
from api.apis import create_contact, get_all_contacts, get_contact, update_contact, delete_contact, get_birthdays_within_7_days


class TestAPIs(unittest.TestCase):

    def setUp(self):
        self.mock_user = User(id=1, username="testuser", email="test@example.com")
        self.mock_db_session = MagicMock(spec=Session)
        self.mock_contact = Contact(id=1, first_name="John", last_name="Doe", email="john@example.com")

    def test_create_contact(self):
        # Test creation of a new contact
        contact_data = {"first_name": "John", "last_name": "Doe", "email": "john@example.com"}
        response = create_contact(contact_data, current_user=self.mock_user)
        self.assertIsInstance(response, dict)
        self.assertEqual(response["first_name"], "John")
        self.assertEqual(response["last_name"], "Doe")
        self.assertEqual(response["email"], "john@example.com")

    def test_get_all_contacts(self):
        # Test fetching all contacts
        self.mock_db_session.query.return_value.all.return_value = [self.mock_contact]
        contacts = get_all_contacts(db=self.mock_db_session)
        self.assertIsInstance(contacts, list)
        self.assertEqual(len(contacts), 1)
        self.assertIsInstance(contacts[0], Contact)

    def test_get_contact(self):
        # Test fetching a specific contact
        self.mock_db_session.query.return_value.filter.return_value.first.return_value = self.mock_contact
        contact = get_contact(contact_id=1, db=self.mock_db_session, current_user=self.mock_user)
        self.assertIsInstance(contact, Contact)
        self.assertEqual(contact.id, 1)
        self.assertEqual(contact.first_name, "John")

    # Test other API functions similarly

if __name__ == '__main__':
    unittest.main()
