# nodes.py
import uuid
import sqlite3

from create_db import conn

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
        if not text_data.get("text") or not text_data.get("title"):
            return {'message': 'Text or title missing'}, 400

        user_id = session.get("user_id")
        if not user_id:
            return {'message': 'User not authenticated'}, 401
        
        cursor = None
        try:
            cursor = conn.cursor()

            node_id = str(uuid.uuid4())
            query = '''
                INSERT INTO nodes (node_id, text, title, user_id)
                VALUES (?, ?, ?, ?)
            '''
            cursor.execute(query, (node_id,
             text_data.get("text"), text_data.get("title"), user_id))
            
            conn.commit()

            print("Text saved successfully")
            return {'message': 
            'Text saved successfully', 'node_id': node_id}, 200

        except Exception as e:
            return {'message': str(e)}, 500
        
        finally:
            if cursor:
                cursor.close()