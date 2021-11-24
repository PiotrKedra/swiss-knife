import json
import os
import socket

import select

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
    http_server.bind(('', network_settings['port']))

    http_server.listen(128)
    http_server.listen(5)
    http_server.setblocking(False)

    connections = {}
    requests = {}
    responses = {}
    server_fd = http_server.fileno()

    poll = select.poll()
    poll.register(http_server.fileno(), select.POLLIN)

    while True:
        events = poll.poll(1)

        for fileno, event in events:
            if fileno == server_fd:
                connection, address = http_server.accept()
                connection.setblocking(False)

                fd = connection.fileno()
                poll.register(fd, select.POLLIN)
                connections[fd] = connection
                requests[fd] = ''
                responses[fd] = ''

            elif event & select.POLLIN:
                data = connections[fileno].recv(1024)
                if data and data.decode() != "QUIT":
                    poll.modify(fileno, select.POLLOUT)
                    content_length = str(len(data)).encode()
                    response = b'HTTP/1.0 200 OK\r\n'
                    response += b'Content-Length: ' + content_length + b'\r\n\r\n'
                    response += data
                    requests[fileno] = ''

                else:
                    print('[{:02d}] exit or hung up'.format(fileno))
                    poll.unregister(fileno)
                    connections[fileno].close()
                    del connections[fileno], requests[fileno], responses[fileno]

            elif event & select.POLLOUT:
                byteswritten = connections[fileno].send(responses[fileno])
                responses[fileno] = responses[fileno][byteswritten:]
                poll.modify(fileno, select.POLLIN)


if __name__ == '__main__':
    main()
