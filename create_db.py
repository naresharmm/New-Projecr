import sqlite3
conn = sqlite3.connect('app.db')
cursor = conn.cursor()
def create_tables():


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            node_ids TEXT
        )
    ''')

    conn.commit()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nodes (
            node_id TEXT PRIMARY KEY,
            text TEXT NOT NULL,
            title TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
