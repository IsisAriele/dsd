import Pyro4

uri = input("Qual é o URI do objeto banco? ").strip()
banco = Pyro4.Proxy(uri)

def menu():
    print("\nMenu:")
    print("1. Registrar")
    print("2. Login")
    print("3. Consultar Saldo")
    print("4. Depositar")
    print("5. Sacar")
    print("6. Sair")
    return input("Escolha uma opção: ").strip()

def main():
    username = None
    password = None
    while True:
        opcao = menu()
        if opcao == '1':
            username = input("Digite seu nome de usuário: ").strip()
            password = input("Digite sua senha: ").strip()
            print(f"\n >>> {banco.registrar_cliente(username, password)}")
        elif opcao == '2':
            username = input("Digite seu nome de usuário: ").strip()
            password = input("Digite sua senha: ").strip()
            print(f"\n >>> {banco.autenticar(username, password)}")
        elif opcao == '3':
            if username and password:
                print(f"\n >>> {banco.consultar_saldo(username, password)}")
            else:
                print("\n >>> Por favor, faça login primeiro.")
        elif opcao == '4':
            if username and password:
                valor = float(input("Digite o valor para depositar: ").strip())
                print(f"\n >>> {banco.depositar(username, password, valor)}")
            else:
                print("\n >>> Por favor, faça login primeiro.")
        elif opcao == '5':
            if username and password:
                valor = float(input("Digite o valor para sacar: ").strip())
                print(f"\n >>> {banco.sacar(username, password, valor)}")
            else:
                print("\n >>> Por favor, faça login primeiro.")
        elif opcao == '6':
            print("\n >>> Saindo...")
            break
        else:
            print("\n >>> Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
