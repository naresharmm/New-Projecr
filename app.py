from views import app
#WORKING FILE
import create_db
create_db.create_tables()

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)
