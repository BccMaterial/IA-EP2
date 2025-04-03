class SatisfacaoRestricoes():
    """
    Classe que armazena as restrições e verifica
    se os valores e domínios estão consistentes e
    de acordo com as restrições
    """

    def __init__(self, variaveis, dominios):
        self.variaveis = variaveis
        self.dominios = dominios
        self.restricoes = {}

        for variavel in self.variaveis:
            self.restricoes[variavel] = []
            if variavel not in self.dominios:
                raise LookupError(f"(Init) Variável {variavel} não possui domínio")


    def adicionar_restricao(self, restricao):
        """
        Adiciona um objeto Restrição à lista de restrições
        """
        for variavel in restricao.variaveis:
            if variavel not in self.variaveis:
                raise LookupError(f"(AdicionarRestricao) Variavel {variavel} não definida previamente!")
            self.restricoes[variavel].append(restricao)

    def esta_consistente(self, variavel, atribuicao):
        """
        Verifica se os valores associados nas variáveis
        respeitam todas as restrições
        """
        for restricao in self.restricoes[variavel]:
            if not restricao.esta_satisfeita(atribuicao):
                return False
        return True

    def busca_backtracking(self, atribuicao = {}, qtd_atribuicoes = 0):
        """
        Função recursiva que se comporta como DFS,
        procurando por estados válidos
        """

        # Retorna sucesso quando todas as variáveis forem atribuídas
        if qtd_atribuicoes == 0:
            qtd_atribuicoes = len(self.variaveis)

        if len(atribuicao) == qtd_atribuicoes:
            return atribuicao

        # Pra cada variável em `self.variaveis`, verifica se não está atribuída 
        # nos parametros
        variaveis_nao_atribuidas = [v for v in self.variaveis if v not in atribuicao]
        primeira_variavel = variaveis_nao_atribuidas[0]
        for valor in self.dominios[primeira_variavel]:
            atribuicao_local = atribuicao.copy()
            atribuicao_local[primeira_variavel] = valor
            if self.esta_consistente(primeira_variavel, atribuicao_local):
                resultado = self.busca_backtracking(atribuicao_local)
                if resultado is not None:
                    return resultado
        return None
