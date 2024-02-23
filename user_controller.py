
import sqlite3
from cryptography.fernet import Fernet

from user import UserValidator
class UserController:
    def __init__(self, session: dict, request) -> None:
        self.session = session
        self.request = request
        self.cipher_suite = Fernet(b'DHML65d-nY3iZL1vsWkrmzf2kSfoHQ9Fnv6IWlyIPzQ=')

    def register(self, form_data: dict) -> bool:
        password_form = form_data.get("password")
        encrypted_password = self.cipher_suite.encrypt(password_form.encode()).decode()
        if UserValidator().validate_registration(form_data):
            try:
                conn = sqlite3.connect('app.db')
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO users (phone_number, email, password, node_ids)
                    VALUES (?, ?, ?, ?)
                ''', (form_data['phone_number'], form_data['email'], encrypted_password, ''))

                conn.commit()
                conn.close()

                self.session["phone_number"] = form_data["phone_number"]
                return True

            except Exception as e:
                print(str(e))
                return False
        else:
            return False

    def login(self, phone_number: str, password: str) -> bool:
        try:
            conn = sqlite3.connect('app.db')
            cursor = conn.cursor()

            
            cursor.execute('SELECT password FROM users WHERE phone_number = ?', (phone_number,))
            user_data = cursor.fetchone()
            conn.close()

            if user_data:
                dec_password = self.cipher_suite.decrypt(user_data[0].encode()).decode()
                if dec_password == password:
                    self.session["phone_number"] = phone_number
                    return True

        except Exception as e:
            print(str(e))

        return False
    def get_profile(self) -> dict:
        phone_number = self.session.get("phone_number")
        if phone_number:
            nodes = {}
            try:
                conn = sqlite3.connect('app.db')
                cursor = conn.cursor()

                
                cursor.execute('SELECT node_ids FROM users WHERE phone_number = ?', (phone_number,))
                user_data = cursor.fetchone()
                if user_data:
                    node_ids = user_data[0].split(',')
                    
                    
                    for node_id in node_ids:
                        cursor.execute('SELECT * FROM nodes WHERE node_id = ?', (node_id,))
                        node_data = cursor.fetchone()
                        if node_data:
                            nodes[node_id] = {'text': node_data[1]} 
                    
                conn.close()
            except Exception as e:
                print(str(e))
            return nodes