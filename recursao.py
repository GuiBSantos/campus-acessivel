"""Percursos recursivos da hierarquia do inventário."""


def custo_total(no):
    """Caso base: folha soma somente suas próprias barreiras."""
    total = sum(barreira['custo'] for barreira in no['barreiras'])
    for filho in no['subsetores']:
        total += custo_total(filho)
    return total


def contar_barreiras(no):
    """Caso base: folha devolve a quantidade local."""
    total = len(no['barreiras'])
    for filho in no['subsetores']:
        total += contar_barreiras(filho)
    return total


def contar_por_tipo(no, tipo):
    """Caso base: folha conta apenas ocorrências locais do tipo."""
    total = sum(1 for barreira in no['barreiras'] if barreira['tipo'] == tipo)
    for filho in no['subsetores']:
        total += contar_por_tipo(filho, tipo)
    return total


def profundidade(no):
    """Caso base: folha tem profundidade 1."""
    maior = 0
    for filho in no['subsetores']:
        valor = profundidade(filho)
        if valor > maior:
            maior = valor
    return 1 + maior


def achatar(no, caminho=''):
    """Caso base: folha copia suas barreiras; preserva a árvore original."""
    caminho = caminho + '/' + no['nome'] if caminho else no['nome']
    registros = [dict(barreira, caminho=caminho) for barreira in no['barreiras']]
    for filho in no['subsetores']:
        registros.extend(achatar(filho, caminho))
    return registros


def caminho_da_barreira(no, codigo):
    """Casos base: código local encontrado, ou folha sem correspondência."""
    for barreira in no['barreiras']:
        if barreira['codigo'] == codigo:
            return no['nome']
    for filho in no['subsetores']:
        caminho = caminho_da_barreira(filho, codigo)
        if caminho is not None:
            return no['nome'] + '/' + caminho
    return None


def resumo_hierarquico(no, nivel=0, formatar_custo=None):
    """Imprimir totais por nó. Caso base: folha não faz novas chamadas."""
    custo = (formatar_custo(custo_total(no)) if formatar_custo else f"R$ {custo_total(no):.2f}")
    print(f"{'  ' * nivel}{no['nome']}: {contar_barreiras(no)} barreiras | {custo}")
    for filho in no['subsetores']:
        resumo_hierarquico(filho, nivel + 1, formatar_custo)


def preparar_pacote(barreiras, orcamento, pesos):
    """Converter dinheiro em centavos para não ultrapassar o teto por arredondamento."""
    from decimal import Decimal, InvalidOperation
    from ordenacao import beneficio_total_item

    def centavos(valor):
        try:
            numero = Decimal(str(valor))
            if not numero.is_finite() or numero < 0 or numero * 100 != (numero * 100).to_integral_value():
                raise ValueError('Use valores monetários não negativos com até duas casas decimais.')
            return int(numero * 100)
        except InvalidOperation as erro:
            raise ValueError('Valor monetário inválido.') from erro

    teto = centavos(orcamento)
    candidatos = []
    for registro in barreiras:
        beneficio = beneficio_total_item(registro, pesos)
        custo = centavos(registro['custo'])
        # Poda legítima: com custos positivos, esse item não cabe em combinação alguma.
        if custo <= teto:
            candidatos.append((registro, custo, beneficio))
    return candidatos, teto


def melhor_pacote_exaustivo(barreiras, orcamento, pesos, indice=0, contador=None):
    """Explorar incluir/excluir; empate por menor custo, depois códigos crescentes.

    contador, quando fornecido, é uma lista de um inteiro. Inclui chamadas base.
    O chamador deve avisar e confirmar a execução acima de 20 candidatos.
    """
    from ordenacao import bubble_sort
    if not isinstance(indice, int) or indice < 0 or indice > len(barreiras):
        raise ValueError('Índice inicial inválido.')
    ordenadas, _, _ = bubble_sort(barreiras[indice:], 'codigo', True)
    candidatos, teto = preparar_pacote(ordenadas, orcamento, pesos)
    if contador is None:
        contador = [0]

    def visitar(posicao, saldo):
        contador[0] += 1
        # Caso base: todos os candidatos já foram decididos.
        if posicao == len(candidatos):
            return 0, 0, []
        melhor = visitar(posicao + 1, saldo)
        registro, custo, beneficio = candidatos[posicao]
        if custo <= saldo:
            b, c, codigos = visitar(posicao + 1, saldo - custo)
            incluir = (b + beneficio, c + custo, [registro['codigo']] + codigos)
            if (incluir[0] > melhor[0] or
                (incluir[0] == melhor[0] and (incluir[1] < melhor[1] or
                 (incluir[1] == melhor[1] and incluir[2] < melhor[2])))):
                melhor = incluir
        return melhor

    beneficio, custo, codigos = visitar(0, teto)
    return beneficio, custo / 100, codigos, contador[0]


def pacote_guloso(barreiras, orcamento, pesos):
    """Selecionar por índice; pular itens que não cabem e continuar o percurso."""
    from ordenacao import bubble_sort, calcular_indices
    registros = [dict(item) for item in barreiras]
    calcular_indices(registros, pesos)
    ranking, _, _ = bubble_sort(registros)
    candidatos, saldo = preparar_pacote(ranking, orcamento, pesos)
    beneficio = custo = 0
    codigos = []
    for registro, valor, ganho in candidatos:
        if valor <= saldo:
            saldo -= valor
            custo += valor
            beneficio += ganho
            codigos.append(registro['codigo'])
    return beneficio, custo / 100, codigos, 0
