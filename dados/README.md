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

## Contrato numerico estrito

`referencia_norma` exige numero finito nao negativo na mesma unidade de `medida`. JSON null, booleanos, textos, NaN e infinito sao rejeitados. No CSV use numero com ponto ou virgula decimal; vazio e null sao erros.

`tipo` aceita `rampa_inclinada`, `porta_estreita`, `sinalizacao_ausente` e `elevador_ausente`. Categorias de observacao ou avaliacao foram retiradas do contrato operacional. Pendencia normativa preenchida ou status normativo diferente de `confirmado` impedem a importacao. A validacao estrutural nao substitui a verificacao das evidencias.

O inventario operacional esta vazio: nenhum dos 15 registros estava totalmente confirmado. A hierarquia de locais foi preservada. Todos os registros anteriores estao integralmente em `registros_pendentes.json`, fora do ranking e dos calculos de orcamento. Esse arquivo e historico documental e nao e importavel pelo contrato estrito.

B01 ainda depende da confirmacao do segmento e da referencia condicional de 6.25%; B03 e observacao, mesmo tendo referencia numerica de 80 cm. Os outros registros possuem referencias ou evidencias pendentes. Custos e alcances tambem eram estimados. Nao foram criados numeros para preencher essas lacunas.

Para reincluir registros, resolver as pendencias documentadas, comprovar a barreira, informar referencia numerica compativel e fontes das medidas, custos e alcances. O requisito de 15 barreiras permanece pendente. Dados ficticios de testes estao somente em `tests/fixtures`.
