# Dados do projeto

Aguardar a reconciliação descrita em `docs/pendencias_piloto.md` antes de montar `inventario.json`.

A ficha digitada usará campos separados por ponto e vírgula, nesta ordem:

```text
caminho;codigo;ambiente;tipo;descricao;medida;unidade;referencia_norma;gravidade;pessoas_dia;custo;intervencao;coletado_por;data_coleta
```

O piloto é fonte preliminar. Não converter faixas de custo em preços arbitrários, nem preencher medidas ou alcance ausentes com zero. Preservar uma relação entre os códigos B01–B15 e os futuros códigos SETOR-SUBSETOR-NN.
