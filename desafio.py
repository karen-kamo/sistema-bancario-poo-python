from classes import Cliente, PessoaFisica, Conta, ContaCorrente, Historico, Transacao, Saque, Deposito


def filtrar_cliente(cpf, clientes):
  clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
  return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
  if not cliente.contas:
    print("\n@@@ Cliente não possui conta! @@@")
    return
  return cliente.contas[0]

def criar_cliente(clientes):
  cpf = input("Informe o CPF (somente números): ")
  cliente = filtrar_cliente(cpf, clientes)

  if cliente:
    print("\n@@@ Já existe cliente com esse CPF! @@@")
    return 
  
  nome = input("Informe o nome completo: ")
  data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
  endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

  cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

  clientes.append(cliente)
  print("\n=== Cliente criado com sucesso! ===")

def criar_conta(numero_conta, clientes, contas):
  cpf = input("Informe o CPF do cliente: ")
  cliente = filtrar_cliente(cpf, clientes)

  if not cliente:
    print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado. @@@")
    return
  
  conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
  contas.append(conta)
  cliente.contas.append(conta)

  print("\n=== Conta criada com sucesso! ===")

def sacar(clientes):
  cpf = input("Informe o CPF do cliente: ")
  cliente = filtrar_cliente(cpf, clientes)

  if not cliente:
    print("\n@@@ Cliente não encontrado! @@@")
    return
  
  valor = float(input("Informe o valor do saque: "))
  transacao = Saque(valor)

  conta = recuperar_conta_cliente(cliente)
  if not conta:
    return
  
  cliente.realizar_transacao(conta, transacao)

def depositar(clientes):
  cpf = input("Informe o CPF do cliente: ")
  cliente = filtrar_cliente(cpf, clientes)

  if not cliente:
    print("\n@@@ Cliente não encontrado! @@@")
    return
  
  valor = float(input("Informe o valor do depósito: "))
  transacao = Deposito(valor)

  conta = recuperar_conta_cliente(cliente)
  if not conta:
    return
  
  cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
  cpf = input("Informe o CPF do cliente: ")
  cliente = filtrar_cliente(cpf, clientes)

  if not cliente:
    print("\n@@@ Cliente não encontrado! @@@")
    return

  conta = recuperar_conta_cliente(cliente)
  if not conta:
    return

  print("\n================ EXTRATO ================")
  transacoes = conta.historico.transacoes

  extrato = ""
  if not transacoes:
    extrato = "Não foram realizadas movimentações."
  else:
    for transacao in transacoes:
      extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

  print(extrato)
  print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
  print("==========================================")

def listar_contas(contas):
  for conta in contas:
    print("=" * 30)
    print(conta)

def main():
  clientes = []
  contas = []

  while True:
    print("""\n
    ========== MENU ==========
    [1]\tNovo usuário
    [2]\tCriar conta
    [3]\tSacar
    [4]\tDepositar
    [5]\tExtrato
    [6]\tListar contas
    [7]\tSair
    """)
    opcao = int(input("Opção desejada: "))

    if opcao == 1:
      criar_cliente(clientes)
    elif opcao == 2:
      numero_conta = len(contas) + 1
      criar_conta(numero_conta, clientes, contas)
    elif opcao == 3:
      sacar(clientes)
    elif opcao == 4:
      depositar(clientes)
    elif opcao == 5:
      exibir_extrato(clientes)
    elif opcao == 6:
      listar_contas(contas)
    elif opcao == 7:
      print("\nObrigado por utilizar nossos serviços!")
      break
    else:
      print("Digite uma opção válida!")

main()


  


