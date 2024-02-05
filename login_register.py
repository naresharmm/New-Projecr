import json
from flask import Blueprint
from flask import (
    request,
    session,
    render_template,
    redirect,
    url_for
)
from user import UserValidator
from cryptography.fernet import Fernet
from countries import get_countries
key = Fernet.generate_key()
cipher_suite = Fernet(b'DHML65d-nY3iZL1vsWkrmzf2kSfoHQ9Fnv6IWlyIPzQ=')

login_register = Blueprint('login_register', __name__)
@login_register.route('/register', methods=['GET'])
def register_form():
    """
    Render the registration form.

    Returns:
        str: The rendered HTML content of the registration form.
    """
    return render_template('registration.html', countries=get_countries())

@login_register.route('/register', methods=['POST'])
def register():
    """
    Register a new user.

    Returns:
        str: A redirection to the user's profile page if 
        registration is successful, otherwise an error message.
    """
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
        return redirect(url_for('profile'))
    else:
        return "Data inputted wrong"

@login_register.route('/login', methods=['GET'])
def login_form():
    """
    Render the login form.

    Returns:
        str: The rendered HTML content of the login form.
    """
    return render_template('login.html')

@login_register.route('/login', methods=['POST'])
def login():
    """
    Log in an existing user.

    Returns:
        str: A redirection to the user's profile page if login is successful,
        otherwise an error message.
    """
    phone_number: str = request.form.get('phone_number')
    password: str = request.form.get('password')
    with open('data/users.json', 'r', encoding='utf-8') as file:
        users: dict = json.load(file)

    dec_password = cipher_suite.decrypt(users[phone_number]["password"]).decode()
    if phone_number in users and dec_password == password:
        session["phone_number"] = phone_number
        return redirect(url_for('profile'))
    else:
        return "Phone number or password is incorrect"

@login_register.route('/logout', methods=['GET'])
def logout():
    """
    Log out the current user and clear their session.

    Returns:
        str: A redirection to the home page.
    """
    session.clear()
    return redirect(url_for('home'))