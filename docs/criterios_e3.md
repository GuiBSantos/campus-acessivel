# Critérios do MVP E3

O inventário operacional é `dados/inventario.json`; no checkout atual ele tem a
hierarquia, mas zero registros. O PDF de inventário do Grupo 5 apresenta 15 itens
preliminares B01–B15, ainda não convertidos para o contrato operacional. O exemplo
fictício está em `tests/fixtures/demonstracao.json`, somente para testes.

O PDF registra medidas de rampas, portas e cabine do elevador, além de contagens
preliminares. Não contém custos cotados nem alcance em pessoas/dia. A escala
piloto tem quatro categorias; a conversão para 1–5 e sua aprovação continuam a
cargo do grupo. B03 foi aprovado por Antonio como oportunidade de conforto com
gravidade baixa, sem alegação de não conformidade. B04 é um elevador existente
com problema de uso observado. Consulte `docs/pendencias_piloto.md` e
`docs/validacao_normativa.md` para os pontos que ainda precisam de evidência ou
decisão.

## Modelo provisório para demonstrar o algoritmo

Benefício = gravidade × peso_gravidade + pessoas_dia × peso_pessoas_dia.
Índice = benefício / (custo / 1000). Custos devem ser positivos.
Pesos de demonstração: gravidade = 1 e pessoas_dia = 1. Eles demonstram a fórmula,
mas misturam escalas e não representam uma decisão validada pelo grupo.
Antes de usar dados reais, o grupo deve aprovar pesos, escala de gravidade,
método de contagem de pessoas/dia e fontes de custo. Não converter categorias
verbais do piloto automaticamente em números.

Ranking: índice decrescente; em empate, código crescente, independentemente da
direção escolhida para o índice. Bubble Sort próprio conta cada comparação
entre registros e cada troca. A lista original não é reordenada.

Campos numéricos aceitam ponto ou vírgula decimal; pessoas/dia é inteiro não negativo,
gravidade é inteiro de 1 a 5, custo é positivo e medida é não negativa.
CSV UTF-8 separado por ponto e vírgula, caminho separado por `/` ou `>`, incluindo
setor e ambiente. O último componente deve coincidir com `ambiente`.
JSON inválido ou inventário inconsistente é recusado antes da gravação.


## Convenções atualizadas em 12/11/2026

- Bubble sem parada antecipada e Selection fazem n(n−1)/2 comparações.
- Insertion usa trocas adjacentes. Assim seu número de trocas coincide com o
  Bubble para a mesma entrada e o mesmo desempate. Comparações contam avaliações
  entre registros, não cada operador interno do desempate.
- O desempate das três ordenações continua sendo código crescente.
- Buscas contam registros examinados; o custo de ordenar antes da binária é
  mostrado separadamente. Lista já ordenada é pré-condição das funções binárias.
- Pacotes maximizam a soma dos benefícios, não a soma dos índices. A exaustiva
  desempata pelo menor custo e depois pela lista de códigos crescente.
- Valores monetários dos pacotes são convertidos em centavos, sem arredondamento
  silencioso; mais de duas casas é erro. Toda chamada da exaustiva conta,
  inclusive as chamadas base, após a poda de itens individualmente inviáveis.
- Pesos permanecem provisórios; a revisão não alterou decisões ou dados do grupo.
