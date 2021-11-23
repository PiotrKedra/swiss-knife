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
        if data:
            response = b'HTTP/1.0 200 OK\r\nDate: Mon, 1 Jan 1996 01:01:01 GMT\r\n'
            response += b'Content-Type: text/plain\r\nContent-Length: 0\r\n\r\n'
            response += b'Hello, world!\r\n\r\n' + data
            print(data)
            connection.sendall(response)
        connection.close()


if __name__ == '__main__':
    main()
