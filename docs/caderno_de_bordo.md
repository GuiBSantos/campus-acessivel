# Caderno de bordo — Grupo 5

## 04/11/2026 — Estrutura inicial

- Solicitação: Guilherme pediu a criação da estrutura do projeto com base no piloto.
- Apoio utilizado: ChatGPT analisou o PDF e preparou módulos, pastas e documentação.
- Produzido: esqueleto de funções, orientações de dados e lista de divergências do piloto.
- Estado: algoritmos não implementados; inventário final ainda não validado.
- Revisão e alterações pelo grupo: pendentes de registro pelos integrantes.
- Participação presencial ou divisão de tarefas: não informadas nesta sessão.

## Divisão de responsabilidades

- Antônio: dados, medidas e fotos.
- Guilherme: código, testes e funcionamento.
- Raphael: revisão do projeto e das medidas.

## Uso de IA

Para cada uso, registrar o pedido, o retorno, o que o grupo alterou e por quê. A preparação do README e desta estrutura utilizou ChatGPT. O conteúdo foi validado pelo grupo e as alterações foram submetidas por pull request (PR).

## Um defeito que encontramos

Defeito reproduzível: `confere_com_o_python` aplicava negação numérica à chave textual `codigo` em ordem decrescente, causando `TypeError`. O teste `test_ordenacoes_permutacoes_empates_imutabilidade_e_contadores` revelou o problema. Correção: comparação de referência estável que funciona com texto e números. As inconsistências documentais do piloto estão em `pendencias_piloto.md`; não substituem a evidência de defeito de software registrada aqui.

## 04/11/2026 — MVP técnico para a E3

- Pedido: preparar demonstração em main.py para 05/11, separar tarefas por branches e publicar no GitHub.
- Apoio de IA: Codex implementou validação, importação CSV, montagem de árvore, persistência JSON, percursos recursivos, Bubble Sort, demonstração e testes automatizados.
- Fonte recebida: Campus_Acessivel_Grupo5_Inventario_Piloto (2).pdf. Transcrição de B01–B15 com medidas e categorias preservadas. Custos numéricos e pessoas/dia não constam do documento.
- Decisão técnica proposta pela IA: separar demonstração fictícia do levantamento real. Pesos 1 e 1 são somente demonstrativos; não houve aprovação dos critérios pelo grupo.
- Resultado: fluxo técnico demonstrável; conciliação final, valores reais, fotos e aprovação humana permanecem pendentes. A demonstração não comprova inventário de campo validado.
- Revisão e alterações pelo grupo: ainda não informadas. Não presumir participação, aprovação ou validação coletiva.
- Verificação: suíte E3 cobre entrada inválida, códigos repetidos, CSV, persistência, árvore de profundidade variável, ranking, desempate, rastreabilidade do piloto e execução de main.py.
- Defeito de software do projeto: ainda deve ser documentado pelo grupo com evidência real; um erro de expectativa de recuo no teste foi corrigido durante o desenvolvimento, sem alteração do comportamento do resumo.

## 05/11/2026 — Recebimento do inventário estimado

- Pedido: conferir o JSON estimado anexado, substituir o arquivo anterior e renomeá-lo; remover pendências somente se não faltasse informação.
- Alteração com apoio de IA: `piloto_pendente.json` substituído pelo arquivo fornecido, salvo como `inventario_estimado.json`; árvore documental e referências atualizadas.
- Conferência: 15 registros com códigos finais únicos, caminhos e valores numéricos; faltam campos operacionais e confirmação das hipóteses. Mantidas as pendências e as declarações originais de estimativa sem cotação ou contagem de campo.
- Não foi atribuída aos integrantes coleta ou verificação que o arquivo não documenta. A demonstração padrão continua separada dos dados estimados.

## 05/11/2026 — Menu da demonstração E3

- Pedido: avançar na interface enquanto os dados de campo são confirmados.
- Apoio de IA: Codex implementou menu em main.py para carregar exemplo fictício, JSON e CSV, validar estrutura, mostrar hierarquia, ranking e demonstração completa.
- Execução automática preservada com `--demo`, `--inventario` e `--ficha`. Consultas não alteram o arquivo; carga inválida preserva o inventário anterior.
- Verificação: dez testes passaram, incluindo uso do menu, opções inválidas, arquivo ausente, importação CSV e encerramento por fim de entrada.
- Dados de campo e estimativas não foram modificados nesta tarefa. Aprovação e revisão humana continuam a ser registradas pelos integrantes.

## 05/11/2026 — Saídas, conferências e roteiro de apresentação

