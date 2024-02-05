import json

from flask import Blueprint,session,request,jsonify
from datetime import datetime
import uuid
save_get = Blueprint('save_get',__name__)

@save_get.route('/save_text', methods=['GET', 'POST'])
def save_text():
    request_data: dict = json.loads(request.get_data().decode("utf-8"))
    text: str = request_data.get("text")
    title: str = request_data.get("title")

    if not text or not title:
        return jsonify({'message': 'Text or title missing'}), 400

    user_phone: str = session.get("phone_number")
    if not user_phone:
        return jsonify({'message': 'User not authenticated'}), 401

    text_uuid: str = str(uuid.uuid4())

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

    return jsonify({'message': 'Text saved successfully', 'uuid': text_uuid}), 200


@save_get.route('/get_saved_texts')
def get_saved_texts():
    """
    Return the saved texts for the current user.

    Returns:
        str: A JSON response containing the saved texts for the current user or an error message.
    """
    user_phone = session.get("phone_number")
    with open('data/users.json', 'r', encoding='utf-8') as users_file:
        users = json.load(users_file)
        user_node_ids = users[user_phone]['node_ids']

    with open('data/node.json', 'r', encoding='utf-8') as nodes_file:
        nodes = json.load(nodes_file)
        user_texts = [nodes[node_id]["text"] for node_id in user_node_ids if node_id in nodes]  

    return jsonify({'texts': user_texts}), 200