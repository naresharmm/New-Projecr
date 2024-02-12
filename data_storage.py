import json
from flask import jsonify

class DataController:
    @staticmethod
    def delete_text(request, session):
        data = request.get_json()
        text_to_delete = data.get('text')

        if not text_to_delete:
            return jsonify({'message': 'No text provided'}), 400

        current_user_phone = session.get("phone_number")

        if not current_user_phone:
            return jsonify({'message': 'User not authenticated'}), 401

        try:
            with open('data/users.json', 'r+', encoding='utf-8') as users_file:
                users = json.load(users_file)
                user_node_ids = users.get(current_user_phone, {}).get("node_ids", [])

                with open('data/node.json', 'r+', encoding='utf-8') as nodes_file:
                    nodes = json.load(nodes_file)

                    text_id = next((nid for nid in user_node_ids if nid in
                                    nodes and nodes[nid]["text"] == text_to_delete), None)

                    if text_id:
                        del nodes[text_id]
                        user_node_ids.remove(text_id)

                        nodes_file.seek(0)
                        json.dump(nodes, nodes_file, indent=2)
                        nodes_file.truncate()

                        users_file.seek(0)
                        json.dump(users, users_file, indent=2)
                        users_file.truncate()

                        return jsonify({'message': 'Text deleted successfully'}), 200
                    else:
                        return jsonify({'message': 'Text not found'}), 404

        except Exception as e:
            return jsonify({'message': str(e)}), 500
