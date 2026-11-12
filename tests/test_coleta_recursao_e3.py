import copy
import csv
import json
from pathlib import Path
import tempfile
import unittest

from coleta import (NUMEROS, TEXTOS, gravar_inventario, importar_ficha_campo,
                    ler_inventario, montar_arvore, validar_registro, validar_setor)
from recursao import (achatar, caminho_da_barreira, contar_barreiras,
                      contar_por_tipo, custo_total, profundidade,
                      resumo_hierarquico)

BASE = Path(__file__).resolve().parents[1]
INVENTARIO = BASE / 'dados' / 'inventario.json'


def iterar_registros(no):
    pilha = [no]
    while pilha:
        atual = pilha.pop()
        for barreira in atual['barreiras']:
            yield atual['nome'], barreira
        for filho in atual['subsetores']:
            pilha.append(filho)


class ColetaRecursaoE3(unittest.TestCase):
    def setUp(self):
        self.setor = ler_inventario(INVENTARIO)
        self.registros = achatar(self.setor)

    def test_inventario_operacional_tem_15_registros_com_contrato_valido(self):
        self.assertEqual(validar_setor(self.setor), [])
        self.assertEqual(len(self.registros), 15)
        codigos = [registro['codigo'] for registro in self.registros]
        self.assertEqual(len(codigos), len(set(codigos)))
        self.assertEqual({registro['codigo_piloto'] for registro in self.registros},
                         {f'B{i:02}' for i in range(1, 16)})
        for registro in self.registros:
            for campo in TEXTOS:
                self.assertIsInstance(registro[campo], str, (registro['codigo'], campo))
                self.assertTrue(registro[campo].strip(), (registro['codigo'], campo))
            for campo in NUMEROS:
                self.assertIsInstance(registro[campo], (int, float),
                                      (registro['codigo'], campo))
                self.assertNotIsInstance(registro[campo], bool)
            self.assertEqual(len(registro['data_coleta']), 10)
            self.assertEqual(validar_registro(registro), [])

    def test_b03_permanece_oportunidade_e_nao_descumprimento(self):
        b03 = next(r for r in self.registros if r['codigo_piloto'] == 'B03')
        self.assertEqual(b03['medida'], 80)
        self.assertEqual(b03['unidade'], 'cm')
        self.assertEqual(b03['gravidade'], 2)
        self.assertIn('oportunidade de melhoria', b03['base_estimativa'].casefold())
        self.assertIn('ampliar', b03['intervencao'].casefold())

    def test_validar_registro_rejeita_campos_ausentes_tipos_limites_e_datas(self):
        valido = copy.deepcopy(self.registros[0])
        self.assertEqual(validar_registro(valido), [])
        self.assertTrue(validar_registro(None))
        for campo in TEXTOS + NUMEROS:
            registro = dict(valido)
            del registro[campo]
            self.assertTrue(validar_registro(registro), campo)
        for data in ('20261021', '2026-W43-3', '2026-02-30', None, ''):
            registro = dict(valido, data_coleta=data)
            self.assertTrue(any('data_coleta' in e for e in validar_registro(registro)), data)
        for campo, valor in (('gravidade', 6), ('gravidade', 2.5),
                             ('pessoas_dia', -1), ('custo', 0),
                             ('medida', -0.1), ('custo', float('inf')),
                             ('medida', float('nan')), ('gravidade', True),
                             ('descricao', 'curta')):
            registro = dict(valido, **{campo: valor})
            self.assertTrue(validar_registro(registro), (campo, valor))
        self.assertEqual(validar_registro(dict(valido, pessoas_dia=10**400)), [])

    def test_validar_registro_e_setor_detectam_codigo_e_hierarquia(self):
        registro = copy.deepcopy(self.registros[0])
        usados = [registro['codigo']]
        self.assertTrue(any('repetido' in erro
                            for erro in validar_registro(registro, usados)))
        self.assertTrue(any('SETOR-SUBSETOR' in erro
                            for erro in validar_registro(dict(registro, codigo='B01'))))
        setor = copy.deepcopy(self.setor)
        setor['subsetores'][0]['subsetores'][0]['barreiras'].append(
            copy.deepcopy(setor['subsetores'][1]['barreiras'][0]))
        self.assertTrue(any('repetido' in erro for erro in validar_setor(setor)))
        setor = copy.deepcopy(self.setor)
        setor['subsetores'][0]['subsetores'][0]['barreiras'][0]['ambiente'] = 'Ambiente incorreto'
        self.assertTrue(any('ambiente difere' in erro for erro in validar_setor(setor)))
        setor = copy.deepcopy(self.setor)
        setor['subsetores'].append(copy.deepcopy(setor['subsetores'][0]))
        self.assertTrue(any('Subsetor repetido' in erro for erro in validar_setor(setor)))
        self.assertTrue(validar_setor(None))
        setor = {'nome': 'Raiz', 'barreiras': [], 'subsetores': [None]}
        self.assertTrue(validar_setor(setor))

    def test_importar_csv_montar_arvore_e_rejeitar_entradas_invalidas(self):
        campos = ('caminho',) + TEXTOS + NUMEROS
        with tempfile.TemporaryDirectory() as pasta:
            ficha = Path(pasta) / 'ficha.csv'
            with ficha.open('w', encoding='utf-8-sig', newline='') as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=campos, delimiter=';')
                escritor.writeheader()
                escritor.writerows({campo: registro[campo] for campo in campos}
                                    for registro in self.registros)
            registros, erros = importar_ficha_campo(ficha)
            self.assertEqual(erros, [])
            self.assertEqual(len(registros), 15)
            reconstruida = montar_arvore(registros)
            self.assertEqual(achatar(reconstruida), registros)

            ficha.write_text('codigo\nB01\n', encoding='utf-8')
            self.assertEqual(importar_ficha_campo(ficha)[0], [])
            self.assertTrue(importar_ficha_campo(ficha)[1])

            with ficha.open('w', encoding='utf-8', newline='') as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=campos, delimiter=';')
                escritor.writeheader()
                linha = {campo: self.registros[0][campo] for campo in campos}
                linha['caminho'] = 'Raiz/Outro'
                escritor.writerow(linha)
            erros = importar_ficha_campo(ficha)[1]
            self.assertTrue(any('último componente' in erro for erro in erros))

        with self.assertRaisesRegex(ValueError, 'Nenhum registro'):
            montar_arvore([])
        dois_setores = [dict(self.registros[0], caminho='Raiz/A'),
                        dict(self.registros[1], caminho='Outro/B')]
        with self.assertRaisesRegex(ValueError, 'mesmo setor'):
            montar_arvore(dois_setores)

    def test_persistencia_json_roundtrip_e_recusa_inventario_invalido(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / 'inventario.json'
            gravar_inventario(caminho, self.setor)
            self.assertEqual(ler_inventario(caminho), self.setor)
            original = caminho.read_bytes()
            invalido = copy.deepcopy(self.setor)
            invalido['subsetores'][0]['subsetores'][0]['barreiras'][0]['custo'] = 0
            with self.assertRaises(ValueError):
                gravar_inventario(caminho, invalido)
            self.assertEqual(caminho.read_bytes(), original)
            caminho.write_text('{', encoding='utf-8')
            with self.assertRaises(json.JSONDecodeError):
                ler_inventario(caminho)
            caminho.write_text('{"nome":"Raiz","barreiras":[{}],"subsetores":[]}',
                               encoding='utf-8')
            with self.assertRaises(ValueError):
                ler_inventario(caminho)

    def test_percursos_recontam_arvore_e_totais_por_subsetor(self):
        pares = list(iterar_registros(self.setor))
        custos_por_raiz = {}
        contagens_por_raiz = {}
        for registro in self.registros:
            primeiro_nivel = registro['caminho'].split('/')[1]
            custos_por_raiz[primeiro_nivel] = custos_por_raiz.get(primeiro_nivel, 0) + registro['custo']
            contagens_por_raiz[primeiro_nivel] = contagens_por_raiz.get(primeiro_nivel, 0) + 1
        self.assertEqual(len(pares), contar_barreiras(self.setor))
        self.assertEqual(contar_barreiras(self.setor), 15)
        self.assertEqual(custo_total(self.setor), 134460)
        self.assertEqual(profundidade(self.setor), 4)
        self.assertEqual(contagens_por_raiz, {
            'Bloco B': 4, 'Rampa principal entre blocos': 1,
            'Salas de aula (padrão em todos os blocos)': 1, 'Auditório': 1,
            'Áreas livres (Blocos A e B)': 1, 'Bloco D': 2, 'Bloco E': 2,
            'Bloco A': 1, 'Bloco C': 2,
        })
        self.assertEqual(custos_por_raiz['Bloco B'], 13460)
        self.assertEqual(custos_por_raiz['Rampa principal entre blocos'], 40000)
        self.assertEqual(custos_por_raiz['Auditório'], 60000)
        self.assertEqual(contar_por_tipo(self.setor, 'Braille'), 8)
        self.assertEqual(contar_por_tipo(self.setor, 'tipo ausente'), 0)

    def test_folhas_vazias_caminhos_achatamento_e_resumo(self):
        folha = {'nome': 'Folha vazia', 'barreiras': [], 'subsetores': []}
        self.assertEqual(custo_total(folha), 0)
        self.assertEqual(contar_barreiras(folha), 0)
        self.assertEqual(contar_por_tipo(folha, 'Rampa'), 0)
        self.assertEqual(profundidade(folha), 1)
        self.assertEqual(achatar(folha), [])
        b01 = next(r for r in self.registros if r['codigo_piloto'] == 'B01')
        self.assertEqual(caminho_da_barreira(self.setor, b01['codigo']),
                         'Prédio do Ensino Superior — UNASP-EC/Bloco B/Rampa de acesso entre pavimentos')
        self.assertIsNone(caminho_da_barreira(self.setor, 'NAO-EXISTE-99'))
        original = copy.deepcopy(self.setor)
        achatados = achatar(self.setor)
        self.assertEqual(achatados[0]['caminho'].split('/')[0], self.setor['nome'])
        achatados[0]['custo'] = -1
        self.assertEqual(self.setor, original)
        import contextlib
        import io
        capturada = io.StringIO()
        with contextlib.redirect_stdout(capturada):
            resumo_hierarquico(self.setor)
        saida = capturada.getvalue()
        self.assertIn('15 barreiras', saida)
        self.assertIn('R$ 134460.00', saida)
        formatada = io.StringIO()
        with contextlib.redirect_stdout(formatada):
            resumo_hierarquico(folha, formatar_custo=lambda valor: f'R${valor:.0f}')
        self.assertIn('Folha vazia: 0 barreiras | R$0', formatada.getvalue())


if __name__ == '__main__':
    unittest.main()
