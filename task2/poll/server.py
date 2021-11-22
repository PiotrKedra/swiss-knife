import select
import socket


def main():
    http_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_server.setsockopt(socket.SOL_SOCKET, 25, str("wlo1" + '\0').encode('utf-8'))
    http_server.bind(('', 820))
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
                    responses[fileno] = data
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
