from contextlib import redirect_stdout
from decimal import Decimal
from io import StringIO
from math import isclose
from pathlib import Path

from coleta import validar_setor
from ordenacao import bubble_sort, selection_sort, insertion_sort, calcular_indices, confere_com_o_python
from recursao import achatar, contar_barreiras, custo_total, profundidade, resumo_hierarquico


def reais(valor):
    texto = f'{valor:,.2f}'
    return 'R$ ' + texto.replace(',', '_').replace('.', ',').replace('_', '.')


def origem_campo(registro, campo):
    origens = registro.get('origens', {})
    origem = origens.get(campo) if isinstance(origens, dict) else None
    if isinstance(origem, str) and origem.strip():
        return origem.strip()
    if registro.get('coletado_por') == 'Dados sintéticos':
        return 'fictício — demonstração didática'
    if campo == 'medida' and any(p in registro['unidade'].casefold()
                                for p in ('hipótese', 'não medida', 'sem medição')):
        return 'estimada / sem medição confirmada'
    if campo in ('custo', 'pessoas_dia') and registro.get('base_estimativa'):
        return 'estimado (ver base_estimativa)'
    return 'não informada'


def conferir_inventario(setor, esperado=15):
    erros = validar_setor(setor)
    if erros:
        return erros
    registros = achatar(setor)
    oportunidades = [registro for registro in registros
                     if registro.get('classificacao') == 'oportunidade_melhoria']
    if oportunidades:
        candidatos = len(registros) - len(oportunidades)
        codigos = ', '.join(registro['codigo'] for registro in oportunidades)
        erros.append(f'Classificacao: {codigos} e oportunidade de melhoria e nao conta '
                     f'como barreira comprovada; {candidatos} candidatos restantes, '
                     'ainda sujeitos a validacao de campo.')
        if candidatos < esperado:
            erros.append(f'Quantidade elegivel: minimo de {esperado} barreiras; '
                         f'{candidatos} candidatos apos excluir oportunidades. '
                         f'Faltam pelo menos {esperado - candidatos} ocorrencias comprovadas.')
    if len(registros) < esperado:
        erros.append(f'Quantidade: mínimo de {esperado} barreiras, encontradas {len(registros)}.')
    codigos = []
    pilotos = []
    grupos = {}
    for registro in registros:
        codigo = registro['codigo']
        if codigos.count(codigo):
            erros.append(f'Código duplicado: {codigo}.')
        codigos.append(codigo)
        piloto = registro.get('codigo_piloto')
        if piloto:
            pilotos.append(piloto)
        caminho = registro['caminho']
        if caminho not in grupos:
            grupos[caminho] = {'quantidade': 0, 'custo': Decimal('0')}
        grupos[caminho]['quantidade'] += 1
        grupos[caminho]['custo'] += Decimal(str(registro['custo']))
    if pilotos and esperado == 15:
        for i in range(1, 16):
            codigo = f'B{i:02}'
            if pilotos.count(codigo) != 1:
                erros.append(f'Cobertura do piloto: {codigo} deve aparecer uma vez.')

    if len(grupos) < 3:
        erros.append('Cobertura: mínimo de 3 ambientes com barreiras.')
    if profundidade(setor) < 2:
        erros.append('Hierarquia: mínimo de 2 níveis.')
    quantidade = sum(grupo['quantidade'] for grupo in grupos.values())
    total = sum((grupo['custo'] for grupo in grupos.values()), Decimal('0'))
    if quantidade != contar_barreiras(setor):
        erros.append('Contagem por ambientes difere do total recursivo.')
    if not isclose(float(total), custo_total(setor), rel_tol=0, abs_tol=0.005):
        erros.append('Custos por ambientes diferem do total recursivo.')
    return erros


def matriz_ambiente_tipo(registros):
    ambientes, tipos = [], []
    for registro in registros:
        if registro['caminho'] not in ambientes:
            ambientes.append(registro['caminho'])
        if registro['tipo'] not in tipos:
            tipos.append(registro['tipo'])
    matriz = [[0 for tipo in tipos] for ambiente in ambientes]
    for registro in registros:
        matriz[ambientes.index(registro['caminho'])][tipos.index(registro['tipo'])] += 1
    return ambientes, tipos, matriz


