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

@bp.route('/edit/user', methods=['POST'])
@cross_origin()
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

        c.execute("SELECT * FROM enrollment WHERE id=?", (id,))
        courses = c.fetchall()
        section_code = [i[1] for i in courses]
        course_name = [i[2] for i in courses]
        start_time_hour = [i[3] for i in courses]
        start_time_minute = [i[4] for i in courses]
        end_time_hour = [i[5] for i in courses]
        end_time_minute = [i[6] for i in courses]
        days = [i[7] for i in courses]
        course_type = [i[8] for i in courses]
        
        c.execute("SELECT friend_id FROM friend WHERE id=?", (id,))
        friends = c.fetchall()
        friend_ids = [i[0] for i in friends]
        friend_names = []
        for nid in friend_ids:
            c.execute("SELECT name FROM student WHERE id=?", (nid,))
            name = c.fetchone()
            friend_names.append(name[0])

        c.execute("SELECT id FROM friend_request WHERE friend_id=?", (id,))
        friend_reqs = c.fetchall()
        friend_req_ids = [i[0] for i in friend_reqs]
        friend_req_names = []
        for nid in friend_req_ids:
            c.execute("SELECT name FROM student WHERE id=?", (nid,))
            name = c.fetchone()
            friend_req_names.append(name[0])

    except sqlite3.DatabaseError as e:
        print(f"Error: {e}")
        return f"Failed to view user details due to a database error: {e}."
    finally:
        conn.close()

    
    courses = []
    for i in range(len(section_code)):
        courses.append({
            "sectionCode": section_code[i],
            "courseName": course_name[i],
            "time": [{'hour': start_time_hour[i], 'minute': start_time_minute[i]}, {'hour': end_time_hour[i], 'minute': end_time_minute[i]}],
            "days": days[i],
            "courseType": course_type[i]
        })

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
        c.execute('SELECT id, name FROM student WHERE name LIKE ?', (f'%{keyword}%',))
        result = c.fetchall()
        users = [{"id": row[0], "name": row[1]} for row in result]
    except sqlite3.DatabaseError as e:
        print(f"Error: {e}")
        return f"Failed to search users due to a database error: {e}."
    finally:
        conn.close()
    return {"users": users}

@bp.route('/view/user/day', methods=['GET'])
@cross_origin()
def get_course_info_by_day():
    id = flask.request.args.get('id', '')
    days = 'MTuWThF'
    conn = sqlite3.connect('database.db')
    try:
        course_info = []
        for i in range(len(days)):
            c = conn.cursor()
            if days[i] == 'T':
                c.execute("SELECT section_code FROM enrollment WHERE days LIKE ? AND id=?", (f'%{days[i:i+1]}%',id))
                i += 1
            else:
                c.execute("SELECT section_code FROM enrollment WHERE days LIKE ? AND id=?", (f'%{days[i]}%',id))
            courses = c.fetchall()
            courses_flat = [course[0] for course in courses]
            course_day = []
            for j in range(len(courses_flat)):
                c.execute("SELECT course_name, start_time_hour, start_time_minute, end_time_hour, end_time_minute, course_type FROM enrollment WHERE section_code=?", (courses_flat[j],))
                results = c.fetchone()
                course_day.append({
                    "courseName": results[0],
                    "time": [results[1] + (results[2] / 60), results[3] + (results[4] / 60)],
                    "courseType": results[5]
                })
            course_info.append(course_day)
        return course_info

    except sqlite3.DatabaseError as e:
        print(f"Error: {e}")
        return f"Failed to get course info due to a database error: {e}"
    finally:
        conn.close()
    return {"ok": True}