# Pendências de entrega — Antonio

Atualizado em 12/11/2026, conforme o código e a documentação disponíveis.

## Situação atual

- O contrato operacional exige `referencia_norma` numérica, finita e não negativa. A validação e a importação CSV rejeitam referências vazias, `null`, textos e pendências normativas explícitas.
- O inventário operacional está **sem barreiras**. A hierarquia foi preservada, mas os 15 registros anteriores foram separados em [registros_pendentes.json](dados/registros_pendentes.json). Nenhum estava integralmente confirmado; eles não participam do ranking atual.
- Separar registros pendentes não resolve a coleta nem comprova o mínimo exigido. Não preencher lacunas com zero, números presumidos ou ocorrências duplicadas.
- A última execução registrada da suíte passou com **32 testes**. Isso verifica o software, não a validade das medições ou das decisões do grupo.

## 1. Validar o inventário — pendente

- [ ] Obter o PDF original do piloto, fichas e fotos identificadas por código.
- [ ] Conferir medidas, unidades, locais, datas e responsáveis de cada ocorrência.
- [ ] Resolver as divergências descritas em [validação do piloto](docs/validacao_dados_piloto.md) e [validação normativa](docs/validacao_normativa.md).
- [ ] Confirmar segmentos, desníveis e inclinações de B01/B02. O limite de 6,25% de B01 continua condicional.
- [ ] Identificar o equipamento de B04 e medir o obstáculo de B05; não usar o degrau hipotético de 15 cm.
- [ ] Contar as portas e verificar a identificação completa dos acessos de B06–B11 e B14–B15.
- [ ] Verificar mobiliário, equipamentos e demanda de B12/B13; as contagens atuais não comprovam insuficiência.
- [ ] Documentar fontes de custos e pessoas/dia. Todos os valores anteriores eram estimados; registrar método, data e responsável, evitando contar pessoas repetidas como beneficiários distintos.
- [ ] Reintroduzir no inventário apenas registros com as pendências resolvidas e evidências vinculadas.

## 2. Confirmar as 15 barreiras — pendente

- [ ] Comprovar pelo menos 15 barreiras distintas, distribuídas conforme os ambientes e níveis exigidos no enunciado.
- [ ] Manter B03 fora da contagem enquanto houver apenas a largura informada de 80 cm e uma oportunidade de melhoria. Para reincluir, comprovar um obstáculo efetivo.
- [ ] Buscar outra ocorrência real caso B03 não se qualifique. Não dividir ou duplicar registros apenas para completar a quantidade.
- [ ] Para cada barreira, reunir código, local, descrição, medida, unidade, foto, data, responsável e justificativa verificável.

**Condição de conclusão:** 15 registros comprovados no inventário operacional. Hoje há zero; os 14 candidatos restantes do piloto também não equivalem a 14 barreiras confirmadas.

## 3. Ajustar o contrato dos dados — implementação feita; conferência final pendente

- [x] Exigir referência normativa numérica e adaptar a importação CSV e a validação JSON.
- [x] Retirar categorias de observação/avaliação do contrato operacional e preservar os registros pendentes separadamente.
- [x] Testar rejeição de referências inválidas e de pendências explícitas.
- [ ] Comparar a lista completa de categorias com o enunciado original. Atualmente o código aceita `rampa_inclinada`, `porta_estreita`, `sinalizacao_ausente` e `elevador_ausente`; confirmar se há outras obrigatórias.
- [ ] Ao reincluir dados, garantir que `referencia_norma` represente a mesma grandeza e unidade de `medida`, com fonte aplicável ao caso.
- [ ] Conferir importação, gravação e reabertura com o inventário final preenchido. A validação de formato não confirma a evidência de campo.

## 4. Definir os critérios finais — pendente de decisão do grupo

