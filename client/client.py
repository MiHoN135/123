import requests

from server.storage import Storage
from vixod import dudu


class asd:

    def __init__(self):
        self.r = dudu().returi()

'''# Регистрация пользователя
r2 = requests.post("http://127.0.0.1:8000/register",
    json={
        "login": "test_user",
        "password": "test_password"
    })
print(r2.text)
'''

'''r3 = requests.post("http://127.0.0.1:8000/login",
    json={
        "login": "test_user",
        "password": "test_password"
    })
print(r3.text)'''
storage = Storage(db_path='C:\\Users\\MIHON\\PycharmProjects\\DZ2\\server\\my.db')
tokens = storage.get_active_tokens()
print(tokens)
try:
    x = requests.post(
        "http://localhost:8000/logout",
        headers={"Authorization": f"Bearer {tokens[asd().r - 1]}"} ) # ← Токен передаётся здесь
    print(x.text)
except IndexError as e:
    print(f'Всего {len(tokens)} пользователя')
    x = requests.post(
        "http://localhost:8000/logout",
        headers={"Authorization": f"Bearer {tokens[asd().r - 1]}"})  # ← Токен передаётся здесь
    print(x.text)
