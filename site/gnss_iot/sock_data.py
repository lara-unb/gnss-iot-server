import pybinn
import select
import socket
from gnss_iot_server.settings import sock, create_connection

def get_data():
    socket_list = [sock]
    read_sockets, write_sockets, error_sockets = select.select(socket_list,[],[],.5)
    if read_sockets:        
        data = read_sockets[0].recv(4096)
        data = pybinn.loads(data) 
        print(sock)
        return data
    else:
        print("ainda não")
        return 0
            