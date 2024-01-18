''' flask project
'''

from flask import Flask, render_template, request, redirect, url_for

from user import UserValidator

from countries import get_countries


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/')
def home():
    '''
    function'''
    countries = get_countries()
    return render_template('home.html', countries = countries)

@app.route('/profile')
def profile():
    '''function
    '''
    return render_template('profile.html')

@app.route('/register', methods=['GET'])
def register_form():
    '''function
    '''
    return render_template('register.html', countries = get_countries)
@app.route('/register', methods=['POST'])
def register():
    '''function
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

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=8080)