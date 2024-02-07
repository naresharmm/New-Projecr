import json
from flask import Blueprint, request, jsonify, session
text_manager = Blueprint('text_manager', __name__)

class TextManagerRoutes:
    @staticmethod
    @text_manager.route('/profile/edit_text', methods=['POST'])
    def edit_text():
        """
        Edit the title of a text for the current user.
        Returns:
            str: A JSON response indicating whether 
            the text title was edited successfully or an error message.
        """
        data = request.get_json()
        new_text = data.get('new_text')
        
        if not new_text:
            return jsonify({'message': 'New text missing'}), 400

        current_user_phone = session.get("phone_number")
        
        if not current_user_phone:
            return jsonify({'message': 'User not authenticated'}), 401

        try:
            with open('data/users.json', 'r', encoding='utf-8') as users_file, \
                 open('data/node.json', 'r+', encoding='utf-8') as nodes_file:
                
                users = json.load(users_file)
                user_node_ids = users.get(current_user_phone, 
                {}).get("node_ids", [])
                nodes = json.load(nodes_file)

                text_id = next((nid for nid in user_node_ids
                if nodes.get(nid, {}).get("text") == data.get('old_text')), None)

                if text_id:
                    nodes[str(text_id)]["text"] = new_text
                    nodes_file.seek(0)
                    json.dump(nodes, nodes_file, indent=2)
                    nodes_file.truncate()
                    return jsonify({'message':
                     'Text edited successfully'}), 200
                else:
                    return jsonify({'message': 
                    'Text not found for the current user'}), 404

        except Exception as e:
            return jsonify({'message': str(e)}), 500

    @staticmethod
    @text_manager.route('/profile/delete_text', methods=['POST'])
    def delete_text():
        """
        Delete a text by its title.
        Returns:
            str: A JSON response indicating whether
            the text was deleted successfully or an error message.
        """
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



# @staticmethod
# @text_manager.route('/profile/delete_text/<nid>', methods=['POST'])
# def delete_text(nid):
#     """
#     Delete a text by its node ID.
#     Returns:
#         str: A JSON response indicating whether
#         the text was deleted successfully or an error message.
#     """
#     current_user_phone = session.get("phone_number")

#     if not current_user_phone:
#         return jsonify({'message': 'User not authenticated'}), 401

#     try:
#         with open('data/users.json', 'r+', encoding='utf-8') as users_file:
#             users = json.load(users_file)
#             user_node_ids = users.get(current_user_phone, {}).get("node_ids", [])

#             with open('data/node.json', 'r+', encoding='utf-8') as nodes_file:
#                 nodes = json.load(nodes_file)

#                 if nid in user_node_ids and nid in nodes and nodes[nid]["text"] == text_to_delete:
#                     del nodes[nid]
#                     user_node_ids.remove(nid)

#                     nodes_file.seek(0)
#                     json.dump(nodes, nodes_file, indent=2)
#                     nodes_file.truncate()

#                     users_file.seek(0)
#                     json.dump(users, users_file, indent=2)
#                     users_file.truncate()

#                     return jsonify({'message': 'Text deleted successfully'}), 200
#                 else:
#                     return jsonify({'message': 'Text not found'}), 404

#     except Exception as e:
#         return jsonify({'message': str(e)}), 500
