from http.server import HTTPServer
from storage import Storage

class Path:
    """
    Класс определяющий все доступные пути (routes) сервера
    """
    REGISTER = "/register"
    LOGIN = "/login"
    LOGOUT = "/logout"

    @staticmethod
    def get_paths():
        return [Path.REGISTER, Path.LOGIN, Path.LOGOUT]

class Server(HTTPServer):
    """
    Класс ядра сервера
    """
    def __init__(self, address, request_handler, paths: Path, db: Storage):
        """
        С помощью super() мы безопасно наследуем методы класса HTTPServer,
        при этом используя наши собственные реализации address и request_handler
        :param address: адрес нашего сервера, например ('localhost', 8000)
        :param request_handler: обработчик запросов
        """
        super().__init__(address, request_handler)
        self.path = paths
        self.db = db