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
    if UserValidator.validate_registration(request.form): 
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
    except Exception as e:
        print(f'Error saving text: {e}')

@app.route('/get_saved_texts')
def get_saved_texts():
    try:
        with open('form.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return jsonify({'texts': data}), 200
    except Exception as e:
        print(f'Error fetching saved texts: {e}')

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=8080)
