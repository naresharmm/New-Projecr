from functools import wraps
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    session
)
from countries import get_countries
from delete_blueprint import delete_blueprint
from edit_blueprint import edit_blueprint 
from login_register import login_register
from save_get import save_get

app = Flask(__name__) 
app.register_blueprint(login_register)
app.register_blueprint(edit_blueprint)
app.register_blueprint(delete_blueprint)
app.register_blueprint(save_get)
app.secret_key = 'your_secret_key_here'

def login_required(view):
    """
    Decorator to check if the user is logged in before accessing a view.

    Args:
        view (function): The view function to be wrapped.

    Returns:
        function: The wrapped view function.
    """
    @wraps(view)
    def wrapped_view(**kwargs):
        if not session.get("phone_number", None):
            return redirect(url_for('home'))
        return view(**kwargs)
    return wrapped_view


@app.route('/')
def home():
    """
    Render the home page.

    Returns:
        str: The rendered HTML content of the home page.
    """
    countries: list[str] = get_countries()
    if session.get("phone_number"):
        login_status = "Logged in as: " + session["phone_number"]
    else:
        login_status = "Not logged in"
    
    return render_template('home.html', countries=countries, login_status=login_status)

@app.route('/profile')
@login_required
def profile():
    """
    Render the user's profile page.
    """
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)