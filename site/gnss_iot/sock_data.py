from gnss_iot_server.settings import sock
import pybinn

def get_data(token_device):
    dados = sock.recv(1024)
    dados = pybinn.loads(dados)
    print(dados["id"])
    print(token_device)
    if dados["id"] == token_device:
        return dados["coord"]
