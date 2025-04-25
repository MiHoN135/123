import hashlib
import sqlite3
from uuid import uuid4

class User:
    """ 
    Класс-модель объекта пользователя
    """ 
    def __init__(self, user_id, login, password, email=None, age=None, created_at=None):
        self.user_id = user_id
        self.login = login
        self.password = password
        self.email = email
        self.age = age
        self.created_at = created_at

class Storage:
    """ 
    Класс отвечающий за хранение информации
    """ 
    def __init__(self, db_path='./my.db'):
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()
        self.active_sessions = []  # Список для хранения активных сессий
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
            user_id TEXT PRIMARY KEY NOT NULL,
            login TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            age INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Sessions (
            auth_id INT NOT NULL,
            token TEXT NOT NULL,
            user_id TEXT NOT_NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            deleted_at DATETIME,
            deleted BOOL DEFAULT false
            )
            ''')
        self.db.commit()

    def register_user(self, login, password, email=None, age=None) -> User | None:
        """ 
        Метод отвечающий за сохранение пользователя в хранилище
        """
        _id = str(uuid4())
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute('''
        INSERT INTO Users (
        user_id, login, password, email, age)
        VALUES(?, ?, ?, ?, ?)
        ''',
        (_id, login, hashed_password, email, age))
        self.db.commit()
        return User(_id, login, hashed_password)

    def start_session(self, auth_id, token, user_id):
        session = token
        self.active_sessions.append(session)
        print(self.active_sessions)
        self.cursor.execute('''
        INSERT INTO Sessions (
        auth_id, token, user_id)
        VALUES (?, ?, ?)''',
        (auth_id, token, user_id))
        self.db.commit()

    def get_user_by_login(self, login):
        self.cursor.execute('''
        SELECT *
        FROM Users
        WHERE login = ?''', (login,))
        row = self.cursor.fetchone()
        return User(*row)

    def end_session(self, auth_id):
        """Помечает сессию как завершенную с текущей меткой времени"""
        self.cursor.execute('''
                UPDATE Sessions 
                SET deleted_at = CURRENT_TIMESTAMP, 
                    deleted = true
                WHERE auth_id = ? AND deleted = false
            ''', (auth_id,))
        self.db.commit()