# IA-EP2

## O problema

Além dos Hotéis-Escola para os cursos de Hotelaria, o Senac vai abrir cursos de 
piloto de avião e comissário de bordo e para isto vai montar uma Companhia Aérea Escola.

Esta companhia aérea precisa organizar seus voos diários para garantir que todos os 
destinos sejam atendidos e que as restrições operacionais e regulatórias sejam cumpridas.
A companhia aérea possui um conjunto de aviões para alocar a cada voo.

Existem vários destinos para os quais a companhia aérea voa. Cada voo tem uma origem e 
um destino específico, bem como uma duração de voo que depende da distância entre as 
cidades. Cada voo tem um horário de partida e chegada específico, que deve ser 
respeitado para garantir a eficiência das operações da companhia aérea.

As restrições a serem satisfeitas incluem:
1. Cada voo deve ser alocado a uma aeronave disponível e adequada para o tipo de rota.
2. Cada aeronave só pode ser usada em um voo por vez e deve ter um tempo mínimo de 
manutenção entre os voos. Este tempo é de cerca de 1h antes do embarque e 0,5h depois 
do desembarque.
3. Os horários de partida e chegada dos voos devem respeitar as restrições operacionais
e regulatórias, incluindo horários de pouso e decolagem.

O objetivo é encontrar uma alocação de aviões que atenda a todas as restrições e minimize 
o número total de aviões necessários para cobrir todos os voos.

Para ajudar a visualizar o problema, aqui está uma tabela com as rotas, os tempos de voo 
e o número de voos diários estimados:

| Origem               | Destino              | Tempo de Voo (Horas) | Número de voos diários|
|----------------------|----------------------|----------------------|-----------------------|
| São Paulo (GRU)      | Rio de Janeiro (GIG) | 1.0                  | 10                    |
| São Paulo (GRU)      | Brasília (BSB)       | 2.0                  | 6                     |
| São Paulo (GRU)      | Belo Horizonte (CNF) | 1.5                  | 8                     |
| Rio de Janeiro (GIG) | São Paulo (GRU)      | 1.0                  | 10                    |
| Rio de Janeiro (GIG) | Brasília (BSB)       | 2.0                  | 5                     |
| Rio de Janeiro (GIG) | Belo Horizonte (CNF) | 1.5                  | 6                     |
| Brasília (BSB)       | São Paulo (GRU)      | 2.0                  | 6                     |
| Brasília (BSB)       | Rio de Janeiro (GIG) | 2.0                  | 5                     |
| Brasília (BSB)       | Belo Horizonte (CNF) | 1.5                  | 7                     |
| Belo Horizonte (CNF) | São Paulo (GRU)      | 1.5                  | 8                     |
| Belo Horizonte (CNF) | Rio de Janeiro (GIG) | 1.5                  | 6                     |
| Belo Horizonte (CNF) | Brasília (BSB)       | 1.5                  | 7                     |

O objetivo é minimizar o número de aeronaves usadas para cobrir todas as rotas de voo de 
ida e volta para cada dia. Podemos usar um solver de satisfação de restrições para 
resolver esse problema e encontrar uma solução ótima.
