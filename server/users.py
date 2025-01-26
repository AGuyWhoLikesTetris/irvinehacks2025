import flask
import api
import sqlite3
from flask_cors import CORS, cross_origin

bp = flask.Blueprint('users', __name__)

@bp.route('/check_user_exists', methods=['GET'])
@cross_origin()
def check_user_exists():
    '''Requires id in the form of a query param'''
    id = flask.request.args.get('id', '')
    conn = sqlite3.connect('database.db')
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM student WHERE id=?", (id,))
        user = c.fetchone()
    except sqlite3.DatabaseError as e:
        print(f"Error: {e}")
        return f"Failed to check if user exists due to a database error: {e}."
    finally:
        conn.close()
    if user:
        return {"exists": True}
    return {"exists": False}

@bp.route('/add/user', methods=['POST'])
@cross_origin()
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
    return {"ok": True}

@bp.route('/delete/user', methods=['POST'])
@cross_origin()
def delete_user(id):
    '''Requires id in the form of a query param'''
    id = flask.request.json['id']
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
    return {"ok": True}

@bp.route('/edit/user')
@cross_origin
def edit_user():
    '''Requires id and a list of new values in json data'''
    try:
        content = flask.request.json
        id = content['id']
        name = content['name']
        major = content['major']
        grade = content['grade']
    except KeyError as e:
        return f"Missing key in JSON input: {e}", 400
    conn = sqlite3.connect('database.db')
    try:
        c = conn.cursor()
        c.execute("UPDATE student SET name=?, major=?, grade=? WHERE id=?", (name, major, grade, id))
        conn.commit()
    except sqlite3.DatabaseError as e:
        print(f"Error: {e}")
        return f"Failed to edit user due to a database error: {e}."
    finally:
        conn.close()
    return {"ok": True}

@bp.route('/view/user')
@cross_origin()
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

@bp.route('/search/users', methods=['GET'])
@cross_origin()
def search_users():
    '''Requires keyword in the form of a query param'''
    keyword = flask.request.args.get('keyword', '')
    conn = sqlite3.connect('database.db')
    try:
        c = conn.cursor()
        c.execute('SELECT id FROM student WHERE name LIKE ?', (f'%{keyword}%',))
        result = c.fetchall()
        user_ids = [row[0] for row in result]
    except sqlite3.DatabaseError as e:
        print(f"Error: {e}")
        return f"Failed to search users due to a database error: {e}."
    finally:
        conn.close()
    return {"user_ids": user_ids}