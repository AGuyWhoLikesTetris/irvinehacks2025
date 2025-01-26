import flask
import api
import sqlite3
from flask_cors import CORS, cross_origin

bp = flask.Blueprint('friends', __name__)

@bp.route('/add/friend', methods=['POST'])
@cross_origin()
def add_friend():
    '''Requires id in query param and friend_id in json data'''
    try:
        content = flask.request.json
        id = content['id']
        friend_id = content['friend_id']
    except KeyError as e:
        return f"Missing key in JSON input: {e}", 400
    conn = sqlite3.connect('database.db')
    try:
        c = conn.cursor()
        c.execute("SELECT friend_id FROM friend_request WHERE id=?", (friend_id,))
        f_reqs = c.fetchall()
        f_reqs = [i[0] for i in f_reqs]
        if id not in f_reqs:
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
    return {"ok": True}

@bp.route('/delete/friend', methods=['POST'])
@cross_origin()
def delete_friend():
    '''Requires id in query param and friend_id in json data'''
    try:
        content = flask.request.json
        id = content['id']
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
    return {"ok": True}


@bp.route('/add/friend_request', methods=['POST'])
@cross_origin()
def add_friend_request():
    '''Requires id in query param and friend_id in json data'''
    try:
        content = flask.request.json
        id = content['id']
        friend_id = content['friend_id']
    except KeyError as e:
        return f"Missing key in JSON input: {e}", 400
    conn = sqlite3.connect('database.db')
    try:
        c = conn.cursor()
        c.execute("SELECT id FROM friend WHERE friend_id=?", (id,))
        friends_flattened = [i[0] for i in c.fetchall()] 
        if friend_id in friends_flattened:
            return "Friend already exists."
        c.execute("INSERT INTO friend_request (id, friend_id) \
                    VALUES (?, ?)", (id, friend_id))
        print(f"friend_req to {friend_id}")
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
        return f"Failed to add friend request due to a database error: {e}"
    finally:
        conn.close()
    return {"ok": True}

@bp.route('/delete/friend_request', methods=['POST'])
@cross_origin()
def delete_friend_request():
    '''Requires id in query param and friend_id in json data'''
    try:
        content = flask.request.json
        id = content['id']
        friend_id = content['friend_id']
    except KeyError as e:
        return f"Missing key in JSON input: {e}", 400
    conn = sqlite3.connect('database.db')
    try:
        c = conn.cursor()
        c.execute("DELETE FROM friend_request WHERE id=? AND friend_id=?", (friend_id, id))
        c.execute("DELETE FROM friend_request WHERE id=? AND friend_id=?", (id, friend_id))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
        return f"Failed to add friend due to a database error: {e}"
    finally:
        conn.close()
    return {"ok": True}

@bp.route('/suggest_friends', methods=['GET'])
@cross_origin()
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

@bp.route('/view/friends/day', methods=['GET'])
@cross_origin()
def get_course_info_by_day():
    id = flask.request.args.get('id', '')
    days = ['M','Tu','W','Th',"F"]
    try:
        course_info = []
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT friend_id FROM friend WHERE id=?", (id,))
        friends = c.fetchall()
        friends = [friend[0] for friend in friends]
        for i in range(len(days)):
            course_day = []
            for k in range(len(friends)):
                c = conn.cursor()
                c.execute("SELECT section_code FROM enrollment WHERE days LIKE ? AND id=?", (f'%{days[i]}%',friends[k]))
                courses = c.fetchall()
                courses_flat = [course[0] for course in courses]
                for j in range(len(courses_flat)):
                    c.execute("SELECT course_name, start_time_hour, start_time_minute, end_time_hour, end_time_minute, course_type FROM enrollment WHERE section_code=?", (courses_flat[j],))
                    results = c.fetchone()
                    course_day.append({
                        "courseName": results[0],
                        "time": [results[1] + (results[2] / 60), results[3] + (results[4] / 60)],
                        "courseType": results[5],
                        "id": friends[k]
                    })
            course_info.append(course_day)
        return course_info

    except sqlite3.DatabaseError as e:
        print(f"Error: {e}")
        return f"Failed to get course info due to a database error: {e}"
    finally:
        conn.close()
    return {"ok": True}