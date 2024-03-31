import socket
import threading

def handle_client(conn, addr):
    print(f"Conexão de: {addr}")
    try:
        perguntas_respostas = [
            ("Qual a capital da França?", "paris"),
            ("Qual o maior planeta do sistema solar?", "júpiter"),
        ]
        for pergunta, resposta_correta in perguntas_respostas:
            acertou = False
            while not acertou:
                conn.send(pergunta.encode())
                resposta_cliente = conn.recv(1024).decode().lower().strip()

                if resposta_cliente == resposta_correta:
                    msg = "Parabéns! Você acertou."
                    conn.send(msg.encode())
                    acertou = True  # Sai do loop para a próxima pergunta
                else:
                    msg = "Incorreto. Tente novamente."
                    conn.send(msg.encode())
    finally:
        conn.close()

def iniciar_servidor():
    host = 'localhost'
    porta = 12345

    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind((host, porta))
    servidor_socket.listen(5)
    print("Servidor aguardando conexões...")

    try:
        while True:
            conn, addr = servidor_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

    except KeyboardInterrupt:
        print("\nServidor encerrando...")
    finally:
        servidor_socket.close()

if __name__ == '__main__':
    iniciar_servidor()
