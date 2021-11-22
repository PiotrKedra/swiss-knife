import select, socket, sys, queue


def main():
    http_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_server.setsockopt(socket.SOL_SOCKET, 25, str("wlo1" + '\0').encode('utf-8'))
    http_server.bind(('', 834))
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
                data = s.recv(1024)
                if data:
                    message_queues[s].put(data)
                    if s not in outputs:
                        outputs.append(s)
                else:
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()
                    del message_queues[s]

        for s in writable:
            try:
                next_msg = message_queues[s].get_nowait()
            except queue.Empty:
                outputs.remove(s)
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
