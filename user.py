# user.py
import re

class UserValidator:
    @staticmethod
    def validate_registration(request_form):
        """Validate a user's registration data based on the given form input.

        Parameters:
            request_form (dict): A dictionary containing user registration data. Expected keys are
            'username', 'phone_number', 'password', 'password2', 'email', and 'country'.

        Returns:
            bool: True if all provided data is valid according to the validation criteria, False otherwise.
        """
        username = request_form.get('username')
        phone_number = request_form.get("phone_number")
        password = request_form.get('password')
        password2 = request_form.get('password2')
        email = request_form.get('email')
        country = request_form.get('country')

        return all((username, password, email, country)) and \
            UserValidator.is_valid_phone(phone_number) and \
            UserValidator.is_valid_email(email) and \
            UserValidator.is_valid_password(password, password2)

    @staticmethod
    def is_valid_phone(phone_number):
        """Validate a phone number based on specific criteria.

        Parameters:
            phone_number (str): The phone number to be validated.

        Returns:
            bool: True if the phone number matches the Armenian phone number format (+374xxxxxxxx), False otherwise.
        """
        return re.match(r'^\+374\d{8}$', phone_number)

    @staticmethod
    def is_valid_email(email):
        """Validate an email address based on specific criteria.

        Parameters:
            email (str): The email address to be validated.

        Returns:
            bool: True if the email address is in a valid format, False otherwise.
                  The valid format includes 1-10 alphanumeric characters,
                  followed by an @ symbol, domain name of 1-10 alphanumeric characters,
                  and a domain suffix of 1-10 letters.
        """
        return re.match(r'^[a-zA-Z0-9._%+-]{1,10}@[a-zA-Z0-9.-]{1,10}\.[a-zA-Z]{1,10}$', email)

    @staticmethod
    def is_valid_password(password, password2):
        """Validate a password based on specific criteria and check if it matches the confirmed password.

        Parameters:
            password (str): The password to be validated.
            password2 (str): The confirmation password to be compared with the first password.

        Returns:
            bool: True if the password meets the required format and matches the confirmation password, False otherwise.
        """
        return UserValidator.has_valid_format(password) and password == password2

    @staticmethod
    def has_valid_format(password):
        """Check if a password meets a specified format criteria.

        Parameters:
            password (str): The password to be checked for format.

        Returns:
            bool: True if the password contains at least one lowercase letter, one uppercase letter,
                  and one digit, and is at least 8 characters long, False otherwise.
        """
        return re.match(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$",
            password
        )