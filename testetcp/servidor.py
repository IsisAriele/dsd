import socket


QUESTOES = [
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

HOST = "localhost"
PORT = 8005

HIGHSCORES = {}

def run_server():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen() 

    print(f"Aguardando conexões em {HOST}:{PORT}")

    try:
        while True:
            client_socket, client_address = servidor.accept()
            questionario(client_socket, client_address)
    except KeyboardInterrupt:
        print("Parando servidor...")
        servidor.close()


def questionario(client_socket, client_address):
    identificador_do_cliente = f"{client_address[0]}:{client_address[1]}"
    print(f"Nova conexão de {identificador_do_cliente}")
    print(f"Pontuações: {HIGHSCORES}")

    nickname = registrar_jogador(client_socket)
    respostas_corretas = 0

    for pergunta, resposta in QUESTOES:
        client_socket.send(pergunta.encode("utf-8"))

        resposta_do_cliente = client_socket.recv(1024)
        resposta_do_cliente = resposta_do_cliente.decode("utf-8")

        if resposta_do_cliente.lower() == resposta.lower():
            respostas_corretas += 1

    salvar_pontuacao(client_socket, nickname, respostas_corretas)
    print(f"Finalizando conexão com {identificador_do_cliente}...")
    client_socket.close()


def registrar_jogador(client_socket):
    client_socket.send("Informe um nickname: ".encode("utf-8"))
    nickname = client_socket.recv(1024)
    nickname = nickname.decode("utf-8")

    HIGHSCORES[nickname] = 0

    return nickname


def salvar_pontuacao(client_socket, nickname, qtd_de_acertos):
    HIGHSCORES[nickname] = qtd_de_acertos
    client_socket.send(f"Pontuação final: {qtd_de_acertos}".encode("utf-8"))

run_server()