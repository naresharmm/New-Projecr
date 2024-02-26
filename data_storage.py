import sqlite3

class DataController:
    """
    DataController class for managing text data.
    """
    def __init__(self, session: dict, request):
        """
        Initialize the object.

        Parameters
        ----------
        session : dict
            A dictionary representing the session.
        request : YourRequestType
            An object representing the request.

        Returns
        -------
        None
        """
        self.session = session
        self.request = request

    def delete_text(self, node_id: str) -> dict:
        """
        Delete text associated with a node.

        Parameters
        ----------
        node_id : str

        Returns
        -------
        dict
        """
        user_phone = self.session.get("phone_number")
        if not user_phone:
            return {'message': 'User not authenticated'}, 401
        
        try:
            conn = sqlite3.connect('app.db')
            cursor = conn.cursor()

            cursor.execute('DELETE FROM nodes WHERE node_id = ?', (node_id,))
            
            conn.commit()
            conn.close()

            return {'message': 'Text deleted successfully'}, 200

        except Exception as e:
            return {'message': str(e)}, 500

    def edit_text(self, node_id: int) -> dict:
        """
        Edit text associated with a node.

        Parameters
        ----------
        node_id : str
        The ID of the node whose text needs to be edited.

        Returns
        -------
        dict
        """
        data = self.request.get_json()
        new_text = data.get('new_text')

        if not new_text:
            return {'message': 'New text not provided'}, 400

        user_phone = self.session.get("phone_number")
        if not user_phone:
            return {'message': 'User not authenticated'}, 401

        try:
            conn = sqlite3.connect('app.db')
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM nodes WHERE node_id = ?', (node_id,))
            if not cursor.fetchone():
                return {'message': 'Text node not found'}, 404

            conn.commit()
            conn.close()

            return {'message': 'Text edited successfully'}, 200

        except Exception as e:
            return {'message': str(e)}, 500
