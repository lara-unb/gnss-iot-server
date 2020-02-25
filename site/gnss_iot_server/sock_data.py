
import selectors
import types
import socket
import pybinn
import time

HOST = '127.0.0.1'
PORT = 8888
token = 'TOKENSERVIDOR'


def create_connection(ids, sel):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
        s.setblocking(False)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(data_in=[], data_out=[])
        sel.register(s, events, data=data)
        s.send(token.encode())
        ids.append("none")
        s.send(pybinn.dumps(ids))

    except ConnectionRefusedError as erro_connection:
        print(erro_connection)


def get_data(key, mask, sel):

    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        dados = sock.recv(1024)
        if dados:
            dados_decode = pybinn.loads(dados)
            return dados_decode
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
