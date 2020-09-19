import requests


def test_login():
    username='seveniruby'
    password='hogwarts'
    r=requests.post(
        'http://127.0.0.1:5000/login',
        json={
            'username': username,
            'password': password
        }
    )
    print(r.text)
    assert r.status_code == 200

    token = r.json()['token']
    assert token is not None

    r = requests.get(
        'http://127.0.0.1:5000/testcase',
        headers={'Authorization': f'Bearer {token}'}
    )
    print(r.json())
    assert r.status_code == 200




def test_testcase_get():
    r=requests.get(
        'http://127.0.0.1:5000/testcase'
    )
    print(r.json())
    assert r.status_code == 401



