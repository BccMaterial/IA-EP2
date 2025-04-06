import random

#Gene: no nosso contexto, um gene será uma aeronave alocada a um determinado voo
#Domínio: no nosso contexto, o domínio sera o conjunto de aeronaves disponíveis para uma determinada rota
#Indivíduo: no nosso contexto, o indivíduo sera uma lista de valores inteiros que indica as aeronaves dedicadas a cada voo

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

def calcular_total_voos(): #Visita cada tupla e retorna o valor total de voos
    val = 0
    for voo in rotasVoo:
        val+= voo[3]
    return val

pop_tamanho = 300 #Valor escolhido aleatoriamente. Procurar um valor mais adequado depois
num_geracoes = 400 #Valor escolhido aleatoriamente. Procurar um valor mais adequado depois
chance_crossover = 0.5 #Valor escolhido aleatoriamente. Procurar um valor mais adequado depois
chance_mutacao = 0.3 #Valor escolhido aleatoriamente. Procurar um valor mais adequado depois
val_total_voos = calcular_total_voos()
val_max_aeronaves = val_total_voos // 3  #Estimativa inicial do valor máximo de aeronaves. Ver com mais detalhes depois

def gerar_individuo(): #Sorteia uma aeronave aleatoria e adiciona a uma lista
    individuo = []
    for i in range(val_total_voos):
        individuo.append(random.randint(0, val_max_aeronaves-1)) #Verificar depois, não lembro muito bem de como randint() funciona
    return individuo

def gerar_populacao():
    pop = []
    for i in range(pop_tamanho):
        pop.append(gerar_individuo())
    return pop

def fitness(individuo): #Função de fitness considerando as restrições do problema
    val_penalidade = 0 #Valor que é subtraido do fitness de um indivíduo caso ele desrespeite regras
    voos_aeronaves = {}
    pos_aeronave = 0

    for rota in rotasVoo:
        local_partida, local_chegada, duracao_voo, numero_voos = rota #Associa cada elemento das tupla a 4 variáveis

        for i in range(numero_voos):
            aeronave = individuo[pos_aeronave]
            pos_aeronave += 1 #Avança uma posição no indivíduo

            if aeronave not in voos_aeronaves:
                voos_aeronaves[aeronave] = []

            voos_aeronaves[aeronave].append((local_partida, local_chegada, duracao_voo))

    #Restrição de conflito de horários
    for aeronaves, voos in voos_aeronaves.items(): #items retorna os valores de cada key do dicinário
        horario = 0 #Começa a meia noite

        for i in range(len(voos)): #Percorre as tuplas do dicionário
            local_partida, local_chegada, duracao_voo = voos[i] #Associa cada elemento das tupla a 4 variáveis

            horario_embarque = horario + 1.0 #Uma hora de embarque
            horario_desembarque = horario_embarque + duracao_voo + 0.5 #0.5 é o tempo de desembarque

            if i > 0: #Verifica se não é o primeiro voo(deve existir pelo menos 2 elementos para comparar os dois)
                _, _, duracao_voo_anterior = voos[i - 1] #Pega a duração do voo na tupla anterior
                horario_chegada_voo_anterior = horario + duracao_voo_anterior + 0.5

                if horario_embarque < horario_chegada_voo_anterior:
                    val_penalidade += 10 #Adiciona uma penalidade caso embarque antes da chegada do voo anterior

            horario = horario_desembarque #Atualiza o horário atual

    #Restrição número específico de voos
    for local_partida, local_chegada, duracao_voo, numero_voos in rotasVoo:
        cont = 0

        for voos in voos_aeronaves.values():
            for voo in voos:
                if voo[0] == local_partida and voo[1] == local_chegada:
                    cont += 1
        if cont != numero_voos:
            val_penalidade += 20 * abs(cont - numero_voos)

    #Restrição chegada
    for voos in voos_aeronaves.values():
        if voos: #Verifica se as tuplas existem
            local_primeiro_voo = voos[0][0] #Local de partida na primeira tupla
            local_ultimo_voo = voos[-1][1] #Local de chegada da última tupla

            if local_primeiro_voo != local_ultimo_voo:
                val_penalidade += 100
    return val_penalidade

def mutar(individuo, chance_mutacao):
    for i in range(len(individuo)):
        if random.random() < chance_mutacao:
            individuo[i] = random.randint(0, val_max_aeronaves -1) #Altera o gene caso a chance de mutação seja maior que o valor aleatório
    return individuo #Retorna o indivíduo mutado ou não

def crossover(individuo_pai1, individuo_pai2, chance):
    if random.random() < chance: #Sortei um valor aleatório e ver se é menor que a chance
        pos_corte = random.randint(1, len(individuo_pai1 -1)) #Não pode cortar na pos 0 ou na ultima pos
        novo_individuo = individuo_pai1[:pos_corte] + individuo_pai2[pos_corte:]
        novo_individuo2 = individuo_pai2[:pos_corte] + individuo_pai1[pos_corte:]
        return novo_individuo, novo_individuo2
    else:
        return individuo_pai1[:], individuo_pai2[:]

def selecao(populacao, fitness, torneio_len):
    individuos_selecionados = []

    for i in range(2):
        selecao_torneio = random.sample()