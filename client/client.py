import requests

r2 = requests.post('http://127.0.0.1:8000/regster', json={"login": "test_user", "password": "test_password"})

print(r2.text)