import json
from flask import jsonify

class DataController:
    def __init__(self, session, request):
        self.session = session
        self.request = request

    def delete_text(self, node_id):
        try:
            user_phone = self.session.get("phone_number")
            if not user_phone:
                return {'message': 'User not authenticated'}, 401
            
            with open('data/node.json', 'r+') as nodes_file:
                nodes = json.load(nodes_file)
                if node_id not in nodes:
                    return {'message': 'Node ID not found'}, 404
                
                del nodes[node_id]
                nodes_file.seek(0)
                json.dump(nodes, nodes_file, indent=2)
                nodes_file.truncate()
            
            with open('data/users.json', 'r+') as users_file:
                users = json.load(users_file)
                if user_phone not in users or 'node_ids' not in users[user_phone]:
                    return {'message': 'User node IDs not found'}, 404
                
                user_node_ids = users[user_phone]['node_ids']
                if node_id in user_node_ids:
                    user_node_ids.remove(node_id)
                
                users_file.seek(0)
                json.dump(users, users_file, indent=2)
                users_file.truncate()
                
            return {'message': 'Text deleted successfully'}, 200

        except Exception as e:
            return {'message': str(e)}, 500

    def edit_text(self, node_id, request):
        data = self.request.get_json()
        new_text = data.get('new_text')

        if not new_text:
            return {'message': 'New text not provided'}, 400

        user_phone = self.session.get("phone_number")
        if not user_phone:
            return {'message': 'User not authenticated'}, 401

        try:
            with open('data/users.json', 'r+') as users_file:
                users = json.load(users_file)
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

                        return {'message': 'Text edited successfully'}, 200
                    else:
                        return {'message': 'Text not found'}, 404

        except Exception as e:
            return {'message': str(e)}, 500