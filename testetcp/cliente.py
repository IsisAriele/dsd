import socket

HOST = "192.168.1.9"
TCP_PORT = 8007
UDP_PORT = 8008

def registrar_nickname(nickname):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # Envia o nickname para o servidor via UDP
        s.sendto(nickname.encode('utf-8'), (HOST, UDP_PORT))
        mensagem, _ = s.recvfrom(1024) # Recebe a confirmação do registro
        print(mensagem.decode('utf-8')) # Exibe a mensagem de confirmação

def run_client():
    nickname = input("Digite seu nickname: ")
    registrar_nickname(nickname) # Registra o nickname no servidor

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, TCP_PORT)) # Conecta ao servidor TCP

        s.send(nickname.encode('utf-8'))  # Envia o nickname para o servidor TCP

        while True:
            mensagem_do_servidor = s.recv(1024).decode('utf-8') # Recebe mensagem do servidor

            if "Informe um nickname: " in mensagem_do_servidor:
                continue  # Já enviamos o nickname, então ignoramos esta mensagem

            if "Pontuação final" in mensagem_do_servidor:
                print(mensagem_do_servidor) # Exibe a pontuação final
                break # Encerra o loop

            print(mensagem_do_servidor) # Exibe a pergunta do quiz
            resposta = input("Resposta: ")  # Solicita a resposta ao jogador
            s.send(resposta.encode('utf-8')) # Envia a resposta para o servidor

if __name__ == "__main__":
    run_client()
