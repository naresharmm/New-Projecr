# user.py

import re

class UserValidator:
  
    def validate_registration(request_form):
        '''
        Validates user registration based on form input
        '''
        username = request_form.get('username')
        phone_number = request_form.get("phone_number")
        password = request_form.get('password')
        password2 = request_form.get('password2')
        email = request_form.get('email')
        country = request_form.get('country')

        return all([username, password, email, country]) and \
               UserValidator.is_valid_phone(phone_number) and \
               UserValidator.is_valid_email(email) and \
               UserValidator.is_valid_password(password, password2)


    def is_valid_phone(phone_number):
        ''' Checks phone validation '''
        return bool(re.match(r'^\+374\d{8}$', phone_number))

  
    def is_valid_email(email):
        ''' Checks email validation '''
        return bool(re.match(r'^\w+@[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$', email))


    def is_valid_password(password, password2):
        ''' Checks password validation '''
        return UserValidator.has_valid_format(password) and password == password2

    def has_valid_format(password):
        ''' Checks password format '''
        return bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", password))
