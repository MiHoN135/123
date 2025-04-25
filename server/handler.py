import hashlib
from http.server import BaseHTTPRequestHandler
from random import randint

import jwt

from server import Server, Path
from json import dumps, loads

class Handler(BaseHTTPRequestHandler):
    """
    Класс хендлера. Отвечает за маршрутизацию запросов и их реализацию.
    """
    def __init__(self, request, client_address, server_class: Server):
        self.server: Server = server_class
        super().__init__(request, client_address, server_class)

    def do_GET(self):
        """ Маршрутизатор GET запросов """
        if self.path not in Path.get_paths():
            print("GET handler")
            response = dumps({"message": "Hello World!"})
            self.set_response(response) 
            return

    def do_POST(self):
        if self.path == self.server.path.REGISTER:
            self.register_impl()
        if self.path == self.server.path.LOGIN:
            self.login_impl()

    def handle_404(self):
        """ Обработка несуществующих маршрутов """
        response = dumps({"message": f"Route {self.path} does not exists"})
        self.set_response(response, 404)

    def set_response(self, response, error=None):
        """ Формировщик ответа сервера """
        if error is not None:
            self.send_response(error)
        else:
            self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(str(response).encode('utf-8'))

    def register_impl(self):
        """ Реализация запроса no пути 0.0.0.0:8000/register """
        data = self.get_post_body()
        login = data.get("login")
        password = data.get("password")
        user = self.server.db.register_user(login=login, password=password)
        if user is None:
            error_response = dumps({"message": "User already exists!"})
            self.set_response(error_response, 400)
        else:
            response = dumps({
                "message": "User registered!",
                "user_id": user.user_id,
                "login": user.login,
                "password_hash": user.password
            })
            self.set_response(response)

    def get_post_body(self):
        """ Метод получения данных из запроса пользователя """
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        return loads(post_body)

    def login_impl(self):
        data = self.get_post_body()
        user = self.server.db.get_user_by_login(data.get("login"))
        hashed_password = hashlib.sha256(data.get("password").encode()).hexdigest()
        if user.password != hashed_password:
            self.set_response(dumps({'error': "invalid password"}), 401)
        auth_id = randint(0, 99999)
        encoded_jwt = jwt.encode(
            {'auth_id': auth_id, "user_id": user.user_id},
            '123',
            algorithm="HS256"
        )
        self.server.db.start_session(auth_id, encoded_jwt, user.user_id)
        self.set_response(dumps({'message': "authorized", "token": encoded_jwt}))