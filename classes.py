import datetime
from abc import ABC, abstractmethod

class Cliente:
  def __init__(self, endereco):
    self.endereco = endereco
    self.contas = []

  def realizar_transacao(self, conta, transacao):
    transacao.registrar(conta)

  def adicionar_conta(self, conta):
      self.contas.append(conta)
  
class PessoaFisica(Cliente):
  def __init__(self, cpf, nome, data_nascimento, endereco):
    super().__init__(endereco)
    self.cpf = cpf
    self.nome = nome
    self.data_nascimento = data_nascimento

class Conta:
  def __init__(self, numero, cliente):
    self._saldo = 0
    self._numero = numero
    self._agencia = "00000-0"
    self._cliente = cliente
    self._historico = Historico()

  @property
  def saldo(self):
    return self._saldo
  
  @property
  def numero(self):
    return self._numero
  
  @property
  def agencia(self):
    return self._agencia
  
  @property
  def cliente(self):
    return self._cliente
  
  @property
  def historico(self):
    return self._historico
  
  @classmethod
  def nova_conta(cls, cliente, numero):
    return cls(numero, cliente)
  
  def sacar(self, valor):
    if valor > self._saldo:
      print("\n@@@ Operação falhou! Seu saldo é insuficiente. @@@")
      return False
    
    if valor > 0:
      self._saldo -= valor
      print("\n=== Saque realizada com sucesso! ===")
      return True

    return False
  
  def depositar(self, valor):
    if valor > 0:
      self._saldo += valor
      print("\n === Depósito realizado com sucesso! ===")
      return True
    else:
      print("\n@@@ Operação falhou! O valor informado deve ser positiva. @@@")

    return False

class ContaCorrente(Conta):
  def __init__(self, numero, cliente, limite=1000, limite_saques=3):
    super().__init__(numero, cliente)
    self._limite = limite
    self._limite_saques = limite_saques

  def sacar(self, valor):
    numero_saques = len(
      [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
    )

    if valor > self._limite:
      print("\n@@@ Operação falhou! O valor excede o limite. @@@")

    elif numero_saques >= self._limite_saques:
      print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
    
    else:
      return super().sacar(valor)
    
  def __str__(self):
    return f"""\
      Agência:\t{self.agencia}
      C/C:\t\t{self.numero}
      Titular:\t{self.cliente.nome}
    """

class Historico:
  def __init__(self):
    self._transacoes = []

  @property
  def transacoes(self):
    return self._transacoes

  def adicionar_transacao(self, transacao):
    self._transacoes.append(
      {
        "tipo": transacao.__class__.__name__,
        "valor": transacao.valor,
        "data": datetime.datetime.now()
      }
    )

class Transacao(ABC):
  @property
  @abstractmethod
  def valor(self):
    pass

  @abstractmethod
  def registrar(self, conta):
    pass

class Saque(Transacao):
  def __init__(self, valor):
    self._valor = valor

  @property
  def valor(self):
    return self._valor
  
  def registrar(self, conta):
    sucesso_transacao = conta.sacar(self.valor)

    if sucesso_transacao:
      conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
  def __init__(self, valor):
    self._valor = valor

  @property
  def valor(self):
    return self._valor
  
  def registrar(self, conta):
    sucesso_transacao = conta.depositar(self.valor)

    if sucesso_transacao:
      conta.historico.adicionar_transacao(self)
