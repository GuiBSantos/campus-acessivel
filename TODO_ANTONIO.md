# Pendências de entrega — Antonio

Atualizado em 12/11/2026, conforme o código e a documentação disponíveis.

## Situação atual

- O PDF `Campus_Acessivel_Grupo5_Inventario_Piloto (2)..pdf` contém 15 registros preliminares e medições de campo; ainda não foi convertido para `dados/inventario.json`.
- O contrato exige referência numérica quando há critério dimensional aplicável. B04 pode ser registrado como observação de uso (`elevador_inadequado`, `status_normativo: nao_avaliado`, referência `null`) sem alegar infração normativa.
- `dados/inventario.json` continua com a hierarquia vazia. Não há `dados/registros_pendentes.json` no checkout atual; este TODO não deve afirmar que esse arquivo existe.
- B01/B02 têm comprimentos, larguras e ângulo de aproximadamente 7° medido em campo, confirmado pelo grupo como dado observado. `tan(7°) × 100` resulta em aproximadamente 12,3%; desnível e projeção derivados da geometria permanecem estimativas, não medições adicionais.
- Antonio aprovou registrar B03 como oportunidade de melhoria de conforto, com gravidade baixa, sem chamá-la de não conformidade; e B04 como elevador existente inadequado ao uso observado, sem classificá-lo como ausente.
- Permanecem pendentes a medida de B05, a contagem total de portas em B06–B11/B14–B15, a conferência das quantidades/recursos do laboratório e a inclusão das fotos no repositório.
- A suíte atual passou com **36 testes** após as alterações descritas abaixo; isso verifica o software, não a validade das medições ou decisões do grupo.

## 1. Validar o inventário — pendente

- [x] Obter e ler o PDF do inventário de 15 registros; converter os dados para o inventário operacional ainda está pendente.
- [ ] Conferir medidas, unidades, locais, datas e responsáveis de cada ocorrência.
- [ ] Resolver as divergências registradas em [pendencias_piloto.md](docs/pendencias_piloto.md) e [validacao_normativa.md](docs/validacao_normativa.md); `docs/validacao_dados_piloto.md` não existe no checkout.
- [ ] B04 é elevador existente. Identificar tipo/modelo somente se forem afirmar conformidade normativa; registrar separadamente o desconforto e a dependência de ajuda observados.
- [ ] Medir e descrever o vão/desnível que impede o acesso em B05; a intervenção precisa de uma dimensão observada.
- [ ] Contar o total de portas verificadas, além das portas identificadas, em B06–B11 e B14–B15.
- [ ] Confirmar o total de computadores do laboratório e registrar o que torna as duas estações acessíveis; documentar o efeito prático de haver um teclado Braille.
- [ ] Documentar fontes de custos e pessoas/dia. Todos os valores anteriores eram estimados; registrar método, data e responsável, evitando contar pessoas repetidas como beneficiários distintos.
- [ ] Reintroduzir no inventário apenas registros com as pendências resolvidas e evidências vinculadas.

## 2. Confirmar as 15 barreiras — pendente

- [ ] Comprovar pelo menos 15 barreiras distintas, distribuídas conforme os ambientes e níveis exigidos no enunciado.
- [x] Registrar B03 como `porta_conforto`, oportunidade de melhoria e gravidade baixa (1 na escala do sistema), sem afirmar descumprimento do mínimo de 80 cm.
- [ ] Confirmar com o grupo/professor se B03 pode compor as 15 barreiras exigidas; o programa a exclui da contagem mínima enquanto estiver classificada como oportunidade.
- [ ] Se B03 não contar, comprovar outra ocorrência real para atingir 15 barreiras elegíveis. Não dividir ou duplicar registros.
- [ ] Para cada barreira, reunir código, local, descrição, medida, unidade, foto, data, responsável e justificativa verificável.

**Condição de conclusão:** 15 barreiras comprovadas no inventário operacional. O PDF apresenta 15 registros preliminares; B03 está aprovado como oportunidade e, se não for aceito pelo professor como uma das 15, serão necessárias 15 barreiras confirmadas entre as demais ocorrências e qualquer ocorrência adicional comprovada.

## 3. Ajustar o contrato dos dados — implementação feita; conferência final pendente

