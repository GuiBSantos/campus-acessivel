# Crescimento da busca exaustiva — experimento didático

**Natureza dos dados:** totalmente fictícios, gerados a partir da fixture de demonstração. Estes números avaliam o algoritmo; não são resultados das barreiras do campus.

**Condições:** Python 3; pesos `gravidade=1` e `pessoas_dia=1`; cada item recebeu gravidade cíclica de 1 a 5, alcance `10 × posição` e custo `R$ 100 + R$ 10 × (posição − 1)`. A tabela compara dois tetos: o custo total de todos os itens, que não restringe combinações, e um teto didático fixo de R$ 200. A contagem inclui chamadas base e ocorre depois da poda de candidatos cujo custo individual supera o teto.

| Itens originais | Teto | Candidatos após poda | Chamadas recursivas | Observação |
| ---: | ---: | ---: | ---: | --- |
| 4 | R$ 460,00 | 4 | 31 | Sem restrição efetiva; `2^(4+1) − 1`. |
| 4 | R$ 200,00 | 4 | 15 | Combinações deixam de ramificar quando o saldo não comporta o próximo item. |
| 8 | R$ 1.080,00 | 8 | 511 | Sem restrição efetiva; `2^(8+1) − 1`. |
| 8 | R$ 200,00 | 8 | 45 | Vários ramos de inclusão são cortados pelo saldo restante. |
| 12 | R$ 1.860,00 | 12 | 8.191 | Sem restrição efetiva; `2^(12+1) − 1`. |
| 12 | R$ 200,00 | 11 | 78 | Um item é removido antes da recursão por custar mais que o teto. |
| 16 | R$ 2.800,00 | 16 | 131.071 | Sem restrição efetiva; `2^(16+1) − 1`. |
| 16 | R$ 200,00 | 11 | 78 | Cinco itens são removidos pela poda individual; os demais ramos também sofrem poda pelo saldo. |

## Interpretação

Sem podas, cada item cria dois ramos — incluir ou não incluir — e a árvore completa tem `2^(n+1) − 1` chamadas contando as folhas. Dobrar o número de itens eleva rapidamente o trabalho: de 31 chamadas com 4 itens para 131.071 com 16. Por isso a busca exaustiva é útil para conjuntos pequenos, mas não escala para centenas de barreiras.

O teto reduz o trabalho de duas formas. Primeiro, itens mais caros que o orçamento são removidos antes da recursão. Depois, quando o saldo não comporta o item atual, seu ramo de inclusão não é aberto. Com o teto didático de R$ 200, o experimento cai de 8.191 para 78 chamadas com 12 itens; com 16, cai de 131.071 para 78 chamadas porque cinco candidatos são removidos e nenhum par dos 11 restantes cabe no teto: os dois itens mais baratos somam R$ 210.

O segundo teto foi escolhido apenas para demonstrar podas, sem relação com orçamento real do campus. A análise final de A4 ainda deve usar o inventário validado e tetos justificados pelo grupo.
