import json
from flask import session
from cryptography.fernet import Fernet
from user import UserValidator
from data_storage import DataController


class UserController:
    def __init__(self):
        self.data_controller = DataController()
        self.cipher_suite = Fernet(b'DHML65d-nY3iZL1vsWkrmzf2kSfoHQ9Fnv6IWlyIPzQ=')

    def register(self, form_data):
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

    def login(self, phone_number, password):
        with open('data/users.json', 'r', encoding='utf-8') as file:
            users = json.load(file)

        dec_password = self.cipher_suite.decrypt(users[phone_number]["password"]).decode()
        if phone_number in users and dec_password == password:
            session["phone_number"] = phone_number
            return True
        else:
            return False

    def logout(self):
        session.clear()
        return True
