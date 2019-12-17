import pybinn
import select
import socket

HOST = '127.0.0.1'
PORT = 8889

def create_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))        
        return s

    except ConnectionRefusedError as erro_connection:
        print(erro_connection)
        return "No connection"


def get_data(sock):
    sock_list  = [sock]
    read_sockets, write_sockets, error_sockets = select.select(
            sock_list, [], [], None)
    if read_sockets:
        data = read_sockets[0].recv(1024)
        data = pybinn.loads(data)
        return data
    else:
        return "No data"

if __name__ == "__main__":
    
    sock = create_connection()

    while True:
        data = get_data(sock)
        print(data)