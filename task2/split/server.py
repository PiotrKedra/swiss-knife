import socket


def main():
    http_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_server.setsockopt(socket.SOL_SOCKET, 25, str("wlo1" + '\0').encode('utf-8'))
    http_server.bind(('', 808))
    http_server.listen(128)
    while True:
        connection, addr = http_server.accept()
        data = connection.recv(1024)
        if not data:
            break
        connection.sendall(data)
    connection.close()


if __name__ == '__main__':
    main()
