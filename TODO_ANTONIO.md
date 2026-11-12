# Pendências de entrega — Antonio

Atualizado em 12/11/2026, conforme o código e a documentação disponíveis.

## Situação atual

- O PDF `Campus_Acessivel_Grupo5_Inventario_Piloto (2)..pdf` contém 15 registros preliminares e medições de campo; ainda não foi convertido para `dados/inventario.json`.
- O contrato exige referência numérica quando há critério dimensional aplicável. B04 pode ser registrado como observação de uso (`elevador_inadequado`, `status_normativo: nao_avaliado`, referência `null`) sem alegar infração normativa.
- `dados/inventario.json` continua com a hierarquia vazia. Não há `dados/registros_pendentes.json` no checkout atual; este TODO não deve afirmar que esse arquivo existe.
- B01/B02: comprimento e largura medidos com trena; ângulo aproximado de 7° medido com inclinômetro, conforme informado pelo grupo. `tan(7°) × 100` resulta em aproximadamente 12,3%; desnível e projeção derivados da geometria permanecem estimativas, não medições adicionais. Não é necessário refazer essas medições.
- Antonio confirmou B03 como barreira de conforto/passagem, com gravidade baixa, sem chamá-la de não conformidade dimensional; e B04 como elevador existente inadequado ao uso observado, sem classificá-lo como ausente.
- B05 agora tem registro de dois degraus de 11 cm de altura na área livre do Bloco A inferior; portas de correr e largura descrita como ampla. As contagens totais dos oito setores com barreiras de Braille foram conciliadas: 75 portas, 22 com Braille e 53 sem. B105 e B103 foram registrados como exemplos de laboratórios com 2 postos reservados cada; ainda não representam todos os laboratórios.
- Fotos B01–B15 foram copiadas e associadas conforme a sequência informada. Permanecem pendentes custos numéricos e pessoas/dia, além de documentar outros laboratórios se forem incluídos na análise.
- A suíte atual passou com **36 testes** após as alterações descritas abaixo; isso verifica o software, não a validade das medições ou decisões do grupo.

## 1. Validar o inventário — pendente

- [x] Obter e ler o PDF do inventário de 15 registros; converter os dados para o inventário operacional ainda está pendente.
- [x] Conferir as medidas/unidades disponíveis no PDF e complementos, os locais, a data de atualização (21/10/2026) e os integrantes do Grupo 5. A data exata por ocorrência não está discriminada na fonte.
- [x] Conciliar os complementos já fornecidos — método das rampas, medida e foto de B05, totais de portas, exemplos de laboratórios e fotos B01–B15 — nas documentações e na matriz complementar.
- [ ] Resolver as pendências restantes descritas em [pendencias_piloto.md](docs/pendencias_piloto.md) e [validacao_normativa.md](docs/validacao_normativa.md), sem afirmar conformidade do elevador ou de sinalização além do que foi efetivamente verificado.
- [x] Registrar B04 como elevador existente com problema de uso observado, sem afirmar conformidade ou infração normativa; tipo/modelo só é necessário se o grupo optar por uma conclusão normativa.
- [x] Registrar em B05 os dois degraus de 11 cm de altura na área livre do Bloco A inferior; largura descrita como ampla e portas de correr.
- [x] Conciliar o total de portas nos setores B06–B11/B14–B15 com a quantidade com Braille do piloto: 75 no total, 22 com Braille e 53 sem. Banheiros ficaram fora do conjunto analisado.
- [x] Registrar os exemplos de B105 (48 computadores, 2 postos reservados) e B103 (36 computadores, 2 postos reservados), com um posto para cadeirante e outro para pessoa com deficiência visual. Justificativa de limitação simultânea documentada; não é cota normativa nem levantamento de todos os laboratórios.
- [ ] Documentar fontes de custos e pessoas/dia. Todos os valores anteriores eram estimados; registrar método, data e responsável, evitando contar pessoas repetidas como beneficiários distintos.
- [ ] Reintroduzir no inventário apenas registros com as pendências resolvidas e evidências vinculadas.

