import argparse
import json
from pathlib import Path
import sys
import tempfile

from coleta import gravar_inventario, importar_ficha_campo, ler_inventario, montar_arvore, validar_setor, alterar_barreira
from relatorio import conferir_inventario, exportar_relatorio, texto_resumo, texto_ranking
from recursao import contar_barreiras, achatar
from ordenacao import bubble_sort
from busca import busca_sequencial, busca_binaria_iterativa, busca_binaria_recursiva
from relatorio import texto_desempenho, texto_sensibilidade, texto_planos, matriz_ambiente_tipo

BASE = Path(__file__).resolve().parent


def demonstrar(setor, pesos, esperado=15):
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
    setor = None
    ficticio = False
    origem = 'nenhum'
    while True:
        print(f'\nInventário carregado: {origem}')
        print('1 — Carregar inventário do projeto')
        print('2 — Carregar inventário JSON')
        print('3 — Importar ficha CSV')
        print('4 — Validar inventário carregado')
        print('5 — Mostrar resumo hierárquico')
        print('6 — Mostrar ranking')
        print('7 — Executar demonstração completa')
        print('8 — Exportar relatório de texto')
        print('9 — Localizar barreira por código')
        print('10 — Matriz ambiente × tipo')
        print('11 — Comparar pacotes sob orçamento')
        print('12 — Desempenho e sensibilidade')
        print('13 — Ranking com algoritmo escolhido')
        print('14 — Cadastrar / editar / remover barreira')
        print('15 — Salvar inventário em novo arquivo JSON')
        print('0 — Sair')
        try:
            opcao = input('Opção: ').strip()
            if opcao == '0':
                return 0
            if opcao in ('1', '2', '3'):
                caminho = (BASE / 'dados/inventario.json' if opcao == '1'
                           else Path(input('Caminho do arquivo: ').strip()).expanduser())
                novo = carregar_ficha(caminho) if opcao == '3' else ler_inventario(caminho)
                setor = novo
                ficticio = False
                origem = str(caminho)
                print(f'Inventário carregado: {contar_barreiras(setor)} barreiras.')
                avisar_origem(ficticio)
            elif opcao in ('4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15'):
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
                    elif opcao == '8':
                        destino = Path(input('Novo arquivo de relatório (.txt): ').strip()).expanduser()
                        exportar_relatorio(destino, setor, pesos, 4 if ficticio else 15)
                        print(f'Relatório salvo em {destino}.')
                    elif opcao == '9':
                        codigo = input('Código: ').strip()
                        metodo = input('Busca (sequencial/iterativa/recursiva): ').strip()
                        metodos = {'sequencial': busca_sequencial, 'iterativa': busca_binaria_iterativa,
                                   'recursiva': busca_binaria_recursiva}
                        if metodo not in metodos:
                            raise ValueError('Método de busca inválido.')
                        registros = achatar(setor)
                        if metodo != 'sequencial':
                            registros, comparacoes, trocas = bubble_sort(registros, 'codigo', True)
                            print(f'Ordenação prévia: {comparacoes} comparações, {trocas} trocas.')
                        posicao, comparacoes = metodos[metodo](registros, codigo)
                        print(registros[posicao] if posicao != -1 else 'Código não encontrado.')
                        print(f'Busca: {comparacoes} comparações.')
                    elif opcao == '10':
                        ambientes, tipos, matriz = matriz_ambiente_tipo(achatar(setor))
                        print('Ambiente | ' + ' | '.join(tipos))
                        for ambiente, linha in zip(ambientes, matriz):
                            print(ambiente + ' | ' + ' | '.join(str(n) for n in linha))
                    elif opcao == '11':
                        tetos = [float(valor.strip().replace(',', '.')) for valor in
                                 input('Orçamentos separados por ; (ex.: 1000;2000;5000;10000): ').split(';')]
                        resultado = texto_planos(setor, pesos, tetos)
                        print(resultado)
                        if '(>20)' in resultado:
                            print('A busca exaustiva pode explorar até 2^n combinações.')
                            if input('Executar mesmo assim? Digite SIM: ').strip() == 'SIM':
                                resultado = texto_planos(setor, pesos, tetos, permitir_grande=True)
                                print(resultado)
                        destino = input('Salvar comparação em novo .txt (Enter para pular): ').strip()
                        if destino:
                            with open(destino, 'x', encoding='utf-8') as arquivo:
                                arquivo.write(resultado + '\n')
                    elif opcao == '14':
                        acao = input('Ação (cadastrar/editar/remover): ').strip()
                        codigo = input('Código atual: ').strip() if acao != 'cadastrar' else None
                        registro = caminho = None
                        if acao != 'remover':
                            caminho = input('Caminho de um ambiente existente: ').strip()
                            print('Informe um objeto JSON com os campos do registro (na edição, apenas alterações).')
                            registro = json.loads(input('Registro JSON: '))
                        setor = alterar_barreira(setor, acao, codigo, registro, caminho)
                        print('Alteração validada em memória. Use opção 15 para salvar.')
                    elif opcao == '15':
                        destino = Path(input('Novo arquivo JSON: ').strip()).expanduser()

                        conteudo = json.dumps(setor, ensure_ascii=False, indent=2, allow_nan=False)
                        with destino.open('x', encoding='utf-8') as arquivo:
                            arquivo.write(conteudo + '\n')
                        print(f'Inventário salvo em {destino}.')
                    elif opcao == '13':
                        metodo = input('Ordenação (bubble/selection/insertion): ').strip()
                        if metodo not in ('bubble', 'selection', 'insertion'):
                            raise ValueError('Ordenação inválida.')
                        print(texto_ranking(setor, pesos, metodo)[0])
                    elif opcao == '12':
                        print(texto_desempenho(setor, pesos))
                        print(texto_sensibilidade(setor, pesos))
            else:
                print('Opção inválida. Escolha um número de 0 a 15.')
        except (EOFError, KeyboardInterrupt):
            print('\nEncerrando o menu.')
            return 0
        except (OSError, ValueError, RecursionError) as erro:
            print(f'Não foi possível executar: {erro}')


def main(argv=None):
    parser = argparse.ArgumentParser(description='Menu E3: python main.py; demonstração automática: python main.py --demo.')
    origem = parser.add_mutually_exclusive_group()
    origem.add_argument('--demo', action='store_true', help='Executar demonstração com o inventário do projeto sem menu')
    origem.add_argument('--inventario', type=Path, help='Executar com um inventário JSON sem menu')
    origem.add_argument('--ficha', type=Path, help='Executar com uma ficha CSV sem menu')
    parser.add_argument('--peso-gravidade', type=float, default=1)
    parser.add_argument('--peso-pessoas', type=float, default=1)
    args = parser.parse_args(argv)
    pesos = {'gravidade': args.peso_gravidade, 'pessoas_dia': args.peso_pessoas}
    print('Campus Acessível — Grupo 5 — análise de intervenções')
    if not args.demo and args.inventario is None and args.ficha is None:
        return menu(pesos)
    avisar_origem(False)
    try:
        setor = (carregar_ficha(args.ficha) if args.ficha
                 else ler_inventario(args.inventario or BASE / 'dados/inventario.json'))
        demonstrar(setor, pesos)
    except (OSError, ValueError, RecursionError) as erro:
        print(f'Não foi possível executar: {erro}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
