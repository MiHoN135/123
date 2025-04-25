import hashlib
from uuid import uuid4

class User:
    """ 
    Класс-модель объекта пользователя
    """ 
    def __init__(self, user_id, login, password):
        self.user_id = user_id
        self.login = login
        self.password = password

class Storage:
    """ 
    Класс отвечающий за хранение информации
    """ 
    def __init__(self):
        self.users = {}

    def register_user(self, login, password) -> User | None:
        """ 
        Метод отвечающий за сохранение пользователя в хранилище
        """ 
        if login in self.users.keys():
            return None
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.users[login] = User(str(uuid4()), login, hashed_password)
        return self.users[login]