import random

rotasVoo = [
  ("São Paulo (GRU)", "Rio de Janeiro (GIG)", 1.0, 10),
  ("São Paulo (GRU)", "Brasília (BSB)", 2.0, 6),
  ("São Paulo (GRU)", "Belo Horizonte (CNF)", 1.5, 8),
  ("Rio de Janeiro (GIG)", "São Paulo (GRU)", 1.0, 10),
  ("Rio de Janeiro (GIG)", "Brasília (BSB)", 2.0, 5),
  ("Rio de Janeiro (GIG)", "Belo Horizonte (CNF)", 1.5, 6),
  ("Brasília (BSB)", "São Paulo (GRU)", 2.0, 6),
  ("Brasília (BSB)", "Rio de Janeiro (GIG)", 2.0, 5),
  ("Brasília (BSB)", "Belo Horizonte (CNF)", 1.5, 7),
  ("Belo Horizonte (CNF)", "São Paulo (GRU)", 1.5, 8),
  ("Belo Horizonte (CNF)", "Rio de Janeiro (GIG)", 1.5, 6),
  ("Belo Horizonte (CNF)", "Brasília (BSB)", 1.5, 7),
]
def calcular_total_voos():  #Visita cada tupla e retorna o valor total de voos
  return sum(voo[3] for voo in rotasVoo)

pop_tamanho = 200  #Valor escolhido aleatoriamente. Procurar um valor mais adequado depois
num_geracoes = 300  #Valor escolhido aleatoriamente. Procurar um valor mais adequado depois
chance_crossover = 0.2  #Valor escolhido aleatoriamente. Procurar um valor mais adequado depois
chance_mutacao = 0.1  #Valor escolhido aleatoriamente. Procurar um valor mais adequado depois
val_total_voos = calcular_total_voos()
val_max_aeronaves = val_total_voos // 4  #Estimativa inicial do valor máximo de aeronaves. Ver com mais detalhes depois
fitness_cache = {}


def gerar_individuo():
  return [random.randint(0, val_max_aeronaves - 1) for i in range(val_total_voos)]


def gerar_populacao():
  return [gerar_individuo() for i in range(pop_tamanho)]

def fitness(individuo):  #Função de fitness considerando as restrições do problema
  chave = tuple(individuo)
  if chave in fitness_cache:
    return fitness_cache[chave]

  val_fitness = 1000
  val_penalidade = 0  #Valor que é subtraido do fitness de um indivíduo caso ele desrespeite regras
  voos_aeronaves = {}
  pos_aeronave = 0

  for rota in rotasVoo:
    local_partida, local_chegada, duracao_voo, numero_voos = rota  #Associa cada elemento das tupla a 4 variáveis

    for i in range(numero_voos):
      aeronave = individuo[pos_aeronave]
      pos_aeronave += 1  #Avança uma posição no indivíduo
      voos_aeronaves.setdefault(aeronave, []).append((local_partida, local_chegada, duracao_voo))

  #Restrição de conflito de horários
  for voos in voos_aeronaves.values(): #items retorna os valores de cada key do dicinário
    horario = 0  #Começa a meia noite

    for i, (local_partida, local_chegada, duracao_voo) in enumerate(voos):
      horario_embarque = horario + 1.0
      horario_desembarque = horario_embarque + duracao_voo + 0.5
      if i > 0:
        _, _, duracao_anterior = voos[i - 1]
        horario_desembarque_anterior = horario + duracao_anterior + 0.5

        if horario_embarque < horario_desembarque_anterior:
          val_penalidade += 10

      horario = horario_desembarque

  #Restrição número de voos
  for local_partida, local_chegada, _, numero_voos in rotasVoo:
    count = sum(1 for vs in voos_aeronaves.values() for v in vs if v[0] == local_partida and v[1] == local_chegada)  #For aninhado em uma única linha para verificar se o local de chegada é igual ao local de partida
    if count != numero_voos:
        val_penalidade += 20 * abs(count - numero_voos)

  #Restrição lugar de chegada
  for voos in voos_aeronaves.values():
    if voos and voos[0][0] != voos[-1][1]: #Verifica se a ultima posição é igual a primeira
      val_penalidade += 100

  fitness_cache[chave] = val_fitness - val_penalidade #Valor de fitness específico naquela chave
  return fitness_cache[chave]

def mutar(individuo):
  for i in range(len(individuo)):
    if random.random() < chance_mutacao:
      individuo[i] = random.randint(0, val_max_aeronaves - 1) #Altera o gene caso a chance de mutação seja maior que o valor aleatório
  return individuo #Retorna o indivíduo mutado ou não

def crossover(p1, p2):
  ponto = random.randint(1, len(p1) - 1)
  return p1[:ponto] + p2[ponto:], p2[:ponto] + p1[ponto:]

def selecao(populacao):
  pop_ordenada = sorted(populacao, key=fitness, reverse=True)
  elites = pop_ordenada[:2]  #2 primeiros elementos da população ordenada
  nova_pop = elites[:]

  while len(nova_pop) < len(populacao):
    torneio = random.sample(populacao, 3) #lista com 3 items selecionados aleatoriamentes de uma sequência
    melhor_individuo = max(torneio, key=fitness)  #Obtem o indivíduo com maior fitness
    nova_pop.append(melhor_individuo)  #Adiciona o melhor indivíduo do torneio para a próxima geração
  return nova_pop

def algoritmo_genetico():
  populacao = gerar_populacao()

  for i in range(num_geracoes):
    nova_populacao = selecao(populacao)
    proxima_geracao = nova_populacao[:2]

    while len(proxima_geracao) < pop_tamanho:
      individuos_pais = random.sample(nova_populacao, 2) #Lista com 2 items sorteados aleatoriamente de uma sequência

      if random.random() < chance_crossover:
        individuo_filho1, individuo_filho2 = crossover(individuos_pais[0], individuos_pais[1])
      else:
        individuo_filho1, individuo_filho2 = individuos_pais[0][:], individuos_pais[1][:]
      proxima_geracao.extend([mutar(individuo_filho1), mutar(individuo_filho2)])

    populacao = proxima_geracao[:pop_tamanho]

  return max(populacao, key=fitness)

melhor = algoritmo_genetico()
print("Melhor indivíduo:", melhor)
print("Fitness:", fitness(melhor))