- [x] Exigir referência normativa numérica e adaptar a importação CSV e a validação JSON.
- [x] Retirar categorias de observação/avaliação do contrato operacional e preservar os registros pendentes separadamente.
- [x] Testar rejeição de referências inválidas e de pendências explícitas.
- [x] Comparar categorias com o Anexo A: o código agora inclui as 14 categorias listadas e as categorias justificadas `porta_conforto` e `elevador_inadequado`.
- [ ] Ao reincluir dados, garantir que `referencia_norma` represente a mesma grandeza e unidade de `medida`, com fonte aplicável ao caso.
- [ ] Conferir importação, gravação e reabertura com o inventário final preenchido. A validação de formato não confirma a evidência de campo.

## 4. Definir os critérios finais — pendente de decisão do grupo

- [ ] Aprovar a escala de gravidade de 1 a 5 e justificar a classificação de cada barreira.
- [ ] Aprovar os pesos de gravidade e pessoas/dia. Os atuais são 1 e 1 e continuam provisórios; avaliar a diferença de escala entre as variáveis.
- [ ] Aprovar a fórmula de benefício e índice de prioridade.
- [ ] Confirmar os desempates implementados: ranking por código crescente; pacote por maior benefício, menor custo e depois códigos crescentes.
- [ ] Aprovar método e fontes de custo e alcance; registrar decisões, responsáveis e data no caderno de bordo.
- [ ] Atualizar código e textos que indicam critérios provisórios somente depois dessa decisão.

## 5. Análise da exaustiva — experimento didático pronto; integração final pendente

O contador de chamadas recursivas está implementado, incluindo casos base. Uma análise didática para 4, 8, 12 e 16 itens já está em [analise_crescimento_exaustiva.md](resultados/analise_crescimento_exaustiva.md); falta referenciá-la no relatório técnico final.

- [x] Executar entradas didáticas de tamanhos 4, 8, 12 e 16.
- [x] Registrar tamanho, candidatos após poda, orçamento, chamadas e condições do experimento didático.
- [x] Explicar o crescimento combinatório e o efeito das podas, identificando a análise como fictícia.
- [x] Separar o experimento didático dos resultados do inventário do grupo.
- [x] Salvar tabela e interpretação em `resultados/`; referenciar no relatório técnico final continua pendente.

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
- [x] Atualizar `resultados/README.md` para descrever a análise didática disponível e distinguir resultados finais pendentes.

**Não usar saídas do inventário vazio como análise final das barreiras do campus.**

## 8. Testar em outra máquina — sem comprovação registrada

- [ ] Baixar uma cópia limpa do repositório em outra máquina e registrar sistema e versão do Python.
- [ ] Executar `python main.py` e testar importação JSON/CSV, busca, ordenação e comparação de pacotes.
- [ ] Salvar e reabrir o inventário, conferindo códigos e valores preservados.
- [ ] Testar exportações, acentos e execução fora da pasta do projeto.
- [ ] Registrar resultado, data, responsável e eventuais correções.

## 9. Fechar a versão de entrega — pendente

- [x] Executar `python -m unittest discover -s tests -q`: 36 testes passaram após os ajustes atuais. Repetir após as próximas alterações; conferir UTF-8 no Windows.
- [x] Atualizar o estado principal no README, caderno de bordo e `docs/criterios_e3.md` para refletir o PDF de 15 registros e as mudanças aprovadas; ainda conferir possíveis trechos históricos restantes antes da entrega.
- [x] Distinguir no README de dados e nos resultados os registros do PDF, o inventário operacional vazio e o exemplo fictício; a ficha de fotos e a classificação final ainda precisam ser associadas ao pacote.
- [ ] Conferir inventário, fotos, fontes, tabelas A1–A5, análise e instruções no pacote final.
- [ ] Conferir os requisitos e arquivos efetivamente enviados ao AVA, incluindo abertura dos arquivos da versão entregue.

## Ordem recomendada

Resolver coleta e confirmação das barreiras (1 e 2), conferir o contrato completo (3) e aprovar critérios (4). A análise de crescimento (5) pode avançar com dados didáticos identificados. Gerar cenários e saídas finais (6 e 7) somente com dados e critérios aprovados; depois concluir o teste externo e a entrega (8 e 9).
