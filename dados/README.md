# Dados do projeto

`inventario.json` é a árvore operacional fornecida pelo usuário em
`inventario (1).json`, com 15 registros e quatro níveis. Pode ser carregada
pela opção 2 do menu ou por `python main.py --inventario dados/inventario.json`.
Preserva custos, alcance e algumas medidas estimados; validade estrutural não
confirma coleta ou cotação. A revisão de campo continua necessária.

Os arquivos abaixo preservam versões documentais anteriores, não são a entrada
operacional atual:

- `inventario_estimado.json`: arquivo estimado fornecido pelo usuário, com 15 registros, códigos finais, caminhos, gravidade, custos e pessoas/dia. Preserva medidas originais, hipóteses e pendências; não contém cotações verificadas.
- `arvore_piloto_provisoria.json`: agrupamento documental atualizado pelos caminhos do arquivo estimado, cada código uma única vez; não equivale à confirmação dos locais em campo.
- `demonstracao.json`: quatro registros inteiramente fictícios para demonstrar o MVP; não são medições ou recomendações do grupo.

A árvore provisória tem `codigos_piloto`, não `barreiras`: propositalmente não é
aceita como inventário operacional pelo validador. Consulte `docs/criterios_e3.md`.

A ficha digitada usará campos separados por ponto e vírgula, nesta ordem:

```text
caminho;codigo;ambiente;tipo;descricao;medida;unidade;referencia_norma;gravidade;pessoas_dia;custo;intervencao;coletado_por;data_coleta
```

O piloto é fonte preliminar. Não converter faixas de custo em preços arbitrários, nem preencher medidas ou alcance ausentes com zero. Preservar uma relação entre os códigos B01–B15 e os futuros códigos SETOR-SUBSETOR-NN.

## Conferência do arquivo estimado — 05/11/2026

Os 15 códigos finais são únicos e seguem o formato do programa. Todos os
registros possuem caminho, gravidade entre 1 e 5, custo positivo e pessoas/dia
inteiro não negativo. Isso não comprova coleta ou cotação de campo.

Ainda não é possível passar esse documento diretamente a `main.py --inventario`:
o arquivo contém `registros`, enquanto o programa lê uma árvore com `nome`,
`barreiras` e `subsetores`. Nos registros, `codigo_final` e `descricao_original`
podem ser mapeados para `codigo` e `descricao`, e o ambiente pode ser extraído
do caminho; essa conversão ainda não foi feita. Faltam campos operacionais
`tipo`, `medida`, `unidade`, `referencia_norma`, `intervencao`, `coletado_por`
e `data_coleta`. Algumas medidas estão em `medicoes`; onze registros não possuem
medição nessa lista (embora algumas contagens apareçam nas descrições).
A data de atualização da fonte não confirma a data individual de cada coleta.

Por isso, a chave `pendencias` foi mantida. `base_estimativa` e `estado` também
foram preservados. Em B05, a hipótese de degrau não está confirmada no PDF;
as afirmações normativas nas estimativas não são laudos de conformidade.
