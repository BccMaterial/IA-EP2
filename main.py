from classes.aviao import Aviao
from classes.linhas_aereas import LinhasAereas
import random

# rotasVoo = [
#     ("São Paulo (GRU)", "Rio de Janeiro (GIG)", 1.0, 10),
#     ("São Paulo (GRU)", "Brasília (BSB)", 2.0, 6),
#     ("São Paulo (GRU)", "Belo Horizonte (CNF)", 1.5, 8),
#
#     ("Rio de Janeiro (GIG)", "São Paulo (GRU)", 1.0, 10),
#     ("Rio de Janeiro (GIG)", "Brasília (BSB)", 2.0, 5),
#     ("Rio de Janeiro (GIG)", "Belo Horizonte (CNF)", 1.5, 6),
#
#     ("Brasília (BSB)", "São Paulo (GRU)", 2.0, 6),
#     ("Brasília (BSB)", "Rio de Janeiro (GIG)", 2.0, 5),
#     ("Brasília (BSB)", "Belo Horizonte (CNF)", 1.5, 7),
#
#     ("Belo Horizonte (CNF)", "São Paulo (GRU)", 1.5, 8),
#     ("Belo Horizonte (CNF)", "Rio de Janeiro (GIG)", 1.5, 6),
#     ("Belo Horizonte (CNF)", "Brasília (BSB)", 1.5, 7),
# ]
#
# def calcular_total_voos(): #Visita cada tupla e retorna o valor total de voos
#     val = 0
#     for voo in rotasVoo:
#         val+= voo[3]
#     return val
#
# pop_tamanho = 420 #Valor escolhido aleatoriamente. Procurar um valor mais adequado depois
# num_geracoes = 400 #Valor escolhido aleatoriamente. Procurar um valor mais adequado depois
# chance_crossover = 0.5 #Valor escolhido aleatoriamente. Procurar um valor mais adequado depois
# chance_mutacao = 0.3 #Valor escolhido aleatoriamente. Procurar um valor mais adequado depois
# val_total_voos = calcular_total_voos()
# val_max_aeronaves = val_total_voos // 3  #Estimativa inicial do valor máximo de aeronaves. Ver com mais detalhes depois
#
# def gerar_individuo(): #Sorteia uma aeronave aleatoria e adiciona a uma lista
#     individuo = []
#     for i in range(val_total_voos):
#         individuo.append(random.randint(0, val_max_aeronaves-1)) #Verificar depois, não lembro muito bem de como randint() funciona
#     return individuo
#
# def gerar_populacao():
#     pop = []
#     for i in range(pop_tamanho):
#         pop.append(gerar_individuo())
#     return pop
#
# def fitness(individuo): #Função de fitness considerando as restrições do problema
#     val_penalidade = 0 #Valor que é subtraido do fitness de um indivíduo caso ele desrespeite regras
#     voos_aeronaves = {}
#     pos_aeronave = 0
#
#     for rota in rotasVoo:
#         local_partida, local_chegada, duracao_voo, numero_voos = rota #Associa cada elemento das tupla a 4 variáveis
#
#         for i in range(numero_voos):
#             aeronave = individuo[pos_aeronave]
#             pos_aeronave += 1 #Avança uma posição no indivíduo
#
#             if aeronave not in voos_aeronaves:
#                 voos_aeronaves[aeronave] = []
#
#             voos_aeronaves[aeronave].append((local_partida, local_chegada, duracao_voo))
#
#     #Restrição de conflito de horários
#     for aeronaves, voos in voos_aeronaves.items(): #items retorna os valores de cada key do dicinário
#         horario = 0 #Começa a meia noite
#
#         for i in range(len(voos)): #Percorre as tuplas do dicionário
#             local_partida, local_chegada, duracao_voo = voos[i] #Associa cada elemento das tupla a 4 variáveis
#
#             horario_embarque = horario + 1.0 #Uma hora de embarque
#             horario_desembarque = horario_embarque + duracao_voo + 0.5 #0.5 é o tempo de desembarque
#
#             if i > 0: #Verifica se não é o primeiro voo(deve existir pelo menos 2 elementos para comparar os dois)
#                 _, _, duracao_voo_anterior = voos[i - 1] #Pega a duração do voo na tupla anterior
#                 horario_chegada_voo_anterior = horario + duracao_voo_anterior + 0.5
#
#                 if horario_embarque < horario_chegada_voo_anterior:
#                     val_penalidade += 10 #Adiciona uma penalidade caso embarque antes da chegada do voo anterior
#
#             horario = horario_desembarque #Atualiza o horário atual
#
#     #Restrição número específico de voos
#     for local_partida, local_chegada, duracao_voo, numero_voos in rotasVoo:
#         cont = 0
#
#         for voos in voos_aeronaves.values():
#             for voo in voos:
#                 if voo[0] == local_partida and voo[1] == local_chegada:
#                     cont += 1
#         if cont != numero_voos:
#             val_penalidade += 20 * abs(cont - numero_voos)
#
#     #Restrição chegada
#     for voos in voos_aeronaves.values():
#         if voos: #Verifica se as tuplas existem
#             local_primeiro_voo = voos[0][0] #Local de partida na primeira tupla
#             local_ultimo_voo = voos[-1][1] #Local de chegada da última tupla
#
#             if local_primeiro_voo != local_ultimo_voo:
#                 val_penalidade += 100
#     return val_penalidade
#
# def mutar(individuo, chance_mutacao):
#     for i in range(len(individuo)):
#         if random.random() < chance_mutacao:
#             individuo[i] = random.randint(0, val_max_aeronaves -1) #Altera o gene caso a chance de mutação seja maior que o valor aleatório
#     return individuo #Retorna o indivíduo mutado ou não
#
# def crossover(individuo_pai1, individuo_pai2):
#     if len(individuo_pai1) != len(individuo_pai2):
#         print("Os 2 indivíduos devem ter o mesmo tamanho para que possa ocorrer cross-over")
#         return #Retorna nada
#
#     ponto = random.randint(1, len(individuo_pai1) - 1) #Não pode ser o primeiro nem último elemento do indivíduo
#     novo_individuo1 = individuo_pai1[:ponto] + individuo_pai2[ponto:]
#     novo_individuo2 = individuo_pai2[:ponto] + individuo_pai1[ponto:]
#
#     return novo_individuo1, novo_individuo2
#
# def selecao(populacao, fitness, num_individuos = 3 , num_individuos_elite = 1): #Obs: o num_individuos = 3 pois é uma valor mais balanceado, com boa diversidade e focado em bons indivíduos
#     prox_geracao = []
#     sorted_populacao = sorted(populacao, key= fitness) #Ordena a popualação a partir da função de fitness
#     elites = sorted_populacao[:num_individuos_elite] #Como a população está ordenada por fitness, garante que pega os melhores indivíduos
#     prox_geracao.extend(elites) #.extend() "funde" duas listas
#
#     while len(prox_geracao) < len(populacao):
#         torneio = random.sample(populacao, num_individuos) #.sample() retorna uma lista com um número especifo de items aleatórios de uma sequência
#         melhor_individuo = min(torneio, key=fitness) #No nosso contexto, o vencedor será o com menor fitness(menos penalidades)
#         prox_geracao.append(melhor_individuo) #Adiciona o melhor indivíduo para a próxima geração
#
#     return prox_geracao
#
# def algoritmo_genetico():
#     populacao = gerar_populacao()
#
#     for geracao in range(num_geracoes):
#         nova_populacao = selecao(populacao, fitness, num_individuos = 3, num_individuos_elite = 2) #Seleção
#         prox_geracao = nova_populacao[:2] #Mantém os 2 melhores indivíduos
#
#         while len(prox_geracao) < pop_tamanho: #Usado para aplicar mutação e crossover
#             pais = random.sample(nova_populacao, 2) #Seleciona 2 pais de maneira aleatória
#
#             if random.random() < chance_crossover: #Crossover:
#                 novo_individuo1, nova_individuo2 = crossover(pais[0], pais[1])
#             else:
#                 novo_individuo1, nova_individuo2 = pais[0][:], pais[1][:] #Cópia
#
#             #Mutação:
#             novo_individuo1 = mutar(novo_individuo1, chance_mutacao)
#             nova_individuo2 = mutar(nova_individuo2, chance_mutacao)
#
#             prox_geracao.extend([novo_individuo1, nova_individuo2])
#
#         populacao = prox_geracao[:pop_tamanho]
#
#     return min(populacao, key = fitness) #Melhor indivíduo
#
# melhor_solucao = algoritmo_genetico()
# print("Melhor indivíduo:", melhor_solucao)
# print("Fitness final:", fitness(melhor_solucao))

linhas_aereas = LinhasAereas(random.randint(0, 20))
# print(linhas_aereas)
aviao = Aviao(linhas_aereas)

for x in range(0, len(aviao.rota)):
  print(f"{x}:\t{aviao.rota[x]}")
