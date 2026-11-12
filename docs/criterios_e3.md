# Critérios finais do modelo de prioridade

## Decisão técnica adotada

Para manter uma regra única e comparável, este projeto adota gravidade e alcance em escala de 1 a 5, com pesos de 60% e 40%. A escolha prioriza a remoção de impedimentos graves sem ignorar quantas pessoas encontram a barreira. É uma decisão metodológica do projeto para análise acadêmica; não é norma técnica nem aprovação institucional do campus.

- **Gravidade (1–5):** 1 = desconforto leve; 2 = dificuldade com alternativa próxima; 3 = limitação relevante; 4 = grande restrição ou necessidade frequente de ajuda; 5 = acesso impedido ou risco imediato.
- **Alcance (1–5):** percentual estimado de usuários únicos do ambiente que encontram a barreira em um dia típico: até 20% = 1; 21–40% = 2; 41–60% = 3; 61–80% = 4; 81–100% = 5. Registrar também numerador, denominador, período e método.
- **Benefício:** 0,6 × gravidade + 0,4 × alcance.
- **Índice custo-benefício:** benefício ÷ (custo em reais / 1.000).
- **Empates:** código crescente. Para seleção de pacote, maior benefício total, depois menor custo e códigos crescentes.

O campo `pessoas_dia` registra exposição bruta. Como o grupo autorizou usar o fluxo estimado, o inventário usa `usuarios_dia: 1600` como denominador proxy global e converte a proporção em nota de alcance. Essa aproximação não é contagem local; substituí-la por usuários do ambiente quando houver dados. O programa calcula benefício = 0,6 × gravidade + 0,4 × nota de alcance.

Detalhamento de fontes e contas: `docs/estimativas_custo.md`.

## Regra para custos

Usar custo total da intervenção (quantidade × preço unitário + instalação/mão de obra + transporte). Guardar fonte, data, escopo, quantidade e responsável. Orçamento formal ou cotações locais prevalecem. Preços públicos são estimativas de referência e não cotações do UNASP. Custos sem comparável direto permanecem placeholders de planejamento e não devem orientar contratação nem pacote final.

## Registros e evidência

O inventário operacional é `dados/inventario.json`, com B01–B15. `dados/validacao_normativa.json` e `docs/validacao_normativa.md` registram limites documentais. `null` com status `pendente` significa que ainda não há referência numérica comparável; no elevador, `nao_avaliado` significa observação funcional sem conclusão normativa. Nenhum status documental equivale a laudo ou vistoria.

B03 permanece barreira de conforto com gravidade 1, sem alegação de infração aos 80 cm. B04 descreve dificuldade observada em elevador existente, sem afirmar ausência ou desconformidade normativa. B12/B13 são limitações de capacidade relatadas, sem cotas normativas ou demanda simultânea medida.

## Critérios do software

Medida é não negativa; gravidade é inteiro 1–5; pessoas/dia é inteiro não negativo; custo deve ser positivo para permitir o cálculo. Referência normativa numérica deve corresponder à mesma grandeza/unidade da medida quando aplicável. Referência desconhecida fica nula e pendente, sem inventar zero ou transferir limites de outra grandeza.

CSV usa UTF-8, `;` e caminho separado por `/` ou `>`; JSON preserva `origens` e `base_estimativa`. A validação estrutural verifica tipos e consistência, mas não atesta medições, estimativas, acessibilidade ou conformidade.

## Algoritmos e contagens

Bubble Sort sem parada antecipada e Selection Sort fazem n(n−1)/2 comparações. Insertion Sort usa trocas adjacentes; buscas binárias exigem entrada ordenada. A busca contabiliza registros examinados e informa separadamente a ordenação preparatória. A busca exaustiva avalia pacotes dentro do teto, conta chamadas base e desempata por menor custo e códigos. Resultados didáticos em `resultados/analise_crescimento_exaustiva.md` usam dados sintéticos.
