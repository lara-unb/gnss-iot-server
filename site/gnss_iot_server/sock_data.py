import pybinn
import socket
import types
import selectors

import pickle

HOST = '127.0.0.1'
PORT = 9999


ids = ["3236D37B277EC67E4C49929986AC6CED"]


def create_connection(ids, sel):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((HOST, PORT))
        s.setblocking(False)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(data_in=[], data_out=[])
        sel.register(s, events, data=data)
        s.send(pickle.dumps(ids))

    except ConnectionRefusedError as erro_connection:
        print(erro_connection)


def get_data(key, mask, sel):

    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        dados = sock.recv(1024)
        if dados:
            dados = pickle.loads(dados)
            print(dados)
            return dados
        else:
            sel.unregister(sock)
            sock.close()
            return None
    else:
        return None

if __name__ == "__main__":

    sel = selectors.DefaultSelector()
    sock = create_connection(ids, sel)

    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data != None:
                get_data(key, mask, sel)
