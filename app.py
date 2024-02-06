from flask import Flask

from functools import wraps
from countries import get_countries
from text_manager import text_manager 
from UserAuthBlueprint import UserAuthBlueprint
from data_storage import data_storage

app = Flask(__name__) 
app.register_blueprint(UserAuthBlueprint)
app.register_blueprint(text_manager)
app.register_blueprint(data_storage)
app.secret_key = 'your_secret_key_here'

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)