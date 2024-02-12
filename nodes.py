import json
import uuid
from datetime import datetime


class NodesController:
    @staticmethod
    def save_text(request_data, session):
        text = request_data.get("text")
        title = request_data.get("title")

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

    @staticmethod
    def get_saved_texts(session):
        user_phone = session.get("phone_number")
        with open('data/users.json', 'r', encoding='utf-8') as users_file:
            users = json.load(users_file)
            user_node_ids = users[user_phone]['node_ids']

        with open('data/node.json', 'r', encoding='utf-8') as nodes_file:
            nodes = json.load(nodes_file)
            user_texts = [nodes[node_id]["text"] for node_id in user_node_ids if node_id in nodes]  

        return {'texts': user_texts}, 200
    