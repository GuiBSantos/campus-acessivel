"""Demonstração E3: python main.py (sem dependências externas)."""

import argparse
from pathlib import Path
import sys
import tempfile

from coleta import gravar_inventario, importar_ficha_campo, ler_inventario, montar_arvore
from ordenacao import bubble_sort, calcular_indices, confere_com_o_python
from recursao import achatar, contar_barreiras, custo_total, profundidade, resumo_hierarquico

BASE = Path(__file__).resolve().parent


def demonstrar(setor, pesos):
    """Validar round-trip JSON, imprimir hierarquia e ranking próprio."""
    with tempfile.TemporaryDirectory(prefix='campus-e3-') as pasta:
        arquivo = Path(pasta) / 'inventario.json'
        gravar_inventario(arquivo, setor)
        recarregado = ler_inventario(arquivo)
        if recarregado != setor:
            raise ValueError('Falha na conferência da persistência JSON.')
    print('Persistência JSON: gravação e leitura conferidas.')
    print('\nRESUMO HIERÁRQUICO')
    resumo_hierarquico(recarregado)
    print(f'Profundidade: {profundidade(recarregado)} níveis')
    print(f'Total: {contar_barreiras(recarregado)} barreiras | R$ {custo_total(recarregado):.2f}')
    registros = achatar(recarregado)
    calcular_indices(registros, pesos)
    ranking, comparacoes, trocas = bubble_sort(registros)
    if not confere_com_o_python(ranking, 'indice', False):
        raise ValueError('Falha na conferência do ranking.')
    print('\nRANKING — Bubble Sort próprio; empate por código crescente')
    print(f'Pesos: gravidade={pesos["gravidade"]}, pessoas/dia={pesos["pessoas_dia"]}')
    for posicao, registro in enumerate(ranking, 1):
        print(f'{posicao}. {registro["codigo"]} | índice {registro["indice"]:.4f} | {registro["caminho"]}')
    print(f'Comparações: {comparacoes} | Trocas: {trocas} | Conferência: OK')
    return ranking


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    origem = parser.add_mutually_exclusive_group()
    origem.add_argument('--inventario', type=Path, help='JSON com inventário validado')
    origem.add_argument('--ficha', type=Path, help='CSV separado por ponto e vírgula')
    parser.add_argument('--peso-gravidade', type=float, default=1)
    parser.add_argument('--peso-pessoas', type=float, default=1)
    args = parser.parse_args(argv)
    print('Campus Acessível — Grupo 5 — MVP E3')
    if args.inventario is None and args.ficha is None:
        print('DEMONSTRAÇÃO FICTÍCIA: estes dados e pesos não são resultados do piloto.')
        print('O piloto real permanece parcialmente conciliado; consulte docs/criterios_e3.md.')
    else:
        print('Pesos provisórios: valide os critérios com o grupo antes de recomendar intervenções.')
    try:
        if args.ficha:
            registros, erros = importar_ficha_campo(args.ficha)
            if erros:
                raise ValueError('\n'.join(erros))
            setor = montar_arvore(registros)
        else:
            setor = ler_inventario(args.inventario or BASE / 'dados/demonstracao.json')
        demonstrar(setor, {'gravidade': args.peso_gravidade, 'pessoas_dia': args.peso_pessoas})
    except (OSError, ValueError, RecursionError) as erro:
        print(f'Não foi possível executar: {erro}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
