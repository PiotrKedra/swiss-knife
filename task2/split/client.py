import socket


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, 25, str("wlo1" + '\0').encode('utf-8'))
    client.connect(('', 834))

    response = "HTTP/1.1 200 OK\r\n"
    response += "\r\n"
    response += "<h1>Hello Swiss Knife Lab</h1>"

    count = 0
    client.sendall(response.encode())
    data = client.recv(1024)
    print('Received', repr(data))
    count+= 1

    client.close()


if __name__ == '__main__':
    main()
