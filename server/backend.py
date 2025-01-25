import flask
import json
import requests
import sqlite3

app = flask.Flask(__name__)

def init_db():
    connection = sqlite3.connect('database.db')
    c = connection.cursor()

    # student table
    c.execute('''CREATE TABLE IF NOT EXISTS student(
        id INTEGER NOT NULL PRIMARY KEY,
        name TEXT,
        degree TEXT,
        grade INTEGER
         ) STRICT;''')

    # enrollment table 
    c.execute('''CREATE TABLE IF NOT EXISTS enrollment(
        id INTEGER NOT NULL,
        course_id TEXT NOT NULL,
        PRIMARY KEY (id, course_id),
        FOREIGN KEY (id) REFERENCES student(id)
         ) STRICT;''')

    # friend table 
    c.execute('''CREATE TABLE IF NOT EXISTS friend(
        id INTEGER NOT NULL,
        friend_id TEXT NOT NULL,
        PRIMARY KEY (id, friend_id),
        FOREIGN KEY (id) REFERENCES student(id)
        FOREIGN KEY (friend_id) REFERENCES student(id)
         ) STRICT;''')

    # friend_requests table 
    c.execute('''CREATE TABLE IF NOT EXISTS friend_request(
        id INTEGER NOT NULL,
        friend_id TEXT NOT NULL,
        PRIMARY KEY (id, friend_id),
        FOREIGN KEY (id) REFERENCES student(id)
        FOREIGN KEY (friend_id) REFERENCES student(id)
         ) STRICT;''')

    connection.commit()
    connection.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM student")
    users = c.fetchall()
    conn.close()
    return users

@app.route('/add/user', methods=['POST'])
def add_user():
    '''Requires id, name, degree, grade in json data'''
    content = flask.request.json
    id = content['id']
    name = content['name']
    degree = content['degree']
    grade = content['grade']
    if name:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO student (id, name, degree, grade) \
                    VALUES (?, ?, ?, ?)", (id, name, degree, grade))
        conn.commit()
        conn.close()
    return flask.redirect(flask.url_for('index'))

@app.route('/delete')
def delete_user(id):
    '''Requires id in the form of a query param'''
    id = flask.request.args.get('id', '')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM student WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return flask.redirect(flask.url_for('index'))

@app.route('/view')
def view():
    '''Requires id in the form of a query param'''
    id = flask.request.args.get('id', '')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM student WHERE id=?", (id,))
    user = c.fetchone()
    c.execute("SELECT course_id FROM enrollment WHERE id=?", (id,))
    courses = c.fetchall()
    courses_flat = [i[0] for i in courses]
    c.execute("SELECT friend_id FROM friend WHERE id=?", (id,))
    friends = c.fetchall()
    friends_flat = [int(i[0]) for i in friends]
    conn.close()
    rtn_obj = {'id': user[0], 'name': user[1], 'degree': user[2], 'grade': user[3], 'courses': courses_flat, 'friends': friends_flat}
    return rtn_obj

@app.route('/add/classes', methods=['POST'])
def add_classes():
    '''Requires id in query param and a list of classes in json data'''
    content = flask.request.json
    id = flask.request.args.get('id', '')
    classes = content['classes']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    print(classes)
    for course_id in classes:
        print(course_id)
        c.execute("INSERT INTO enrollment (id, course_id) \
                    VALUES (?, ?)", (id, course_id))
    conn.commit()
    conn.close()
    return flask.redirect(flask.url_for('index'))

@app.route('/add/friend_request', methods=['POST'])
def add_friend_request():
    '''Requires id in query param and friend_id in json data'''
    content = flask.request.json
    id = flask.request.args.get('id', '')
    friend_id = content['friend_id']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO friend_request (id, friend_id) \
                VALUES (?, ?)", (friend_id, id))
    conn.commit()
    conn.close()
    return flask.redirect(flask.url_for('index'))

@app.route('/add/friend', methods=['POST'])
def add_friend():
    '''Requires id in query param and friend_id in json data'''
    content = flask.request.json
    id = flask.request.args.get('id', '')
    friend_id = content['friend_id']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO friend (id, friend_id) \
                VALUES (?, ?)", (id, friend_id))
    conn.commit()
    conn.close()
    return flask.redirect(flask.url_for('index'))

if __name__ == "__main__":
    init_db()
    app.run(port=8000, debug=True)