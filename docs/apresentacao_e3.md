# Roteiro de demonstração e defesa — E3

## Execução

Use Python 3, sem instalar pacotes. Na pasta do repositório:

```bash
python main.py
```

Sequência para ensaiar: 1 (carregar inventário do projeto), 4 (conferir), 5 (hierarquia),
6 (ranking), 8 (salvar em um novo arquivo .txt) e 0 (sair).
Para uma demonstração automática com os mesmos 15 registros: `python main.py --demo`.
Para carregar os 15 registros: opção 2, informe `dados/inventario.json`.
Para executar diretamente: `python main.py --inventario dados/inventario.json`.
A opção 3 importa CSV. Os arquivos documentais intermediários foram removidos.
O inventário atual foi fornecido em `inventario (1).json`; preserva hipóteses e
estimativas. O exemplo fictício fica apenas em `tests/fixtures` para testes.

## O que mostrar e explicar

1. **Validação:** campos obrigatórios, números válidos e código único em toda a árvore.
   A conferência verifica quantidade esperada (15 no inventário),
   e B01–B15 exatamente uma vez quando houver códigos de origem do piloto.
2. **Persistência:** a opção 7 grava e relê um JSON em diretório temporário e compara
   os dados; não substitui o arquivo de entrada.
3. **Hierarquia:** cada nó possui barreiras locais e subsetores. Os resumos dos
   pais já incluem filhos; não se deve somar todas as linhas da hierarquia.
   A tabela de totais locais usa o caminho completo e soma cada registro uma vez.
   Ela confere contagem e custo com os resultados recursivos, com tolerância
   inferior a um centavo para arredondamento numérico.
4. **Índice:** benefício = 0,6 × gravidade + 0,4 × nota de alcance (ambas de 1 a 5).
   Índice = benefício / (custo / 1000). O alcance usa exposição estimada dividida pelo denominador proxy autorizado de 1.600 pessoas/dia; explique que é aproximação global, não contagem local.
5. **Bubble Sort:** compara pares vizinhos e troca os que estão fora de ordem.
   Cada passagem coloca um elemento no fim da parte ainda não ordenada.
   Para antes se nenhuma troca ocorrer. Custo quadrático no pior caso.
   Conta comparações entre registros e trocas. Ordena uma cópia da lista.
   Maior índice vem primeiro; em empate, menor código em ordem alfabética.
   `sorted()` existe somente na função separada de conferência.
6. **Origens:** cada registro pode ter `origens` com textos para `custo`,
   `pessoas_dia` e `medida`. Por exemplo:

   ```json
   {"origens": {"custo": "estimado; hipótese de preço por placa", "pessoas_dia": "estimado; sem contagem", "medida": "medição de campo; ficha identificada"}}
   ```

   Na ausência desses dados, o programa informa “não informada”. Arquivos legados
   com `base_estimativa` têm custo e alcance marcados como estimados; hipóteses
   na unidade de medida são sinalizadas. O exemplo usado nos testes é identificado como
   fictício. A base completa é preservada na saída e no relatório; não se presume
   confirmação de campo pela simples existência de um número.

## Casos base da recursão

| Função | Caso base e retorno |
| --- | --- |
| `custo_total` | Folha: soma somente custos locais; nó vazio retorna 0. |
| `contar_barreiras` | Folha: quantidade de barreiras locais; nó vazio retorna 0. |
| `contar_por_tipo` | Folha: quantidade local do tipo solicitado. |
| `profundidade` | Folha tem profundidade 1; pai adiciona 1 à maior profundidade dos filhos. |
| `achatar` | Folha copia seus registros e acrescenta o caminho; sem filhos não há novas chamadas. |
| `caminho_da_barreira` | Encontrado no nó: retorna nome; busca esgotada: retorna None. |
| `resumo_hierarquico` | Imprime o nó; folha não chama a função novamente. |

## Situação dos módulos

| Módulo | Implementado para E3 | Pendente para E4 |
| --- | --- | --- |
| `coleta.py` | Validação, CSV, árvore, leitura e gravação JSON | Cadastro/edição/remoção interativos, se exigidos no sistema completo |
| `recursao.py` | Contagens, custos, profundidade, caminhos e resumo | Melhor pacote exaustivo |
| `ordenacao.py` | Índice, Bubble Sort, desempate e conferência | Selection Sort e Insertion Sort |
| `relatorio.py` | Moeda, tabela, origens, conferências, matriz e exportação textual | Comparação de pacotes e achados finais |
| `busca.py` | Não utilizado na E3 | Sequencial, binária iterativa e recursiva |

Os NotImplementedError restantes são limitações reais, não funcionalidades
prontas. Não basta remover um TODO para implementar a função.

## Verificação

```bash
python -m unittest discover -s tests -v
```

Explique o que foi conferido e diferencie consistência do programa de confirmação
dos dados. Na defesa, cada integrante deve conseguir mostrar um percurso recursivo
com um exemplo pequeno e explicar uma comparação e um desempate do Bubble Sort.
