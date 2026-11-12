import csv
import json
import math
import re
from datetime import date
from pathlib import Path

TEXTOS = ('codigo', 'ambiente', 'tipo', 'descricao', 'unidade',
          'intervencao', 'coletado_por', 'data_coleta')
NUMEROS = ('medida', 'gravidade', 'pessoas_dia', 'custo')


TIPOS = frozenset((
    # Categorias do Anexo A do caderno do aluno.
    'degrau_isolado', 'desnivel_soleira', 'piso_irregular', 'rampa_inclinada',
    'ausencia_corrimao', 'porta_estreita', 'circulacao_estreita', 'balcao_alto',
    'interruptor_alto', 'mobiliario_inadequado', 'banheiro_inadequado',
    'sinalizacao_ausente', 'vaga_ausente', 'elevador_ausente',
    # Categorias específicas justificadas pelo inventário do Grupo 5.
    'porta_conforto', 'elevador_inadequado',
))

CLASSIFICACOES = frozenset(('barreira', 'oportunidade_melhoria'))


def calcular_inclinacao_percentual(desnivel_vertical, projecao_horizontal):
    """Calcula a inclinação de uma rampa a partir de medidas no mesmo sistema de unidade."""
    valores = (desnivel_vertical, projecao_horizontal)
    if any(isinstance(valor, bool) or not isinstance(valor, (int, float))
           or (isinstance(valor, float) and not math.isfinite(valor)) for valor in valores):
        raise ValueError('Desnível e projeção horizontal devem ser números finitos.')
    if desnivel_vertical < 0 or projecao_horizontal <= 0:
        raise ValueError('Desnível não pode ser negativo e projeção deve ser positiva.')
    return desnivel_vertical / projecao_horizontal * 100


def estimar_geometria_rampa(comprimento_inclinado, angulo_graus):
    """Estima desnível, projeção e inclinação usando comprimento e ângulo medidos."""
    valores = (comprimento_inclinado, angulo_graus)
    if any(isinstance(valor, bool) or not isinstance(valor, (int, float))
           or (isinstance(valor, float) and not math.isfinite(valor)) for valor in valores):
        raise ValueError('Comprimento e ângulo devem ser números finitos.')
    if comprimento_inclinado <= 0 or not 0 < angulo_graus < 90:
        raise ValueError('Comprimento deve ser positivo e ângulo entre 0° e 90°.')
    angulo = math.radians(angulo_graus)
    desnivel = comprimento_inclinado * math.sin(angulo)
    projecao = comprimento_inclinado * math.cos(angulo)
    return {
        'desnivel_estimado': desnivel,
        'projecao_horizontal_estimada': projecao,
        'inclinacao_percentual': calcular_inclinacao_percentual(desnivel, projecao),
    }


