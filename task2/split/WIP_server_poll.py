import select, socket, sys, queue


def main():
    http_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_server.setsockopt(socket.SOL_SOCKET, 25, str("wlo1" + '\0').encode('utf-8'))
    http_server.bind(('', 818))
    http_server.listen(128)
    http_server.listen(5)
    http_server.setblocking(False)

    pollObj = select.poll()
    pollObj.register(http_server.fileno(), select.POLLIN)
    fd_event_dict: dict = {}

    while True:
        # By default, the blockage will be blocked until the os detects the arrival of data and informs the program by event notification, then the blockage will be removed.
        fd_event_list: list = pollObj.poll()  # [(socket corresponding file descriptor, what event is this file descriptor),...]
        for fd, event in fd_event_list:
            # If the listener socket has data coming, it waits for a new client connection.
            if fd == http_server.fileno():
                client, info = http_server.accept()
                # Register the new socket into epoll
                pollObj.register(client.fileno(), select.POLLIN)
                # Store the corresponding relationship between file descriptors and sockets in a dictionary
                fd_event_dict[client.fileno()] = client
            elif event == select.POLLIN:
                # Determine whether a connected socket has data sent in
                recv_data: str = fd_event_dict[fd].recv(1024).decode("utf-8")
                if recv_data:
                    connection, addr = http_server.accept()
                    data = connection.recv(1024)
                else:
                    print("### if no data close connection and removed from epoll FD")
                    fd_event_dict[fd].close()
                    pollObj.unregister(fd)
                    del fd_event_dict[fd]


if __name__ == '__main__':
    main()
