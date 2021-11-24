import json
import os
import socket

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def get_network_settings():
    with open(os.path.join(__location__, 'network_settings.txt')) as json_file:
        data = json.load(json_file)
        return data


def main():
    network_settings = get_network_settings()

    address_info = socket.getaddrinfo(
        f"{network_settings['ip']}%{network_settings['interface']}",
        network_settings['port'],
        socket.AF_INET6,
        socket.SOCK_STREAM
    )
    (family, sock_type, proto, canon_name, sock_address) = address_info[0]
    http_server = socket.socket(family, sock_type, proto)

    # http_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # http_server.setsockopt(socket.SOL_SOCKET, 25, str(network_settings['interface'] + '\0').encode('utf-8'))

    http_server.bind(('', network_settings['port']))
    http_server.listen(128)
    while True:
        connection, address = http_server.accept()
        data = connection.recv(1024)
        if data:
            content_length = str(len(data)).encode()
            response = b'HTTP/1.0 200 OK\r\n'
            response += b'Content-Length: ' + content_length + b'\r\n\r\n'
            response += data
            print(data)
            connection.sendall(response)
        connection.close()


if __name__ == '__main__':
    main()
