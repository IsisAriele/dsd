import socket

HOST = 'localhost'
TCP_PORT = 8007
UDP_PORT = 8008

def registrar_nickname(nickname):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(nickname.encode('utf-8'), (HOST, UDP_PORT))
        mensagem, _ = s.recvfrom(1024)
        print(mensagem.decode('utf-8'))

def run_client():
    nickname = input("Digite seu nickname: ")
    registrar_nickname(nickname)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, TCP_PORT))

        s.send(nickname.encode('utf-8'))

        while True:
            mensagem_do_servidor = s.recv(1024).decode('utf-8')

            if "Informe um nickname: " in mensagem_do_servidor:
                continue  # Já enviamos o nickname, então ignoramos esta mensagem

            if "Pontuação final" in mensagem_do_servidor:
                print(mensagem_do_servidor)
                break

            print(mensagem_do_servidor)
            resposta = input("Resposta: ")
            s.send(resposta.encode('utf-8'))

if __name__ == "__main__":
    run_client()
