import json
from cryptography.fernet import Fernet

from flask import session,request

from user import UserValidator
from data_storage import DataController

class UserController:
    def __init__(self, session: dict, request: request) -> None:
        """
        Initialize the UserController.

        Parameters
        ----------
        session : dict
            The session object from Flask.
        request : request
            The request object from Flask.
        """
        self.data_controller = DataController(session, request)
        self.cipher_suite = Fernet(b'DHML65d-nY3iZL1vsWkrmzf2kSfoHQ9Fnv6IWlyIPzQ=')

    def register(self, form_data: dict) -> bool:
        """
        Register a new user.

        Parameters
        ----------
        form_data : dict
            The form data containing user information.

        Returns
        -------
        bool
            True if registration is successful, False otherwise.
        """
        password_form = form_data.get("password")
        encrypted_password = self.cipher_suite.encrypt(password_form.encode()).decode()
        if UserValidator.validate_registration(form_data):
            with open('data/users.json', 'r+', encoding='utf-8') as file:
                users = json.load(file)
                file.seek(0)
                file.truncate()
                user_phone = form_data.get("phone_number")
                session["phone_number"] = user_phone
                users[user_phone] = {
                    "email": form_data.get('email'),
                    "password": encrypted_password,
                    "node_ids": []
                }
                json.dump(users, file, indent=2)
            return True
        else:
            return False

    def login(self, phone_number: str, password: str) -> bool:
        """
        Login a user.

        Parameters
        ----------
        phone_number : str
            The phone number of the user.
        password : str
            The password of the user.

        Returns
        -------
        bool
            True if login is successful, False otherwise.
        """
        with open('data/users.json', 'r', encoding='utf-8') as file:
            users = json.load(file)

        dec_password = self.cipher_suite.decrypt(users[phone_number]["password"]).decode()
        if phone_number in users and dec_password == password:
            session["phone_number"] = phone_number
            return True
        else:
            return False

    def logout(self) -> bool:
        """
        Logout the current user.

        Returns
        -------
        bool
            True if logout is successful.
        """
        session.clear()
        return True