def texto_ranking(setor, pesos, algoritmo="bubble"):
    algoritmos = {"bubble": bubble_sort, "selection": selection_sort, "insertion": insertion_sort}
    """Gerar tabela e detalhes com as hipóteses originais, sem alterar dados."""
    registros = achatar(setor)
    calcular_indices(registros, pesos)
    ranking, comparacoes, trocas = algoritmos[algoritmo](registros)
    if not confere_com_o_python(ranking, 'indice', False):
        raise ValueError('Falha na conferência do ranking.')
    linhas = [f'RANKING — {algoritmo.title()} Sort próprio; empate por código crescente',
              f'Pesos provisórios: gravidade={pesos["gravidade"]}, pessoas/dia={pesos["pessoas_dia"]}',
              'Origens: veja custo, alcance e medida nos detalhes de cada registro.',
              f'{"Pos":>3}  {"Código":<16} {"Grav.":>5} {"Pessoas/dia":>11} {"Custo":>18} {"Índice":>12}']
    for posicao, registro in enumerate(ranking, 1):
        linhas.append(f'{posicao:>3}  {registro["codigo"]:<16} {registro["gravidade"]:>5} '
                      f'{registro["pessoas_dia"]:>11} {reais(registro["custo"]):>18} {registro["indice"]:>12.4f}')
    linhas.append(f'Comparações: {comparacoes} | Trocas: {trocas} | Conferência: OK')
    linhas.append('\nDETALHES E ORIGEM DOS VALORES')
    for registro in ranking:
        linhas.extend([f'\n{registro["codigo"]} — {registro["descricao"]}',
                       f'Ambiente: {registro["caminho"]}',
                       f'Custo: {reais(registro["custo"])} | origem: {origem_campo(registro, "custo")}',
                       f'Alcance: {registro["pessoas_dia"]} pessoas/dia | origem: {origem_campo(registro, "pessoas_dia")}',
                       f'Medida: {registro["medida"]} {registro["unidade"]} | origem: {origem_campo(registro, "medida")}',
                       f'Intervenção: {registro["intervencao"]}'])
        if registro.get('base_estimativa'):
            linhas.append('Hipóteses / base da estimativa: ' + registro['base_estimativa'])
    return '\n'.join(linhas), ranking


def texto_resumo(setor, esperado=15):
    saida = StringIO()
    with redirect_stdout(saida):
        print('RESUMO HIERÁRQUICO')
        resumo_hierarquico(setor, formatar_custo=reais)
    linhas = [saida.getvalue().rstrip(), f'Profundidade: {profundidade(setor)} níveis',
              f'Total: {contar_barreiras(setor)} barreiras | {reais(custo_total(setor))}',
              'Custos consolidados podem incluir estimativas ou dados fictícios; consulte as origens nos detalhes.',
              '\nTOTAIS LOCAIS POR AMBIENTE (sem duplicar subtotais)']
    grupos = {}
    for registro in achatar(setor):
        grupo = grupos.setdefault(registro['caminho'], [0, Decimal('0')])
        grupo[0] += 1
        grupo[1] += Decimal(str(registro['custo']))
    for caminho, (quantidade, custo) in grupos.items():
        linhas.append(f'{caminho}: {quantidade} barreiras | {reais(custo)}')
    linhas.append('\nA3 — TOTAIS POR SUBSETOR DE PRIMEIRO NÍVEL')
    for filho in setor['subsetores']:
        linhas.append(f"{filho['nome']}: {contar_barreiras(filho)} barreiras | {reais(custo_total(filho))}")
    registros = achatar(setor)
    if registros:
        graves, _, _ = bubble_sort(registros, 'gravidade', False)
        linhas.append(f"Barreira mais grave (empate por código): {graves[0]['codigo']} | {graves[0]['caminho']}")
    erros = conferir_inventario(setor, esperado)
    linhas.append('\nCONFERÊNCIAS')
    linhas.extend(erros or [f'OK: {contar_barreiras(setor)} códigos únicos; contagens e custos por ambientes conferem com o total.'])
    linhas.append('Consistência dos dados não comprova medições, cotações ou conformidade normativa.')
    return '\n'.join(linhas)


