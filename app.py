import json
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


@app.route('/')
def home():
    countries = get_countries()
    return render_template('home.html', countries=countries)


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/register', methods=['GET'])
def register_form():
    return render_template('register.html', countries=get_countries())


@app.route('/registration-failed')
def registration_failed():
    return render_template('registration_failed.html')


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


@app.route('/save_text', methods=['POST'])
def save_text():
    print("hi")
    with open('data/node.json', 'r+', encoding='utf-8') as file:
        nodes = json.load(file)
        file.seek(0)

        user_phone = session.get("phone_number", "123456789")

        text = request.form.get('text')
        title = request.form.get('title')
        if text and title:
            text_uuid = str(uuid.uuid4())

            nodes[text_uuid] = {
                "text": text,
                "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "title": title
            }
            print("hi")
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
        print("Yes")
        with open('data/node.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return jsonify({'texts': data}), 200
    except Exception as e:
        print(f'Error fetching saved texts: {e}')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)
