import json
import socket


def get_network_settings():
    with open('network_settings.txt') as json_file:
        data = json.load(json_file)
        return data


def main():
    network_settings = get_network_settings()

    http_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_server.setsockopt(socket.SOL_SOCKET, 25, str(network_settings['interface'] + '\0').encode('utf-8'))
    http_server.bind(('', network_settings['port']))
    http_server.listen(128)
    while True:
        connection, address = http_server.accept()
        data = connection.recv(1024)
        content_length = "Content-Length:%d\r\n" % len(data)
        if data:
            data = b"HTTP/1.1 200 OK\r\n" + content_length.encode() + b"\r\n" + data
            print(data)
            connection.sendall(data)
        connection.close()


if __name__ == '__main__':
    main()
