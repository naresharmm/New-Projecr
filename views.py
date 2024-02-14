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
user_controller = UserController()
data_controller = DataController()


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if not session.get("phone_number", None):
            return redirect(url_for('home'))
        return view(**kwargs)
    return wrapped_view


@app.route('/')
def home():
    countries = get_countries()
    return render_template('home.html', countries=countries)

@app.route('/profile')
@login_required
def profile():
    """
    Render the user's profile page.
    """
    user_phone = session.get("phone_number")
    nodes = {}

    if user_phone:
        with open('data/users.json', 'r', encoding='utf-8') as users_file:
            users = json.load(users_file)
            user_node_ids = users.get(user_phone, {}).get('node_ids', [])
        with open('data/node.json', 'r', encoding='utf-8') as nodes_file:
            all_nodes = json.load(nodes_file)

        nodes = {node_id: all_nodes.get(node_id) for node_id in user_node_ids if node_id in all_nodes}

    return render_template('profile.html', nodes=nodes)

   
@app.route('/register', methods=['GET'])
def register_form():
    return render_template('registration.html', countries=get_countries())


@app.route('/register', methods=['POST'])
def register():
    if user_controller.register(request.form):
        return redirect(url_for('profile'))
    else:
        return "Data inputted wrong"


@app.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    if user_controller.login(request.form.get('phone_number'), \
        request.form.get('password')):
        return redirect(url_for('profile'))
    else:
        return "Phone number or password is incorrect"


@app.route('/logout', methods=['GET'])
def logout():
    user_controller.logout()
    return redirect(url_for('home'))


@app.route('/save_text', methods=['GET', 'POST'])
def save_text():
    response, status_code = NodesController.save_text(
        json.loads(request.get_data().decode("utf-8")),
        session
    )
    return jsonify(response), status_code


@app.route('/get_saved_texts')
def get_saved_texts():
    response, status_code = NodesController.get_saved_texts(session)
    return jsonify(response), status_code


@app.route('/profile/delete_text/<node_id>', methods = ['GET', 'POST'])
def delete_text(node_id):
    print(node_id)
    response, status_code = DataController.delete_text(node_id, session)
    return jsonify(response), status_code


@app.route('/profile/edit_text/<node_id>', methods=['POST'])  
def edit_text(node_id):
    try:
        response, status_code = \
        DataController.edit_text(request, session, node_id)  
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({'message': str(e)}), 500