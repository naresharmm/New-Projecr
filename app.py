import json
import uuid
from functools import wraps
from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    session
)
from cryptography.fernet import Fernet

from user import UserValidator
from countries import get_countries

key = Fernet.generate_key()
cipher_suite = Fernet(key)

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        """Check if the user is logged in before accessing a view."""
        if not session.get("phone_number", None):
            return redirect(url_for('home'))

        return view(**kwargs)

    return wrapped_view
@app.route('/home')
def home():
    """Render the home page.

    Returns:
        str: The rendered HTML content of the home page.
    """
    countries: list[str] = get_countries()
    return render_template('home.html', countries=countries)

@app.route('/profile')
@login_required
def profile():
    """Render the user's profile page.

    Returns:
        str: The rendered HTML content of the user's profile page.
    """
    return render_template('profile.html')

@app.route('/register', methods=['GET'])
def register_form():
    """Render the registration form.

    Returns:
        str: The rendered HTML content of the registration form.
    """
    return render_template('registration.html', countries=get_countries())

@app.route('/register', methods=['POST'])
def register():
    """Register a new user.

    Returns:
        str: A redirection to the user's profile page if registration is successful, or an error message if registration fails.
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

def decrypt_password(encrypted_password):
    cipher_suite = Fernet(key)
    decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
    return decrypted_password

@app.route('/login', methods=['GET'])
def login_form():
    """Render the login form.

    Returns:
        str: The rendered HTML content of the login form.
    """
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    """Log in an existing user.

    Returns:
        str: A redirection to the user's profile page if login is successful, or an error message if login fails.
    """
    phone_number: str = request.form.get('phone_number')
    provided_password: str = request.form.get('password')
    
    with open('data/users.json', 'r', encoding='utf-8') as file:
        users: dict = json.load(file)
        
    if phone_number in users:
        encrypted_password = users[phone_number]["password"]
        decrypted_password = decrypt_password(encrypted_password)

        if provided_password == decrypted_password:
            session["phone_number"] = phone_number
            return redirect(url_for('profile'))

    return "Phone number or password is incorrect"

@app.route('/save_text', methods=['GET', 'POST'])
def save_text():
    """Save a text provided by the user.

    Returns:
        str: A JSON response indicating whether the text was saved successfully or an error message.
    """
    with open('data/node.json', 'r+', encoding='utf-8') as file:
        nodes: dict = json.load(file)
        file.seek(0)

        user_phone: str = session.get("phone_number")
        request_data: dict = json.loads(request.get_data().decode("utf-8"))
        text: str = request_data.get("text")
        title: str = request_data.get("title")
        if text and title:
            text_uuid: str = str(uuid.uuid4())
            nodes[text_uuid] = {
                "title": title,
                "text": text,
                "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user_phone": user_phone
            }
            json.dump(nodes, file, indent=2)

    with open('data/users.json', 'r+', encoding='utf-8') as file:
        users: dict = json.load(file)

        file.seek(0)

        users[user_phone]['node_ids'].append(text_uuid)

        json.dump(users, file, indent=2)

    return jsonify(
        {'message': 'Text saved successfully', 'uuid': text_uuid}
    ), 200

@app.route('/get_saved_texts')
def get_saved_texts():
    """Return the saved texts for the current user.

    Returns:
        str: A JSON response containing the saved texts for the current user or an error message.
    """
    try:
        with open('data/node.json', 'r', encoding='utf-8') as file:
            nodes: dict = json.load(file)
        show_list: list[str] = [
            nodes[key]["title"] for key in nodes if nodes[key]["user_phone"] \
                    == session.get("phone_number")
        ]
        return jsonify({'texts': show_list}), 200
    except Exception as e:
        print(f'Error fetching saved texts: {e}')

@app.route('/profile/delete_text', methods=['POST'])
def delete_text():
    """Delete a text by its title.

    Returns:
        str: A JSON response indicating whether the text was deleted successfully or an error message.
    """
    data: dict = request.get_json()
    print("Received data:", data)  
    title: str = data.get('title')  

    if not title:
        return jsonify({'message': 'No title provided'}), 400

    current_user_phone: str = session.get("phone_number")
    if not current_user_phone:
        return jsonify({'message': 'User not authenticated'}), 401

    try:
        with open('data/node.json', 'r+') as file:
            nodes: dict = json.load(file)

            text_id: str = None
            for node_id, node in nodes.items():
                if node.get("user_phone") == current_user_phone and node.get("title") == title:
                    text_id = node_id
                    break

            if text_id:
                del nodes[text_id]

                file.seek(0)
                file.truncate()
                json.dump(nodes, file, indent=2)

        with open('data/users.json', 'r+') as file2:
            users: dict = json.load(file2)
            if current_user_phone in users:
                users[current_user_phone]["node_ids"].remove(text_id)
                file2.seek(0)
                file2.truncate()
                json.dump(users, file2, indent=2)

        return jsonify({'message': 'Text deleted successfully'}), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/profile/edit_text', methods=['POST'])
def edit_text():
    """Edit the title of a text for the current user.

    Returns:
        str: A JSON response indicating whether the text title was edited successfully or an error message.
    """
    data: dict = request.get_json()
    print("Received data:", data)  
    old_title: str = data.get('old_title')
    new_title: str = data.get('new_title')

    if not old_title or not new_title:
        return jsonify({'message': 'Title missing'}), 400

    current_user_phone: str = session.get("phone_number")
    if not current_user_phone:
        return jsonify({'message': 'User not authenticated'}), 401

    try:
        with open('data/node.json', 'r+') as file:
            nodes: dict = json.load(file)

            text_id: str = None
            for node_id, node in nodes.items():
                if node.get("user_phone") == current_user_phone and node.get("title") == old_title:
                    text_id = node_id
                    node["title"] = new_title
                    break

            if text_id is None:
                return jsonify({'message': 'Text not found'}), 404

            file.seek(0)
            file.truncate()
            json.dump(nodes, file, indent=2)

        return jsonify({'message': 'Text edited successfully'}), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)
