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
            data = "HTTP/1.1 200 OK\r\n" + "Content-Type: text/html\r\n" + "\r\n" + "<h1>hello SWK</h1>"
            print(data)
            connection.send(data.encode())
        connection.close()


if __name__ == '__main__':
    main()
