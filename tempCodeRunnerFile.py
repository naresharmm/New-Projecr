''' Flask project
'''
import uuid 
from datetime import datetime
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for

from user import UserValidator

from countries import get_countries


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/')
def home():
    '''
    Renders the home page with a list of countries.
    '''
    countries = get_countries()
    return render_template('home.html', countries = countries)

@app.route('/profile')
def profile():
    '''
    Returns a rendered HTML displaying profile page
    '''
    return render_template('profile.html')

@app.route('/register', methods=['GET'])
def register_form():
    '''
    Returns a rendered HTML template displaying the registration form.
    '''
    return render_template('register.html', countries = get_countries)

@app.route('/registration-failed')
def registration_failed():
    ''' 
    Renders the page of registration failure.
    
    '''
    return render_template('registration_failed.html')

@app.route('/register', methods=['POST'])
def register():
    '''
    Handles user registration based on form input
    '''
    if UserValidator.validate_registration(request.form):
        uui = str(uuid.uuid4())
        user_data = {
            "email": request.form.get('email'),
            "password": request.form.get('password'),  # You might want to hash this
            "node_ids": []
        }

        #Programm loading existing users
        with open('users.json', 'r', encoding='utf-8') as file:
            users = json.load(file)
        users[request.form.get("phone_number")] = user_data
        with open('users.json', 'w', encoding='utf-8') as file:
            json.dump(users, file, ensure_ascii=False, indent=2)

        return redirect(url_for('profile'))
    else:
        return render_template('registration_failed.html')
    

@app.route('/save_text', methods=['POST'])
def save_text():
    try:
        text = request.json.get('text')
        title = request.json.get('title')

        if text and title:
            text_uuid = str(uuid.uuid4())  # generating uuid for each text
            text_data = {
                "text": text,
                "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "title": title
            }

            with open('node.json', 'r', encoding='utf-8') as file:
                nodes = json.load(file)

            nodes[text_uuid] = text_data  # Use text's UUID as key

            with open('node.json', 'w', encoding='utf-8') as file:
                json.dump(nodes, file, ensure_ascii=False, indent=2)

            return jsonify({'message': 'Text saved successfully', 'uuid': text_uuid}), 200

    except Exception as e:
        print(f'Error saving text: {e}')
        return jsonify({'error': str(e)}), 500


@app.route('/get_saved_texts')
def get_saved_texts():
    try:
        with open('node.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return jsonify({'texts': data}), 200
    except Exception as e:
        print(f'Error fetching saved texts: {e}')

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=8080)
