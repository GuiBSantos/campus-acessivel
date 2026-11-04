"""Índice provisório e Bubble Sort próprio para a E3."""

import math

from coleta import validar_registro


def indice_prioridade(barreira, pesos):
    """Calcular benefício por mil reais; rejeitar valores inválidos."""
    erros = validar_registro(barreira)
    if erros:
        raise ValueError('; '.join(erros))
    for fator in ('gravidade', 'pessoas_dia'):
        peso = pesos.get(fator)
        if isinstance(peso, bool) or not isinstance(peso, (int, float)) or not math.isfinite(peso) or peso < 0:
            raise ValueError(f'Peso inválido: {fator}.')
    if pesos['gravidade'] + pesos['pessoas_dia'] == 0:
        raise ValueError('Pelo menos um peso deve ser positivo.')
    beneficio = barreira['gravidade'] * pesos['gravidade'] + barreira['pessoas_dia'] * pesos['pessoas_dia']
    return beneficio / (barreira['custo'] / 1000)


def calcular_indices(lista, pesos):
    """Calcular todos os índices antes de atualizar os registros."""
    indices = [indice_prioridade(barreira, pesos) for barreira in lista]
    for barreira, indice in zip(lista, indices):
        barreira['indice'] = indice


def bubble_sort(lista, chave='indice', crescente=False):
    """Ordenar cópia; empates por código crescente; contar comparações e trocas."""
    resultado = list(lista)
    comparacoes = trocas = 0
    for fim in range(len(resultado) - 1, 0, -1):
        mudou = False
        for i in range(fim):
            comparacoes += 1
            a, b = resultado[i], resultado[i + 1]
            trocar = (a[chave] > b[chave]) if crescente else (a[chave] < b[chave])
            if a[chave] == b[chave]:
                trocar = a['codigo'] > b['codigo']
            if trocar:
                resultado[i], resultado[i + 1] = b, a
                trocas += 1
                mudou = True
        if not mudou:
            break
    return resultado, comparacoes, trocas


def selection_sort(lista, chave="indice", crescente=False):
    """Devolver (lista_ordenada, comparacoes, trocas), sem alterar a entrada."""
    raise NotImplementedError("Implementação pendente pelo grupo.")


def insertion_sort(lista, chave="indice", crescente=False):
    """Devolver (lista_ordenada, comparacoes, trocas), sem alterar a entrada."""
    raise NotImplementedError("Implementação pendente pelo grupo.")


def confere_com_o_python(ordenada, chave, crescente):
    """Conferir ordenação e desempate; único uso de sorted no projeto."""
    esperado = sorted(ordenada, key=lambda item: (item[chave] if crescente else -item[chave], item['codigo']))
    return ordenada == esperado
