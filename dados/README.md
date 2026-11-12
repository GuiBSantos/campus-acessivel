# Dados do projeto

`inventario.json` é o inventário operacional e atualmente conserva a hierarquia
do setor, mas ainda não contém barreiras. O PDF `Campus_Acessivel_Grupo5_Inventario_Piloto (2)..pdf`
apresenta 15 registros preliminares; sua conversão depende de resolver os campos
pendentes e ajustar o contrato abaixo.

```bash
python main.py --inventario dados/inventario.json
```

O menu oferece a opção 1 para carregá-lo diretamente; `python main.py --demo` executa o fluxo completo com esse mesmo arquivo. A validação estrutural não confirma medidas, custos, alcance ou conformidade normativa.

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

`referencia_norma` deve ser número finito não negativo e comparável à mesma grandeza/unidade de `medida`. Quando não houver referência aplicável confirmada, use null com `status_normativo: "pendente"`; para observação funcional do elevador, use null com `nao_avaliado`. Esses estados não comprovam conformidade. Booleanos, textos, NaN e infinito são rejeitados.

`tipo` aceita as 14 categorias do Anexo A do caderno e também `porta_conforto` e `elevador_inadequado`, justificadas pelo inventário do grupo. `classificacao` pode ser `barreira` ou `oportunidade_melhoria`; oportunidades não contam no mínimo de 15 barreiras. O status `pendente` admite referência nula até a documentação ser completada; `nao_avaliado` é reservado à observação funcional do elevador. A validação estrutural não substitui a verificação das evidências.

O inventário contém B01–B15. B03 é barreira de conforto, gravidade 1, sem alegação de infração dimensional. B04 é elevador existente com dificuldade de uso observada. B05 registra dois degraus de 11 cm. Os setores B06–B11/B14–B15 somam 75 portas, 22 com Braille e 53 sem; isso não verifica outras formas de identificação acessível. B105/B103 são exemplos, não levantamento de todos os laboratórios. Fotos estão em `fotos/`. Custos e pessoas/dia são estimativas históricas e exigem validação local; veja `docs/estimativas_custo.md`.

Antes de usar os resultados para recomendação, completar referências aplicáveis, cotações locais e alcance com denominadores, método e período. O modelo de prioridade adotado está documentado em `docs/criterios_e3.md`. Dados ficticios de testes estao somente em `tests/fixtures`.
