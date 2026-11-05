# Critérios do MVP E3

O inventário operacional é `dados/inventario.json`, fornecido pelo usuário
na versão `inventario (1).json`. Possui 15 registros B01–B15 e quatro níveis.
Substitui os arquivos documentais intermediários, removidos da versão atual.
O exemplo fictício está em `tests/fixtures/demonstracao.json`, somente para testes.

O arquivo operacional é estruturalmente válido, mas contém estimativas e
hipóteses, preservadas em `base_estimativa`. Validade estrutural não comprova
medição ou cotação. A escala informada converte Crítica=5, Alta=4, Média=3 e
Baixa=2, reservando 1 a incômodo mínimo; sua aprovação cabe ao grupo.
A revisão das localizações, normas, demanda, custos e alcance permanece
necessária. Consulte `docs/pendencias_piloto.md` para as divergências da fonte.

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
