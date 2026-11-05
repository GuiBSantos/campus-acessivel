# Critérios do MVP E3

O PDF do piloto foi transcrito, preservando medidas e categorias originais.
Em 05/11 o usuário forneceu `dados/inventario_estimado.json`, que substitui
`piloto_pendente.json`. O arquivo acrescenta códigos finais, caminhos e valores
estimados de gravidade, custos e pessoas/dia, com suas hipóteses. Seu próprio
estado informa ausência de cotação e contagem de campo; não é inventário validado.
A escala proposta nesse arquivo converte Crítica=5, Alta=4, Média=3 e Baixa=2,
com 1 reservado a incômodo mínimo. Trata-se de uma proposta registrada no arquivo,
sem presumir aprovação ou conferência de campo.

`dados/arvore_piloto_provisoria.json` foi atualizado pelos caminhos informados,
com cada código uma vez e sem equiparar térreo a inferior. As pendências de
confirmação e os campos operacionais ausentes estão descritos em `dados/README.md`.
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
