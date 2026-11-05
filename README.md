# Campus Acessível

**Da medição à decisão: dados de campo para orientar intervenções de acessibilidade.**

Projeto acadêmico da disciplina **Construção de Algoritmos e Programação**, do UNASP — Campus Engenheiro Coelho, no segundo semestre de 2026.

Este repositório reúne o desenvolvimento de um sistema em Python e a documentação de um levantamento de barreiras de acessibilidade. A proposta é transformar medidas coletadas pelo grupo em uma recomendação justificável: quais intervenções executar, em que ordem e dentro de qual orçamento.

> **Estado do projeto:** MVP técnico da E3 implementado: validação, CSV, JSON, percursos recursivos, resumo hierárquico e ranking com Bubble Sort próprio. A demonstração usa dados fictícios, separados dos 15 registros transcritos do piloto. O inventário real ainda depende de conciliação e valores confirmados. Veja [critérios da E3](docs/criterios_e3.md), [pendências do piloto](docs/pendencias_piloto.md) e [caderno de bordo](docs/caderno_de_bordo.md).

## O problema que queremos resolver

Um setor pode precisar de várias adaptações, mas o orçamento disponível pode não cobrir todas. Escolher apenas a intervenção mais barata ou a barreira mais grave pode deixar de fora uma combinação com maior benefício total.

Nosso trabalho será registrar as barreiras encontradas, estimar o impacto e o custo das intervenções e comparar estratégias de escolha. A recomendação final deverá ser sustentada pelos dados coletados e por resultados reproduzíveis no programa.

## Nosso recorte

| Informação | Definição do grupo |
| --- | --- |
| Setor analisado | Prédio do Ensino Superior — UNASP-EC |
| Curso e turma | Sistemas de Informação — Grupo 5; turma a confirmar |
| Integrantes | Antonio Augusto Rodrigues Soares Júnior; Raphael Rios; Guilherme Barreto dos Santos |
| Ambientes e hierarquia | A documentar a partir do levantamento |
| Período de coleta | Piloto informa coleta atualizada em 21/10/2026; confirmar datas por registro |
| Orçamento de referência | A definir e justificar |

## Do campo à recomendação

1. **Levantar:** identificar, medir e fotografar as barreiras do setor.
2. **Organizar:** registrar os dados em uma árvore de setores, subsetores e ambientes.
3. **Validar:** verificar campos obrigatórios, códigos únicos e consistência dos valores.
4. **Priorizar:** calcular um índice com critérios e pesos definidos pelo grupo.
5. **Comparar:** medir o comportamento dos algoritmos de ordenação, busca e seleção de intervenções.
6. **Recomendar:** apresentar um pacote de intervenções compatível com o orçamento e explicar suas limitações.

O inventário final deverá conter pelo menos **15 barreiras**, distribuídas em **3 ambientes** e **2 níveis de hierarquia**. Cada barreira terá uma medida com unidade e uma foto identificada pelo seu código.

## Funcionalidades previstas

- Importação da ficha de campo, com campos separados por ponto e vírgula.
- Cadastro, edição, remoção e validação de barreiras.
- Gravação e leitura do inventário em arquivo JSON.
- Consulta da hierarquia, com totais e contagens calculados recursivamente.
- Ranking de prioridade com Bubble Sort, Selection Sort e Insertion Sort.
- Localização por código com busca sequencial, binária iterativa e binária recursiva.
- Matriz de contagens por ambiente e tipo de barreira.
- Comparação entre seleção gulosa e busca exaustiva sob um teto de orçamento.
- Exibição de contadores dos algoritmos e exportação de relatório em texto.

## Organização prevista do repositório

Os seis módulos Python estão na raiz. Coleta, percursos recursivos e Bubble Sort estão implementados; buscas, demais ordenações, seleção de pacotes e relatórios finais continuam pendentes. As pastas abaixo já contêm orientações para receber os dados e as entregas.

| Arquivo ou pasta | Responsabilidade |
| --- | --- |
| `main.py` | Menu numerado, entradas do usuário e fluxo do programa |
| `coleta.py` | Cadastro, validação, importação e persistência |
| `recursao.py` | Percurso da árvore, totais e seleção exaustiva |
| `ordenacao.py` | Índice de prioridade e três ordenações próprias |
| `busca.py` | Busca sequencial e duas versões da busca binária |
| `relatorio.py` | Matriz, tabelas e exportação de resultados |
| `dados/` | Ficha digitada e inventário JSON |
| `fotos/` | Evidências de campo, nomeadas pelo código da barreira |
| `docs/` | Árvore do setor, critérios, caderno de bordo e documentos de entrega |
| `resultados/` | Relatórios e tabelas gerados pelo sistema |
| `README.md` | Apresentação do projeto e orientação de uso |

Apenas `main.py` solicitará entradas ao usuário. Os demais módulos receberão os dados necessários por parâmetros.

