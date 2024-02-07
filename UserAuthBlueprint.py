import json
from flask import (
    Blueprint,
    request,
    session,
    render_template,
    redirect,
    url_for,
)
from cryptography.fernet import Fernet
from user import UserValidator
from countries import get_countries
key = Fernet.generate_key()
cipher_suite = Fernet(b'DHML65d-nY3iZL1vsWkrmzf2kSfoHQ9Fnv6IWlyIPzQ=')

UserAuthBlueprint = Blueprint('UserAuthBlueprint', __name__)

class RegisterFormRoute:
    @staticmethod
    @UserAuthBlueprint.route('/register', methods=['GET'])
    def register_form():
        return render_template('registration.html', countries=get_countries())

class RegisterRoute:
    @staticmethod
    @UserAuthBlueprint.route('/register', methods=['POST'])
    def register():
        password_form = request.form.get("password")
        encrypted_password = cipher_suite.encrypt(password_form.encode()).decode()
        if UserValidator.validate_registration(request.form):
            with open('data/users.json', 'r+', encoding='utf-8') as file:
                users: dict = json.load(file)
                file.seek(0)
                file.truncate()
                user_phone: str = request.form.get("phone_number")
                session["phone_number"] = user_phone
                users[user_phone] = {
                    "email": request.form.get('email'),
                    "password": encrypted_password,
                    "node_ids": []
                }
                json.dump(users, file, indent=2)
            return redirect(url_for('data_storage.profile'))
        else:
            return "Data inputted wrong"

class LoginFormRoute:
    @staticmethod
    @UserAuthBlueprint.route('/login', methods=['GET'])
    def login_form():
        return render_template('login.html')

class LoginRoute:
    @staticmethod
    @UserAuthBlueprint.route('/login', methods=['POST'])
    def login():
        phone_number: str = request.form.get('phone_number')
        password: str = request.form.get('password')
        with open('data/users.json', 'r', encoding='utf-8') as file:
            users: dict = json.load(file)

        dec_password = cipher_suite.decrypt(users[phone_number]["password"]).decode()
        if phone_number in users and dec_password == password:
            session["phone_number"] = phone_number
            return redirect(url_for('data_storage.profile'))
        else:
            return "Phone number or password is incorrect"

class LogoutRoute:
    @staticmethod
    @UserAuthBlueprint.route('/logout', methods=['GET'])
    def logout():
        session.clear()
        return redirect(url_for('home'))

