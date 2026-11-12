"""Buscas próprias; uma comparação contada por registro examinado.

As buscas binárias exigem lista previamente ordenada por código crescente.
A ordenação é responsabilidade do chamador, fora do contador da busca.
"""


def busca_sequencial(lista, codigo):
    comparacoes = 0
    for posicao, registro in enumerate(lista):
        comparacoes += 1
        if registro['codigo'] == codigo:
            return posicao, comparacoes
    return -1, comparacoes


def busca_binaria_iterativa(lista, codigo):
    inicio, fim = 0, len(lista) - 1
    comparacoes = 0
    while inicio <= fim:
        meio = (inicio + fim) // 2
        comparacoes += 1
        atual = lista[meio]['codigo']
        if atual == codigo:
            return meio, comparacoes
        if atual < codigo:
            inicio = meio + 1
        else:
            fim = meio - 1
    return -1, comparacoes


def busca_binaria_recursiva(lista, codigo, inicio=0, fim=None, contador=None):
    if fim is None:
        fim = len(lista) - 1
    if contador is None:
        contador = [0]
    # Caso base 1: intervalo vazio, código ausente.
    if inicio > fim:
        return -1, contador[0]
    meio = (inicio + fim) // 2
    contador[0] += 1
    atual = lista[meio]['codigo']
    # Caso base 2: código encontrado.
    if atual == codigo:
        return meio, contador[0]
    if atual < codigo:
        return busca_binaria_recursiva(lista, codigo, meio + 1, fim, contador)
    return busca_binaria_recursiva(lista, codigo, inicio, meio - 1, contador)
