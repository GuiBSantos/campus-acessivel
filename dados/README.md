# Dados do projeto

O inventário real `inventario.json` ainda depende da reconciliação descrita em
`docs/pendencias_piloto.md`.

- `piloto_pendente.json`: 15 registros transcritos do PDF, com medidas e categorias originais; campos não confirmados permanecem nulos.
- `arvore_piloto_provisoria.json`: agrupamento documental, cada código uma única vez; localizações amplas ficam a conciliar.
- `demonstracao.json`: quatro registros inteiramente fictícios para demonstrar o MVP; não são medições ou recomendações do grupo.

A árvore provisória tem `codigos_piloto`, não `barreiras`: propositalmente não é
aceita como inventário operacional pelo validador. Consulte `docs/criterios_e3.md`.

A ficha digitada usará campos separados por ponto e vírgula, nesta ordem:

```text
caminho;codigo;ambiente;tipo;descricao;medida;unidade;referencia_norma;gravidade;pessoas_dia;custo;intervencao;coletado_por;data_coleta
```

O piloto é fonte preliminar. Não converter faixas de custo em preços arbitrários, nem preencher medidas ou alcance ausentes com zero. Preservar uma relação entre os códigos B01–B15 e os futuros códigos SETOR-SUBSETOR-NN.
