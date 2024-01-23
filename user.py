'''user.py
'''

import re

class UserValidator:
    '''Class UserValidator checks validation of inputs
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
        '''Checks if forms are filled
        '''
        return all([self.username, self.password, self.email, self.country])

    def valid_phone(self):
        ''' Checks phone validation
        '''
        return bool(re.match(r'^\+374\d{8}$', self.phone_number))

    def valid_email(self):
        '''Checks validation
        '''
        return bool(re.match(r'^\w+@[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$', self.email))

    def valid_password(self):
        ''' Checks validation password
        '''
        return bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$",
                             self.password))

    def passwords_match(self):
        '''Checks if 2 passwords match 
        '''
        return self.password == self.password_sec