- [ ] Aprovar a escala de gravidade de 1 a 5 e justificar a classificação de cada barreira.
- [ ] Aprovar os pesos de gravidade e pessoas/dia. Os atuais são 1 e 1 e continuam provisórios; avaliar a diferença de escala entre as variáveis.
- [ ] Aprovar a fórmula de benefício e índice de prioridade.
- [ ] Confirmar os desempates implementados: ranking por código crescente; pacote por maior benefício, menor custo e depois códigos crescentes.
- [ ] Aprovar método e fontes de custo e alcance; registrar decisões, responsáveis e data no caderno de bordo.
- [ ] Atualizar código e textos que indicam critérios provisórios somente depois dessa decisão.

## 5. Completar a análise da exaustiva — medição e discussão pendentes

O contador de chamadas recursivas já está implementado, incluindo casos base. Falta produzir a análise para vários tamanhos de entrada.

- [ ] Executar entradas de tamanhos variados, por exemplo 4, 8, 12 e 16 itens, respeitando o limite prático de execução.
- [ ] Registrar tamanho original, candidatos após a poda por custo, orçamento, chamadas e condições do experimento.
- [ ] Explicar o crescimento combinatório e o efeito das podas. No caso sem poda, a árvore binária completa tem `2^(n+1) - 1` chamadas para `n` candidatos.
- [ ] Separar experimentos didáticos com dados fictícios dos resultados do inventário do grupo.
- [ ] Salvar tabela e interpretação em `resultados/` e referenciá-las no relatório.

## 6. Executar os cenários de orçamento — pendente dos dados e critérios finais

- [ ] Escolher pelo menos quatro tetos justificáveis e executar a opção 11 com o inventário validado.
- [ ] Registrar, para ambos os métodos, códigos escolhidos, custo, benefício, quantidade de itens e chamadas da exaustiva.
- [ ] Procurar e explicar uma divergência entre guloso e exaustivo nos dados do grupo.
- [ ] Se os resultados coincidirem, registrar isso honestamente e investigar outros tetos; não alterar dados para forçar divergência. Um exemplo fictício deve ser identificado como didático.
- [ ] Justificar a recomendação final e discutir limitações do modelo.

## 7. Gerar os arquivos de saída — pendente

- [ ] Exportar A1/A2/A3/A5 pela opção 8.
- [ ] Exportar A4 separadamente pela opção 11.
- [ ] Reunir as saídas, a análise de crescimento e a interpretação dos cenários em `resultados/`.
- [ ] Registrar inventário usado, pesos, tetos e comandos/opções para reproduzir os resultados.
- [ ] Atualizar `resultados/README.md`, que ainda informa não haver resultados calculados.

**Não usar saídas do inventário vazio como análise final das barreiras do campus.**

## 8. Testar em outra máquina — sem comprovação registrada

- [ ] Baixar uma cópia limpa do repositório em outra máquina e registrar sistema e versão do Python.
- [ ] Executar `python main.py` e testar importação JSON/CSV, busca, ordenação e comparação de pacotes.
- [ ] Salvar e reabrir o inventário, conferindo códigos e valores preservados.
- [ ] Testar exportações, acentos e execução fora da pasta do projeto.
- [ ] Registrar resultado, data, responsável e eventuais correções.

## 9. Fechar a versão de entrega — pendente

- [ ] Após os ajustes finais, executar `python -m unittest discover -s tests -q` e registrar o resultado. No Windows, conferir também a codificação UTF-8 usada nas execuções anteriores.
- [ ] Atualizar README, caderno de bordo e `docs/criterios_e3.md`: ainda existem trechos históricos descrevendo 15 registros operacionais e funcionalidades como pendentes, apesar de já implementadas.
- [ ] Distinguir claramente dados confirmados, arquivo de pendências e exemplos fictícios.
- [ ] Conferir inventário, fotos, fontes, tabelas A1–A5, análise e instruções no pacote final.
- [ ] Conferir os requisitos e arquivos efetivamente enviados ao AVA, incluindo abertura dos arquivos da versão entregue.

## Ordem recomendada

Resolver coleta e confirmação das barreiras (1 e 2), conferir o contrato completo (3) e aprovar critérios (4). A análise de crescimento (5) pode avançar com dados didáticos identificados. Gerar cenários e saídas finais (6 e 7) somente com dados e critérios aprovados; depois concluir o teste externo e a entrega (8 e 9).
