import socket
import pybinn
import select
HOST = '127.0.0.1'
PORT_SERVER = 8888
PORT_WEB = 8889
token = 'TOKENSERVIDOR'


def connection_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT_SERVER))
    sock.send(token.encode())
    res = sock.recv(1024)
    print("Connection Established!")
    print(res.decode())
    return sock


def connection_web():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT_WEB))
    sock.listen()
    return sock


def main():
    sock_server = connection_server()
    sock_web = connection_web()
    connection, address = sock_web.accept()

    while True:
        
        sock_list = [sock_server]
        read_sockets, write_sockets, error_sockets = select.select(
            sock_list, [], [], None)

        if read_sockets:
            data = read_sockets[0].recv(1024)
            print("Send data for Web App")
            connection.send(data)
            data = pybinn.loads(data)
            print(data)
        else:
            print("Ainda nao !")


if __name__ == "__main__":
    main()
