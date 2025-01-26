import flask
import json
import sqlite3
import api

app = flask.Flask(__name__)

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
    try:
        content = flask.request.json
        id = content['id']
        name = content['name']
        major = content['major']
        grade = int(content['grade'])
    except KeyError as e:
        return f"Missing key in JSON input: {e}", 400
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
    id = flask.request.args.get('id', '')
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
    id = flask.request.args.get('id', '')

    conn = sqlite3.connect('database.db')
    try:
        c = conn.cursor()

        c.execute("SELECT * FROM student WHERE id=?", (id,))
        user = c.fetchone()

        c.execute("SELECT section_code FROM enrollment WHERE id=?", (id,))
        courses = c.fetchall()
        courses_flat = [i[0] for i in courses]
        
        c.execute("SELECT friend_id FROM friend WHERE id=?", (id,))
        friends = c.fetchall()
        friend_ids = [i[0] for i in friends]
        friend_names = []
        for id in friend_ids:
            c.execute("SELECT name FROM student WHERE id=?", (id,))
            name = c.fetchone()
            friend_names.append(name[0])

        c.execute("SELECT id FROM friend_request WHERE friend_id=?", (id,))
        friend_reqs = c.fetchall()
        friend_req_ids = [i[0] for i in friend_reqs]
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

    courses = api.retrieve_course_information(courses_flat)

    friends = {}
    for i in range(len(friend_names)):
        friends[friend_ids[i]] = friend_names[i]
    
    friend_reqs = {}
    for i in range(len(friend_req_ids)):
        friend_reqs[friend_req_ids[i]] = friend_req_names[i]

    rtn_obj = {'id': user[0], 'name': user[1], 'major': user[2], 'grade': user[3], 'courses': courses, 'friends': friends, 'friendReqs': friend_reqs}
    return rtn_obj

@app.route('/add/courses', methods=['POST'])
def add_courses():
    '''Requires id and a list of classes in json data'''
    try:
        content = flask.request.json
        id = content['id']
        courses = content['section_codes']
    except KeyError as e:
        return f"Missing key in JSON input: {e}", 400
    conn = sqlite3.connect('database.db')
    try:
        c = conn.cursor()
        for i in range(len(courses)):
            c.execute("INSERT INTO enrollment (id, section_code) \
                        VALUES (?, ?)", (id, courses[i]))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
        return f"Failed to add courses due to a database error: {e}"
    finally:
        conn.close()
    return "Added courses successfully"

@app.route('/delete/courses', methods=['POST'])
def delete_courses():
    '''Requires id in query param and a list of classes in json data'''
    try:
        content = flask.request.json
        id = flask.request.args.get('id', '')
        courses = content['section_code']
    except KeyError as e:
        return f"Missing key in JSON input: {e}", 400
    conn = sqlite3.connect('database.db')
    try:
        c = conn.cursor()
        for i in range(len(courses)):
            c.execute("DELETE FROM enrollment WHERE id=? AND section_code=?", (id, courses[i]))
        conn.commit()
    except sqlite3.DatabaseError as e:
        print(f"Error: {e}")
        return f"Failed to delete courses due to a database error: {e}"
    finally:
        conn.close()
    return "Deleted courses successfully"

@app.route('/add/friend_request', methods=['POST'])
def add_friend_request():
    '''Requires id in query param and friend_id in json data'''
    try:
        content = flask.request.json
        id = flask.request.args.get('id', '')
        friend_id = content['friend_id']
    except KeyError as e:
        return f"Missing key in JSON input: {e}", 400
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
    try:
        content = flask.request.json
        id = flask.request.args.get('id', '')
        friend_id = content['friend_id']
    except KeyError as e:
        return f"Missing key in JSON input: {e}", 400
    conn = sqlite3.connect('database.db')
    try:
        c = conn.cursor()
        c.execute("SELECT friend_id FROM friend_request WHERE id=?", (id,))
        f_reqs = c.fetchall()
        f_reqs = [i[0] for i in f_reqs]
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
    try:
        content = flask.request.json
        id = flask.request.args.get('id', '')
        friend_id = content['friend_id']
    except KeyError as e:
        return f"Missing key in JSON input: {e}", 400
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

@app.route('/suggest_friends')
def suggest_friends():
    '''Requires id in the form of a query param'''
    id = flask.request.args.get('id', '')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Get the user's courses
    c.execute("SELECT section_code FROM enrollment WHERE id=?", (id,))
    user_courses = set([course[0] for course in c.fetchall()])

    # Get all other users and their courses
    c.execute("SELECT id, section_code FROM enrollment WHERE id != ?", (id,))
    all_enrollments = c.fetchall()

    # Get current friends
    c.execute("SELECT friend_id FROM friend WHERE id=?", (id,))
    current_friends = set([friend[0] for friend in c.fetchall()])

    # Calculate similarity scores
    user_similarities = {}
    for enrollment in all_enrollments:
        other_id, course = enrollment
        if other_id not in user_similarities:
            user_similarities[other_id] = 0
        if course in user_courses:
            user_similarities[other_id] += 1

    # Sort users by similarity score
    suggested_friends = sorted(user_similarities.items(), key=lambda x: x[1], reverse=True)

    # Filter out current friends and limit to top 5 suggestions
    suggested_friends = [
        {"id": user_id, "shared_courses": score}
        for user_id, score in suggested_friends
        if user_id not in current_friends and score > 0
    ][:5]

    # Get names for suggested friends
    for friend in suggested_friends:
        c.execute("SELECT name FROM student WHERE id=?", (friend['id'],))
        friend['name'] = c.fetchone()[0]

    conn.close()

    return flask.jsonify(suggested_friends)

@app.route('/students_with_same_course', methods=['GET'])
def students_with_same_course():
    '''Requires id and course_name in the form of query params'''
    id = flask.request.args.get('id', '')
    course_name = flask.request.args.get('course_name', '')
    conn = sqlite3.connect('database.db')
    try:
        c = conn.cursor()

        # Check if the user is enrolled in the given course
        c.execute("SELECT 1 FROM enrollment WHERE id=? AND section_code=?", (id, course_name))
        if not c.fetchone():
            return "The student is not enrolled in the given course", 404

        # Get students with the same course
        c.execute("SELECT id FROM enrollment WHERE section_code=?", (course_name,))
        all_enrollments = c.fetchall()

        # Filter out the given student
        students_with_same_course = [student_id[0] for student_id in all_enrollments if student_id[0] != id]

        # Get names for students
        result = []
        for student_id in students_with_same_course:
            c.execute("SELECT name FROM student WHERE id=?", (student_id,))
            name = c.fetchone()[0]
            result.append({
                "id": student_id,
                "name": name
            })

    except sqlite3.DatabaseError as e:
        print(f"Error: {e}")
        return f"Failed to fetch students with the same course due to a database error: {e}."
    finally:
        conn.close()

    return flask.jsonify(result)

if __name__ == "__main__":
    init_db()
    app.run(port=8000, debug=True)

