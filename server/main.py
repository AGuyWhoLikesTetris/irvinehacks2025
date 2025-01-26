import flask
import json
import sqlite3
import api
from flask_cors import CORS, cross_origin

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
        course_name TEXT NOT NULL,
        start_time_hour INTEGER NOT NULL,
        start_time_minute INTEGER NOT NULL,
        end_time_hour INTEGER NOT NULL,
        end_time_minute INTEGER NOT NULL,
        days TEXT NOT NULL,
        course_type TEXT NOT NULL,
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
@cross_origin()
def index():
    return 'Use the endpoints /add/user, /delete/user, /view/user, /add/courses, /delete/courses, /add/friend, /delete/friend, /students_with_same_course'

if __name__ == "__main__":
    init_db()
    app.run(port=8000, debug=True)

