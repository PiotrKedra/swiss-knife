import socket

def service_client(new_socket):
    # Accept http requests from browsers
    # GET / HTTP/1.1
    request = new_socket.recv(1024)
    print(request)
    # Return http response
    resposne = "HTTP/1.1 200 OK\r\n"
    resposne += "\r\n"
    resposne += "<h1>hello world</h1>"
    new_socket.send(resposne.encode("utf-8"))

    # Close
    new_socket.close()


def main():
    # Create sockets
    http_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Prevent port from being occupied and unable to start program
    #http_server.setsockopt(socket.SOL_SOCKET, 25, str("swissknife0" + '\0').encode('utf-8'))

    # Binding ports
    http_server.bind(("", 8004))
    # Change to listening socket
    http_server.listen(128)
    while True:
        # Wait to connect to the new client
        client, info = http_server.accept()
        # Serve this client
        service_client(client)


if __name__ == "__main__":
    main()
