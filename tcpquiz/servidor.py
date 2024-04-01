import socket

# Definindo a porta e o endereço IP
HOST = "localhost"
PORT = 5000

# Criando o socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associando o socket ao endereço e porta
server_socket.bind((HOST, PORT))

# Abrindo o socket para escuta
server_socket.listen()

# Aceitando a conexão do cliente
client_socket, client_address = server_socket.accept()

# Perguntas e alternativas
perguntas = [
    "Qual é o maior país do mundo em extensão territorial?",
    "Qual é a capital da Austrália?",
    "Qual é o rio mais longo do mundo?",
    "Qual é o maior oceano do mundo?",
    "Qual é a fórmula química da água?",
]

alternativas = [
    ["a) China", "b) Rússia", "c) Canadá", "d) Estados Unidos"],
    ["a) Sydney", "b) Melbourne", "c) Canberra", "d) Brisbane"],
    ["a) Nilo", "b) Amazonas", "c) Mississipi", "d) Yangtze"],
    ["a) Pacífico", "b) Atlântico", "c) Índico", "d) Ártico"],
    ["a) H2O", "b) CO2", "c) NaCl", "d) H2SO4"],
]

# Enviando as perguntas e alternativas para o cliente
for i in range(len(perguntas)):
    client_socket.send(f"{perguntas[i]}\n".encode())
    for j in range(len(alternativas[i])):
        client_socket.send(f"{alternativas[i][j]}\n".encode())

# Recebendo as respostas do cliente
respostas_cliente = []
for i in range(len(perguntas)):
    resposta_cliente = client_socket.recv(1024).decode()
    respostas_cliente.append(resposta_cliente)

# Calculando a pontuação
pontuacao = 0
for i in range(len(perguntas)):
    if respostas_cliente[i] == "a":
        pontuacao += 1

# Enviando a pontuação para o cliente
client_socket.send(f"Sua pontuação foi: {pontuacao}".encode())

# Fechando os sockets
client_socket.close()
server_socket.close()