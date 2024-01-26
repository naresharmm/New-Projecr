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

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

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
    return render_template('profile.html')


@app.route('/register', methods=['GET'])
def register_form():
    return render_template('register.html', countries=get_countries())



@app.route('/register', methods=['POST'])
def register():
    if UserValidator.validate_registration(request.form):
        with open('data/users.json', 'r+', encoding='utf-8') as file:
            users = json.load(file)
            file.seek(0)
            file.truncate()
            user_phone = request.form.get("phone_number")
            session["phone_number"] = user_phone
            users[user_phone] = {
                "email": request.form.get('email'),
                "password": request.form.get('password'),
                "node_ids": []
            }
            json.dump(users, file, indent=2)
        return redirect(url_for('profile'))
    else:
        return "Data inputted wrong"


@app.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    phone_number = request.form.get('phone_number')
    password = request.form.get('password')
    print(phone_number)
    print(password)

    if (phone_number, password):
        session['phone_number'] = phone_number
        return redirect(url_for('profile'))
    else:
        return "Login failed. Invalid credentials."


@app.route('/save_text', methods=['GET', 'POST'])
def save_text():
    with open('data/node.json', 'r+', encoding='utf-8') as file:
        nodes = json.load(file)
        file.seek(0)

        user_phone = session.get("phone_number")
        request_data = json.loads(request.get_data().decode("utf-8"))
        text = request_data.get("text")
        title = request_data.get("title")
        if text and title:
            text_uuid = str(uuid.uuid4())

            nodes[text_uuid] = {
                "title": title,
                "text": text,
                "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user_phone": user_phone
            }
            json.dump(nodes, file, indent=2)

    with open('data/users.json', 'r+', encoding='utf-8') as file:
        users = json.load(file)

        file.seek(0)

        users[user_phone]['node_ids'].append(text_uuid)

        json.dump(users, file, indent=2)

    return jsonify(
        {'message': 'Text saved successfully', 'uuid': text_uuid}
    ), 200
    # except Exception as e:
    #     print(f'Error saving text: {e}')
    #     return jsonify({'error': str(e)}), 500


@app.route('/get_saved_texts')
def get_saved_texts():
    try:
        print(777777777777777)
        with open('data/node.json', 'r', encoding='utf-8') as file:
            nodes = json.load(file)
        print(4444444444444444444)
        show_list = [
            nodes[key]["title"] for key in nodes if nodes[key]["user_phone"] \
                    == session.get("phone_number")
        ]
        print(8888888888888888888888)
        return jsonify({'texts': show_list}), 200
    except Exception as e:
        print(f'Error fetching saved texts: {e}')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)
