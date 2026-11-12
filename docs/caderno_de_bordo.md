# Caderno de bordo — Grupo 5

## 04/11/2026 — Estrutura inicial

- Solicitação: Guilherme pediu a criação da estrutura do projeto com base no piloto.
- Apoio utilizado: ChatGPT analisou o PDF e preparou módulos, pastas e documentação.
- Produzido: esqueleto de funções, orientações de dados e lista de divergências do piloto.
- Estado: algoritmos não implementados; inventário final ainda não validado.
- Revisão e alterações pelo grupo: pendentes de registro pelos integrantes.
- Participação presencial ou divisão de tarefas: não informadas nesta sessão.

## Divisão de responsabilidades

A definir pelo grupo por módulo e etapa.

## Uso de IA

Registrar para cada uso o pedido, o retorno, o que o grupo alterou e por quê. A preparação do README e desta estrutura utilizou ChatGPT. Nenhuma validação humana ou aprovação coletiva é presumida.

## Um defeito que encontramos

A preencher com um defeito real, a execução ou teste que o revelou e a correção. As inconsistências documentais do piloto estão em pendencias_piloto.md; não substituem automaticamente a evidência de defeito exigida na entrega.

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
- Retorno da IA: código e revisão técnica em `docs/revisao_2026-11-12.md`.
- Alterações e justificativas humanas sobre esse retorno: pendentes de registro
  pelos integrantes. Não se presume aprovação dos critérios nem coleta adicional.
