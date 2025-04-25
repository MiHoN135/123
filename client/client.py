import requests

'''# Регистрация пользователя
r2 = requests.post("http://127.0.0.1:8000/register",
    json={
        "login": "test_user",
        "password": "test_password"
    })
print(r2.text)
'''
# Авторизация пользователя
r3 = requests.post("http://127.0.0.1:8000/login",
    json={
        "login": "test_user",
        "password": "test_password"
    })
print(r3.text)