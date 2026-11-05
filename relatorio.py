"""Tabelas, rastreabilidade, conferências e relatório de texto da E3."""

from contextlib import redirect_stdout
from decimal import Decimal
from io import StringIO
from math import isclose
from pathlib import Path

from coleta import validar_setor
from ordenacao import bubble_sort, calcular_indices, confere_com_o_python
from recursao import achatar, contar_barreiras, custo_total, profundidade, resumo_hierarquico


def reais(valor):
    """Formatar moeda sem depender da configuração regional da máquina."""
    texto = f'{valor:,.2f}'
    return 'R$ ' + texto.replace(',', '_').replace('.', ',').replace('_', '.')


def origem_campo(registro, campo):
    """Ler origem explícita; manter a incerteza em arquivos legados."""
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
    """Conferir códigos, cobertura e somas independentes por caminho completo."""
    erros = validar_setor(setor)
    if erros:
        return erros
    registros = achatar(setor)
    if len(registros) != esperado:
        erros.append(f'Quantidade: esperadas {esperado} barreiras, encontradas {len(registros)}.')
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
        if len(pilotos) != 15:
            erros.append('Cobertura do piloto: esperados 15 códigos de origem.')
    quantidade = sum(grupo['quantidade'] for grupo in grupos.values())
    total = sum((grupo['custo'] for grupo in grupos.values()), Decimal('0'))
    if quantidade != contar_barreiras(setor):
        erros.append('Contagem por ambientes difere do total recursivo.')
    if not isclose(float(total), custo_total(setor), rel_tol=0, abs_tol=0.005):
        erros.append('Custos por ambientes diferem do total recursivo.')
    return erros


def matriz_ambiente_tipo(registros):
    """Matriz de contagens, com caminhos completos para ambientes homônimos."""
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


def texto_ranking(setor, pesos):
    """Gerar tabela e detalhes com as hipóteses originais, sem alterar dados."""
    registros = achatar(setor)
    calcular_indices(registros, pesos)
    ranking, comparacoes, trocas = bubble_sort(registros)
    if not confere_com_o_python(ranking, 'indice', False):
        raise ValueError('Falha na conferência do ranking.')
    linhas = ['RANKING — Bubble Sort próprio; empate por código crescente',
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
    """Incluir totais locais sem somar novamente os subtotais da árvore."""
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
    erros = conferir_inventario(setor, esperado)
    linhas.append('\nCONFERÊNCIAS')
    linhas.extend(erros or [f'OK: {esperado} códigos únicos; contagens e custos por ambientes conferem com o total.'])
    linhas.append('Consistência dos dados não comprova medições, cotações ou conformidade normativa.')
    return '\n'.join(linhas)


def gerar_relatorio(setor, pesos, esperado=15):
    """O texto exportado preserva as mesmas ressalvas exibidas no terminal."""
    ranking, _ = texto_ranking(setor, pesos)
    registros = achatar(setor)
    ambientes, tipos, matriz = matriz_ambiente_tipo(registros)
    linhas = ['Campus Acessível — relatório E3',
              'Valores podem ser estimados, fictícios ou ter origem não informada. Consulte os detalhes.',
              texto_resumo(setor, esperado), ranking, '\nMATRIZ AMBIENTE × TIPO', 'Ambiente | ' + ' | '.join(tipos)]
    for ambiente, linha in zip(ambientes, matriz):
        linhas.append(ambiente + ' | ' + ' | '.join(str(valor) for valor in linha))
    return '\n\n'.join(linhas) + '\n'


def exportar_relatorio(caminho, setor, pesos, esperado=15):
    """Criar relatório sem sobrescrever arquivos existentes."""
    texto = gerar_relatorio(setor, pesos, esperado)
    with Path(caminho).open('x', encoding='utf-8') as arquivo:
        arquivo.write(texto)
