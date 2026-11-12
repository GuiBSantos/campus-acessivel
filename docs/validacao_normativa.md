# Conferência normativa documental — 12/11/2026

Esta análise confronta o piloto e o inventário com fontes normativas. Não é vistoria nem laudo de acessibilidade. A confirmação das condições físicas requer conferência no local por responsável habilitado. A autorização para definir critérios não substitui medidas ausentes.

## Fontes

- [S1 — ABNT NBR 9050:2020, versão corrigida 2021, texto disponibilizado pelo Governo do Paraná](https://www.pibema.pr.gov.br/pagina/construir/abnt_nbr9050.pdf).
- [S2 — Catálogo ABNT: NBR 9050, status em vigor](https://www.abntcatalogo.com.br/sebrae/norma.aspx?Q=R0xSeFNpSnIxMU0vUk5wQThYdUVIemhZTkhlUHdyK01INVZheVZrZGlHWT0%3D).
- [S3 — Catálogo ABNT: NBR 16858-3:2022, status em vigor](https://www.abntcatalogo.com.br/sebrae/norma.aspx?Q=anFOUVM5UVdoYzBtcjNxaHVtTjRBMlU0MmNjUDFzM3ZyTlJMenBoSzlwbz0%3D).
- [S4 — Lei 13.146/2015, art. 28, publicação da Câmara](https://www2.camara.leg.br/legin/fed/lei/2015/lei-13146-6-julho-2015-781174-publicacaooriginal-147468-pl.html).

O catálogo confirma a edição da NBR 9050 usada. Para o elevador, S3 confirma a norma específica atual, mas seu texto integral não foi consultado: não atribuímos dimensão mínima universal de cabine.

## Critérios conferidos em S1 (síntese)

| ID | Seção | Critério |
| --- | --- | --- |
| R | 6.6.2.1, tabela 4 | Desnível por segmento: até 1,50 m → até 5%; até 1,00 m → até 6,25%; até 0,80 m → até 8,33%. |
| RX | 6.6.2.2, tabela 5 | Exceção de reforma: acima de 10% até 12,5%, desnível máximo 0,075 m, um segmento; exige esgotar soluções regulares. |
| P | 6.11.2.4 | Vão livre de porta: largura mínima 0,80 m; altura mínima 2,10 m. |
| S | 5.4.1 | Portas/passagens sinalizadas exigem identificação acessível; conferir parede/batente. Informação tátil não fica na folha móvel. |
| A | 10.15.2 | Ambientes pedagógicos precisam de conexão por rota acessível. |
| M | 9.3.1.3–4 | Mesa: tampo mínimo 0,90 m; altura 0,75–0,85 m; vão inferior mínimo 0,80 × 0,73 × 0,50 m (largura/altura/profundidade). |

O percentual do item 10.16.6 trata de terminais em bibliotecas/centros de leitura; não é automaticamente uma cota para laboratório. S4 orienta recursos conforme necessidades educacionais; não fundamenta uma quantidade fixa de teclados Braille.

## Aplicação aos registros — inferências, não novas medições

| Piloto | Decisão documental | Falta para fechar |
| --- | --- | --- |
| B01 | Tipo candidato: `rampa_inclinada`. Referência condicional: 6,25%, critério R. | Confirmar que 7,84 m é um segmento inclinado contínuo e que o ângulo de 7° representa esse segmento. |
| B02 | Tipo candidato: `rampa_inclinada`. Sem valor único aplicável ao segmento descrito; redimensionamento precisa considerar divisão e patamares. | Medir desnível de cada trecho e delimitar segmentos reais. |
| B03 | 80 cm como referência da largura, critério P. O valor medido atende esse requisito isolado. Não chamar de porta estreita com essa evidência. | Verificar porta por porta, vão efetivamente livre e demais condições de uso. Manter como observação/oportunidade, não barreira confirmada. |
| B04 | Equipamento existente: não classificar como `elevador_ausente`. Referência dimensional pendente. | Identificar elevador versus plataforma, modelo, instalação, portas e documentação técnica; selecionar norma e tabela aplicáveis. |
| B05 | Critério A fundamenta investigação do acesso; não há referência dimensional determinada. | Identificar e medir o obstáculo. O degrau de 15 cm do JSON é hipótese, não medição. |
| B06–B11, B14–B15 | `sinalizacao_ausente` apenas após conferir a identificação completa de cada acesso; critério S. | Fotografar porta, parede adjacente e batente; conferir identificação visual, tátil e eventuais soluções sonoras. Contar o total real. |
| B12 | Avaliar características dos postos pelo critério M. A contagem de dois postos não permite concluir insuficiência. | Medir mobiliário, circulação e identificar demanda. Não comparar “2 estações” com centímetros de uma mesa. |
| B13 | Não foi identificada cota numérica de teclados nas fontes consultadas. | Levantar necessidades de uso e recursos efetivamente disponíveis. Um teclado não prova atendimento nem insuficiência. |

### Cálculo derivado das rampas

Se os comprimentos do piloto forem inclinados e cada trecho mantiver aproximadamente 7°:

- B01: h = 7,84 × sen(7°) ≈ 0,955 m.
- B02: h = 12,76 × sen(7°) ≈ 1,555 m por trecho.
- Inclinação: tan(7°) × 100 ≈ 12,28%.

Esses resultados são cálculos a partir do piloto, não desníveis medidos. Nessas condições, B01 excede R; B02 requer revisão também da segmentação; RX não justifica os trechos descritos. A expressão “8,33% para desnível até 1,50 m” do caderno não reproduz corretamente a tabela 4. Registre a divergência e não use o anexo simplificado para dimensionar uma obra.

## Decisão sobre o modelo de dados

O arquivo complementar `dados/validacao_normativa.json` cobre os 15 códigos do piloto, sem substituir o inventário operacional.

- `referencia_numerica` só contém número quando representa a mesma grandeza da medição.
- `null` significa referência não fechada nesta auditoria. Não é zero e não significa aprovação desse formato pelo professor.
- `tipo_candidato` organiza a futura migração; não comprova existência da barreira.
- Tipos adicionais sugeridos para investigação: `equipamento_elevacao_em_avaliacao`, `acesso_em_avaliacao`, `posto_trabalho_em_avaliacao`, `recurso_assistivo_em_avaliacao`. Sua justificativa fica registrada aqui e no caderno de bordo. Não devem ser apresentados como categorias oficiais da norma.
- B03 deve permanecer rastreável, mas não contar como barreira comprovada apenas para completar quinze itens.
- Não converter a contagem estimada de portas em uma porcentagem normativa inventada. Também não usar 0 como substituto de referência desconhecida.
- Antes da migração operacional: adaptar validação/importação, separar observações de barreiras confirmadas e tornar explícita a elegibilidade no ranking. O programa atual ainda classifica os 15 registros recebidos, incluindo hipóteses.

A conferência normativa não valida gravidade, fluxo, preços ou a recomendação financeira. Esses critérios continuam sendo decisões documentadas do grupo.


## Atualizacao: inventario sem hipoteses

O contrato operacional agora exige referencia normativa numerica. Os 15 registros anteriores foram preservados em `dados/registros_pendentes.json` e retirados do inventario operacional e do ranking, pois nenhum estava integralmente confirmado. As descricoes anteriores da simulacao com 15 registros sao historicas. O inventario conserva a hierarquia, mas tem zero barreiras; o minimo academico continua pendente. Consulte `dados/README.md` para o contrato atual.
