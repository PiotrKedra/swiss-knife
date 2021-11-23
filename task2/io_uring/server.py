import socket
import time
from liburing import *
import errno


EVENT_TYPE_ACCEPT = 0
EVENT_TYPE_READ = 1
EVENT_TYPE_WRITE = 2

def add_accept_request(ring, server_socket, client_addr, client_addr_len):
    sqe = io_uring_get_sqe(ring)
    io_uring_prep_accept(sqe, server_socket, client_addr, client_addr_len, 0)
    io_uring_sqe_set_data(sqe, EVENT_TYPE_ACCEPT)
    io_uring_submit(ring)

def add_read_request(ring, client_socket):
    buffer = bytearray(1024)
    iov = iovec(buffer)

    sqe = io_uring_get_sqe(ring)
    io_uring_prep_readv(sqe, client_socket, iov[0].iov_base, iov[0].iov_len, 0)
    io_uring_sqe_set_data(sqe, EVENT_TYPE_READ)
    io_uring_submit(ring)

def add_write_request(ring, client_socket):
    sqe = io_uring_get_sqe(ring) # sqe(submission queue entry)
    response_body = "<h1>hello world</h1>"
    resposne = "HTTP/1.1 200 OK\r\n"
    resposne += "Content-Length:%d\r\n" % len(response_body)
    resposne += "\r\n"
    response = resposne.encode("utf-8")
    buffer = bytearray(response)
    iov = iovec(buffer)

    sqe = io_uring_get_sqe(ring)
    io_uring_prep_writev(sqe, client_socket, iov[0].iov_base, iov[0].iov_len, 0)
    io_uring_sqe_set_data(sqe, EVENT_TYPE_WRITE)
    io_uring_submit(ring)

def add_close_request(ring, client_socket):
    sqe = io_uring_get_sqe(ring)
    io_uring_prep_close(sqe, client_socket)
    io_uring_submit(ring)


ring = io_uring()
cqes = io_uring_cqes()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, True)
sock.bind(("", 8000))
sock.listen(128)
sockfd = sock.fileno()

try:
    
    io_uring_queue_init(256, ring, 0)
    cqes = io_uring_cqes()
    addr, addrlen = sockaddr()

    add_accept_request(ring, sockfd, addr, addrlen)

    client_sockets = []
    close_sockets = []

    while(True):

        print('Loop iteration...')
        io_uring_wait_cqe(ring, cqes)

        # get current request from the queue
        cqe = cqes[0]

        # handle io_uring errors
        if(cqe.res < 0):
            print('# Error (' + str(cqe.res) + ') ' + errno.errorcode[abs(cqe.res)] + ' in event_type: ' + str(cqe.user_data))
            print('Exiting...')
            exit()
        else:
            print('No error. Code ' + str(cqe.res) + '. While event_type: ' + str(cqe.user_data))

        
        if(cqe.user_data == EVENT_TYPE_ACCEPT):
            add_accept_request(ring, sockfd, addr, addrlen)
            # here as cqe.res we should get client_socket as a result from accept request?
            add_write_request(ring, cqe.res)
            close_sockets.append(cqe.res)

        # elif(cqe.user_data == EVENT_TYPE_READ):
        #     client_socket = client_sockets.pop(0)
        #     add_write_request(ring, client_socket)
        #     close_sockets.append(client_socket)

        elif(cqe.user_data == EVENT_TYPE_WRITE):
            client_socket = close_sockets.pop(0)
            add_close_request(ring, client_socket)
        

        # clear current request & move to next
        io_uring_cqe_seen(ring, cqe)

        # sleep to see output
        time.sleep(2)

finally:
    sock.close()
    io_uring_queue_exit(ring)
