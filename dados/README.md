# Dados do projeto

`inventario.json` é o inventário operacional e atualmente conserva a hierarquia
do setor, mas ainda não contém barreiras. O PDF `Campus_Acessivel_Grupo5_Inventario_Piloto (2)..pdf`
apresenta 15 registros preliminares; sua conversão depende de resolver os campos
pendentes e ajustar o contrato abaixo.

```bash
python main.py --inventario dados/inventario.json
```

O menu oferece a opção 1 para carregá-lo diretamente; `python main.py --demo`
executa o fluxo completo com esse mesmo arquivo. Como ele está vazio, ainda não
produz resultados do inventário de campo. Validação estrutural não confirma
medidas, custos ou alcance.

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

`referencia_norma` exige número finito não negativo na mesma unidade de `medida`, exceto para `elevador_inadequado` observado sem alegação normativa: nesse caso, use `referencia_norma: null` e `status_normativo: "nao_avaliado"`. No CSV, deixe a referência vazia e informe esse status. JSON null em outros casos, booleanos, textos, NaN e infinito são rejeitados.

`tipo` aceita as 14 categorias do Anexo A do caderno e também `porta_conforto` e `elevador_inadequado`, justificadas pelo inventário do grupo. `classificacao` pode ser `barreira` ou `oportunidade_melhoria`; oportunidades não contam no mínimo de 15 barreiras. Pendência normativa preenchida impede a importação; o status `nao_avaliado` é permitido somente no caso observacional do elevador descrito acima. A validação estrutural não substitui a verificação das evidências.

O inventário PDF lista B01–B15, mas os campos operacionais ainda não foram convertidos para JSON. B03 foi aprovado por Antonio como oportunidade de melhoria de conforto com gravidade baixa, sem alegação de não conformidade. B04 é um elevador existente com dificuldade de uso observada, não um elevador ausente. O complemento documental registra os degraus de B05, os totais de portas por setor e exemplos de postos acessíveis em B105/B103. As fotos B01–B15 estão em `fotos/`. Custos, alcance diário e inventário completo dos laboratórios continuam pendentes.

Para reincluir registros, resolver as pendencias documentadas, comprovar a barreira, informar referencia numerica compativel e fontes das medidas, custos e alcances. O grupo confirmou B01?B15 como barreiras; ainda faltam os campos operacionais completos. Dados ficticios de testes estao somente em `tests/fixtures`.
