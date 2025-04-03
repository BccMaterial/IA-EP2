import random

#Gene: no nosso contexto, um gene será uma aeronave alocada a um determinado voo
#Domínio: no nosso contexto, o domínio sera o conjunto de aeronaves disponíveis para uma determinada rota
#Indivíduo: no nosso contexto, o indivíduo sera uma lista de valores inteiros que indica as aeronaves dedicadas a cada voo

rotasVoo = [ #Lista incluindo o local de partida, chegada, tempo de voo e número de voos
    ("São Paulo(GRU)", "Rio de Janeiro(GIG)", 1.0, 10),
    ("São Paulo(GRU)", "Brasilia", 2.0, 6)


] #Terminar de copiar da tabela depois

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
val_max_aeronaves = val_total_voos // 2  #Estimativa inicial do valor máximo de aeronaves. Ver com mais detalhes depois

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

print(gerar_populacao())
