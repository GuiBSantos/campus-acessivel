# Revisão do piloto — Grupo 5

Fonte: Campus_Acessivel_Grupo5_Inventario_Piloto (2).pdf, oito páginas, coleta atualizada em 21/10/2026.

## Informações confirmadas no documento

- Curso: Sistemas de Informação.
- Integrantes: Antonio Augusto Rodrigues Soares Júnior, Raphael Rios e Guilherme Barreto dos Santos.
- Setor: Prédio do Ensino Superior — UNASP-EC.
- Tabela com 15 registros preliminares, B01 a B15. Isso ainda não comprova 15 barreiras validadas.

## Pendências para montar o inventário

| Item | O que conferir |
| --- | --- |
| B01 e B02 | Preservar as medidas e a inclinação aproximada informadas; esclarecer localização, trechos e referência aplicável antes da classificação final. |
| B03 | O próprio piloto diz que 80 cm, isoladamente, não comprova não conformidade. Identificar ocorrências específicas e o obstáculo efetivo. |
| B04 | A tabela descreve um elevador medido; a árvore menciona elevador não implementado. Esclarecer se são locais diferentes. |
| B05 | Detalhar obstáculo, medidas e ocorrências dos Blocos A e B. |
| B06 a B11, B14 e B15 | Conciliar contagens de portas com Braille e afirmações de ausência na árvore. Registrar quais portas precisam de intervenção e o total observado. |
| B12 e B13 | Quantidades de estações e teclados, isoladamente, não demonstram insuficiência. Documentar demanda, contexto e critérios. |
| Árvore | Conciliar pavimentos térreo, inferior e superior; não assumir que térreo e inferior são sinônimos. Posicionar cada ocorrência uma única vez. |
| Itens extras da árvore | Corrimãos, piso tátil e audiodescrição não têm correspondência clara na tabela B01–B15. Confirmar evidências e eventual inclusão. |
| Fotos finais | B14 aparece associado a B16.jpg; o item final aparece como B17 onde a tabela usa B15. Corrigir identificação. |
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
