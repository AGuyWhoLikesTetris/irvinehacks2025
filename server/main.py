import flask
import json
import sqlite3
import api
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)

import courses, friends, users

app.register_blueprint(courses.bp)
app.register_blueprint(friends.bp)
app.register_blueprint(users.bp)

def init_db():
    connection = sqlite3.connect('database.db')
    c = connection.cursor()

    # student table
    c.execute('''CREATE TABLE IF NOT EXISTS student(
        id TEXT NOT NULL PRIMARY KEY,
        name TEXT,
        major TEXT,
        grade INTEGER
         ) STRICT;''')

    # enrollment table 
    c.execute('''CREATE TABLE IF NOT EXISTS enrollment(
        id TEXT NOT NULL,
        section_code INTEGER NOT NULL,
        PRIMARY KEY (id, section_code),
        FOREIGN KEY (id) REFERENCES student(id)
         ) STRICT;''')

    # friend table 
    c.execute('''CREATE TABLE IF NOT EXISTS friend(
        id TEXT NOT NULL,
        friend_id TEXT NOT NULL,
        PRIMARY KEY (id, friend_id),
        FOREIGN KEY (id) REFERENCES student(id)
        FOREIGN KEY (friend_id) REFERENCES student(id)
         ) STRICT;''')

    # friend_requests table 
    c.execute('''CREATE TABLE IF NOT EXISTS friend_request(
        id TEXT NOT NULL,
        friend_id TEXT NOT NULL,
        PRIMARY KEY (id, friend_id),
        FOREIGN KEY (id) REFERENCES student(id)
        FOREIGN KEY (friend_id) REFERENCES student(id)
         ) STRICT;''')

    connection.commit()
    connection.close()

@app.route('/')
@cross.origin()
def index():
    conn = sqlite3.connect('database.db')
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM student")
        users = c.fetchall()
    except sqlite3.DatabaseError as e:
        print(f"Error: {e}")
        return f"Failed to fetch users due to a database error: {e}."
    finally:
        conn.close()
    return users

if __name__ == "__main__":
    init_db()
    app.run(port=8000, debug=True)

