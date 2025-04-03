class IndividuoSimples:
  def fitness(self):
    raise NotImplementedError("Fitness não implementado")

  def mutacao(self):
    raise NotImplementedError("Mutacao não implementado")

class Individuo(IndividuoSimples):
  def crossover(self):
    raise NotImplementedError("Crossover não implementado")
