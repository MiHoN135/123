import argparse
from server import Server, Path
from handler import Handler
from storage import Storage

def start_server(addr, port, server_class=Server, handler_class=Handler):
    """Функция запуска сервера. Она будет прописана в main()"""
    server_address = (addr, port)
    http_server = server_class(server_address, handler_class, Path(), Storage())
    print(f"Starting server on {addr}:{port}"); http_server.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Сервер авторизации", usage="Используйте параметры --listen, --port чтобы задать URL")
    parser.add_argument("-l", "--listen", default="0.0.0.0", help="IP адрес сервера")
    parser.add_argument("-p", "--port", type=int, default=8000, help="Порт")
    args = parser.parse_args(); start_server(addr=args.listen, port=args.port)