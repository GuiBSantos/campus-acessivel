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


def resumo_hierarquico(no, nivel=0):
    """Imprimir totais por nó. Caso base: folha não faz novas chamadas."""
    print(f"{'  ' * nivel}{no['nome']}: {contar_barreiras(no)} barreiras | R$ {custo_total(no):.2f}")
    for filho in no['subsetores']:
        resumo_hierarquico(filho, nivel + 1)


def melhor_pacote_exaustivo(barreiras, orcamento, pesos, indice=0, contador=None):
    """Devolver (beneficio, custo, lista_de_codigos, chamadas)."""
    raise NotImplementedError("Implementação pendente pelo grupo.")

