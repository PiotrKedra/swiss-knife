import json
import os
import queue
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
        f"fe80::e63d:1aff:fe72:f1%{network_settings['interface']}",
        network_settings['port'],
        socket.AF_INET6,
        socket.SOCK_STREAM
    )
    (family, sock_type, proto, canon_name, sock_address) = address_info[0]
    http_server = socket.socket(family, sock_type, proto)
    http_server.bind(('', network_settings['port']))

    http_server.listen(128)
    http_server.listen(5)
    inputs = [http_server]
    outputs = []
    message_queues = {}

    while inputs:
        readable, writable, exceptional = select.select(
            inputs, outputs, inputs)
        for s in readable:
            if s is http_server:
                connection, client_address = s.accept()
                connection.setblocking(0)
                inputs.append(connection)
                message_queues[connection] = queue.Queue()
            else:
                try:
                    data = s.recv(1024)
                    if data:
                        content_length = str(len(data)).encode()
                        response = b'HTTP/1.0 200 OK\r\n'
                        response += b'Content-Length: ' + content_length + b'\r\n\r\n'
                        response += data
                        message_queues[s].put(data)
                        if s not in outputs:
                            outputs.append(s)
                    else:
                        if s in outputs:
                            outputs.remove(s)
                        inputs.remove(s)
                        s.close()
                        del message_queues[s]
                except ConnectionResetError:
                    inputs.remove(s)
                    if s in outputs:
                        outputs.remove(s)
                    s.close()
                    del message_queues[s]

        for s in writable:
            try:
                next_msg = message_queues[s].get_nowait()
            except queue.Empty:
                outputs.remove(s)
            except KeyError:
                s.close()
            else:
                s.send(next_msg)

        for s in exceptional:
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del message_queues[s]


if __name__ == '__main__':
    main()
