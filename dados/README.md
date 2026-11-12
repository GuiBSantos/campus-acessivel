# Dados do projeto

`inventario.json` é o único inventário operacional: 15 registros B01–B15,
organizados em uma árvore de quatro níveis, fornecidos pelo usuário.

```bash
python main.py --inventario dados/inventario.json
```

O menu oferece a opção 1 para carregá-lo diretamente; `python main.py --demo`
executa o fluxo completo com esse mesmo arquivo. Hipóteses e estimativas
permanecem em `base_estimativa`, inclusive o degrau de 15 cm e as quantidades
de portas. Validação estrutural não confirma medidas, custos ou alcance.

Os arquivos intermediários de inventário estimado e árvore provisória foram
retirados da versão atual; seu histórico continua no Git. O exemplo fictício
foi movido para `tests/fixtures/demonstracao.json`, usado somente pelos testes.

## Ficha CSV

UTF-8, campos separados por ponto e vírgula nesta ordem:

```text
caminho;codigo;ambiente;tipo;descricao;medida;unidade;referencia_norma;gravidade;pessoas_dia;custo;intervencao;coletado_por;data_coleta
```

O caminho contém setor e ambiente, separados por `/` ou `>`. Decimais aceitam ponto ou vírgula. Para preservar origens
por campo e hipóteses detalhadas, prefira JSON. O CSV básico não contém esses
metadados e a saída marca a origem como não informada.