- Pedido: identificar estimativas, melhorar leitura, conferir cobertura/totais e preparar defesa.
- Apoio de IA: Codex implementou tabelas com moeda brasileira, detalhes de origem por campo, exportação textual sem sobrescrever arquivos, matriz de contagens e conferências independentes dos totais.
- Arquivos sem origem explícita são sinalizados; a existência de valores não comprova coleta. Metadados e hipóteses são preservados no relatório.
- Roteiro em `docs/apresentacao_e3.md`: execução, recursão, casos base, Bubble Sort, desempate e limites atuais. As buscas, ordenações adicionais e seleção de pacotes continuam pendentes para E4.
- Verificação automatizada: 15 testes, cobrindo também divergência de totais, cobertura B01–B15, origens e exportação pelo menu. Não se presume revisão humana dos dados.

## 05/11/2026 — Incorporação do inventário operacional

- Pedido: adicionar a última versão do JSON anexado ao repositório.
- Arquivo: `inventario (1).json` copiado integralmente para `dados/inventario.json`, sem alterar medidas, autoria declarada ou hipóteses.
- Verificação com apoio de IA: validação estrutural, cobertura B01–B15, códigos únicos, totais por ambientes e execução completa. Total informado/estimado: R$ 134.460,00.
- Custos, alcance e medidas marcadas como hipótese continuam estimados. Não se presume confirmação de campo pela aprovação estrutural do arquivo.

## 05/11/2026 — Limpeza dos protótipos de dados

- Pedido: remover o protótipo agora que existe um inventário operacional.
- Com apoio de IA, removidos os dois JSONs intermediários e movido o exemplo fictício para a pasta de testes. Histórico anterior preservado no Git.
- Menu (opção 1) e `--demo` agora usam `dados/inventario.json`, com 15 registros. Hipóteses e estimativas continuam explícitas.
- Documentação e testes atualizados; essa limpeza não constitui revisão de campo dos valores.


## 12/11/2026 — Revisão do estado atual e correções

- Solicitação: Guilherme pediu análise do projeto e mudanças necessárias.
- Ferramenta de IA: Codex/ChatGPT revisou o commit atual, implementou os
  algoritmos pendentes, CRUD, integração e testes, sem alterar o inventário.
- Defeito reproduzível: `confere_com_o_python` aplicava negação numérica à chave
  textual `codigo` em ordem decrescente, causando TypeError. Correção: comparação
  de referência estável que funciona com texto e números. Evidência automatizada:
  `test_ordenacoes_permutacoes_empates_imutabilidade_e_contadores`.
- Verificação: 31 testes passaram. Convenções dos contadores foram documentadas.
- Retorno da IA: revisão técnica registrada em documento de trabalho posteriormente removido da versão de produção.
- Alterações e justificativas humanas sobre esse retorno: pendentes de registro
  pelos integrantes. Não se presume aprovação dos critérios nem coleta adicional.


## 12/11/2026 — Conferência normativa documental

- Pedido: Guilherme autorizou conferir normas e definir referências fundamentadas.
- Apoio de IA: ChatGPT consultou o texto da NBR 9050 corrigida em 2021, o catálogo ABNT e legislação oficial; produziu `docs/validacao_normativa.md` e a matriz complementar de quinze ocorrências.
- Resultado: duas referências numéricas documentadas, uma delas condicional; demais casos dependem de contexto, equipamento, inspeção ou grandeza adequada. Não houve vistoria nem validação humana presumida.
- Correção: reconhecida a simplificação incorreta do anexo sobre rampas. A conferência distingue desnível por segmento, condições do piloto e conclusões condicionais.
- Categorias adicionais de investigação propostas: equipamento_elevacao_em_avaliacao, acesso_em_avaliacao, posto_trabalho_em_avaliacao, recurso_assistivo_em_avaliacao. Motivo: não rotular como inexistente ou inadequado aquilo que os dados ainda não comprovam. Não são categorias oficiais da norma.
- Inventário e código preservados. Matriz separada evita que referências desconhecidas sejam aceitas como registros finais completos.
- Revisão dos integrantes e eventuais alterações sobre o retorno da IA: a registrar pelo grupo.


## 12/11/2026 — Tratamento de B03, B04 e conferência de rampas

