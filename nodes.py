import json
import uuid
from datetime import datetime
from typing import Dict, Union

class NodesController:
    def save_text(self, text_data: Dict[str, Union[str, None]], 
                  session: Dict[str, Union[str, None]]):
        """
        Save a text node.

        Parameters
        --------------
        text_data : dict
            A dictionary containing the text and title to be saved.
        session : dict
            A dictionary containing session information, 
            including the user's phone number.

        Returns
        --------------
        tuple
            A tuple containing a dictionary message about the status 
            of the save operation and an HTTP status code.
        """
        text = text_data.get("text")
        title = text_data.get("title")

        if not text or not title:
            return {'message': 'Text or title missing'}, 400

        user_phone = session.get("phone_number")
        if not user_phone:
            return {'message': 'User not authenticated'}, 401
        text_uuid = str(uuid.uuid4())

        with open('data/node.json', 'r', encoding='utf-8') as file:
            nodes = json.load(file)

        nodes[text_uuid] = {
            "title": title,
            "text": text,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        with open('data/node.json', 'w', encoding='utf-8') as file:
            json.dump(nodes, file, indent=2)
        
        with open('data/users.json', 'r', encoding='utf-8') as file:
            users = json.load(file)

        users[user_phone]['node_ids'].append(text_uuid)
        with open('data/users.json', 'w', encoding='utf-8') as file:
            json.dump(users, file, indent=2)

        return {'message': 'Text saved successfully', 'uuid': text_uuid}, 200
    
    def get_saved_texts(self, session: Dict[str, Union[str, None]]):
        """
        Get saved texts for the current user.

        Parameters
        --------------
        session : dict
            A dictionary containing
              session information, including the user's phone number.

        Returns
        --------------
        tuple
            A tuple containing a 
            dictionary of user texts and an HTTP status code.
        """
        user_phone = session.get("phone_number")
        with open('data/users.json', 'r', encoding='utf-8') as users_file:
            users = json.load(users_file)
            user_node_ids = users[user_phone]['node_ids']

        with open('data/node.json', 'r', encoding='utf-8') as nodes_file:
            nodes = json.load(nodes_file)
            user_texts = [nodes[node_id]["text"] for node_id in user_node_ids if node_id in nodes]

        return {'texts': user_texts}, 200

    def delete_text(self, node_id: str) -> Dict[str, str]:
        """
        Delete a text node.

        Parameters
        --------------
        node_id : str
            The ID of the text node to delete.

        Returns
        --------------
        dict
            A dictionary containing a message about the status of the deletion.
        """
        with open('data/node.json', 'r', encoding='utf-8') as file:
            nodes = json.load(file)

        if node_id in nodes:
            del nodes[node_id]
            with open('data/node.json', 'w', encoding='utf-8') as file:
                json.dump(nodes, file, indent=2)
            return {'message': 'Text deleted successfully'}
        else:
            return {'message': 'Text not found'}
