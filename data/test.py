from requests import get, post, delete, put
import datetime


if __name__ == '__main__':
    print(get('http://localhost:8080/api/jobs').json())
    print(get('http://localhost:8080/api/jobs/1').json())
    print(get('http://localhost:8080/api/jobs/-1').json())
    print(get('http://localhost:8080/api/jobs/abc').json())

    print(get('http://localhost:8080/api/v2/users').json())
    print(get('http://localhost:8080/api/v2/users/1').json())
    print(get('http://localhost:8080/api/v2/users/999').json())
    print(get('http://localhost:8080/api/v2/users/not_int').json())

    params = {
        "id": 4,
        "job": "a",
        "team_leader": 4,
        "work_size": 10,
        "collaborators": "2,4,5",
        "start_date": datetime.datetime.now,
        "end_date": datetime.datetime.now,
        "is_finished": True,
        "category": 1
    }  # CORRECT
    print(post('http://localhost:8080/api/jobs/', params=params).json())
    params = {
        "id": 5,
        "job": "b",
        "team_leader": 3,
        "work_size": "1",
        "collaborators": "1,3,5",
        "start_date": datetime.datetime.now,
        "end_date": datetime.datetime.now,
        "is_finished": True,
        "category": 1
    }  # WORK SIZE STRING
    print(post('http://localhost:8080/api/jobs/', params=params).json())
    params = {
        "id": 4,
        "job": "a",
        "team_leader": 4,
        "work_size": 10,
        "collaborators": "1",
        "start_date": datetime.datetime.now,
        "end_date": datetime.datetime.now,
        "is_finished": True,
        "category": 1
    }  # EXISTING WORK INCLUDING id
    print(post('http://localhost:8080/api/jobs/', params=params).json())
    params = {
        "id": -1,
        "job": -1,
        "team_leader": -1,
        "work_size": -1,
        "collaborators": -1,
        "start_date": -1,
        "end_date": -1,
        "is_finished": -1,
        "category": -1
    }  # BRUH
    print(post('http://localhost:8080/api/jobs/', params=params).json())
    print(get('http://localhost:8080/api/jobs/').json())

    print(delete('http://localhost:8080/api/jobs/3').json())
    print(delete('http://localhost:8080/api/jobs/999').json())
    print(delete('http://localhost:8080/api/jobs/not_int').json())
    print(get('http://localhost:8080/api/jobs/').json())

    print(put('http://localhost:8080/api/jobs_edit/', json={'id': 1, 'job': 'aaa'}).json())  # NICE
    print(put('http://localhost:8080/api/jobs_edit/', json={'id': -1, 'job': 'aaa'}).json())  # NOT EXISTING id
    print(put('http://localhost:8080/api/jobs_edit/', json={'id': 1, 'super idol asulym': 'aaa'}).json())  # WRONG VARIABLE
    print(put('http://localhost:8080/api/jobs_edit/').json())  # BRUH
    print(get('http://localhost:8080/api/jobs/').json())

    print(post('http://localhost:5000/api/v2/users').json())
    print(post('http://localhost:5000/api/v2/users', json={'name': 'Alisa'}).json())
    print(post('http://localhost:5000/api/v2/users',
               json={'name': 'Alisa', 'position': 'junior biologist',
                     'surname': 'Selezneva', 'age': 15, 'address': 'module_7',
                     'speciality': 'biology',
                     'hashed_password': 'selezen',
                     'email': 'alisa@mars.org'}).json())

    print(delete('http://localhost:5000/api/v2/users/1').json())
    print(delete('http://localhost:5000/api/v2/users/999').json())
    print(delete('http://localhost:5000/api/v2/users/a').json())
