import socket
import pickle
import json
import pybinn
import time

HOST = '127.0.0.1'
PORT = 8888

token = 'TOKENSERVIDOR'

coord = []


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.send(token.encode())
    res = s.recv(1024)

    print(res.decode())


    while True:
        coord = s.recv(1024)
        coord = pybinn.loads(coord)
        print(coord)
