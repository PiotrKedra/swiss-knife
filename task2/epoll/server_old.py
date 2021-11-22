import socket
import re
import select
import resource

# increase max open connections (while benchmarking with wrk we exceeded limit)
resource.setrlimit(resource.RLIMIT_NOFILE, (65536, 65536))


def service_client(new_socket: object, request: str):

    response_body = "<h1>hello world</h1>"
    resposne = "HTTP/1.1 200 OK\r\n"
    resposne += "Content-Length:%d\r\n" % len(response_body)
    resposne += "\r\n"
    resposne += response_body
    new_socket.send(resposne.encode("utf-8"))


def main():
    http_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    http_server.setsockopt(socket.SOL_SOCKET, 25, str("swissknife0" + '\0').encode('utf-8'))
    http_server.bind(("192.168.55.1", 800))
    http_server.listen(128)
    http_server.setblocking(False)

    epl = select.epoll()
    # Register the FD (file descriptor) corresponding to the listening socket into epoll
    epl.register(http_server.fileno(), select.EPOLLIN)
    # Storing the correspondence between fd file descriptors and sockets
    fd_event_dict: dict = {}
    while True:
        # By default, the blockage will be blocked until the os detects the arrival of data and informs the program by event notification, then the blockage will be removed.
        fd_event_list: list = epl.poll()  # [(socket corresponding file descriptor, what event is this file descriptor),...]
        for fd, event in fd_event_list:
            # If the listener socket has data coming, it waits for a new client connection.
            if fd == http_server.fileno():
                client, info = http_server.accept()
                # Register the new socket into epoll
                epl.register(client.fileno(), select.EPOLLIN)
                # Store the corresponding relationship between file descriptors and sockets in a dictionary
                fd_event_dict[client.fileno()] = client
            elif event == select.EPOLLIN:
                # Determine whether a connected socket has data sent in
                recv_data: str = fd_event_dict[fd].recv(1024).decode("utf-8")
                if recv_data:
                    service_client(fd_event_dict[fd], recv_data)
                else:
                    print("### if no data close connection and removed from epoll FD")
                    fd_event_dict[fd].close()
                    epl.unregister(fd)
                    del fd_event_dict[fd]
        

if __name__ == '__main__':
    main()