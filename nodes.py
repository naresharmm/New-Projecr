import uuid
import sqlite3

class NodesController:
    def save_text(self, text_data: dict, session: dict):
        """
        Save a text node.

        Parameters
        ---------------
            text_data (dict):
            session (dict): 

        Returns
        -----------------
            tuple:
        """
        text = text_data.get("text")
        title = text_data.get("title")

        if not text or not title:
            return {'message': 'Text or title missing'}, 400

        user_phone = session.get("phone_number")
        if not user_phone:
            return {'message': 'User not authenticated'}, 401
        
        try:
            conn = sqlite3.connect('app.db')
            cursor = conn.cursor()

            node_id = str(uuid.uuid4())
            cursor.execute('''
                INSERT INTO nodes (node_id, text, title, user_id)
                VALUES (?, ?, ?, (SELECT id FROM users WHERE phone_number = ?))
            ''', (node_id, text, title, user_phone))
            
            conn.commit()
            conn.close()

            return {'message': 'Text saved successfully', 'node_id': node_id}, 200

        except Exception as e:
            return {'message': str(e)}, 500