## Como os dados serão representados

Cada barreira será um dicionário com os campos obrigatórios definidos no caderno da disciplina:

| Grupo de informações | Campos |
| --- | --- |
| Identificação | `codigo`, `ambiente`, `tipo`, `descricao` |
| Medição e referência | `medida`, `unidade`, `referencia_norma` |
| Avaliação e intervenção | `gravidade`, `pessoas_dia`, `custo`, `intervencao` |
| Rastreabilidade | `coletado_por`, `data_coleta` |

O código seguirá o padrão `SETOR-SUBSETOR-NN` e será único no inventário. A ficha digitada incluirá também o `caminho` hierárquico do ambiente.

A árvore será formada por dicionários com `nome`, `barreiras` e `subsetores`. Cada subsetor poderá conter novos níveis. O percurso recursivo permitirá processar ramos de profundidades diferentes sem fixar uma quantidade de laços aninhados.

Medidas de campo e estimativas terão origens distintas registradas: a medida será obtida no local; a gravidade terá uma escala escrita; o alcance terá um método de estimativa; e o custo terá uma fonte ou método verificável.

## Como vamos definir a prioridade

O modelo exigido pela disciplina é:

```text
benefício = soma dos fatores multiplicados pelos respectivos pesos
índice de prioridade = benefício / (custo / 1000)
```

**Gravidade** e **pessoas afetadas por dia** serão fatores obrigatórios. Um terceiro fator só será incluído se houver um campo coletado que o sustente.

Antes de produzir o ranking, o grupo deverá documentar:

- A escala de gravidade de 1 a 5.
- O método de estimativa de pessoas afetadas por dia.
- As fontes e o método de estimativa dos custos.
- Os fatores, os pesos e a justificativa de cada escolha.
- A regra de desempate, aplicada de forma consistente nas três ordenações.

Essas decisões permanecem em aberto nesta versão. Serão definidas com base no piloto, sem adotar pesos ou resultados fictícios.

### Ranking e pacote de intervenções

O ranking expressa a prioridade individual. O pacote responde quais intervenções cabem juntas no orçamento.

| Estratégia | Funcionamento previsto |
| --- | --- |
| Gulosa | Percorre o ranking e inclui cada intervenção se ela couber no saldo disponível |
| Exaustiva | Explora recursivamente combinações de inclusão e exclusão e seleciona a de maior benefício total dentro do teto |

A comparação considerará benefício total, custo, quantidade de intervenções e chamadas recursivas. Antes da busca exaustiva, serão descartadas intervenções cujo custo individual ultrapasse o orçamento. O programa deverá avisar quando houver mais de 20 candidatos, devido ao crescimento combinatório da busca.

## Tecnologias e limites do trabalho

- **Python 3**, executado no terminal.
- Apenas a **biblioteca padrão** do Python.
- Funções e módulos, com listas, matrizes e dicionários.
- Persistência em arquivo **JSON**.
- Algoritmos de busca e ordenação implementados pelo grupo.

O escopo da disciplina não permite bibliotecas externas, interface gráfica ou web, banco de dados, classes ou orientação a objetos. Não há dependências para instalar com `pip`.

`sorted()`, `list.sort()`, `min()`, `max()` e o operador `in` não poderão substituir os algoritmos exigidos. O uso de `sorted()` será restrito à função separada de conferência `confere_com_o_python`, conforme o enunciado.

## Execução do MVP E3

Na raiz do repositório, sem instalar pacotes:

```bash
python main.py
python main.py --demo
python -m unittest discover -s tests -v
```

A execução padrão abre um menu: carregar demonstração fictícia (1), carregar
JSON (2), importar CSV (3), validar (4), mostrar hierarquia (5), ranking (6),
demonstração completa (7), exportar relatório textual (8) e sair (0). Carregue um arquivo antes de consultar.
Uma falha ao carregar outro arquivo preserva o inventário anterior em memória.
O menu não grava por cima dos arquivos de entrada.

Com `--demo`, a execução automática usa **quatro barreiras fictícias** em três ambientes. Exibe
aviso, confere gravação/leitura JSON em pasta temporária, imprime a hierarquia
e mostra o ranking com comparações e trocas. Não altera os dados de entrada.
Essa demonstração não é uma recomendação de intervenções reais.

Para usar um inventário confirmado ou importar uma ficha completa:

```bash
python main.py --inventario dados/inventario.json
python main.py --ficha dados/ficha.csv --peso-gravidade 1 --peso-pessoas 1
```

O JSON `dados/inventario.json` está incluído e contém 15 registros com estimativas
e hipóteses explícitas; não representa cotações ou contagens confirmadas. A ficha
CSV ainda deve ser preparada pelo grupo. Dados inválidos
interrompem a execução com mensagem e código de saída 1. Caminhos fornecidos são
relativos ao diretório atual; os dados padrão são localizados a partir de main.py.
Somente main.py solicita entradas. As opções `--demo`, `--inventario` e
`--ficha` executam diretamente o fluxo completo, sem abrir o menu.
Consulte [contrato e critérios](docs/criterios_e3.md).

