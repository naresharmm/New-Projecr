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

@app.route('/')
def home() -> str:
    countries = get_countries()
    return render_template('home.html', countries=countries)

@app.route('/profile')
def profile() -> str:
    nodes = user_controller.get_profile(session)
    return render_template('profile.html', nodes=nodes)

@app.route('/register', methods=['GET'])
def register_form() -> str:
    return render_template('registration.html', countries=get_countries())

@app.route('/register', methods=['POST'])
def register() -> str:
    if user_controller.register(request.form, session):
        return redirect(url_for('profile'))
    else:
        return "Data inputted wrong"

@app.route('/login', methods=['GET'])
def login_form() -> str:
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login() -> str:
    if user_controller.login(request.form.get('phone_number'), request.form.get('password'), session):
        return redirect(url_for('profile'))
    else:
        return "Phone number or password is incorrect"

@app.route('/logout', methods=['GET'])
def logout() -> str:
    session.clear()
    return redirect(url_for('home'))

@app.route('/save_text', methods=['POST'])
def save_text() -> str:
    data_controller = DataController(session, request)
    request_data = request.get_json()
    response, status_code = NodesController().save_text(text_data=request_data, session=session)
    return jsonify(response), status_code

@app.route('/get_saved_texts')
def get_saved_texts() -> str:
    data_controller = DataController(session, request)
    response, status_code = NodesController.get_saved_texts(session)
    return jsonify(response), status_code

@app.route('/profile/delete_text/<node_id>', methods=['GET', 'POST'])
def delete_text(node_id: str) -> str:
    data_controller = DataController(session, request)
    response, status_code = data_controller.delete_text(node_id)
    return jsonify(response), status_code

@app.route('/profile/edit_text/<node_id>', methods=['POST'])
def edit_text(node_id: str) -> str:
    data_controller = DataController(session, request)
    response, status_code = data_controller.edit_text(node_id)
    return jsonify(response), status_code
