import requests

class APIError(Exception):
    """An API Error Exception"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return f"APIError: status={self.status}"

def _retrieve_course_api_result(section_code: list[int]):
    section_codes = ",".join([str(code) for code in section_code])
    url = "https://anteaterapi.com/v2/rest/websoc"
    params = {"year": 2025, "quarter": "Winter", "sectionCodes": section_codes}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise APIError(response.status_code)

def retrieve_course_information(section_codes: list[int]):
    if section_codes == []:
        return []
    course_list = []
    original_data = _retrieve_course_api_result(section_codes)        
    for school in original_data['data']['schools']:
        for department in school['departments']:
            for course in department['courses']:
                for section in course['sections']:
                    day = section['meetings'][0]['days']
                    startTime = section['meetings'][0]['startTime']
                    endTime = section['meetings'][0]['endTime']
                    section_code = int(section['sectionCode'])
                    time = (startTime, endTime)
                    name = course['deptCode'] + " " + course['courseNumber']
                    course_type = section['sectionType']
                    course_list.insert(0, {
                        "sectionCode": section_code,
                        "courseName": name,
                        "time": time,
                        "days": day,
                        "courseType": course_type
                    })
    return course_list

def check_valid_section_code(section_code: int):
    response = _retrieve_course_api_result([section_code])
    print(response)
    if response['data']['schools'] != []:
        return True
    else:
        return False