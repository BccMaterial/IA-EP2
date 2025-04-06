###################
### CLASSE BASE ###
###################

class Restricao():
    def __init__(self, variaveis):
        self.variaveis = variaveis

    def esta_satisfeita(self, atribuicao):
        """
        # Definição
        Verifica se a restrição implementada está satisfeita
        
        # Parâmetros
        A atribuição é um dicionário, onde:
        - A chave é a variável
        - O valor é o "valor de domínio" atribuído
        """
        return True

##########################
### AVIÃO - RESTRIÇÕES ###
##########################

# Sabemos que o primeiro slot é embarque, e o último é desembarque
class Manutencao(Restricao):
  def __init__(self, i):
    super().__init__([i])
    self.voo = i

  def esta_satisfeita(self, atribuicao):
    if self.voo not in atribuicao:
      return True
    return atribuicao[self.voo] == (None, None, 0)

# Sabemos também que a origem da primeira viagem é igual ao destino da última 
class OrigemIgualDestino(Restricao):
  def __init__(self, voo1, voo2):
    super().__init__([voo1, voo2])
    self.voo1 = voo1
    self.voo2 = voo2

  def esta_satisfeita(self, atribuicao):
    if self.voo1 not in atribuicao or self.voo2 not in atribuicao:
      return True
    
    return atribuicao[self.voo1][0] == atribuicao[self.voo2][1]

class TempoViagem(Restricao):
  def __init__(self, voo, slots):
    super().__init__([x for x in range(voo, voo + slots)])
    self.slots = [x for x in range(voo, voo + slots)]

  def esta_satisfeita(self, atribuicao):
    if any(atribuicao[slot] not in atribuicao for slot in self.slots):
      return True

    return all(\
      atribuicao[slot] == atribuicao[self.voo] \
      for slot in self.slots \
    )

class TempoEsperado(Restricao):
  def __init__(self, voo, tempo):
    super().__init__([voo])
    self.voo = voo
    self.tempo = tempo

  def esta_satisfeita(self, atribuicao):
    if self.voo not in atribuicao:
      return True
    
    return atribuicao[self.voo][2] == self.tempo

class RotaEspecifica(Restricao):
  def __init__(self, voo, rota):
    super().__init__([voo])
    self.voo = voo
    self.rota = rota

  def esta_satisfeita(self, atribuicao):
    if self.voo not in atribuicao:
      return True

    return atribuicao[self.voo] == self.rota
