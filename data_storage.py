import json
import uuid
from functools import wraps
from datetime import datetime

from flask import (
    Blueprint,
    jsonify,
    request,
    session,
    redirect,
    url_for,
    render_template,
)

from countries import get_countries

data_storage = Blueprint('data_storage', __name__)

class DataStorageRoutes:
    @staticmethod
    def login_required(view):
        """
        Decorator to check if the user is logged in before accessing a view.

        Args:
            view (function): The view function to be wrapped.

        Returns:
            function: The wrapped view function.
        """
        @wraps(view)
        def wrapped_view(**kwargs):
            if not session.get("phone_number", None):
                return redirect(url_for('home'))
            return view(**kwargs)
        return wrapped_view

    @staticmethod
    @data_storage.route('/')
    def home():
        """
        Render the home page.

        Returns:
            str: The rendered HTML content of the home page.
        """
        countries: list[str] = get_countries()
        if session.get("phone_number"):
            login_status = "Logged in as: " + session["phone_number"]
        else:
            login_status = "Not logged in"
        return render_template('home.html', countries=countries, login_status=login_status)

    @staticmethod
    @data_storage.route('/profile')
    @login_required
    def profile():
        """
        Render the user's profile page.
        """
        return render_template('profile.html')

    @staticmethod
    @data_storage.route('/save_text', methods=['GET', 'POST'])
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

    @staticmethod
    @data_storage.route('/get_saved_texts')
    def get_saved_texts():
        user_phone = session.get("phone_number")
        with open('data/users.json', 'r', encoding='utf-8') as users_file:
            users = json.load(users_file)
            user_node_ids = users[user_phone]['node_ids']

        with open('data/node.json', 'r', encoding='utf-8') as nodes_file:
            nodes = json.load(nodes_file)
            user_texts = [nodes[node_id]["text"] for node_id in user_node_ids if node_id in nodes]

        return jsonify({'texts': user_texts}), 200
