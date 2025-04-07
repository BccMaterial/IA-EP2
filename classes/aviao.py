from classes.geneticos.gene import Gene
from classes.restricoes.satisfacao_restricoes import SatisfacaoRestricoes
import classes.restricoes.restricoes as restricoes
import random

class Aviao(Gene):
  def __init__(self, linhas_aereas = None):
    # Lista incluindo o local de partida, chegada, tempo de voo e número de voos
    # As tuplas representam: Origem, Destino, Tempo
    # (None, None, 0) = Tempo ocioso
    self.rotasVoo = [ 
      # Local de partida        Local de chegada          Hrs (Tempo restante)
      ("São Paulo (GRU)",       "Rio de Janeiro (GIG)",   1.0),
      ("São Paulo (GRU)",       "Brasília (BSB)",         2.0),
      ("São Paulo (GRU)",       "Belo Horizonte (CNF)",   1.5),
      ("Rio de Janeiro (GIG)",  "São Paulo (GRU)",        1.0),
      ("Rio de Janeiro (GIG)",  "Brasília (BSB)",         2.0),
      ("Rio de Janeiro (GIG)",  "Belo Horizonte (CNF)",   1.5),
      ("Brasília (BSB)",        "São Paulo (GRU)",        2.0),
      ("Brasília (BSB)",        "Rio de Janeiro (GIG)",   2.0),
      ("Brasília (BSB)",        "Belo Horizonte (CNF)",   1.5),
      ("Belo Horizonte (CNF)",  "São Paulo (GRU)",        1.5),
      ("Belo Horizonte (CNF)",  "Rio de Janeiro (GIG)",   1.5),
      ("Belo Horizonte (CNF)",  "Brasília (BSB)",         1.5),
      (None,                    None,                     0)
    ]
    
    # Vamos precisar da classe LinhasAereas as seguintes info:
    # - Qtd de aviões
    # - Qtd de viagens já preenchidas
    # - Qtd de viagens necessárias
    self.linhas_aereas = linhas_aereas
    self.rota = None
    self.variaveis = []
    self.dominios = {}
    # While pra evitar solução impossível (caso haja)
    while self.rota is None:
      self.gerar_gene()
    # self.qtdVoos = len(self.rota)

  def definir_restricoes(self):
    """
    Com base nas restrições do problema, adicionamos as restrições das rotas.
    A definição das restrições é feita de forma aleatória, ou seja, a rota traçada
    pelo avião (gene) é randomizada, mas sempre é mantido como manutenção os dois primeiros
    slots (00:00 e 00:30), e o último (23:30).
    """
    self.restricoes = SatisfacaoRestricoes(self.variaveis, self.dominios)
    # Restrições de manutenção fixas
    self.restricoes.adicionar_restricao(restricoes.Manutencao(0))
    self.restricoes.adicionar_restricao(restricoes.Manutencao(1))
    self.restricoes.adicionar_restricao(restricoes.Manutencao(47))

    # Definição da primeira viagem:
    # Escolhe a primeira rota (Juntamente com o aeroporto de origem) 
    ultima_rota = random.choice(self.rotasVoo[:-1])
    origem_rota = ultima_rota[0]
    # Essa variável sempre vai ser a quantidade de slots que a rota vai ocupar
    tempo_viagem = int(ultima_rota[2] * 2)
    ultimo_indice = 2

    # Para cada slot, seta a restrição "RotaEspecifica", com o indice e a rota escolhida
    for i in range(ultimo_indice, ultimo_indice + tempo_viagem):
      self.restricoes.adicionar_restricao(restricoes.RotaEspecifica(i, ultima_rota))
    self.qtdVoos += 1 # Incrementa a quantidade de voos, para ser usado pela classe "LinhasAereas"

    # Incrementa com a quantidade de slots, para sabermos sempre qual é o índice atual
    ultimo_indice += tempo_viagem
    # Entre as viagens, sempre há 3 slots de manutenção (que é o embarque e desembarque)
    for i in range(0, 3):
      self.restricoes.adicionar_restricao(restricoes.Manutencao(ultimo_indice + i))
    ultimo_indice += 3 # Somamos também o slot de manutenção

    # print(f"limite_fim: {limite_fim}")

    # Até o slot 47, tentaremos definir rotas de forma aleatória
    while ultimo_indice < 47:
      ultimo_destino = ultima_rota[1]
      # Algumas rotas não conseguem preencher todos os horários sempre, então
      # randomizamos até chegar perto do final.

      # O numero 10 foi escolhido fazendo testes, se passar disso, corre o risco de dar erro
      if 48 - ultimo_indice > 10:
        # Com base no destino da última viagem, decide a próxima rota
        proximas_rotas = [x for x in self.rotasVoo if x[0] == ultimo_destino]
        proxima_rota = random.choice(proximas_rotas)
        tempo_viagem = int(proxima_rota[2] * 2)

        # Adiciona as restrições para os slots
        for i in range(ultimo_indice, ultimo_indice + tempo_viagem):
          self.restricoes.adicionar_restricao(restricoes.RotaEspecifica(i, proxima_rota))

        ultimo_indice += tempo_viagem
        for i in range(0, 3):
          self.restricoes.adicionar_restricao(restricoes.Manutencao(ultimo_indice + i))
        ultimo_indice += 3
        ultima_rota = proxima_rota # A próxima rota que tinhamos escolhido vira a última rota que o avião passou
        self.qtdVoos += 1 # Incrementamos a quantidade de voos aqui também
      else:
        # Caso estejamos perto do fim, voltamos ao aeroporto de origem
        proximas_rotas = [x for x in self.rotasVoo if x[0] == ultimo_destino and x[1] == origem_rota]
        proxima_rota = proximas_rotas[0] if len(proximas_rotas) > 0 else None

        # Não dá tempo de fazer outras viagens, então entrará em manutenção
        # Esse if é caso o avião já esteja no aeroporto de origem, com isso,
        # Os índices restantes serão de manutenção.
        if proxima_rota is None:
          for i in range(ultimo_indice, 47):
            self.restricoes.adicionar_restricao(restricoes.Manutencao(i))
          break

        # Caso não esteja no aeroporto de origem, traçaremos uma rota até lá,
        # e então, os índices restantes serão de manutenção (caso haja)
        tempo_viagem = int(proxima_rota[2] * 2)
        for i in range(ultimo_indice, ultimo_indice + tempo_viagem):
          self.restricoes.adicionar_restricao(restricoes.RotaEspecifica(i, proxima_rota))
        ultimo_indice += tempo_viagem
        self.qtdVoos += 1

        for i in range(ultimo_indice, 47):
          self.restricoes.adicionar_restricao(restricoes.Manutencao(i))
          ultimo_indice += 1

  def definir_variaveis(self):
    # "00:00", "00:30", "01:00", "01:30", "02:00", "02:30",
    # "03:00", "03:30", "04:00", "04:30", "05:00", "05:30",
    # "06:00", "06:30", "07:00", "07:30", "08:00", "08:30",
    # "09:00", "09:30", "10:00", "10:30", "11:00", "11:30",
    # "12:00", "12:30", "13:00", "13:30", "14:00", "14:30",
    # "15:00", "15:30", "16:00", "16:30", "17:00", "17:30",
    # "18:00", "18:30", "19:00", "19:30", "20:00", "20:30",
    # "21:00", "21:30", "22:00", "22:30", "23:00", "23:30",
    # Tive que mudar, pra ficar mais fácil de lidar com os dados
    # TODO: Conversão pra leitura (0 = "00:00", 1 = "00:30"...)

    # 0 -> 00:00, 1 -> 00:30, 2 -> 01:00 ...
    self.variaveis = list(range(0, 48))

    # O domínio do gene são as rotas
    for variavel in self.variaveis:
      self.dominios[variavel] = self.rotasVoo

  def gerar_gene(self):
    self.qtdVoos = 0
    self.definir_variaveis()
    self.definir_restricoes()
    self.rota = self.restricoes.busca_backtracking()
