import random
from classes.geneticos.individuo import Individuo
from classes.geneticos.populacao import Populacao
from classes.restricoes.satisfacao_restricoes import SatisfacaoRestricoes
from classes.aviao import Aviao

# OBS: Ao gerar o indivíduo, satisfazer as restrições
class LinhasAereas(Individuo):
  def __init__(self, qtdAvioes):
    self.genes = []
    self.voosNecessarios = 0
    self.qtdAvioes = qtdAvioes
    self.rotasVoo = [
      # Local de partida        Local de chegada          Hrs   Num
      ("São Paulo (GRU)",       "Rio de Janeiro (GIG)",   1.0,  10),
      ("São Paulo (GRU)",       "Brasilia (BSB)",         2.0,  6 ),
      ("São Paulo (GRU)",       "Belo Horizonte (CNF)",   1.5,  8 ),
      ("Rio de Janeiro (GIG)",  "São Paulo (GRU)",        1.0,  10),
      ("Rio de Janeiro (GIG)",  "Brasília (BSB)",         2.0,  5 ),
      ("Rio de Janeiro (GIG)",  "Belo Horizonte (CNF)",   1.5,  6 ),
      ("Brasília (BSB)",        "São Paulo (GRU)",        2.0,  6 ),
      ("Brasília (BSB)",        "Rio de Janeiro (GIG)",   2.0,  5 ),
      ("Brasília (BSB)",        "Belo Horizonte (CNF)",   1.5,  7 ),
      ("Belo Horizonte (CNF)",  "São Paulo (GRU)",        1.5,  8 ),
      ("Belo Horizonte (CNF)",  "Rio de Janeiro (GIG)",   1.5,  6 ),
      ("Belo Horizonte (CNF)",  "Brasília (BSB)",         1.5,  7 )
    ]

    # Sobre o campo abaixo:
    # Inicialmente, não temos nenhum voo
    # Conforme vamos preenchendo as viagens, vamos adicionando nesse array.
    # Com isso, sabemos que a rota SP-RJ já foi preenchida, logo, não precisa 
    # mais de nenhuma rota a mais dessa.
    self.qtdPorRota = [0 for x in self.rotasVoo]

    # Visita cada tupla e retorna o valor total de voos
    self.voosNecessarios = sum([x[3] for x in self.rotasVoo])

    # Gera os genes (Aviões)
    self.gerar_individuo()

  # RESTRIÇÕES
  # qtdVoos == totalVoos 
  # Obs.: Capaz nem de precisar disso.
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
  def __str__(self):
    # Não tem identação na string pra não colocar tab na hora de printar
    return \
    f"""
SENAC Linhas Aéreas
---------------------------------------
Qtd. total de Voos: {self.voosNecessarios}
Qtd. de aviões: {self.qtdAvioes}
"""

  def gerar_individuo(self):
    # Pra cada avião, cria um objeto Aviao
    # for _ in range(self.qtdAvioes):
        # self.genes.append(Aviao(self)) # Tá certo 👍
    pass

class PopulacaoLinhasAereas(Populacao):
  pass
