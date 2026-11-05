"""Validação, importação e persistência usando apenas biblioteca padrão."""

import csv
import json
import math
import re
from datetime import date
from pathlib import Path

TEXTOS = ('codigo', 'ambiente', 'tipo', 'descricao', 'unidade',
          'referencia_norma', 'intervencao', 'coletado_por', 'data_coleta')
NUMEROS = ('medida', 'gravidade', 'pessoas_dia', 'custo')


def validar_registro(barreira, codigos_usados=None):
    """Devolver problemas e registrar códigos para detectar duplicatas."""
    if not isinstance(barreira, dict):
        return ['Barreira deve ser um dicionário.']
    erros = []
    for campo in TEXTOS:
        valor = barreira.get(campo)
        if not isinstance(valor, str) or not valor.strip():
            erros.append(f'{campo}: texto obrigatório.')
        elif campo == 'descricao' and len(valor.strip()) < 10:
            erros.append('descricao: detalhe insuficiente para ser verificável.')
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
    """Validar árvore e unicidade global. Caso base: nó sem descendentes."""
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
    """Importar linhas válidas e devolver erros com os números das linhas."""
    registros, erros, codigos = [], [], []
    with open(caminho, encoding='utf-8-sig', newline='') as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=';')
        obrigatorios = ('caminho',) + TEXTOS + NUMEROS
        for campo in obrigatorios:
            if leitor.fieldnames is None or leitor.fieldnames.count(campo) != 1:
                return [], [f'Cabeçalho ausente ou duplicado: {campo}.']
        for linha, registro in enumerate(leitor, 2):
            problemas = []
            for campo in NUMEROS:
                try:
                    registro[campo] = (int(registro[campo]) if campo in
                                       ('gravidade', 'pessoas_dia') else float(registro[campo]))
                except (TypeError, ValueError):
                    problemas.append(f'{campo}: número inválido.')
            caminho_no = registro.get('caminho') or ''
            partes = [parte.strip() for parte in caminho_no.split('/')]
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
    """Agrupar registros por caminho sem supor pavimentos do piloto."""
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
    """Validar antes de gravar; não substituir arquivos em caso de erro."""
    erros = validar_setor(setor)
    if erros:
        raise ValueError('\n'.join(erros))
    conteudo = json.dumps(setor, ensure_ascii=False, indent=2, allow_nan=False)
    Path(caminho).write_text(conteudo + '\n', encoding='utf-8')


def ler_inventario(caminho):
    """Ler JSON e recusar inventários inconsistentes."""
    with open(caminho, encoding='utf-8') as arquivo:
        setor = json.load(arquivo)
    erros = validar_setor(setor)
    if erros:
        raise ValueError('\n'.join(erros))
    return setor
