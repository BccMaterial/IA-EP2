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
    # Não sei se vai precisar desses dois ifs comentados
    # if self.slot[0] == None and self.voo_i == 0:
    #   return True
    # if self.slot[0] is not None and self.voo_i == 0:
    #   return False
    if self.voo1 not in atribuicao or self.voo2 not in atribuicao:
      return True
    
    return atribuicao[self.voo1][0] == atribuicao[self.voo2][1]

class DestinoIgualOrigem(Restricao):
  def __init__(self, voo1, voo2):
    super().__init__([voo1, voo2])
    self.voo1 = voo1
    self.voo2 = voo2

  def esta_satisfeita(self, atribuicao):
    if self.voo_atual not in atribuicao or self.proximo_voo not in atribuicao:
      return True

    # Se algum dos slots é manutenção, não há restrição
    if atribuicao[self.voo2] == (None, None, 0) or atribuicao[self.voo1] == (None, None, 0):
      return True

    # Verifica se o destino do voo_atual == origem do proximo_voo
    return atribuicao[self.voo1][1] == atribuicao[self.voo2][0]

class TempoViagem(Restricao):
  def __init__(self, voo, slots):
    super().__init__([x for x in range(voo, voo + slots)])
    self.slots = [x for x in range(voo, voo + slots)]

  def esta_satisfeita(self, atribuicao):
    # Qualquer atribuicao não preenchida, retorna True
    if any(atribuicao[slot] not in atribuicao for slot in self.slots):
      return True

    return all(atribuicao[slot] == atribuicao[self.voo] for slot in self.slots)

