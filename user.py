'''user.py
'''
import re

class UserValidator:
    '''checks validation
    '''
    def __init__(self, username, phone_number, password,
                 password_sec, email,country):
        self.username = username
        self.phone_number = phone_number
        self.password = password
        self.password_sec = password_sec
        self.email = email
        self.country = country

    def form_filled(self):
        '''function
        '''
        return all([self.username, self.password, self.email, self.country])

    def valid_phone(self):
        '''function
        '''
        return bool(re.match(r'^\+374\d{8}$', self.phone_number))

    def valid_email(self):
        '''function
        '''
        return bool(re.match(r'^\w+@[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$', self.email))

    def valid_password(self):
        '''function
        '''
        return bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$",
                             self.password))

    def passwords_match(self):
        '''function
        '''
        return self.password == self.password_sec
