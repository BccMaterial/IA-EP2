import random
from classes.geneticos.individuo import Individuo
from classes.geneticos.populacao import Populacao
from classes.restricoes.satisfacao_restricoes import SatisfacaoRestricoes

# OBS: Ao gerar o indivíduo, satisfazer as restrições
class LinhasAereas(Individuo):
  def __init__(self):
    # Lista incluindo o local de partida, chegada, tempo de voo e número de voos
    self.rotasVoo = [ 
      # Local de partida        Local de chegada          Hrs   Num
      ("São Paulo (GRU)",       "Rio de Janeiro (GIG)",   1.0,  10),
      ("São Paulo (GRU)",       "Brasilia (BSB)",         2.0,  6),
      ("São Paulo (GRU)",       "Belo Horizonte (CNF)",   1.5,  8),
      ("Rio de Janeiro (GIG)",  "São Paulo (GRU)",        1.0,  10),
      ("Rio de Janeiro (GIG)",  "Brasília (BSB)",         2.0,  5),
      ("Rio de Janeiro (GIG)",  "Belo Horizonte (CNF)",   1.5,  6),
      ("Brasília (BSB)",        "São Paulo (GRU)",        2.0,  6),
      ("Brasília (BSB)",        "Rio de Janeiro (GIG)",   2.0,  5),
      ("Brasília (BSB)",        "Belo Horizonte (CNF)",   1.5,  7),
      ("Belo Horizonte (CNF)",  "São Paulo (GRU)",        1.5,  8),
      ("Belo Horizonte (CNF)",  "Rio de Janeiro (GIG)",   1.5,  6),
      ("Belo Horizonte (CNF)",  "Brasília (BSB)",         1.5,  7)
    ]
    self.variaveis = []
    self.dominios = {}
    self.genes = []
    self.totalVoos = 0

    # Visita cada tupla e retorna o valor total de voos
    for voo in self.rotasVoo:
        self.totalVoos += voo[3]

  def definir_restricoes(self):
    self.restricoes = SatisfacaoRestricoes(self.variaveis, self.dominios)

  def definir_variaveis(self):
    pass

  def definir_dominios(self):
    pass

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
    self.definir_variaveis()
    self.definir_dominios()
    self.genes = self.restricoes.busca_backtracking()

class PopulacaoLinhasAereas(Populacao):
  pass
