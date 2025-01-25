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
    tasks = c.fetchall()
    conn.close()
    return tasks

@app.route('/add', methods=['POST'])
def add_task():
    id = flask.request.form['id']
    name = flask.request.form['name']
    if name:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO student (id, name) \
                    VALUES (?, ?)", (id, name))
        conn.commit()
        conn.close()
    return flask.redirect(flask.url_for('index'))

@app.route('/delete/<int:id>')
def delete_task(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM student WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return flask.redirect(flask.url_for('index'))

if __name__ == "__main__":
    init_db()
    app.run(port=8000, debug=True)