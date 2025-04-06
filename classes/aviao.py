from classes.geneticos.gene import Gene
from classes.restricoes.satisfacao_restricoes import SatisfacaoRestricoes
import classes.restricoes.restricoes as restricoes
import random

class Aviao(Gene):
  def __init__(self, linhas_aereas):
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
    while self.rota is None:
      self.gerar_gene_backtracking()
    self.qtdVoos = len(self.rota)

  def definir_restricoes(self):
    self.restricoes = SatisfacaoRestricoes(self.variaveis, self.dominios)
    # Restrições de manutenção fixas
    self.restricoes.adicionar_restricao(restricoes.Manutencao(0))
    self.restricoes.adicionar_restricao(restricoes.Manutencao(1))
    self.restricoes.adicionar_restricao(restricoes.Manutencao(47))

    # Definição da primeira viagem:
    # Pega primeira cidade (Q foi sorteada)
    ultima_rota = random.choice(self.rotasVoo[:-1])
    print(f"Primeira rota: {ultima_rota}")
    tempo_viagem = int(ultima_rota[2] * 2)
    ultimo_indice = 2
    
    ###############################
    ### Restrição destino final ###
    ###############################

    possives_rotas_finais = [x for x in self.rotasVoo if x[0] == ultima_rota[1]]
    rota_final = random.choice(possives_rotas_finais)
    rota_final_tempo = int(rota_final[2] * 2)

    # Até quando o while vai:
    limite_fim = 46 - rota_final_tempo - 4
    limite_inicio = ultimo_indice + tempo_viagem + 3

    # Manutenções da última rota
    for i in range(47 - rota_final_tempo, 47):
      self.restricoes.adicionar_restricao(restricoes.TempoEsperado(i, float(rota_final_tempo / 2)))
      self.restricoes.adicionar_restricao(restricoes.OrigemIgualDestino(2, i))
      self.restricoes.adicionar_restricao(restricoes.OrigemIgualDestino(i, 47 - rota_final_tempo - 4))

    self.restricoes.adicionar_restricao(restricoes.TempoViagem(46 - rota_final_tempo, rota_final_tempo))

    # Manutenções da última rota
    for i in range(47 - rota_final_tempo - 3, 47 - rota_final_tempo):
      self.restricoes.adicionar_restricao(restricoes.Manutencao(i))

    ################################################################

    # Adiciona os slots da viagem
    self.restricoes.adicionar_restricao(restricoes.TempoViagem(ultimo_indice, tempo_viagem))

    for i in range(ultimo_indice, ultimo_indice + tempo_viagem):
      self.restricoes.adicionar_restricao(restricoes.TempoEsperado(i, float(tempo_viagem / 2)))

    ultimo_indice += tempo_viagem
    for i in range(0, 3):
      self.restricoes.adicionar_restricao(restricoes.Manutencao(ultimo_indice + i))
    ultimo_indice += 3

    print(f"limite_fim: {limite_fim}")
    print(f"limite_inicio: {limite_inicio}")
    while ultimo_indice < limite_fim - 5:
      ultimo_destino = ultima_rota[1]
      proximas_rotas = [x for x in self.rotasVoo if x[0] == ultimo_destino]
      proxima_rota = random.choice(proximas_rotas)
      tempo_viagem = int(proxima_rota[2] * 2)

      self.restricoes.adicionar_restricao(restricoes.TempoViagem(ultimo_indice, tempo_viagem))

      for i in range(ultimo_indice, ultimo_indice + tempo_viagem):
        self.restricoes.adicionar_restricao(restricoes.TempoEsperado(i, float(tempo_viagem / 2)))
        self.restricoes.adicionar_restricao(restricoes.OrigemIgualDestino(i, ultimo_indice - 4))

      ultimo_indice += tempo_viagem
      for i in range(0, 3):
        self.restricoes.adicionar_restricao(restricoes.Manutencao(ultimo_indice + i))
      ultimo_indice += 3
      ultima_rota = proxima_rota

    print(f"ultimo_indice parou em: {ultimo_indice - 1}")
    print(f"slots que sobraram: {44 - ultimo_indice - rota_final_tempo}")

  def gerar_gene(self):
    slot_manutencao = self.rotasVoo[-1]
    temp_lista = self.rotasVoo[:len(self.rotasVoo)-1]
    random.shuffle(temp_lista)
    self.rotasVoo = [*temp_lista, slot_manutencao]
    # Restrições de manutenção fixas
    self.rota.append(slot_manutencao)
    self.rota.append(slot_manutencao)

    # Definição da primeira viagem:
    # Pega primeira cidade (Q foi sorteada)
    ultima_rota = self.rotasVoo[0]
    origem_rota = ultima_rota[0]
    tempo_viagem = int(ultima_rota[2] * 2)
    ultimo_indice = 3

    # Adiciona os slots da viagem
    for _ in range(0, tempo_viagem):
      self.rota.append(ultima_rota)

    ultimo_indice += tempo_viagem
    for _ in range(0, 3):
      self.rota.append(slot_manutencao)
    ultimo_indice += 3

    ultimo_destino = None
    while ultimo_indice < 42:
      ultimo_destino = ultima_rota[1]
      proximas_rotas = [x for x in self.rotasVoo if x[0] == ultimo_destino]
      proxima_rota = random.choice(proximas_rotas)

      tempo_viagem = int(proxima_rota[2] * 2)
      # Adiciona os slots da viagem
      for _ in range(0, tempo_viagem):
        self.rota.append(proxima_rota)

      ultimo_indice += tempo_viagem
      for i in range(0, 3):
        self.rota.append(slot_manutencao)
      ultimo_indice += 3
      ultima_rota = proxima_rota

    if ultima_rota[1] != origem_rota:
      rota_final = [x for x in self.rotasVoo if x[0] == ultima_rota[1] and x[1] == origem_rota]
      proxima_rota = rota_final[0] if len(rota_final) > 0 else None
      tempo_viagem = int(proxima_rota[2] * 2)

      for i in range(0, tempo_viagem):
        self.rota.append(proxima_rota)
      ultimo_indice += tempo_viagem


    print(f"Tamanho rota: {len(self.rota)}")
    self.rota.append(self.rotasVoo[-1])

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

    self.variaveis = list(range(0, 48))

    for variavel in self.variaveis:
      self.dominios[variavel] = self.rotasVoo

  def gerar_gene_backtracking(self):
    slot_manutencao = self.rotasVoo[-1]
    temp_lista = self.rotasVoo[:len(self.rotasVoo)-1]
    random.shuffle(temp_lista)
    self.rotasVoo = [*temp_lista, slot_manutencao]
    self.definir_variaveis()
    self.definir_restricoes()
    self.rota = self.restricoes.busca_backtracking()
