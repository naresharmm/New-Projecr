from create_db import conn

class DataController:
    """
    DataController class for managing text data.
    """
    def delete_text(self, node_id: str, session: dict) -> dict:
        """
        Delete text associated with a node.

        Parameters
        ----------
        node_id : str
            The ID of the node to delete.
        session : dict
            A dictionary representing the session.

        Returns
        -------
        dict
            A dictionary containing the result of the operation.
        """
        user_id = session.get("user_id")
        if not user_id:
            return {'message': 'User not authenticated'}, 401
        
        try:
            with conn:
                cursor = conn.cursor()

                cursor.execute(
                    'DELETE FROM nodes WHERE node_id = ? AND user_id = ?',
                    (node_id, user_id)
                )
                
                return {'message': 'Text deleted successfully'}, 200

        except Exception as e:
            return {'message': str(e)}, 500


    def edit_text(self, node_id: str, new_text: str, session: dict) -> dict:
        """
        Edit text associated with a node.

        Parameters
        ----------
        node_id : str
            The ID of the node whose text needs to be edited.
        new_text : str
            The new text to be set for the node.
        session : dict
            A dictionary representing the session.

        Returns
        -------
        dict
            A dictionary containing the result of the operation.
        """
        if not new_text:
            return {'message': 'New text not provided'}, 400

        user_id = session.get("user_id")
        if not user_id:
            return {'message': 'User not authenticated'}, 401

        try:
            with conn:
                cursor = conn.cursor()

                cursor.execute(
                    'SELECT * FROM nodes WHERE node_id = ? AND user_id = ?',
                    (node_id,
                     user_id)
                )

                if not cursor.fetchone():
                    return {'message': 'Text node not found'}, 404

                cursor.execute(
                'UPDATE nodes SET text = ? WHERE node_id = ? AND user_id = ?',
                    (new_text,
                     node_id,
                     user_id)
                )

                return {'message': 'Text edited successfully'}, 200

        except Exception as e:
            return {'message': str(e)}, 500
