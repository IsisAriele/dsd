import socket

def conectar_servidor():
    host = 'localhost'
    porta = 12345

    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect((host, porta))

    try:
        while True:
            dados = cliente_socket.recv(1024).decode()
            print(dados)

            if "Parabéns!" in dados or "Incorreto." in dados:
                print(dados)
                if "Parabéns!" in dados:
                    break
                else:
                    continue

            resposta = input("Resposta: ")
            cliente_socket.send(resposta.encode())

    finally:
        cliente_socket.close()

if __name__ == '__main__':
    conectar_servidor()