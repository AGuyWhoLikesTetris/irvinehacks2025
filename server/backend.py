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

@app.route('/add', methods=['POST'])
def add_user():
    '''Requires id, name, degree, grade in form data'''
    id = flask.request.form['id']
    name = flask.request.form['name']
    degree = flask.request.form['degree']
    grade = flask.request.form['grade']
    if name:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO student (id, name, degree, grade) \
                    VALUES (?, ?, ?, ?)", (id, name, degree, grade))
        conn.commit()
        conn.close()
    return flask.redirect(flask.url_for('index'))

@app.route('/delete/<int:id>')
def delete_user(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM student WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return flask.redirect(flask.url_for('index'))

@app.route('/view/<int:id>')
def view(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM student WHERE id=?", (id,))
    user = c.fetchone()
    c.execute("SELECT course_id FROM enrollment WHERE id=?", (id,))
    courses = c.fetchall()
    conn.close()
    rtn_obj = {'id': user[0], 'name': user[1], 'degree': user[2], 'grade': user[3], 'courses': courses}
    return rtn_obj

@app.route('/add_classes', methods=['POST'])
def add_classes():
    id = flask.request.form['id']
    classes = flask.request.form['classes']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    print(classes)
    for course_id in classes:
        print(course_id)
        c.execute("INSERT INTO enrollment (id, course_id) \
                    VALUES (?, ?)", (id, course_id))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    app.run(port=8000, debug=True)