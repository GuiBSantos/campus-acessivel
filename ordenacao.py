import math

from coleta import validar_registro

FLUXO_DIARIO_ESTIMADO = 1600


def nota_alcance(barreira):
    """Converte o fluxo bruto em nota usando o denominador histórico autorizado."""
    numerador = barreira['pessoas_dia']
    denominador = barreira.get('usuarios_dia', FLUXO_DIARIO_ESTIMADO)
    if (isinstance(denominador, bool) or not isinstance(denominador, int)
            or denominador <= 0 or numerador > denominador):
        raise ValueError(f"{barreira.get('codigo')}: pessoas_dia/usuarios_dia inválidos.")
    proporcao = 100 * numerador / denominador
    return 1 if proporcao <= 20 else 2 if proporcao <= 40 else 3 if proporcao <= 60 else 4 if proporcao <= 80 else 5


def indice_prioridade(barreira, pesos):
    erros = validar_registro(barreira)
    if erros:
        raise ValueError('; '.join(erros))
    if not isinstance(pesos, dict):
        raise ValueError('Pesos devem ser um dicionário.')
    for fator in ('gravidade', 'alcance'):
        peso = pesos.get(fator)
        if isinstance(peso, bool) or not isinstance(peso, (int, float)) or (isinstance(peso, float) and not math.isfinite(peso)) or peso < 0:
            raise ValueError(f'Peso inválido: {fator}.')
    if pesos['gravidade'] + pesos['alcance'] == 0:
        raise ValueError('Pelo menos um peso deve ser positivo.')
    try:
        alcance = nota_alcance(barreira)
        beneficio = barreira['gravidade'] * pesos['gravidade'] + alcance * pesos['alcance']
        resultado = beneficio / (barreira['custo'] / 1000)
        if not math.isfinite(resultado):
            raise ValueError('Índice fora da faixa numérica suportada.')
        return resultado
    except (OverflowError, ZeroDivisionError) as erro:
        raise ValueError('Valores fora da faixa numérica suportada.') from erro


def calcular_indices(lista, pesos):
    indices = [indice_prioridade(barreira, pesos) for barreira in lista]
    for barreira, indice in zip(lista, indices):
        barreira['indice'] = indice


def bubble_sort(lista, chave='indice', crescente=False):
    resultado = list(lista)
    comparacoes = trocas = 0
    for fim in range(len(resultado) - 1, 0, -1):
        for i in range(fim):
            comparacoes += 1
            a, b = resultado[i], resultado[i + 1]
            trocar = (a[chave] > b[chave]) if crescente else (a[chave] < b[chave])
            if a[chave] == b[chave]:
                trocar = a['codigo'] > b['codigo']
            if trocar:
                resultado[i], resultado[i + 1] = b, a
                trocas += 1
    return resultado, comparacoes, trocas


def selection_sort(lista, chave="indice", crescente=False):
    resultado = list(lista)
    comparacoes = trocas = 0
    for i in range(len(resultado) - 1):
        melhor = i
        for j in range(i + 1, len(resultado)):
            comparacoes += 1
            if vem_antes(resultado[j], resultado[melhor], chave, crescente):
                melhor = j
        if melhor != i:
            resultado[i], resultado[melhor] = resultado[melhor], resultado[i]
            trocas += 1
    return resultado, comparacoes, trocas


def insertion_sort(lista, chave="indice", crescente=False):
    resultado = list(lista)
    comparacoes = trocas = 0
    for i in range(1, len(resultado)):
        j = i
        while j > 0:
            comparacoes += 1
            if not vem_antes(resultado[j], resultado[j - 1], chave, crescente):
                break
            resultado[j], resultado[j - 1] = resultado[j - 1], resultado[j]
            trocas += 1
            j -= 1
    return resultado, comparacoes, trocas


def confere_com_o_python(ordenada, chave, crescente):
    por_codigo = sorted(ordenada, key=lambda item: item['codigo'])
    esperado = sorted(por_codigo, key=lambda item: item[chave], reverse=not crescente)
    return ordenada == esperado


def vem_antes(a, b, chave, crescente):
    if a[chave] == b[chave]:
        return a['codigo'] < b['codigo']
    return a[chave] < b[chave] if crescente else a[chave] > b[chave]


def beneficio_total_item(barreira, pesos):
    indice_prioridade(barreira, pesos)
    return barreira['gravidade'] * pesos['gravidade'] + nota_alcance(barreira) * pesos['alcance']
