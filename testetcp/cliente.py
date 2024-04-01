import socket


def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    HOST = "localhost"
    PORT = 8003
    client.connect((HOST, PORT))

    while True:
        mensagem_do_servidor = client.recv(1024)
        mensagem_do_servidor = mensagem_do_servidor.decode("utf-8")
        if "Pontuação final" in mensagem_do_servidor:
            print(mensagem_do_servidor)
            break

        print(mensagem_do_servidor)
        msg = input("Resposta: ")
        client.send(msg.encode("utf-8")[:1024])

run_client()