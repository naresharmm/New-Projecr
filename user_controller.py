from cryptography.fernet import Fernet

import hashlib

from create_db import conn

from user import UserValidator

class UserController:
    def __init__(self):
        """
        Initializes the UserController with a Fernet cipher suite.
        """
        self.cipher_suite =\
         Fernet(b'DHML65d-nY3iZL1vsWkrmzf2kSfoHQ9Fnv6IWlyIPzQ=')
    def generate_slug(self, user_id: int, phone_number: str) -> str:
        """
        Generate a unique slug for the user based on user_id and phone_number.

        Parameters:
        ------------------------
        user_id : int 
        phone_number : str 

        Returns:
        ------------------------
        str
        """
        # Concatenate user_id and phone_number
        combined_data = str(user_id) + phone_number

        # Generate hash using hashlib
        hashed_data = hashlib.sha256(combined_data.encode()).hexdigest()

        # Return the first 10 characters of the hashed data as slug
        return hashed_data[:10]
    


    def register(self, form_data: dict, session: dict) -> bool:
        """
        Registers a new user.

        Parameters:
        ------------------------
        form_data (dict): 
        session (dict): 

        Returns:
        ------------------------
        bool:
        """
        password_form = form_data.get("password")
        encrypted_password = self.cipher_suite.encrypt(password_form.encode()).decode()

        if not UserValidator().validate_registration(form_data):
            return False
        
        with conn:
            cursor = conn.cursor()
            slug = self.generate_slug(cursor.lastrowid, form_data['phone_number'])  # Generate slug
            cursor.execute(
                '''
                INSERT INTO users (phone_number, email, password, slug)
                VALUES (?, ?, ?, ?)
                ''',\
                (\
                form_data['phone_number'],
                form_data['email'],
                encrypted_password,
                slug)  # Insert slug into database
            )
            session["user_id"] = cursor.lastrowid
            return True

    def login(self, phone_number: str, password: str, session: dict) -> bool:
        """
        Logs a user into the system.

        Parameters:
        ------------------------
        phone_number : str 
        password : str 
        session : dict 

        Returns:
        ------------------------
        bool
        """
        with conn:
            cursor = conn.cursor()
            cursor.execute(\
            'SELECT id, password FROM users WHERE phone_number = ?',\
            (
            phone_number,
              )
            )
            user_data = cursor.fetchone()

        if user_data:
            user_id, hashed_password = user_data
            dec_password = self.cipher_suite.decrypt(\
                hashed_password.encode()).decode()
            if dec_password == password:
                session["user_id"] = user_id
                return True
        return False

    def get_profile(self, session: dict) -> dict:
        """
        Retrieves the profile data of the authenticated user.

        Parameters:
        ------------------------
        session : dict 

        Returns:
        ------------------------
        dict:
        """
        user_id = session.get("user_id")
        if user_id:
            nodes = {}
            with conn:
                cursor = conn.cursor()
                cursor.execute(
                    '''
                    SELECT node_id, text, title FROM nodes WHERE user_id = ?
                    ''',\
                (
                user_id,
                    )
                )
                user_texts = cursor.fetchall()
            for row in user_texts:
                nodes[row[0]] = {'title': row[2], 'text': row[1]}
            return nodes
        else:
            return {'message': 'User not authenticated'}, 401
    