## 2. Confirmar as 15 barreiras — classificação confirmada; registro completo pendente

- [x] Grupo confirmou os 15 registros B01–B15 como barreiras, incluindo B03 como barreira de conforto/passagem.
- [x] Registrar B03 como `porta_conforto`, classificada como barreira e gravidade baixa (1 sugerida), sem afirmar descumprimento do mínimo de 80 cm.
- [ ] Completar no inventário operacional a distribuição exigida por ambientes e níveis, além de intervenção, custo, alcance diário e referência aplicável.
- [x] Excluir piso tátil, corrimãos e audiodescrição do escopo; não cadastrar como ocorrências adicionais.
- [x] Associar as fotos B01–B15 aos códigos correspondentes; os arquivos estão em `fotos/` e a correspondência está documentada.
- [ ] Completar por ocorrência os dados restantes que não aparecem no piloto, em especial data/responsável individual quando disponíveis, intervenção, custo e alcance diário.

**Condição de conclusão:** o grupo confirmou os 15 registros B01–B15 como barreiras. B03 conta como barreira de conforto/passagem, sem alegação de infração dimensional. Falta completar os campos operacionais e confirmar a distribuição exigida.

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
- [x] Conferir os desempates implementados: ranking por código crescente; pacote por maior benefício, menor custo e depois códigos crescentes.
- [ ] Aprovar método e fontes de custo e alcance; registrar decisões, responsáveis e data no caderno de bordo.
- [ ] Atualizar código e textos que indicam critérios provisórios somente depois dessa decisão.

Proposta de escala, pesos 60/40, metodologia de custos e alcance e referências públicas está em [CUSTOS_SUGESTAO.md](CUSTOS_SUGESTAO.md). O grupo ainda precisa aprovar a proposta.

**Proposta para o grupo avaliar:** gravidade de 1 a 5 (1 = desconforto leve sem bloquear uso; 2 = dificuldade pequena com alternativa próxima; 3 = limitação relevante ou desvio; 4 = necessidade frequente de ajuda ou grande restrição; 5 = acesso impedido ou risco imediato). Para comparar alcance em escala compatível, converter a proporção de usuários diários afetados no ambiente para 1–5: até 20%=1, 21–40%=2, 41–60%=3, 61–80%=4, 81–100%=5. Usar benefício = 0,6 × gravidade + 0,4 × alcance; índice = benefício ÷ (custo em R$ / 1.000). Os pesos 60/40 são uma sugestão de partida, não decisão aprovada. Guardar também a contagem bruta de pessoas/dia e o denominador de usuários/dia para rastreabilidade.

**Custos:** estimar cada intervenção por quantidade × preço unitário + mão de obra + transporte/instalação; registrar fonte, data, escopo e responsável. Priorizar orçamento formal ou três cotações comparáveis; quando não houver, usar preço público/catalogado como estimativa e identificá-lo como tal. **Pessoas/dia:** usar horários e ocupação real do ambiente ou observação em dias representativos; estimar usuários únicos que encontram aquela barreira por dia, explicando período, contagem e denominador. Não inventar cotação nem fluxo de pessoas.

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
- [x] Distinguir no README de dados e nos resultados os registros do PDF, o inventário operacional vazio e o exemplo fictício; fotos B01–B15 foram adicionadas.
- [ ] Conferir inventário, fotos, fontes, tabelas A1–A5, análise e instruções no pacote final.
- [ ] Conferir os requisitos e arquivos efetivamente enviados ao AVA, incluindo abertura dos arquivos da versão entregue.

## Ordem recomendada

Resolver coleta e confirmação das barreiras (1 e 2), conferir o contrato completo (3) e aprovar critérios (4). A análise de crescimento (5) pode avançar com dados didáticos identificados. Gerar cenários e saídas finais (6 e 7) somente com dados e critérios aprovados; depois concluir o teste externo e a entrega (8 e 9).
