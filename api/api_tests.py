import unittest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models import Contact, User, Token
from auth.auths import get_current_active_user
from api.apis import create_contact, get_all_contacts, get_contact, update_contact, delete_contact, get_birthdays_within_7_days
from config import SECRET_KEY, ALGORITHM, oauth2_scheme
from starlette.testclient import TestClient
from endpoints import app
from routes import router

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
        

class TestEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_read_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"index.html", response.content)

    def test_read_login(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"login.html", response.content)

    def test_login_user(self):
        response = self.client.post("/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Logowanie udane", response.content)

    def test_read_register(self):
        response = self.client.get("/register")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"register.html", response.content)

    def test_read_contacts(self):
        response = self.client.get("/contacts")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"contacts.html", response.content)

    def test_welcome(self):
        response = self.client.get("/welcome")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"welcome.html", response.content)

    def test_verify_email(self):
        username = "test_user"
        verification_token = "test_token"
        response = self.client.get(f"/verify/{username}/{verification_token}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"login", response.content)
        
        
class TestRoutes(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(router)

    def test_read_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"index.html", response.content)
        self.assertIn(b"Hello, world!", response.content)

    def test_refresh_token(self):
        response = self.client.post("/refresh-token/")
        self.assertEqual(response.status_code, 422)  
        self.assertIn(b"detail", response.content)
        self.assertIn(b"Missing", response.content)  

    def test_refresh_token_with_token(self):
        token = "valid_access_token"
        response = self.client.post("/refresh-token/", data={"current_token": token})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"valid_access_token", response.content) 


if __name__ == '__main__':
    unittest.main()
