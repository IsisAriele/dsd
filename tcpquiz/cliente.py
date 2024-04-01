import socket

def conectar_servidor():
    host = 'localhost'
    porta = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente_socket:
        cliente_socket.connect((host, porta))

        try:
            while True:
                dados = cliente_socket.recv(1024).decode()
                
                if "Fim do Quiz" in dados:
                    print(dados)
                    break

                print(dados, end='')
                if "Parabéns!" in dados or "Incorreto." in dados:
                    continue

                resposta = input()
                cliente_socket.sendall(resposta.encode() + b'\n')

        except Exception as e:
            print("Ocorreu um erro:", e)

if __name__ == '__main__':
    conectar_servidor()
