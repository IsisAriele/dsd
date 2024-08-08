import Pyro4
clientes = {}  # Dicionário para armazenar clientes {username: {password, saldo}}

@Pyro4.expose
class BancoServer(object):
    
    def registrar_cliente(self, username, senha):
        if username in clientes:
            return "Usuário já registrado."

        clientes[username] = {'password': senha, 'saldo': 0}
        return "Registro bem-sucedido."

    def autenticar(self, username, senha):
        if username not in clientes:
            return 404
        if clientes[username]['password'] != senha:
            return 401
        return 200

    def consultar_saldo(self, username, senha):
        if self.autenticar(username, senha) == 200:
            return f"Saldo: {clientes[username]['saldo']}"
        return "Dados de autenticação incorretos."

    def depositar(self, username, senha, valor):
        if self.autenticar(username,senha) == 200:
            clientes[username]['saldo'] += valor
            return f"Depósito de {valor} bem-sucedido. Novo saldo: {clientes[username]['saldo']}"
        return "Dados de autenticação incorretos."

    def sacar(self, username, senha, valor):
        if self.autenticar(username, senha) == 200:
            if clientes[username]['saldo'] < valor:
                return "Saldo insuficiente."
            clientes[username]['saldo'] -= valor
            return f"Saque de {valor} bem-sucedido. Novo saldo: {clientes[username]['saldo']}"
        return "Dados de autenticação incorretos."

# Configuração do servidor Pyro
daemon = Pyro4.Daemon() 
uri = daemon.register(BancoServer) # Quando ele registra a classe, retorna uma uri
print("Ready. Object uri =", uri)
daemon.requestLoop()
