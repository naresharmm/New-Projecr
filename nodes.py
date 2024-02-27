import uuid

from create_db import conn

class NodesController:
    def save_text(self, text_data: dict, session: dict) -> dict:
        """
        Save a text node.

        Parameters
        ---------------
        text_data : dict
        session : dict

        Returns
        -----------------
        dict
        """
        if not text_data.get("text") or not text_data.get("title"):
            return {'message': 'Text or title missing'}

        if not (user_id := session.get("user_id")):
            return {'message': 'User not authenticated'}
        
        with conn:
            cursor = conn.cursor()

        try:
            node_id = str(uuid.uuid4())
            query = '''
                INSERT INTO nodes (node_id, text, title, user_id)
                VALUES (?, ?, ?, ?)
            '''
            cursor.execute(
                query, 
                (
                    node_id,
                    text_data.get("text"),
                    text_data.get("title"),
                    user_id
                )
            )
            conn.commit()

            print("Text saved successfully")
            return {
                'message': 'Text saved successfully',
                'node_id': node_id
            }

        finally:
            cursor.close()
