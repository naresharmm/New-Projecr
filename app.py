''' Flask project
'''
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
    user_validator = UserValidator(
        request.form.get('username'),
        request.form.get("phone_number"),
        request.form.get('password'),
        request.form.get('password2'),
        request.form.get("email"),
        request.form.get("country")
    )

    if user_validator.form_filled() and user_validator.valid_phone() \
            and user_validator.valid_email() and \
            user_validator.valid_password() \
            and user_validator.passwords_match():
        return redirect(url_for('profile'))
    else:
        return render_template('registration_failed.html')

@app.route('/save_text', methods=['POST'])

def save_text():
    '''
    Saving the text
    '''
    try:
        text = request.json.get('text')

        if text:
            with open('form.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            data.append(text)

            with open('form.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)

            return jsonify({'message': 'Text saved successfully.'}), 200

        return jsonify({'message': 'Text not provided.'}), 400
    except Exception as e:
        print(f'Error saving text: {e}')
        return jsonify({'message': ' error occurred while saving the text.'}), 500
if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=8080)
