# Revisão do piloto — Grupo 5

Fonte lida: `Campus_Acessivel_Grupo5_Inventario_Piloto (2)..pdf`, oito páginas, coleta atualizada em 21/10/2026. O documento registra 15 itens preliminares; as pendências abaixo são de classificação, medição complementar e documentação para o sistema, não afirmação de que o grupo não foi a campo.

## Informações confirmadas no documento

- Curso: Sistemas de Informação.
- Integrantes: Antonio Augusto Rodrigues Soares Júnior, Raphael Rios e Guilherme Barreto dos Santos.
- Setor: Prédio do Ensino Superior — UNASP-EC.
- Tabela com 15 registros preliminares, B01 a B15, além de medições de B01–B04, critério de gravidade, faixas de custo e árvore do setor.
- Custos seguem em faixas preliminares; não são cotações numéricas. Pessoas/dia não aparecem no PDF.
- As páginas indicam espaços reservados para fotos. Associar os arquivos fotográficos reais aos códigos antes do pacote final; verificar B14/B16 e B15/B17.

## Pendências para montar o inventário

| Item | O que conferir |
| --- | --- |
| B01 e B02 | O grupo confirma o ângulo aproximado de 7° como medição de campo. `tan(7°) × 100` resulta em aproximadamente 12,3%; desníveis calculados da geometria são estimativas. B02 está descrita como dois trechos de 12,76 m, sem patamares. Não há nova medição pendente para registrar esses dados; desnível/projeção direta só são necessários se o grupo quiser uma conferência geométrica adicional. |
| B03 | Vão útil de 80 cm atende ao mínimo citado. Antonio aprovou classificar como oportunidade de conforto, gravidade baixa, sem alegar não conformidade. Confirmar com grupo/professor se oportunidade conta entre as 15 barreiras. |
| B04 | O elevador existe; dimensões da cabine 1,32 m × 0,89 m e desconforto/dependência de ajuda foram relatados. Usar tipo `elevador_inadequado`; identificar modelo e referência somente para afirmar conformidade normativa. |
| B05 | O grupo esclareceu que falta uma pequena rampa no acesso às áreas livres. Medir o desnível e a largura da passagem para dimensionar e descrever a intervenção. |
| B06 a B11, B14 e B15 | As contagens atuais informam portas com Braille, mas falta o total de portas verificadas por local. Completar total, com identificação e sem identificação. |
| B12 e B13 | O grupo informa 2 estações acessíveis entre cerca de 20 computadores e um teclado Braille. Confirmar contagem exata, o que torna uma estação acessível e descrever o impacto prático da quantidade disponível. |
| Árvore | Conciliar pavimentos térreo, inferior e superior; não assumir que térreo e inferior são sinônimos. Posicionar cada ocorrência uma única vez. |
| Itens extras da árvore | Corrimãos, piso tátil e audiodescrição não têm correspondência clara na tabela B01–B15. Confirmar evidências e eventual inclusão. |
| Fotos finais | O PDF referencia B16.jpg para B14 e B17.jpg para B15. O grupo vai recuperar/adicionar as fotos e confirmar o mapeamento dos arquivos com os códigos finais. |
| Gravidade | O piloto tem quatro categorias verbais; o sistema exige valores de 1 a 5 com critérios escritos. Definir a escala antes de converter. |
| Custo | Obter estimativa numérica por intervenção e registrar fonte/método. As faixas baixo/médio/alto não bastam para otimização. |
| Alcance | Estimar pessoas afetadas por dia com método declarado. |
| Rastreabilidade | Confirmar responsável por cada coleta, data de cada registro, foto, descrição, unidade, referência e intervenção. |
| Códigos | Migrar para SETOR-SUBSETOR-NN preservando tabela de correspondência com B01–B15. |

Não inserir preços, pesos, medidas ou conclusões normativas inventados para fazer o sistema rodar.

## Ordem sugerida de implementação

1. Conciliar a árvore com a tabela e definir o contrato dos registros.
2. Implementar validação e persistência em coleta.py.
3. Implementar percurso, contagens e totais em recursao.py, comentando os casos base.
4. Definir índice e desempate; implementar uma ordenação para o checkpoint.
5. Completar ordenações, buscas e respectivos contadores.
6. Comparar seleção gulosa e exaustiva, integrar menu e relatórios.
