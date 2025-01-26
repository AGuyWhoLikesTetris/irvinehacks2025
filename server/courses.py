import flask
import api
import sqlite3
from flask_cors import CORS, cross_origin


bp = flask.Blueprint('courses', __name__)

@bp.route('/add/courses', methods=['POST'])
@cross_origin()
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
        course_info = api.retrieve_course_information(courses)
        for i in range(len(courses)):
            c.execute("INSERT INTO enrollment (id, section_code, course_name, start_time_hour, start_time_minute, end_time_hour, end_time_minute, days, course_type) \
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (id, course_info[i]['sectionCode'], course_info[i]['courseName'], course_info[i]['time'][0]['hour'], course_info[i]['time'][0]['minute'], course_info[i]['time'][1]['hour'], course_info[i]['time'][1]['minute'], course_info[i]['days'], course_info[i]['courseType']))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
        return f"Failed to add courses due to a database error: {e}"
    except api.APIError as e:
        print(f"Error: {e}")
        return f"Failed to add courses due to an API error: {e}"
    finally:
        conn.close()
    return {"ok": True}

@bp.route('/delete/courses', methods=['POST'])
@cross_origin()
def delete_courses():
    '''Requires id in query param and a list of classes in json data'''
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
            c.execute("DELETE FROM enrollment WHERE id=? AND section_code=?", (id, courses[i]))
        conn.commit()
    except sqlite3.DatabaseError as e:
        print(f"Error: {e}")
        return f"Failed to delete courses due to a database error: {e}"
    finally:
        conn.close()
    return {"ok": True}


@bp.route('/students_with_same_course', methods=['GET'])
@cross_origin()
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