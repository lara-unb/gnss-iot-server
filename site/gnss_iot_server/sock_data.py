import pybinn
import select
import socket

import pickle

HOST = '127.0.0.1'
PORT = 8889

FAILURE_SOCK = -1


def create_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))        
        return s

    except ConnectionRefusedError as erro_connection:
        print(erro_connection)
        return FAILURE_SOCK

def get_data(sock):
    sock_list  = [sock]
    read_sockets, write_sockets, error_sockets = select.select(
            sock_list, [], [], None)
    if read_sockets:
        data = read_sockets[0].recv(1024)
        data = pickle.loads(data)
        return data
    else:
        return "No data"

if __name__ == "__main__":
    sock = create_connection()
    if sock is not  FAILURE_SOCK:
        while True:
            data = get_data(sock)
            print(data)