def validar_registro(barreira, codigos_usados=None):
    if not isinstance(barreira, dict):
        return ['Barreira deve ser um dicionário.']
    erros = []
    for campo in TEXTOS:
        valor = barreira.get(campo)
        if not isinstance(valor, str) or not valor.strip():
            erros.append(f'{campo}: texto obrigatório.')
        elif campo == 'descricao' and len(valor.strip()) < 10:
            erros.append('descricao: detalhe insuficiente para ser verificável.')
    tipo = barreira.get('tipo')
    if not isinstance(tipo, str) or tipo not in TIPOS:
        erros.append('tipo: categoria desconhecida.')
    classificacao = barreira.get('classificacao')
    if (classificacao is not None and
            (not isinstance(classificacao, str) or classificacao not in CLASSIFICACOES)):
        erros.append('classificacao: use barreira ou oportunidade_melhoria.')
    referencia = barreira.get('referencia_norma')
    status_normativo = barreira.get('status_normativo')
    referencia_observacional = (
        (tipo == 'elevador_inadequado' and referencia is None
         and status_normativo == 'nao_avaliado')
        or (referencia is None and status_normativo == 'pendente')
    )
    if (not referencia_observacional and
            (isinstance(referencia, bool) or not isinstance(referencia, (int, float))
             or (isinstance(referencia, float) and not math.isfinite(referencia))
             or referencia < 0)):
        erros.append('referencia_norma: numero finito nao negativo obrigatorio.')
    if barreira.get('pendencia_normativa'):
        erros.append('pendencia_normativa: resolva a pendencia antes de importar.')
    if status_normativo not in (None, 'confirmado', 'pendente') and not referencia_observacional:
        erros.append('status_normativo: registro ainda nao confirmado.')
    codigo = barreira.get('codigo')
    if isinstance(codigo, str):
        if not re.fullmatch(r'[A-Z0-9]+-[A-Z0-9]+-\d{2,}', codigo):
            erros.append('codigo: use SETOR-SUBSETOR-NN.')
        if codigos_usados is not None:
            for anterior in codigos_usados:
                if anterior == codigo:
                    erros.append(f'Código repetido: {codigo}.')
                    break
            codigos_usados.append(codigo)
    for campo in NUMEROS:
        valor = barreira.get(campo)
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            erros.append(f'{campo}: número obrigatório.')
        elif isinstance(valor, float) and not math.isfinite(valor):
            erros.append(f'{campo}: número finito obrigatório.')
        elif campo == 'gravidade' and (not isinstance(valor, int) or not 1 <= valor <= 5):
            erros.append('gravidade: inteiro de 1 a 5.')
        elif campo == 'pessoas_dia' and (not isinstance(valor, int) or valor < 0):
            erros.append('pessoas_dia: inteiro não negativo.')
        elif campo == 'custo' and valor <= 0:
            erros.append('custo: deve ser positivo.')
        elif campo == 'medida' and valor < 0:
            erros.append('medida: não pode ser negativa.')
    data_coleta = barreira.get('data_coleta', '')
    try:
        if not isinstance(data_coleta, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', data_coleta):
            raise ValueError
        date.fromisoformat(data_coleta)
    except (TypeError, ValueError):
        erros.append('data_coleta: data válida no formato AAAA-MM-DD.')
    return erros


def validar_setor(no, codigos=None):
    if codigos is None:
        codigos = []
    if not isinstance(no, dict):
        return ['Setor deve ser um dicionário.']
    erros = []
    if not isinstance(no.get('nome'), str) or not no['nome'].strip():
        erros.append('Setor sem nome válido.')
    for campo in ('barreiras', 'subsetores'):
        if not isinstance(no.get(campo), list):
            erros.append(f'{campo}: lista obrigatória.')
    if erros:
        return erros
    for barreira in no['barreiras']:
        erros.extend(validar_registro(barreira, codigos))
        if isinstance(barreira, dict) and barreira.get('ambiente') != no['nome']:
            erros.append(f'{barreira.get("codigo")}: ambiente difere do nó.')
    nomes = []
    for filho in no['subsetores']:
        if isinstance(filho, dict):
            for nome in nomes:
                if filho.get('nome') == nome:
                    erros.append(f'Subsetor repetido: {nome}.')
            nomes.append(filho.get('nome'))
        erros.extend(validar_setor(filho, codigos))
    return erros


def importar_ficha_campo(caminho):
    registros, erros, codigos = [], [], []
    with open(caminho, encoding='utf-8-sig', newline='') as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=';')
        obrigatorios = ('caminho', 'referencia_norma') + TEXTOS + NUMEROS
        for campo in obrigatorios:
            if leitor.fieldnames is None or leitor.fieldnames.count(campo) != 1:
                return [], [f'Cabeçalho ausente ou duplicado: {campo}.']
        for linha, registro in enumerate(leitor, 2):
            problemas = []
            if None in registro:
                problemas.append('Quantidade de campos maior que o cabeçalho.')
            valor = registro.get('referencia_norma')
            if (valor is None or not str(valor).strip()) and registro.get('tipo') == 'elevador_inadequado' and registro.get('status_normativo') == 'nao_avaliado':
                registro['referencia_norma'] = None
            else:
                try:
                    registro['referencia_norma'] = float(str(valor).replace(',', '.'))
                except (TypeError, ValueError):
                    problemas.append('referencia_norma: n?mero inv?lido.')
            for campo in NUMEROS:
                try:
                    registro[campo] = (int(registro[campo]) if campo in
                                       ('gravidade', 'pessoas_dia') else float(str(registro[campo]).replace(',', '.')))
                except (TypeError, ValueError):
                    problemas.append(f'{campo}: número inválido.')
            caminho_no = registro.get('caminho') or ''
            partes = [parte.strip() for parte in caminho_no.replace('>', '/').split('/')]
            if len(partes) < 2 or any(not parte for parte in partes):
                problemas.append('caminho: informe setor/ambiente sem partes vazias.')
            elif partes[-1] != registro.get('ambiente'):
                problemas.append('caminho: último componente deve ser o ambiente.')
            problemas.extend(validar_registro(registro, codigos))
            if problemas:
                erros.extend(f'Linha {linha}: {problema}' for problema in problemas)
            else:
                registro['caminho'] = '/'.join(partes)
                registros.append(registro)
    return registros, erros


