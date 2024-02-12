import json
from flask import jsonify, request

class DataController:
    @staticmethod
    def delete_text(request, session):
        data = request.get_json()
        node_id = data.get('node_id')

        if not node_id:
            return jsonify({'message': 'No node_id provided'}), 400
        user_phone = session.get("phone_number")
        if not user_phone:
            return jsonify({'message': 'User not authenticated'}), 401
        try:
            with open('data/users.json', 'r+') as users_file:
                users = json.load(users_file)
                user_node_ids = users.get(user_phone, {}).get("node_ids", [])

                with open('data/node.json', 'r+') as nodes_file:
                    nodes = json.load(nodes_file)
                    if node_id in nodes:
                        del nodes[node_id]
                        if node_id in user_node_ids:
                            user_node_ids.remove(node_id)

                        users[user_phone]['node_ids'] = user_node_ids

                        users_file.seek(0)
                        json.dump(users, users_file, indent=2)
                        users_file.truncate()

                        nodes_file.seek(0)
                        json.dump(nodes, nodes_file, indent=2)
                        nodes_file.truncate()

                        return jsonify({'message': 'Text deleted successfully'}), 200
                    else:
                        return jsonify({'message': 'Text not found'}), 404

        except Exception as e:
            return jsonify({'message': str(e)}), 500
    @staticmethod
    def edit_text(request, session):
        data = request.get_json()
        node_id = data.get('node_id')
        new_text = data.get('new_text')

        if not node_id or not new_text:
            return jsonify({'message': 'Node_id or new_text not provided'}), 400

        user_phone = session.get("phone_number")
        if not user_phone:
            return jsonify({'message': 'User not authenticated'}), 401

        try:
            with open('data/users.json', 'r+') as users_file:
                users = json.load(users_file)
                user_node_ids = users.get(user_phone, {}).get("node_ids", [])

                with open('data/node.json', 'r+') as nodes_file:
                    nodes = json.load(nodes_file)

                    if node_id in nodes:
                        nodes[node_id]['text'] = new_text

                        users_file.seek(0)
                        json.dump(users, users_file, indent=2)
                        users_file.truncate()

                        nodes_file.seek(0)
                        json.dump(nodes, nodes_file, indent=2)
                        nodes_file.truncate()

                        return jsonify({'message': 'Text edited successfully'}), 200
                    else:
                        return jsonify({'message': 'Text not found'}), 404

        except Exception as e:
            return jsonify({'message': str(e)}), 500