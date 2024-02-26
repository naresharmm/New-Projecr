import re


class UserValidator:
    def validate_registration(self, request_form: dict) -> bool:
        """Validate a user's registration data based on the given form input.

        Parameters:
        ------------------------
        request_form (dict): 
        
        Returns
        ------------------------
            bool:
        """
        username = request_form.get('username')
        phone_number = request_form.get("phone_number")
        password = request_form.get('password')
        password2 = request_form.get('password2')
        email = request_form.get('email')
        country = request_form.get('country')

        return all((username, password, email, country)) and \
            self.is_valid_phone(phone_number) and \
            self.is_valid_email(email) and \
            self.is_valid_password(password, password2)

    def is_valid_phone(self, phone_number: str) -> bool:
        """Validate a phone number based on specific criteria.

        Parameters
        ------------------------
            phone_number (str): 
            The phone number to be validated.

        Returns
        ------------------------
            bool: 
            True if the phone number matches the format (+374xxxxxxxx)
        """
        return re.match(r'^\+374\d{8}$', phone_number)

    def is_valid_email(self, email: str) -> bool:
        """Validate an email address based on specific criteria.

        Parameters
        ------------------------
            email (str): The email address to be validated.

        Returns
        ------------------------
            bool: 
        """
        return re.match\
        (r'^[a-zA-Z0-9._%+-]{1,10}@[a-zA-Z0-9.-]{1,10}\.[a-zA-Z]{1,10}$', email)

    def is_valid_password(self, password: str, password2: str) -> bool:
        """Validate a password based on 
        specific criteria and 
        check if  matches the  password.

        Parameters
        ------------------------
            password (str): 
            The password to be validated.

        Returns
        ------------------------
            bool:
        """
        return self.has_valid_format(password) and password == password2

    def has_valid_format(self, password: str) -> bool:
        """Check if a password meets a specified format criteria.

        Parameters
        ------------------------
            password (str): 

        Returns
        ------------------------
            bool:
        """
        return re.match(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$",
            password
        )
