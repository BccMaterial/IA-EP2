import random
from classes.geneticos.individuo import Individuo
from classes.geneticos.populacao import Populacao
from classes.restricoes.satisfacao_restricoes import SatisfacaoRestricoes
from classes.aviao import Aviao

# OBS: Ao gerar o indivíduo, satisfazer as restrições
class LinhasAereas(Individuo):
  def __init__(self):
    self.genes = []
    self.totalVoos = 0
    self.qtdAvioes = 0

    # Visita cada tupla e retorna o valor total de voos
    for voo in self.rotasVoo:
        self.totalVoos += voo[3]

  def definir_restricoes(self):
    self.restricoes = SatisfacaoRestricoes(self.variaveis, self.dominios)

  def mutacao(self):
    pass

  def crossover(self):
    pass

  def fitness(self):
    # fitness = qtdAvioes / totalVoos
    return len(self.genes) / self.totalVoos
  
  # Override do "to_string"
  # def __str__(self):
  #   return ""

  def gerar_genes(self):
    for _ in range(self.qtdAvioes):
      novo_aviao = Aviao()
      # Decidir se vai montar tudo quanto inicializar o objeto
      self.genes.append(novo_aviao)

class PopulacaoLinhasAereas(Populacao):
  pass
