import unittest
from unittest.mock import patch, MagicMock
from datetime import timedelta
from jose import jwt
from fastapi import HTTPException, status
from jwts import create_jwt_token, decode_jwt_token
from auths import authenticate_user, create_access_token, login_for_access_token, refresh_access_token, get_current_user, get_current_active_user, send_email
from api.config import SECRET_KEY, ALGORITHM


class TestAuth(unittest.TestCase):

    def test_authenticate_user_correct_credentials(self):
        user = authenticate_user("test", "testpassword")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "test")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.hashed_password, "testpassword")

    def test_authenticate_user_incorrect_credentials(self):
        user = authenticate_user("wrong", "wrongpassword")
        self.assertIsNone(user)

    def test_create_access_token(self):
        token = create_access_token({"sub": "test"}, timedelta(minutes=30))
        self.assertTrue(isinstance(token, str))

    @patch("auths.create_access_token", return_value="valid_access_token")
    def test_login_for_access_token_success(self, mock_create_access_token):
        form_data = MagicMock()
        form_data.username = "test"
        form_data.password = "testpassword"
        response = login_for_access_token(form_data)
        self.assertEqual(response["access_token"], "valid_access_token")

    def test_login_for_access_token_failure(self):
        form_data = MagicMock()
        form_data.username = "wrong"
        form_data.password = "wrongpassword"
        with self.assertRaises(HTTPException):
            login_for_access_token(form_data)

    def test_refresh_access_token(self):
        token = "valid_access_token"
        refreshed_token = refresh_access_token(token)
        self.assertTrue(isinstance(refreshed_token, dict))
        self.assertIn("access_token", refreshed_token)
        self.assertIn("token_type", refreshed_token)

    def test_get_current_user_valid_token(self):
        token = "valid_access_token"
        with patch("auths.decode_jwt_token", return_value={"sub": "test"}):
            user = get_current_user(token)
        self.assertIsNotNone(user)

    def test_get_current_user_invalid_token(self):
        token = "invalid_access_token"
        with self.assertRaises(HTTPException):
            get_current_user(token)

    def test_get_current_active_user_active_user(self):
        user = MagicMock()
        result = get_current_active_user(user)
        self.assertEqual(result, user)

    def test_get_current_active_user_inactive_user(self):
        with self.assertRaises(HTTPException):
            get_current_active_user(None)

    @patch("auths.smtplib.SMTP_SSL")
    def test_send_email(self, mock_smtp):
        email = "test@example.com"
        token = "test_token"
        send_email(email, token)
        mock_smtp_instance = mock_smtp.return_value.__enter__.return_value
        mock_smtp_instance.login.assert_called_once()
        mock_smtp_instance.sendmail.assert_called_once()


class TestJWT(unittest.TestCase):

    def test_create_jwt_token(self):
        data = {"sub": "test"}
        expires_delta = timedelta(minutes=30)
        token = create_jwt_token(data, expires_delta)
        self.assertTrue(isinstance(token, str))

    @patch("jwts.jwt.decode", return_value={"sub": "test"})
    def test_decode_jwt_token_valid_token(self, mock_decode):
        token = "valid_access_token"
        payload = decode_jwt_token(token)
        self.assertEqual(payload["sub"], "test")

    @patch("jwts.jwt.decode", side_effect=jwt.JWTError)
    def test_decode_jwt_token_invalid_token(self, mock_decode):
        token = "invalid_access_token"
        with self.assertRaises(HTTPException) as context:
            decode_jwt_token(token)
        self.assertEqual(context.exception.status_code, status.HTTP_401_UNAUTHORIZED)


if __name__ == '__main__':
    unittest.main()
