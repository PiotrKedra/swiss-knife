import socket
import json


def get_network_settings():
    with open('network_settings.txt') as json_file:
        data = json.load(json_file)
        return data


def service_client(new_socket):
    request = new_socket.recv(1024)
    print(request)

    response = "HTTP/1.1 200 OK\r\n"
    response += "\r\n"
    response += "<h1>Hello Swiss Knife Lab</h1>"
    new_socket.send(response.encode("utf-8"))

    new_socket.close()


def main() -> None:
    # network settings for server
    network_settings = get_network_settings()
    # create sockets
    http_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # prevent port from being occupied and unable to start program
    http_server.setsockopt(socket.SOL_SOCKET, 25, str(network_settings['interface'] + '\0').encode('utf-8'))

    # binding ports
    http_server.bind(('', network_settings['port']))
    # change to listening socket
    http_server.listen(128)
    while True:
        # wait for new client to connect
        client, info = http_server.accept()
        # serve client
        service_client(client)


if __name__ == "__main__":
    main()
