from classes.geneticos.gene import Gene
from classes.restricoes.satisfacao_restricoes import SatisfacaoRestricoes

class Aviao(Gene):
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
    self.dominio = {}

  def definir_restricoes(self):
    self.restricoes = SatisfacaoRestricoes(self.variaveis, self.dominios)

  def definir_variaveis(self):
    self.variaveis = [
      "00:00", "00:30", "01:00", "01:30", "02:00", "02:30",
      "03:00", "03:30", "04:00", "04:30", "05:00", "05:30",
      "06:00", "06:30", "07:00", "07:30", "08:00", "08:30",
      "09:00", "09:30", "10:00", "10:30", "11:00", "11:30",
      "12:00", "12:30", "12:00", "12:30", "13:00", "13:30",
      "14:00", "14:30", "15:00", "15:30", "16:00", "16:30",
      "17:00", "17:30", "18:00", "18:30", "19:00", "19:30",
      "20:00", "20:30", "21:00", "21:30", "22:00", "22:30",
      "23:00", "23:30"
    ]
    possiveisRotas = [(x[0], x[1], x[2]) for x in self.totalVoos]

    for variavel in self.variaveis:
      # As tuplas representam: Origem, Destino, Tempo
      # (None, None, 0) = Tempo ocioso
      self.dominios[variavel] = [(None, None, 0), *possiveisRotas]

  def gerar_gene(self):
    self.definir_variaveis()
    self.rota = self.restricoes.busca_backtracking()
