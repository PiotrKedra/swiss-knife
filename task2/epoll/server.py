import json

import select
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
    http_server.listen(5)
    http_server.setblocking(False)

    connections = {}
    requests = {}
    responses = {}
    server_fd = http_server.fileno()

    poll = select.epoll()
    poll.register(http_server.fileno(), select.EPOLLIN)

    while True:
        events = poll.poll(1)

        for fileno, event in events:
            if fileno == server_fd:
                connection, address = http_server.accept()
                connection.setblocking(False)

                fd = connection.fileno()
                poll.register(fd, select.EPOLLIN)
                connections[fd] = connection
                requests[fd] = ''
                responses[fd] = ''
            elif event & select.EPOLLIN:
                data = connections[fileno].recv(1024)

                if data and data.decode() != "QUIT":
                    poll.modify(fileno, select.EPOLLOUT)
                    # responses[fileno] = b"HTTP/1.1 200 OK\r\n\r\n" + data
                    responses[fileno] = b'HTTP/1.0 200 OK\r\n'
                    responses[fileno] += b'Content-Length: 13\r\n\r\n'
                    responses[fileno] += b'Hello, world!'
                    requests[fileno] = ''
                else:
                    print('[{:02d}] exit or hung up'.format(fileno))
                    poll.unregister(fileno)
                    connections[fileno].close()
                    del connections[fileno], requests[fileno], responses[fileno]

            elif event & select.EPOLLOUT:
                bytes_written = connections[fileno].send(responses[fileno])
                responses[fileno] = responses[fileno][bytes_written:]
                poll.modify(fileno, select.EPOLLIN)


if __name__ == '__main__':
    main()
