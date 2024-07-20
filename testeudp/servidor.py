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
PORT = 8003

HIGHSCORES = {}

def run_server():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.bind((HOST, PORT))

    print(f"Aguardando conexões em {HOST}:{PORT}")

    try:
        while True:
            data, client_address = servidor.recvfrom(1024)
            questionario(servidor, client_address, data)
    except KeyboardInterrupt:
        print("Parando servidor...")
        servidor.close()

def questionario(servidor, client_address, data):
    identificador_do_cliente = f"{client_address[0]}:{client_address[1]}"
    print(f"Nova conexão de {identificador_do_cliente}")
    print(f"Pontuações: {HIGHSCORES}")

    nickname = registrar_jogador(servidor, client_address)

    respostas_corretas = 0
    for pergunta, resposta in QUESTOES:
        servidor.sendto(pergunta.encode("utf-8"), client_address)

        resposta_do_cliente, _ = servidor.recvfrom(1024)
        resposta_do_cliente = resposta_do_cliente.decode("utf-8")

        if resposta_do_cliente.lower() == resposta.lower():
            respostas_corretas += 1

    salvar_pontuacao(servidor, client_address, nickname, respostas_corretas)
    print(f"Finalizando conexão com {identificador_do_cliente}...")

def registrar_jogador(servidor, client_address):
    servidor.sendto("Informe um nickname: ".encode("utf-8"), client_address)
    nickname, _ = servidor.recvfrom(1024)
    nickname = nickname.decode("utf-8")

    HIGHSCORES[nickname] = 0

    return nickname

def salvar_pontuacao(servidor, client_address, nickname, qtd_de_acertos):
    HIGHSCORES[nickname] = qtd_de_acertos
    servidor.sendto(f"Pontuação final: {qtd_de_acertos}".encode("utf-8"), client_address)

run_server()
