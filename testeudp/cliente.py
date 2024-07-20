import socket

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    HOST = "localhost"
    PORT = 8003

    while True:
        client.sendto("Conectar".encode("utf-8"), (HOST, PORT))

        while True:
            mensagem_do_servidor, _ = client.recvfrom(1024)
            mensagem_do_servidor = mensagem_do_servidor.decode("utf-8")
            if "Pontuação final" in mensagem_do_servidor:
                print(mensagem_do_servidor)
                break

            print(mensagem_do_servidor)
            msg = input("Resposta: ")
            client.sendto(msg.encode("utf-8")[:1024], (HOST, PORT))

        resposta = input("Deseja jogar novamente? (S/N): ")
        if resposta.lower() != "s":
            break

    client.close()

run_client()
