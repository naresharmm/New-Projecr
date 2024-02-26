import sqlite3
from cryptography.fernet import Fernet

from user import UserValidator

class UserController:
    def __init__(self) -> None:
        """
        Initializes the UserController with a Fernet cipher suite.
        """
        self.cipher_suite = \
        Fernet(b'DHML65d-nY3iZL1vsWkrmzf2kSfoHQ9Fnv6IWlyIPzQ=')

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
            =
        """
        password_form = form_data.get("password")
        encrypted_password = self.cipher_suite.\
        encrypt(password_form.encode()).decode()
        if UserValidator().validate_registration(form_data):
            try:
                conn = sqlite3.connect('app.db')
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO users (phone_number, email, password)
                    VALUES (?, ?, ?)
                ''',
                (form_data['phone_number'],\
                 form_data['email'], encrypted_password))
                conn.commit()

                session["user_id"] = cursor.lastrowid 
                conn.close()
                return True

            except Exception as e:
                print(str(e))
                return False
        else:
            return False
        
    def login(self, phone_number: str, password: str, session: dict) -> bool:
        """
        Logs a user into the system.

        Parameters:
        ------------------------
        phone_number (str): 
            
        password (str): 
        session (dict): 
            

        Returns:
        ------------------------
        bool:
        """
        try:
            conn = sqlite3.connect('app.db')
            cursor = conn.cursor()

            cursor.execute('SELECT id, password FROM users\
            WHERE phone_number = ?', (phone_number,))
            user_data = cursor.fetchone()
            conn.close()

            if user_data:
                user_id, hashed_password = user_data
                dec_password = self.cipher_suite.\
                decrypt(hashed_password.encode()).decode()
                if dec_password == password:
                    session["user_id"] = user_id
                    return True

        except Exception as e:
            print(str(e))

        return False

    def get_profile(self, session: dict) -> dict:
        """
        Retrieves the profile data of the authenticated user.

        Parameters:
        ------------------------
        session (dict): 

        Returns:
        ------------------------
        dict:
        """
        user_id = session.get("user_id")
        if user_id:
            nodes = {}
            try:
                conn = sqlite3.connect('app.db')
                cursor = conn.cursor()

                cursor.execute('''
                    SELECT node_id, text, title FROM nodes
                    WHERE user_id = ?
                ''', (user_id,))
                user_texts = cursor.fetchall()

                conn.close()

                for row in user_texts:
                    nodes[row[0]] = {'title': row[2], 'text': row[1]}

            except Exception as e:
                print(str(e))
            return nodes
        else:
            return {'message': 'User not authenticated'}, 401
