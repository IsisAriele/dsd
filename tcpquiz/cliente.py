import socket

# Definindo o endereço IP e a porta do servidor
HOST = "localhost"
PORT = 5000

# Criando o socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectando ao servidor
client_socket.connect((HOST, PORT))

# Recebendo as perguntas e alternativas
for i in range(5):
    pergunta = client_socket.recv(1024).decode()
    print(pergunta)
    for j in range(4):
        alternativa = client_socket.recv(1024).decode()
        print(alternativa)

    # Escolhendo a resposta
    resposta = input("Digite sua resposta: ")

    # Enviando a resposta para o servidor
    client_socket.send(resposta.encode())

# Recebendo a pontuação
pontuacao = client_socket.recv(1024).decode()
print(pontuacao)

# Fechando o socket
client_socket.close()