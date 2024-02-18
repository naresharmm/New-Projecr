import json
from functools import wraps

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    session
)


from nodes import NodesController
from countries import get_countries
from data_storage import DataController
from user_controller import UserController

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

data_controller = DataController(session, request)
user_controller = UserController(session, request)


def login_required(view):
    """
    Decorator to ensure that a user is logged in before accessing a view.

    Redirects to the home page if the user is not logged in.

    Parameters
    ------------------------
        view (function): The view function to be decorated.

    Returns
    ------------------------
        function: The wrapped view function.
    """
    @wraps(view)
    def wrapped_view(**kwargs):
        if not session.get("phone_number", None):
            return redirect(url_for('home'))
        return view(**kwargs)
    return wrapped_view

@app.route('/')
def home() -> str:
    """
    Render the home page.

    Returns:
        str: Rendered HTML content for the home page.
    """
    countries = get_countries()
    return render_template('home.html', countries=countries)

@app.route('/profile')
@login_required
def profile() -> str:
    """
    Render the user profile page.

    Returns
    ------------------------
        str: 
        Rendered HTML content for the user profile page.
    """
    if session.get("phone_number"):
        nodes = {}
        with open('data/users.json',encoding="utf-8") as users_file:
            for node_id in json.load(users_file).\
            get(session.get("phone_number"), {}).get('node_ids', []):

                with open('data/node.json',encoding="utf-8") as node_file:
                    node_data = json.load(node_file)

                    if node_id in node_data:
                        nodes[node_id] = node_data[node_id]
        return render_template('profile.html', nodes=nodes)


@app.route('/register', methods=['GET'])
def register_form() -> str:
    """
    Render the registration form.

    Returns
    ------------------------
        str
        Rendered HTML content for the registration form.
    """
    return render_template('registration.html', \
    countries=get_countries())

@app.route('/register', methods=['POST'])
def register() -> str:
    """
    Handle user registration form submission.

    Returns
    ------------------------
        str: Either redirects to the profile page 
        upon successful registration or displays an error message.
    """
    if user_controller.register(request.form):
        return redirect(url_for('profile'))
    else:
        return "Data inputted wrong"

@app.route('/login', methods=['GET'])
def login_form() -> str:
    """
    Render the login form.

    Returns
    ------------------------
        str: Rendered HTML content for the login form.
    """
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login() -> str:
    """
    Handle user login form submission.

    Returns
    ------------------------
        str:
        Either redirects to the profile page
        or sdisplays an error message.
    """
    if user_controller.login(request.form.get('phone_number'),\
     request.form.get('password')):
        return redirect(url_for('profile'))
    else:
        return "Phone number or password is incorrect"

@app.route('/logout', methods=['GET'])
def logout() -> str:
    """
    Handle user logout.

    Returns
    ------------------------
        str: Redirects to the home page after logging out.
    """
    user_controller.logout()
    return redirect(url_for('home'))

@app.route('/save_text', methods=['POST'])
def save_text() -> str:
    """
    Save text data.

    Returns
    ------------------------
        str: JSON response indicating success or failure.
    """
    request_data = request.get_json()
    response, status_code = NodesController().save_text(
        text_data=request_data,
        session=session
    )
    return jsonify(response), status_code

@app.route('/get_saved_texts')
def get_saved_texts() -> str:
    """
    Get saved text data.

    Returns
    ------------------------
        str: JSON response containing saved text data.
    """
    response, status_code = NodesController.get_saved_texts(session)
    return jsonify(response), status_code

@app.route('/profile/delete_text/<node_id>', methods=['GET', 'POST'])
def delete_text(node_id: str) -> str:
    """
    Delete text data.

    Parameters
    ------------------------
        node_id (str): The ID of the text node to delete.

    Returns
    ------------------------
        str:
        JSON response indicating success or failure.
    """
    response, status_code = data_controller.delete_text(node_id)
    return jsonify(response), status_code

@app.route('/profile/edit_text/<node_id>', methods=['POST'])
def edit_text(node_id: str) -> str:
    """
    Edit text data.

    Parameters
    ------------------------
        node_id (str): 
        The ID of the text node to edit.

    Returns
    ------------------------
        str: 
        JSON response indicating success or failure.
    """
    response, status_code = data_controller.edit_text(node_id, request)
    return jsonify(response), status_code
