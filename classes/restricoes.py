###################
### CLASSE BASE ###
###################

class Restricao():
    def __init__(self, variaveis):
        self.variaveis = variaveis

    def esta_satisfeita(self, atribuicao):
        """
        # Definição
        Verifica se a restrição implementada está satisfeita
        
        # Parâmetros
        A atribuição é um dicionário, onde:
        - A chave é a variável
        - O valor é o "valor de domínio" atribuído
        """
        return True


# Exemplo pra ter referência
class SeGostam(Restricao):
    def __init__(self, animal1, animal2):
        super().__init__([animal1, animal2])
        self.animal1 = animal1
        self.animal2 = animal2

    def esta_satisfeita(self, atribuicao):
        if self.animal1 not in atribuicao or self.animal2 not in atribuicao:
            return True
        return atribuicao[self.animal1] == atribuicao[self.animal2]
