import socket
import threading
import unicodedata

def remover_acentos(txt):
    return ''.join((c for c in unicodedata.normalize('NFD', txt) if unicodedata.category(c) != 'Mn')).lower()

# Lista de questões e respostas
QUESTOES = [
    ("Qual a capital da França?", "Paris"),
    ("Qual o primeiro de quem escreveu 'Dom Casmurro'?", "Machado"),
    ("Qual o maior planeta do sistema solar?", "Júpiter"),
    ("Qual é o rio mais longo do mundo?", "Amazonas"),
    ("Qual o símbolo químico do Oxigênio?", "O"),
    ("Qual o primeiro nome de quem pintou a 'Mona Lisa'?", "Leonardo"),
    ("Em que ano o homem pisou na Lua pela primeira vez?", "1969"),
    ("Qual é o maior país do mundo?", "Rússia"),
    ("Qual é o segundo nome do pai da relatividade?", "Einstein"),
    ("Qual é a capital do Egito?", "Cairo"),
    ("Qual processo as plantas usam para converter luz em energia?", "Fotossíntese"),
    ("Qual o maior mamífero terrestre?", "Elefante")
]

# Configuração do servidor
HOST = "192.168.1.9"
TCP_PORT = 8007
UDP_PORT = 8008
HIGHSCORES = {} # Dicionário para armazenar os pontos dos jogadores

# Servidor UDP para registro de nicknames
def udp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as servidor_udp: 
        servidor_udp.bind((HOST, UDP_PORT)) # Associa o servidor à porta UDP
        print(f"Servidor UDP rodando em {HOST}:{UDP_PORT} para registro de nicknames.")

        while True:
            dados, endereco = servidor_udp.recvfrom(1024) # Recebe os dados do cliente
            nickname = dados.decode('utf-8')
            print(f"Nickname {nickname} registrado de {endereco}")
            HIGHSCORES[nickname] = 0
            servidor_udp.sendto(f"Nickname {nickname} registrado com sucesso!".encode('utf-8'), endereco) 

# Servidor TCP para gerenciar o quiz
def tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor_tcp:
        servidor_tcp.bind((HOST, TCP_PORT))
        servidor_tcp.listen(5) 
        print(f"Aguardando conexões em {HOST}:{TCP_PORT} para o quiz.")

        while True:
            client_socket, client_address = servidor_tcp.accept()
            thread = threading.Thread(target=questionario, args=(client_socket, client_address))
            thread.start()

# Função para gerenciar o quiz para cada jogador
def questionario(client_socket, client_address):
    try:
        identificador_do_cliente = f"{client_address[0]}:{client_address[1]}"
        print(f"Nova conexão de {identificador_do_cliente}")

        client_socket.send("Informe um nickname: ".encode("utf-8"))
        nickname = client_socket.recv(1024).decode("utf-8")

        respostas_corretas = 0
        # Envia as perguntas e verifica as respostas
        for pergunta, resposta in QUESTOES:
            client_socket.send(pergunta.encode("utf-8"))
            resposta_do_cliente = client_socket.recv(1024).decode("utf-8")
            if remover_acentos(resposta_do_cliente.lower()) == remover_acentos(resposta.lower()):
                respostas_corretas += 1

        # Atualiza o placar de pontos do jogador
        salvar_pontuacao(nickname, respostas_corretas)
        client_socket.send(f"Pontuação final: {respostas_corretas}".encode("utf-8"))
        print(f"Finalizando conexão com {identificador_do_cliente}...")
        print(f"Pontuações: {HIGHSCORES}")
    finally:
        client_socket.close()

# Função para salvar a pontuação do jogador
def salvar_pontuacao(nickname, qtd_de_acertos):
    HIGHSCORES[nickname] = max(HIGHSCORES.get(nickname, 0), qtd_de_acertos)

# Inicia o servidor UDP e TCP
if __name__ == "__main__":
    udp_thread = threading.Thread(target=udp_server, daemon=True)
    udp_thread.start()

    tcp_server()
