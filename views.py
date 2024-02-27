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

@app.route('/')
def home() -> str:
    countries = get_countries()
    return render_template('home.html', countries=countries)

@app.route('/profile')
def profile() -> str:
    user_controller = UserController() 
    nodes = user_controller.get_profile(session)
    return render_template('profile.html', nodes=nodes)

@app.route('/register', methods=['GET'])
def register_form() -> str:
    return render_template('registration.html', countries=get_countries())

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_controller = UserController() 
        if user_controller.register(request.form, session):
            return redirect(url_for('profile'))
        else:
            error_message = "Passwords don't match. Please try again."
            return render_template('registration.html', error_message=error_message)

@app.route('/login', methods=['GET'])
def login_form() -> str:
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login() -> str:
    user_controller = UserController() 
    if user_controller.login(\
        request.form.get('phone_number'),
        request.form.get('password'), session):
        return redirect(url_for('profile'))
    else:
        error_message =\
        "The phone number or password is incorrect.\
         Please double-check your credentials"
        return render_template('login.html', error_message=error_message)


@app.route('/logout', methods=['GET'])
def logout() -> str:
    session.clear()
    return redirect(url_for('home'))

@app.route('/save_text', methods=['POST'])
def save_text() -> str:
    request_data = request.get_json()
    response = NodesController().save_text(\
        text_data=request_data,
        session=session)
    return jsonify(response)

@app.route('/profile/delete_text/<node_id>', methods=['GET', 'POST'])
def delete_text(node_id: str) -> str:
    data_controller = DataController() 
    response = data_controller.delete_text(node_id, session)
    return jsonify(response)


@app.route('/profile/edit_text/<node_id>', methods=['POST'])
def edit_text(node_id: str) -> str:
    data_controller = DataController() 
    response = data_controller.edit_text(
        node_id,
        request.json.get('new_text'),
        session
    )
    return jsonify(response)