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
        major TEXT,
        grade INTEGER
         ) STRICT;''')

    # enrollment table 
    c.execute('''CREATE TABLE IF NOT EXISTS enrollment(
        id INTEGER NOT NULL,
        course_id TEXT NOT NULL,
        day TEXT NOT NULL,
        time TEXT NOT NULL,
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

@app.route('/add/user', methods=['POST'])
def add_user():
    '''Requires id, name, major, grade in json data'''
    content = flask.request.json
    id = int(content['id'])
    name = content['name']
    major = content['major']
    grade = int(content['grade'])
    if name:
        conn = sqlite3.connect('database.db')
        try:
            c = conn.cursor()
            c.execute("INSERT INTO student (id, name, major, grade) \
                        VALUES (?, ?, ?, ?)", (id, name, major, grade))
            conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
            return f"Failed to add user due to a database error: {e}."
        finally:
            conn.close()
    return "User added successfully"

@app.route('/delete/user')
def delete_user(id):
    '''Requires id in the form of a query param'''
    id = int(flask.request.args.get('id', ''))
    conn = sqlite3.connect('database.db')
    try:
        c = conn.cursor()
        c.execute("DELETE FROM student WHERE id=?", (id,))
        conn.commit()
    except sqlite3.DatabaseError as e:
        print(f"Error: {e}")
        return f"Failed to delete user due to a database error: {e}."
    finally:
        conn.close()
    return "User deleted successfully"

@app.route('/view')
def view():
    '''Requires id in the form of a query param'''
    id = int(flask.request.args.get('id', ''))

    conn = sqlite3.connect('database.db')
    try:
        c = conn.cursor()

        c.execute("SELECT * FROM student WHERE id=?", (id,))
        user = c.fetchone()

        c.execute("SELECT course_id, day, time FROM enrollment WHERE id=?", (id,))
        courses = c.fetchall()
        courses_flat = [i[0] for i in courses]
        day = [i[1] for i in courses]
        time = [i[2] for i in courses]
        
        c.execute("SELECT friend_id FROM friend WHERE id=?", (id,))
        friends = c.fetchall()
        friend_ids = [int(i[0]) for i in friends]
        friend_names = []
        for id in friend_ids:
            c.execute("SELECT name FROM student WHERE id=?", (id,))
            name = c.fetchone()
            friend_names.append(name[0])
        c.execute("SELECT * FROM friend_request")
        friend_reqs = c.fetchall()
        print(friend_reqs)
        c.execute("SELECT id FROM friend_request WHERE friend_id=?", (id,))
        friend_reqs = c.fetchall()
        friend_req_ids = [int(i[0]) for i in friend_reqs]
        friend_req_names = []
        for id in friend_req_ids:
            c.execute("SELECT name FROM student WHERE id=?", (id,))
            name = c.fetchone()
            friend_req_names.append(name[0])
    except sqlite3.DatabaseError as e:
        print(f"Error: {e}")
        return f"Failed to view user details due to a database error: {e}."
    finally:
        conn.close()

    courses = []
    for i in range(len(courses_flat)):
        courses.append({
            'course_name': courses_flat[i],
            'day': day[i],
            'time': time[i]
        })

    friends = {}
    for i in range(len(friend_names)):
        friends[friend_ids[i]] = friend_names[i]
    
    friend_reqs = {}
    for i in range(len(friend_req_ids)):
        friend_reqs[friend_req_ids[i]] = friend_req_names[i]

    rtn_obj = {'id': user[0], 'name': user[1], 'major': user[2], 'grade': user[3], 'courses': courses, 'friends': friends, 'friend_reqs': friend_reqs}
    return rtn_obj

@app.route('/add/courses', methods=['POST'])
def add_courses():
    '''Requires id in query param and a list of classes in json data'''
    content = flask.request.json
    id = int(content['id'])
    day = content['day']
    time = content['time']
    courses = content['course_name']
    conn = sqlite3.connect('database.db')
    try:
        c = conn.cursor()
        for i in range(len(courses)):
            c.execute("INSERT INTO enrollment (id, course_id, day, time) \
                        VALUES (?, ?, ?, ?)", (id, courses[i], day[i], time[i]))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
        return f"Failed to add courses due to a database error: {e}"
    finally:
        conn.close()
    return "Added courses successfully"

@app.route('/add/friend_request', methods=['POST'])
def add_friend_request():
    '''Requires id in query param and friend_id in json data'''
    content = flask.request.json
    id = flask.request.args.get('id', '')
    friend_id = int(content['friend_id'])
    conn = sqlite3.connect('database.db')
    try:
        c = conn.cursor()
        c.execute("INSERT INTO friend_request (id, friend_id) \
                    VALUES (?, ?)", (id, friend_id))
        print(f"friend_req to {friend_id}")
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
        return f"Failed to add friend request due to a database error: {e}"
    finally:
        conn.close()
    return "Friend request sent successfully"

@app.route('/add/friend', methods=['POST'])
def add_friend():
    '''Requires id in query param and friend_id in json data'''
    content = flask.request.json
    id = int(flask.request.args.get('id', ''))
    friend_id = int(content['friend_id'])
    conn = sqlite3.connect('database.db')
    try:
        c = conn.cursor()
        c.execute("SELECT friend_id FROM friend_request WHERE id=?", (id,))
        f_reqs = c.fetchall()
        f_reqs = [int(i[0]) for i in f_reqs]
        if friend_id not in f_reqs:
            return "Friend request does not exist"
        c.execute("INSERT INTO friend (id, friend_id) \
                    VALUES (?, ?)", (id, friend_id))
        c.execute("INSERT INTO friend (id, friend_id) \
                    VALUES (?, ?)", (friend_id, id))
        c.execute("DELETE FROM friend_request WHERE id=? AND friend_id=?", (id, friend_id))
        c.execute("DELETE FROM friend_request WHERE id=? AND friend_id=?", (friend_id, id))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
        return f"Failed to add friend due to a database error: {e}"
    finally:
        conn.close()
    return "Added friend successfully"

@app.route('/delete/friend', methods=['POST'])
def delete_friend():
    '''Requires id in query param and friend_id in json data'''
    content = flask.request.json
    id = flask.request.args.get('id', '')
    friend_id = int(content['friend_id'])
    conn = sqlite3.connect('database.db')
    try:
        c = conn.cursor()
        c.execute("DELETE FROM friend WHERE id=? AND friend_id=?", (id, friend_id))
        c.execute("DELETE FROM friend WHERE id=? AND friend_id=?", (friend_id, id))
        conn.commit()
    except sqlite3.DatabaseError as e:
        print(f"Error: {e}")
        return f"Failed to delete friend due to a database error: {e}"
    finally:
        conn.close()
    return "Deleted friend successfully"

if __name__ == "__main__":
    init_db()
    app.run(port=8000, debug=True)