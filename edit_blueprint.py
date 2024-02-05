import json
from flask import Blueprint
from flask import (
    request,
    jsonify,
    session
)
edit_blueprint = Blueprint('edit_blueprint', __name__)
@edit_blueprint.route('/profile/edit_text', methods=['POST'])
def edit_text():
    """
    Edit the title of a text for the current user.

    Returns:
        str: A JSON response indicating whether the text title was edited successfully or an error message.
    """
    data: dict = request.get_json()
    old_text: str = data.get('old_text')
    new_text: str = data.get('new_text')
    if not old_text or not new_text:
        return jsonify({'message': 'Text missing'}), 400

    current_user_phone: str = session.get("phone_number")
    if not current_user_phone:
        return jsonify({'message': 'User not authenticated'}), 401

    try:
        with open('data/users.json', 'r', encoding='utf-8') as users_file:
            users = json.load(users_file)
            user_node_ids = users[current_user_phone]["node_ids"]

        with open('data/node.json', 'r+', encoding='utf-8') as nodes_file:
            nodes = json.load(nodes_file)
            text_id = next((nid for nid in user_node_ids if nodes[nid]["text"] == old_text), None)

            if text_id:
                nodes[text_id]["text"] = new_text
                nodes_file.seek(0)
                json.dump(nodes, nodes_file, indent=2)
                nodes_file.truncate()
                return jsonify({'message': 'Text edited successfully'}), 200
            else:
                return jsonify({'message': 'Text not found'}), 404

    except Exception as e:
        return jsonify({'message': str(e)}), 500