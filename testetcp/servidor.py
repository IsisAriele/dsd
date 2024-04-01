import socket
import threading
import unicodedata

def remover_acentos(txt):
    return ''.join((c for c in unicodedata.normalize('NFD', txt) if unicodedata.category(c) != 'Mn')).lower()

# Lista de questões e respostas
QUESTOES = [
    ("Qual a capital da França?", "Paris"),
    ("Qual o maior planeta do sistema solar?", "Júpiter"),
    ("Qual é o rio mais longo do mundo?", "Amazonas"),
    ("Quem escreveu 'Dom Casmurro'?", "Machado de Assis"),
    ("Qual o símbolo químico do Oxigênio?", "O"),
    ("Quem pintou a 'Mona Lisa'?", "Da Vinci"),
    ("Em que ano o homem pisou na Lua pela primeira vez?", "1969"),
    ("Qual é o maior país do mundo?", "Rússia"),
    ("Quem é conhecido como o pai da relatividade?", "Einstein"),
    ("Qual é a capital do Egito?", "Cairo"),
    ("Qual processo as plantas usam para converter luz em energia?", "Fotosíntese"),
    ("Qual o maior mamífero terrestre?", "Elefante")
]

# Configuração do servidor
HOST = "localhost"
TCP_PORT = 8003
UDP_PORT = 8004
HIGHSCORES = {}

# Servidor UDP
def udp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as servidor_udp:
        servidor_udp.bind((HOST, UDP_PORT))
        print(f"Servidor UDP rodando em {HOST}:{UDP_PORT} para registro de nicknames.")

        while True:
            dados, endereco = servidor_udp.recvfrom(1024)
            nickname = dados.decode('utf-8')
            print(f"Nickname {nickname} registrado de {endereco}")
            HIGHSCORES[nickname] = 0
            servidor_udp.sendto(f"Nickname {nickname} registrado com sucesso!".encode('utf-8'), endereco)

# Servidor TCP
def tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor_tcp:
        servidor_tcp.bind((HOST, TCP_PORT))
        servidor_tcp.listen(5)
        print(f"Aguardando conexões em {HOST}:{TCP_PORT} para o quiz.")

        while True:
            client_socket, client_address = servidor_tcp.accept()
            thread = threading.Thread(target=questionario, args=(client_socket, client_address))
            thread.start()

def questionario(client_socket, client_address):
    try:
        identificador_do_cliente = f"{client_address[0]}:{client_address[1]}"
        print(f"Nova conexão de {identificador_do_cliente}")
        print(f"Pontuações: {HIGHSCORES}")

        client_socket.send("Informe um nickname: ".encode("utf-8"))
        nickname = client_socket.recv(1024).decode("utf-8")

        respostas_corretas = 0
        for pergunta, resposta in QUESTOES:
            client_socket.send(pergunta.encode("utf-8"))
            resposta_do_cliente = client_socket.recv(1024).decode("utf-8")
            if resposta_do_cliente.lower() == remover_acentos(resposta.lower()):
                respostas_corretas += 1

        salvar_pontuacao(nickname, respostas_corretas)
        client_socket.send(f"Pontuação final: {respostas_corretas}".encode("utf-8"))
        print(f"Finalizando conexão com {identificador_do_cliente}...")
    finally:
        client_socket.close()

def salvar_pontuacao(nickname, qtd_de_acertos):
    HIGHSCORES[nickname] = max(HIGHSCORES.get(nickname, 0), qtd_de_acertos)

if __name__ == "__main__":
    udp_thread = threading.Thread(target=udp_server, daemon=True)
    udp_thread.start()

    tcp_server()
