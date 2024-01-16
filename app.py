import re
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


countries = [
    "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda",
    "Argentina", "Armenia", "Australia", "Austria", "Bahamas", "Bahrain",
    "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan",
    "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei",
    "Bulgaria", "Burkina Faso", "Burundi", "Côte d'Ivoire", "Cabo Verde",
    "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile",
    "China", "Colombia", "Comoros", "Congo (Congo-Brazzaville)", "Costa Rica",
    "Croatia", "Cuba", "Cyprus", "Czechia (Czech Republic)",
    "Democratic Republic of the Congo", "Denmark",  
]

@app.route('/')
def home():
    ''' function
    '''
    return render_template('home.html', countries=countries)

@app.route('/profile')
def profile():
    '''function
    '''
    return render_template('profile.html')

@app.route('/register', methods=['GET'])
def register_form():
    ''' function
    '''
    return render_template('register.html', countries=countries)

@app.route('/register', methods=['POST'])
def register():
    ''' function
    '''
    username = request.form.get('username')
    phone_number = request.form.get("phone_number")
    password = request.form.get('password')
    password_sec = request.form.get('password2')
    email = request.form.get("email")
    country = request.form.get("country")
    form_filled = username and password and email and country

    phone_pattern = r'^\+374\d{8}$'
    email_pattern = r'^\w+@[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$'
    password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"

    matches = re.match(phone_pattern, phone_number) and \
        re.match(email_pattern, email) and re.match(password_pattern, password)

    if form_filled and matches and password == password_sec:
        print("You've registered")
        return redirect(url_for('profile'))
    else:
        print("Registration failed")
        return render_template('registration_failed.html')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)