def gerar_relatorio(setor, pesos, esperado=15):
    ranking, _ = texto_ranking(setor, pesos)
    registros = achatar(setor)
    ambientes, tipos, matriz = matriz_ambiente_tipo(registros)
    linhas = ['Campus Acessível — relatório de análise',
              'Valores podem ser estimados, fictícios ou ter origem não informada. Consulte os detalhes.',
              texto_resumo(setor, esperado), ranking, '\nMATRIZ AMBIENTE × TIPO', 'Ambiente | ' + ' | '.join(tipos)]
    for ambiente, linha in zip(ambientes, matriz):
        linhas.append(ambiente + ' | ' + ' | '.join(str(valor) for valor in linha))
    linhas.extend([texto_desempenho(setor, pesos), texto_sensibilidade(setor, pesos)])
    return '\n\n'.join(linhas) + '\n'


def exportar_relatorio(caminho, setor, pesos, esperado=15):
    texto = gerar_relatorio(setor, pesos, esperado)
    with Path(caminho).open('x', encoding='utf-8') as arquivo:
        arquivo.write(texto)


def texto_desempenho(setor, pesos):
    from busca import busca_sequencial, busca_binaria_iterativa, busca_binaria_recursiva
    registros = achatar(setor)
    calcular_indices(registros, pesos)
    linhas = ['A1 — tamanho | entrada | algoritmo | comparações | trocas']
    tamanhos = []
    for tamanho in (len(registros) // 3, 2 * len(registros) // 3, len(registros)):
        if tamanho > 0 and tamanho not in tamanhos:
            tamanhos.append(tamanho)
    for tamanho in tamanhos:
        base = registros[:tamanho]
        ordenada, _, _ = bubble_sort(base)
        for nome, entrada in (('coleta', base), ('ordenada', ordenada), ('inversa', ordenada[::-1])):
            for algoritmo in (bubble_sort, selection_sort, insertion_sort):
                _, comparacoes, trocas = algoritmo(entrada)
                linhas.append(f'{tamanho} | {nome} | {algoritmo.__name__} | {comparacoes} | {trocas}')
    por_codigo, comparacoes, trocas = bubble_sort(registros, 'codigo', True)
    linhas.append(f'\nA2 — preparo por código: {comparacoes} comparações, {trocas} trocas')
    if por_codigo:
        codigos = [por_codigo[0]['codigo'], por_codigo[len(por_codigo)//2]['codigo'],
                   por_codigo[-1]['codigo'], por_codigo[len(por_codigo)//3]['codigo']]
        ausente = '__AUSENTE__'
        while busca_sequencial(por_codigo, ausente)[0] != -1:
            ausente += '_'
        codigos.append(ausente)
        for codigo in codigos:
            for busca in (busca_sequencial, busca_binaria_iterativa, busca_binaria_recursiva):
                posicao, contagem = busca(por_codigo, codigo)
                linhas.append(f'{codigo} | {busca.__name__} | posição={posicao} | comparações={contagem}')
    return '\n'.join(linhas)


def texto_sensibilidade(setor, pesos):
    linhas = ['A5 — sensibilidade dos pesos provisórios']
    for nome, usados in (('original', pesos),
                         ('gravidade dobrada', dict(pesos, gravidade=2 * pesos['gravidade'])),
                         ('alcance dobrado', dict(pesos, pessoas_dia=2 * pesos['pessoas_dia']))):
        registros = achatar(setor)
        calcular_indices(registros, usados)
        ranking, _, _ = bubble_sort(registros)
        linhas.append(nome + ': ' + ', '.join(item['codigo'] for item in ranking[:10]))
    return '\n'.join(linhas)


def texto_planos(setor, pesos, orcamentos, permitir_grande=False):
    from recursao import pacote_guloso, melhor_pacote_exaustivo, preparar_pacote
    registros = achatar(setor)
    linhas = ['A4 — orçamento | estratégia | benefício | custo | itens | chamadas | códigos']
    for teto in orcamentos:
        candidatos, _ = preparar_pacote(registros, teto, pesos)
        for nome, algoritmo in (('guloso', pacote_guloso), ('exaustivo', melhor_pacote_exaustivo)):
            if nome == 'exaustivo' and len(candidatos) > 20 and not permitir_grande:
                linhas.append(f'{teto}: exaustiva não executada: {len(candidatos)} candidatos (>20).')
                continue
            beneficio, custo, codigos, chamadas = algoritmo(registros, teto, pesos)
            linhas.append(f'{teto} | {nome} | {beneficio} | {custo:.2f} | {len(codigos)} | {chamadas} | {codigos}')
    return '\n'.join(linhas)
