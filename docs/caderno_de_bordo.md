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