def montar_arvore(registros):
    raiz = None
    for registro in registros:
        partes = registro['caminho'].split('/')
        if raiz is None:
            raiz = dict(nome=partes[0], barreiras=[], subsetores=[])
        if partes[0] != raiz['nome']:
            raise ValueError('Todos os registros devem pertencer ao mesmo setor.')
        no = raiz
        for nome in partes[1:]:
            encontrado = None
            for filho in no['subsetores']:
                if filho['nome'] == nome:
                    encontrado = filho
                    break
            if encontrado is None:
                encontrado = dict(nome=nome, barreiras=[], subsetores=[])
                no['subsetores'].append(encontrado)
            no = encontrado
        no['barreiras'].append(dict(registro))
    if raiz is None:
        raise ValueError('Nenhum registro para montar a árvore.')
    erros = validar_setor(raiz)
    if erros:
        raise ValueError('\n'.join(erros))
    return raiz


def gravar_inventario(caminho, setor):
    erros = validar_setor(setor)
    if erros:
        raise ValueError('\n'.join(erros))
    conteudo = json.dumps(setor, ensure_ascii=False, indent=2, allow_nan=False)
    Path(caminho).write_text(conteudo + '\n', encoding='utf-8')


def ler_inventario(caminho):
    with open(caminho, encoding='utf-8') as arquivo:
        setor = json.load(arquivo)
    erros = validar_setor(setor)
    if erros:
        raise ValueError('\n'.join(erros))
    return setor


def alterar_barreira(setor, acao, codigo=None, registro=None, caminho=None):
    import copy
    novo = copy.deepcopy(setor)
    if acao not in ('cadastrar', 'editar', 'remover'):
        raise ValueError('Ação inválida.')
    erros = validar_setor(novo)
    if erros:
        raise ValueError('; '.join(erros))
    encontrado = None
    destino = None
    caminho = caminho.replace('>', '/') if isinstance(caminho, str) else caminho
    if caminho:
        caminho = '/'.join(parte.strip() for parte in caminho.split('/'))
    pilha = [(novo, novo['nome'])]
    while pilha:
        no, atual = pilha.pop()
        if atual == caminho:
            destino = no
        for posicao, item in enumerate(no['barreiras']):
            if item['codigo'] == codigo:
                encontrado = (no, posicao)
        for filho in no['subsetores']:
            pilha.append((filho, atual + '/' + filho['nome']))
    if acao != 'cadastrar' and encontrado is None:
        raise ValueError('Código não encontrado.')
    if acao != 'remover':
        if destino is None:
            raise ValueError('Caminho de destino não encontrado na árvore.')
        if not isinstance(registro, dict):
            raise ValueError('Registro deve ser um objeto JSON.')
        item = dict(encontrado[0]['barreiras'][encontrado[1]]) if acao == 'editar' else {}
        item.update(registro)
        item['ambiente'] = destino['nome']
        if 'caminho' in item:
            item['caminho'] = caminho
    if acao != 'cadastrar':
        del encontrado[0]['barreiras'][encontrado[1]]
    if acao != 'remover':
        destino['barreiras'].append(item)
    erros = validar_setor(novo)
    if erros:
        raise ValueError('; '.join(erros))
    return novo
