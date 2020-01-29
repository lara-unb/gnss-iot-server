import socket
import selectors
import select
import types
import pybinn
import time

import pickle

HOST = '127.0.0.1'
SERVER_PORT = 8888
WEB_PORT = 9999
token = 'TOKENSERVIDOR'


sel = selectors.DefaultSelector()


def sock_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, SERVER_PORT))
    sock.send(token.encode())
    res = sock.recv(1024)
    print(res.decode())
    return sock


def sock_web():
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((HOST, WEB_PORT))
    lsock.listen()
    print("Server for Web App listening on", (HOST, WEB_PORT))
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)


def accetp_wrapper(sock):
    conn, addr = sock.accept()
    print("New Connection from", addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, data_in=[], data_out={})
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask, msg):
    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            recv_data = pickle.loads(recv_data)
            for ids in recv_data:
                if ids not in data.data_in:
                    data.data_in.append(ids)
        else:
            print("Closing connecion ", data.addr)
            sel.unregister(sock)
            sock.close

    else:
        try:
            if msg['id'] in data.data_in:
                msg = pickle.dumps(msg)
                sock.send(msg)

        except:  # Tratar todos os erros
            print("Closing connecion ", data.addr)
            sel.unregister(sock)
            sock.close


def data_server(sock):
    r, w, e = select.select([sock], [], [], None)
    if r:
        data = r[0].recv(1024)
        if data:
            print("Send data to Web App")

            try:
                data = pybinn.loads(data)
                print(data)
                return data
            except:
            	print("Deu erro aqui !")
        else:
            r[0].close()
            return None


if __name__ == "__main__":
    sock = sock_server()
    sock_web()

    try:
        while True:
            events = sel.select(timeout=None)

            data = data_server(sock)
            for key, mask in events:
                if key.data is None:
                    accetp_wrapper(key.fileobj)
                else:
                    service_connection(key, mask, data)
    except KeyboardInterrupt:
        
        print("Handler off...")
    finally:
        sel.close()
