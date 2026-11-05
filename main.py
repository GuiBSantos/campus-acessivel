"""Menu E3: python main.py; demonstração automática: python main.py --demo."""

import argparse
from pathlib import Path
import sys
import tempfile

from coleta import gravar_inventario, importar_ficha_campo, ler_inventario, montar_arvore, validar_setor
from relatorio import conferir_inventario, exportar_relatorio, texto_resumo, texto_ranking
from recursao import contar_barreiras

BASE = Path(__file__).resolve().parent


def demonstrar(setor, pesos, esperado=15):
    """Validar round-trip JSON, imprimir hierarquia e ranking próprio."""
    with tempfile.TemporaryDirectory(prefix='campus-e3-') as pasta:
        arquivo = Path(pasta) / 'inventario.json'
        gravar_inventario(arquivo, setor)
        recarregado = ler_inventario(arquivo)
        if recarregado != setor:
            raise ValueError('Falha na conferência da persistência JSON.')
    print('Persistência JSON: gravação e leitura conferidas.')
    mostrar_resumo(recarregado, esperado)
    return mostrar_ranking(recarregado, pesos)


def mostrar_resumo(setor, esperado=15):
    print('\n' + texto_resumo(setor, esperado))


def mostrar_ranking(setor, pesos):
    texto, ranking = texto_ranking(setor, pesos)
    print('\n' + texto)
    return ranking


def carregar_ficha(caminho):
    registros, erros = importar_ficha_campo(caminho)
    if erros:
        raise ValueError('\n'.join(erros))
    return montar_arvore(registros)


def avisar_origem(ficticio):
    if ficticio:
        print('DEMONSTRAÇÃO FICTÍCIA: estes dados e pesos não são resultados do piloto.')
    else:
        print('Arquivo fornecido: validar a estrutura não confirma medições ou cotações.')
        print('Custos e alcance podem ser estimados; confira as fontes do inventário.')
    print('Pesos provisórios: valide os critérios com o grupo antes de recomendar intervenções.')


def menu(pesos):
    """Manter inventário em memória; falhas de carga preservam o anterior."""
    setor = None
    ficticio = False
    origem = 'nenhum'
    while True:
        print(f'\nInventário carregado: {origem}')
        print('1 — Carregar demonstração fictícia')
        print('2 — Carregar inventário JSON')
        print('3 — Importar ficha CSV')
        print('4 — Validar inventário carregado')
        print('5 — Mostrar resumo hierárquico')
        print('6 — Mostrar ranking')
        print('7 — Executar demonstração completa')
        print('8 — Exportar relatório de texto')
        print('0 — Sair')
        try:
            opcao = input('Opção: ').strip()
            if opcao == '0':
                return 0
            if opcao in ('1', '2', '3'):
                caminho = (BASE / 'dados/demonstracao.json' if opcao == '1'
                           else Path(input('Caminho do arquivo: ').strip()).expanduser())
                novo = carregar_ficha(caminho) if opcao == '3' else ler_inventario(caminho)
                setor = novo
                ficticio = opcao == '1'
                origem = str(caminho)
                print(f'Inventário carregado: {contar_barreiras(setor)} barreiras.')
                avisar_origem(ficticio)
            elif opcao in ('4', '5', '6', '7', '8'):
                if setor is None:
                    print('Carregue um inventário primeiro: opção 1, 2 ou 3.')
                    continue
                if opcao == '4':
                    erros = validar_setor(setor)
                    print('\n'.join(erros) if erros else 'Estrutura válida: campos, códigos e árvore conferidos.')
                    conferencias = conferir_inventario(setor, 4 if ficticio else 15)
                    print('\n'.join(conferencias) if conferencias else 'Conferências: códigos únicos, cobertura e totais por ambientes OK.')
                else:
                    avisar_origem(ficticio)
                    if opcao == '5':
                        mostrar_resumo(setor, 4 if ficticio else 15)
                    elif opcao == '6':
                        mostrar_ranking(setor, pesos)
                    elif opcao == '7':
                        demonstrar(setor, pesos, 4 if ficticio else 15)
                    else:
                        destino = Path(input('Novo arquivo de relatório (.txt): ').strip()).expanduser()
                        exportar_relatorio(destino, setor, pesos, 4 if ficticio else 15)
                        print(f'Relatório salvo em {destino}.')
            else:
                print('Opção inválida. Escolha um número de 0 a 8.')
        except (EOFError, KeyboardInterrupt):
            print('\nEncerrando o menu.')
            return 0
        except (OSError, ValueError, RecursionError) as erro:
            print(f'Não foi possível executar: {erro}')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    origem = parser.add_mutually_exclusive_group()
    origem.add_argument('--demo', action='store_true', help='Executar demonstração fictícia sem menu')
    origem.add_argument('--inventario', type=Path, help='Executar com um inventário JSON sem menu')
    origem.add_argument('--ficha', type=Path, help='Executar com uma ficha CSV sem menu')
    parser.add_argument('--peso-gravidade', type=float, default=1)
    parser.add_argument('--peso-pessoas', type=float, default=1)
    args = parser.parse_args(argv)
    pesos = {'gravidade': args.peso_gravidade, 'pessoas_dia': args.peso_pessoas}
    print('Campus Acessível — Grupo 5 — MVP E3')
    if not args.demo and args.inventario is None and args.ficha is None:
        return menu(pesos)
    avisar_origem(args.demo)
    try:
        setor = (carregar_ficha(args.ficha) if args.ficha
                 else ler_inventario(args.inventario or BASE / 'dados/demonstracao.json'))
        demonstrar(setor, pesos, 4 if args.demo else 15)
    except (OSError, ValueError, RecursionError) as erro:
        print(f'Não foi possível executar: {erro}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