- Pedido: Antonio pediu adaptar o código e o TODO à interpretação do inventário de 15 itens, preservando como pendentes B05, contagens de portas e revisão das quantidades do laboratório.
- Apoio de IA: foram adicionadas funções para calcular inclinação com desnível/projeção e estimar a geometria a partir do comprimento inclinado e ângulo; adicionados os tipos `porta_conforto` e `elevador_inadequado`; oportunidades de melhoria agora ficam fora do mínimo de barreiras.
- Decisões aprovadas por Antonio nesta conversa: B03 é uma oportunidade de conforto, gravidade baixa, sem alegação de não conformidade; B04 é um elevador existente com dificuldade de uso, não um elevador ausente.
- Na data deste registro, ainda pendentes: confirmação coletiva do grupo/professor sobre contar B03 entre as 15; medições de B05; total de portas com/sem Braille; quantidade exata e contexto dos recursos do laboratório; fotos no repositório. O complemento de campo e a associação posterior das imagens estão registrados nas entradas seguintes.
- Verificação: `python -m unittest discover -s tests -q` passou com 36 testes após as alterações.
- Revisão e alterações adicionais dos integrantes: a registrar pelo grupo.

## 12/11/2026 — Análise didática do crescimento exaustivo

- Pedido: identificar trabalho do TODO que poderia avançar antes da conclusão das medições pendentes.
- Apoio de IA: gerou dados sintéticos identificados como didáticos e executou a busca exaustiva para 4, 8, 12 e 16 candidatos, com tetos sem restrição e teto didático de R$ 200. Resultado salvo em `resultados/analise_crescimento_exaustiva.md`.
- Resultado: sem podas, as chamadas observadas foram 31, 511, 8.191 e 131.071; o cenário restrito mostrou remoção de candidatos individualmente inviáveis e cortes por saldo.
- Limite: os dados e tetos são fictícios; não substituem A4 calculado com o inventário validado. A referência no relatório técnico final continua pendente.
- Revisão e alterações dos integrantes: a registrar pelo grupo.

## 12/11/2026 — Complemento de campo: portas, laboratórios e área livre

- Relato do grupo: os números enviados para os setores A–E são totais de portas; as quantidades com Braille já constavam do piloto. Banheiros (8 portas) foram excluídos do conjunto analisado por decisão do grupo.
- Consolidação: para B06–B11/B14–B15, 75 portas no total, 22 com Braille e 53 sem, conforme denominadores informados e numeradores do piloto. A conferência trata de Braille e não presume ausência de outras formas de identificação.
- Laboratórios exemplificados: B105, 48 computadores e 2 postos reservados (um para cadeirante e um para pessoa com deficiência visual); B103, 36 computadores e 2 postos com a mesma distribuição. O grupo justifica possível limitação de capacidade em aulas simultâneas de TI; não há cota normativa nem contagem de todos os laboratórios.
- B05: dois degraus de 11 cm de altura cada na área livre do Bloco A inferior; passagem descrita como ampla, com portas de correr.
- Limite: dados fornecidos pelo grupo foram registrados como relato de campo. Fotos e custos numéricos continuam pendentes; os exemplos B105/B103 não devem ser generalizados para todos os laboratórios.

## 12/11/2026 — Associação das fotos do piloto

- Pedido: Antonio informou que os arquivos da pasta `FOTOS BARREIRAS` seguem uma sequência, começando por Imagem2 = B01.
- Ação: copiadas Imagem2.jpg a Imagem15.jpg para `fotos/B01.jpg` a `fotos/B14.jpg`, sem mover os originais. O mapeamento está documentado em `fotos/README.md`.
- Atualização: Imagem16.jpg foi enviada depois e copiada como `fotos/B15.jpg`, completando a sequência. Para portas, foram associadas imagens representativas, sem necessidade de fotografar cada porta.


## 12/11/2026 ? B03 confirmada como barreira e proposta de custos

- Decis?o mais recente de Antonio: B03 conta como barreira de conforto/passagem. O v?o informado de 80 cm atende ao m?nimo citado; n?o afirmar infra??o dimensional. Com B03, o grupo confirma os 15 c?digos B01?B15 como barreiras.
- Pedido: reunir fontes p?blicas, sugerir custos num?ricos, m?todo de pessoas/dia e escala/pesos sob prazo curto.
- Ação: foi criado documento de trabalho com referências de SINAPI/CAIXA, planilhas e contratos públicos e cálculos de referência; documento removido da versão de produção. As estimativas não foram incorporadas ao inventário nem aprovadas pelo grupo.
- Recomenda??o para decis?o: gravidade e alcance normalizados de 1 a 5, pesos 60/40, custo por R$ 1.000 e m?todo para estimar usu?rios ?nicos/dia. A f?rmula segue como proposta at? aprova??o do grupo.
- Limite: n?o foi encontrada fonte p?blica com fluxo di?rio por pr?dio/setor do campus. Matr?culas gerais n?o equivalem a presen?a di?ria; levantar hor?rios/ocupa??o ou observar fluxo por local. Custos de obras maiores e amplia??o da porta s?o par?metros preliminares, n?o cota??es do UNASP.
