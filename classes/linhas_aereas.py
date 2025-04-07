import random
from classes.geneticos.individuo import Individuo
from classes.geneticos.populacao import Populacao
from classes.restricoes.satisfacao_restricoes import SatisfacaoRestricoes
from classes.aviao import Aviao

# OBS: Ao gerar o indivíduo, satisfazer as restrições
class LinhasAereas(Individuo):
  def __init__(self):
    self.genes = []
    self.voosNecessarios = 0
    self.qtdAvioes = random.randint(2, 12)
    self.chanceMutacao = 0.3
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
    self.qtdPorRota = [0 for _ in self.rotasVoo]

    # Visita cada tupla e retorna o valor total de voos
    self.voosNecessarios = sum([x[3] for x in self.rotasVoo])
    self.totalVoos = 0

    # Gera os genes (Aviões)
    self.gerar_individuo()

  def mutacao(self):
    """
    Com base na probabilidade da mutação, decide se vai alterar o indivíduo, ou
    se vai mantê-lo como está atualmente.
    """
    if random.randint(0, 100) / 100 >= self.chanceMutacao:
      return self
    return LinhasAereas()

  def crossover(self):
    pass

  def fitness(self):
    """
    Calcula com base na quantidade de aviões, voos e voos necessários.
    A função escolhida determina com essas variáveis o quão próximo está de um
    indivíduo bom. Quanto menos aviões e mais voos, mais próximo de 0 estará.

    Obs.: O algoritmo genético vai sempre escolher o melhor indivíduo, mesmo que
    Passe da quantidade de voos necessários.
    """
    # qtdAvioes, voosNecessarios, totalVoos
    k = 236
    return (1 - (self.qtdAvioes / (self.qtdAvioes + k))) * ((self.totalVoos / self.voosNecessarios)**2)
    # return (self.totalVoos / self.qtdAvioes) * self.voosNecessarios
  
  # Override do "to_string"
  def __str__(self):
    return self.imprime()

  def imprime(self):
    # Não tem identação na string pra não colocar tab na hora de printar
    return \
    f"""
SENAC Linhas Aéreas
---------------------------------------
Qtd. total de Voos: {self.totalVoos}
Qtd. voos necessários: {self.voosNecessarios}
Qtd. de aviões: {self.qtdAvioes}
"""

  def gerar_individuo(self):
    """
    Pra cada avião, cria um objeto Aviao. Ao criar um objeto Aviao novo,
    É gerado um gene, onde possui a rota do avião, criada de forma aleatória
    """
    for _ in range(self.qtdAvioes):
      aviao = Aviao(self)
      self.genes.append(aviao)
      self.totalVoos += aviao.qtdVoos

class PopulacaoLinhasAereas(Populacao):
  def __init__(self, Individuo_classe, tamanho_populacao=10):
    super().__init__(Individuo_classe, tamanho_populacao)
    self.chanceCrossover = 0.2
  
  def inicializacao(self):
    pass
  
  def mutacao(self):
    return super().mutacao()
  
  def crossover(self):
    """
    Overview
    O crossover divide a população em dois grupos, e para cada indivíduo nos dois grupos,
    pegar uma quantidade aleatória de genes de cada um, e a partir disso, cria dois
    novos indivíduos.
    """
    if random.randint(0, 100) / 100 >= self.chanceCrossover:
      return self.populacao

    tamanho_pop = len(self.populacao)
    populacao1 = self.populacao[:tamanho_pop // 2]
    populacao2 = self.populacao[tamanho_pop // 2:]
    
    nova_populacao = []
    for ind1, ind2 in zip(populacao1, populacao2):
        ponto_corte = random.randint(1, len(ind1.genes) - 1)
        filho1 = ind1.genes[:ponto_corte] + ind2.genes[ponto_corte:]
        filho2 = ind2.genes[:ponto_corte] + ind1.genes[ponto_corte:]
        nova_populacao.extend([filho1, filho2])
    return nova_populacao

