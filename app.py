import json
from functools import wraps
from datetime import datetime
import uuid
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    session
)
from user import UserValidator
from countries import get_countries
from cryptography.fernet import Fernet

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

key = Fernet.generate_key()
cipher_suite = Fernet(b'DHML65d-nY3iZL1vsWkrmzf2kSfoHQ9Fnv6IWlyIPzQ=')

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

@app.route('/')
def home():
    """
    Render the home page.

    Returns:
        str: The rendered HTML content of the home page.
    """
    countries: list[str] = get_countries()
    return render_template('home.html', countries=countries)

@app.route('/profile')
@login_required
def profile():
    """
    Render the user's profile page.
    """
    return render_template('profile.html')

@app.route('/register', methods=['GET'])
def register_form():
    """
    Render the registration form.

    Returns:
        str: The rendered HTML content of the registration form.
    """
    return render_template('registration.html', countries=get_countries())

@app.route('/register', methods=['POST'])
def register():
    """
    Register a new user.

    Returns:
        str: A redirection to the user's profile page if registration is successful, otherwise an error message.
    """
    password_form = request.form.get("password")
    encrypted_password = cipher_suite.encrypt(password_form.encode()).decode()
    if UserValidator.validate_registration(request.form):
        with open('data/users.json', 'r+', encoding='utf-8') as file:
            users: dict = json.load(file)
            file.seek(0)
            file.truncate()
            user_phone: str = request.form.get("phone_number")
            session["phone_number"] = user_phone
            users[user_phone] = {
                "email": request.form.get('email'),
                "password": encrypted_password,
                "node_ids": []
            }
            json.dump(users, file, indent=2)
        return redirect(url_for('profile'))
    else:
        return "Data inputted wrong"

@app.route('/login', methods=['GET'])
def login_form():
    """
    Render the login form.

    Returns:
        str: The rendered HTML content of the login form.
    """
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    """
    Log in an existing user.

    Returns:
        str: A redirection to the user's profile page if login is successful, otherwise an error message.
    """
    phone_number: str = request.form.get('phone_number')
    password: str = request.form.get('password')
    with open('data/users.json', 'r', encoding='utf-8') as file:
        users: dict = json.load(file)

    dec_password = cipher_suite.decrypt(users[phone_number]["password"]).decode()
    if phone_number in users and dec_password == password:
        session["phone_number"] = phone_number
        return redirect(url_for('profile'))
    else:
        return "Phone number or password is incorrect"

@app.route('/save_text', methods=['GET', 'POST'])
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

    # Read and update nodes
    with open('data/node.json', 'r', encoding='utf-8') as file:
        nodes = json.load(file)

    nodes[text_uuid] = {
        "title": title,
        "text": text,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Write updated nodes back to file
    with open('data/node.json', 'w', encoding='utf-8') as file:
        json.dump(nodes, file, indent=2)

    # Read and update users
    with open('data/users.json', 'r', encoding='utf-8') as file:
        users = json.load(file)

    users[user_phone]['node_ids'].append(text_uuid)

    # Write updated users back to file
    with open('data/users.json', 'w', encoding='utf-8') as file:
        json.dump(users, file, indent=2)

    return jsonify({'message': 'Text saved successfully', 'uuid': text_uuid}), 200


@app.route('/get_saved_texts')
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
        user_texts = [nodes[node_id] for node_id in user_node_ids if node_id in nodes]

    return jsonify({'texts': [text["title"] for text in user_texts]}), 200



@app.route('/profile/delete_text', methods=['POST'])
def delete_text():
    """
    Delete a text by its title.

    Returns:
        str: A JSON response indicating whether the text was deleted successfully or an error message.
    """
    data: dict = request.get_json()
    title: str = data.get('title')
    if not title:
        return jsonify({'message': 'No title provided'}), 400

    current_user_phone: str = session.get("phone_number")
    if not current_user_phone:
        return jsonify({'message': 'User not authenticated'}), 401

    try:
        with open('data/users.json', 'r+', encoding='utf-8') as users_file:
            users = json.load(users_file)
            user_node_ids = users[current_user_phone]["node_ids"]

        with open('data/node.json', 'r+', encoding='utf-8') as nodes_file:
            nodes = json.load(nodes_file)
            text_id = next((nid for nid in user_node_ids if nodes[nid]["title"] == title), None)

            if text_id:
                del nodes[text_id]
                users_file.seek(0)
                json.dump(users, users_file, indent=2)
                users_file.truncate()

                nodes_file.seek(0)
                json.dump(nodes, nodes_file, indent=2)
                nodes_file.truncate()

                users[current_user_phone]["node_ids"].remove(text_id)
                return jsonify({'message': 'Text deleted successfully'}), 200
            else:
                return jsonify({'message': 'Text not found'}), 404

    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/profile/edit_text', methods=['POST'])
def edit_text():
    """
    Edit the title of a text for the current user.

    Returns:
        str: A JSON response indicating whether the text title was edited successfully or an error message.
    """
    data: dict = request.get_json()
    old_title: str = data.get('old_title')
    new_title: str = data.get('new_title')
    if not old_title or not new_title:
        return jsonify({'message': 'Title missing'}), 400

    current_user_phone: str = session.get("phone_number")
    if not current_user_phone:
        return jsonify({'message': 'User not authenticated'}), 401

    try:
        with open('data/users.json', 'r', encoding='utf-8') as users_file:
            users = json.load(users_file)
            user_node_ids = users[current_user_phone]["node_ids"]

        with open('data/node.json', 'r+', encoding='utf-8') as nodes_file:
            nodes = json.load(nodes_file)
            text_id = next((nid for nid in user_node_ids if nodes[nid]["title"] == old_title), None)

            if text_id:
                nodes[text_id]["title"] = new_title
                nodes_file.seek(0)
                json.dump(nodes, nodes_file, indent=2)
                nodes_file.truncate()
                return jsonify({'message': 'Text edited successfully'}), 200
            else:
                return jsonify({'message': 'Text not found'}), 404

    except Exception as e:
        return jsonify({'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)