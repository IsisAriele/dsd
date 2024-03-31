import socket
import unicodedata

def remover_acentos(txt):
    return ''.join((c for c in unicodedata.normalize('NFD', txt) if unicodedata.category(c) != 'Mn')).lower()

def handle_client(conn, addr):
    print(f"Conexão de: {addr}")
    perguntas_respostas = [
    ("Qual a capital da França?", "Paris"),
    ("Qual o maior planeta do sistema solar?", "Júpiter"),
    ("Qual é o rio mais longo do mundo?", "Amazonas"),
    ("Quem escreveu 'Dom Casmurro'?", "Machado"),
    ("Qual o símbolo químico do Oxigênio?", "O"),
    ("Quem pintou a 'Mona Lisa'?", "DaVinci"),
    ("Em que ano o homem pisou na Lua pela primeira vez?", "1969"),
    ("Qual é o maior país do mundo?", "Rússia"),
    ("Quem é conhecido como o pai da relatividade?", "Einstein"),
    ("Qual é a capital do Egito?", "Cairo"),
    ("Qual processo as plantas usam para converter luz em energia?", "Fotosíntese"),
    ("Qual o maior mamífero terrestre?", "Elefante")
]

    try:
        for pergunta, resposta_correta in perguntas_respostas:
            acertou = False
            while not acertou:
                try:
                    conn.sendall(pergunta.encode() + b'\n')
                    resposta_cliente = conn.recv(1024).decode()
                    resposta_cliente = remover_acentos(resposta_cliente).strip()

                    if resposta_cliente == remover_acentos(resposta_correta):
                        msg = "Parabéns! Você acertou.\n"
                        conn.sendall(msg.encode())
                        acertou = True
                    else:
                        msg = "Incorreto. Tente novamente.\n"
                        conn.sendall(msg.encode())

                except BrokenPipeError:
                    print(f"A conexão com {addr} foi perdida.")
                    return
        conn.sendall("Fim do Quiz. Obrigado por participar!\n".encode())
        
    finally:
        conn.close()

def iniciar_servidor():
    host = 'localhost'
    porta = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor_socket:
        servidor_socket.bind((host, porta))
        servidor_socket.listen(5)
        print("Servidor aguardando conexões...")

        try:
            while True:
                conn, addr = servidor_socket.accept()
                handle_client(conn, addr)

        except KeyboardInterrupt:
            print("\nServidor encerrando...")

if __name__ == '__main__':
    iniciar_servidor()