As tarefas foram separadas em branches encadeadas: `feat/e3-inventario`,
`feat/e3-coleta-recursao`, `feat/e3-ranking`, `feat/e3-piloto-documentado` e
`feat/e3-demonstracao`. Cada branch inclui as anteriores; a última integra o MVP.
O menu foi desenvolvido em `feat/e3-menu`.

## Evidências que vamos produzir

O relatório técnico terá de 4 a 6 páginas e será organizado em cinco achados, sempre com números obtidos nos dados do grupo e uma explicação do resultado.

| Achado | Evidência prevista |
| --- | --- |
| A1 — Ordenação | Comparações e trocas dos três algoritmos em três tamanhos de base e três ordens iniciais |
| A2 — Busca | Comparações das três buscas para cinco casos: primeiro, meio, último, outro código intermediário e código inexistente |
| A3 — Hierarquia | Custos e contagens por subsetor, profundidade da árvore e caminho completo da barreira mais grave |
| A4 — Otimização | Comparação gulosa × exaustiva em pelo menos quatro orçamentos, análise de divergência e crescimento das chamadas recursivas |
| A5 — Decisão | Justificativa do índice e análise das dez primeiras posições ao dobrar separadamente os pesos da gravidade e do alcance |

Os resultados ainda não estão disponíveis nesta versão. A recomendação final será registrada após a validação dos dados e a execução dessas análises.

## Colaboração do grupo

As responsabilidades por módulo e por etapa serão registradas no caderno de bordo. Cada sessão deverá informar data, participantes, atividades, dificuldades e decisões.

Como fluxo de colaboração proposto, cada alteração deverá ter uma descrição clara, ser revisada por outro integrante e incluir a atualização da documentação quando mudar dados, critérios ou comportamento do programa. Todos deverão compreender o projeto completo para as defesas e a apresentação.

O caderno de bordo terá também as três seções finais exigidas:

1. Divisão de responsabilidades.
2. Registro de uso de IA: pedido realizado, resposta obtida, alterações feitas pelo grupo e justificativas.
3. Um defeito real encontrado, com a evidência que o revelou e a correção adotada.

**Nota de elaboração:** esta versão inicial do README foi preparada com apoio do ChatGPT a partir do caderno da disciplina. A revisão do grupo e suas alterações deverão ser registradas no caderno de bordo.

## Entregas previstas no caderno da disciplina

| Etapa | Data em 2026 | Entrega |
| --- | --- | --- |
| E1 | 24/09 | Piloto com pelo menos oito barreiras, árvore do setor e critérios iniciais |
| E2 | 15/10 | Inventário completo, ficha digitada, fotos e caderno de bordo atualizado |
| E3 | 05/11 | Coleta e recursão funcionando, resumo hierárquico e ranking por uma ordenação própria |
| E4 | 12/11 | Sistema completo e pacote final congelado, incluindo relatórios, caderno de bordo e revisão por pares |
| E5 | 25 ou 26/11 | Pitch de cinco minutos, demonstração ao vivo e arguição |

As datas acima reproduzem o planejamento do documento-base; não indicam que as entregas já foram concluídas.

## Checklist do pacote final

- [ ] Seis módulos Python implementados e integrados.
- [ ] Inventário JSON com pelo menos 15 barreiras, 3 ambientes e 2 níveis.
- [ ] Ficha de campo preenchida e assinada pelo grupo.
- [ ] Uma foto por barreira, identificada pelo código.
- [ ] Relatório técnico em PDF com os achados A1 a A5.
- [ ] Relatório de texto gerado pelo próprio programa.
- [ ] Caderno de bordo com as três seções obrigatórias.
- [ ] Ficha de revisão por pares assinada pelo grupo revisor.
- [ ] Casos base identificados em comentários nas funções recursivas.
- [ ] Números do relatório reproduzíveis no sistema.
- [ ] Execução verificada em outra máquina.

## Saídas, conferências e apresentação da E3

O ranking inclui gravidade, pessoas/dia, custo em reais e índice. Os detalhes
preservam descrição, caminho, intervenção e base das estimativas. A origem de
custo, alcance e medida é exibida explicitamente; sem informação, fica marcada
como não informada. O relatório exportado pela opção 8 mantém essas ressalvas
e inclui matriz ambiente × tipo. Informe um nome novo: arquivos existentes
não são sobrescritos.

As opções 4 e 5 conferem quantidade esperada, códigos únicos, cobertura do piloto
quando informada, contagens e custos por ambiente contra o total recursivo.
Consulte o [roteiro da apresentação](docs/apresentacao_e3.md) para executar,
explicar os casos base e entender o que ainda falta para a E4.
