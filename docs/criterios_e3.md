# Critérios do MVP E3

O piloto real NÃO foi conciliado. O PDF anexado foi lido e seus 15 registros foram transcritos, preservando
medidas, categorias preliminares e divergências. Custos numéricos e alcance
continuam ausentes.
`dados/piloto_pendente.json` preserva B01–B15 sem inventar valores. A árvore documental
`dados/arvore_piloto_provisoria.json` posiciona cada código uma vez: usa os
locais da tabela quando específicos e mantém B01, B02, B03 e B05 em
“Localização a conciliar”. Não assume que térreo e inferior são equivalentes.
Não há inventário real validado. A árvore de `dados/demonstracao.json` é fictícia,
com quatro barreiras e três ambientes; não comprova a entrega de campo da E2.

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

Campos numéricos aceitam ponto decimal; pessoas/dia é inteiro não negativo,
gravidade é inteiro de 1 a 5, custo é positivo e medida é não negativa.
CSV UTF-8 separado por ponto e vírgula, caminho separado por `/`, incluindo
setor e ambiente. O último componente deve coincidir com `ambiente`.
JSON inválido ou inventário inconsistente é recusado antes da gravação.
