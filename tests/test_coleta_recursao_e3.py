import copy
import csv
import json
from pathlib import Path
import tempfile
import unittest

from coleta import (NUMEROS, TEXTOS, calcular_inclinacao_percentual,
                    estimar_geometria_rampa, gravar_inventario, importar_ficha_campo,
                    ler_inventario, montar_arvore, validar_registro, validar_setor)
from recursao import (achatar, caminho_da_barreira, contar_barreiras,
                      contar_por_tipo, custo_total, profundidade,
                      resumo_hierarquico)

BASE = Path(__file__).resolve().parents[1]
INVENTARIO = BASE / 'tests' / 'fixtures' / 'demonstracao.json'


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

    def test_inventario_operacional_ainda_sem_registros_importados(self):
        self.assertEqual(achatar(ler_inventario(BASE / 'dados/inventario.json')), [])

    def test_referencia_estritamente_numerica(self):
        for valor in (None, '', '80', True, -1, float('nan'), float('inf')):
            self.assertTrue(validar_registro(dict(self.registros[0], referencia_norma=valor)))
        for valor in (0, 6.25, 80):
            self.assertEqual(validar_registro(dict(self.registros[0], referencia_norma=valor)), [])

    def test_calculos_de_rampa_com_dados_do_inventario(self):
        b01 = estimar_geometria_rampa(7.84, 7)
        b02_trecho = estimar_geometria_rampa(12.76, 7)
        self.assertAlmostEqual(b01['inclinacao_percentual'], 12.28, places=2)
        self.assertAlmostEqual(b01['desnivel_estimado'], 0.955, places=3)
        self.assertAlmostEqual(b02_trecho['inclinacao_percentual'], 12.28, places=2)
        self.assertAlmostEqual(b02_trecho['desnivel_estimado'], 1.555, places=3)
        self.assertAlmostEqual(calcular_inclinacao_percentual(
            b01['desnivel_estimado'], b01['projecao_horizontal_estimada']), 12.28, places=2)
        with self.assertRaises(ValueError):
            estimar_geometria_rampa(12.76, 90)
        with self.assertRaises(ValueError):
            calcular_inclinacao_percentual(1, 0)

    def test_tipos_personalizados_e_classificacao_de_melhoria(self):
        base = self.registros[0]
        porta = dict(base, tipo='porta_conforto', classificacao='oportunidade_melhoria', gravidade=1)
        elevador = dict(base, tipo='elevador_inadequado')
        self.assertEqual(validar_registro(porta), [])
        self.assertEqual(validar_registro(elevador), [])
        elevador.update(referencia_norma=None, status_normativo='nao_avaliado')
        self.assertEqual(validar_registro(elevador), [])
        self.assertTrue(validar_registro(dict(elevador, status_normativo=None)))
        self.assertTrue(validar_registro(dict(base, classificacao='fora_da_lista')))

    def test_csv_permite_elevador_observacional_sem_referencia_normativa(self):
        campos = ('caminho', 'referencia_norma') + TEXTOS + NUMEROS + ('status_normativo',)
        registro = dict(self.registros[0], tipo='elevador_inadequado', referencia_norma=None,
                        status_normativo='nao_avaliado',
                        caminho='Raiz > ' + self.registros[0]['ambiente'])
        with tempfile.TemporaryDirectory() as pasta:
            ficha = Path(pasta) / 'observacao.csv'
            with ficha.open('w', encoding='utf-8', newline='') as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=campos, delimiter=';')
                escritor.writeheader()
                escritor.writerow(registro)
            registros, erros = importar_ficha_campo(ficha)
        self.assertEqual(erros, [])
        self.assertIsNone(registros[0]['referencia_norma'])
        self.assertEqual(registros[0]['status_normativo'], 'nao_avaliado')

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
        setor['subsetores'][0]['barreiras'].append(
            copy.deepcopy(setor['subsetores'][1]['barreiras'][0]))
        self.assertTrue(any('repetido' in erro for erro in validar_setor(setor)))
        setor = copy.deepcopy(self.setor)
        setor['subsetores'][0]['barreiras'][0]['ambiente'] = 'Ambiente incorreto'
        self.assertTrue(any('ambiente difere' in erro for erro in validar_setor(setor)))
        setor = copy.deepcopy(self.setor)
        setor['subsetores'].append(copy.deepcopy(setor['subsetores'][0]))
        self.assertTrue(any('Subsetor repetido' in erro for erro in validar_setor(setor)))
        self.assertTrue(validar_setor(None))
        setor = {'nome': 'Raiz', 'barreiras': [], 'subsetores': [None]}
        self.assertTrue(validar_setor(setor))

    def test_importar_csv_montar_arvore_e_rejeitar_entradas_invalidas(self):
        campos = ('caminho', 'referencia_norma') + TEXTOS + NUMEROS
        with tempfile.TemporaryDirectory() as pasta:
            ficha = Path(pasta) / 'ficha.csv'
            with ficha.open('w', encoding='utf-8-sig', newline='') as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=campos, delimiter=';')
                escritor.writeheader()
                escritor.writerows({campo: registro[campo] for campo in campos}
                                    for registro in self.registros)
            registros, erros = importar_ficha_campo(ficha)
            self.assertEqual(erros, [])
            self.assertEqual(len(registros), 4)
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

    def test_csv_rejeita_referencia_vazia_e_pendencia(self):
        campos = ('caminho', 'referencia_norma', 'pendencia_normativa') + TEXTOS + NUMEROS
        with tempfile.TemporaryDirectory() as pasta:
            ficha = Path(pasta) / 'ficha.csv'
            for valor, pendencia in (('', ''), ('null', ''), ('NaN', ''), ('80', 'Confirmar medida')):
                with ficha.open('w', encoding='utf-8', newline='') as arquivo:
                    escritor = csv.DictWriter(arquivo, fieldnames=campos, delimiter=';', extrasaction='ignore')
                    escritor.writeheader()
                    escritor.writerow(dict(self.registros[0], referencia_norma=valor, pendencia_normativa=pendencia))
                registros, erros = importar_ficha_campo(ficha)
                self.assertEqual(registros, [])
                self.assertTrue(erros)

    def test_persistencia_json_roundtrip_e_recusa_inventario_invalido(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / 'inventario.json'
            gravar_inventario(caminho, self.setor)
            self.assertEqual(ler_inventario(caminho), self.setor)
            original = caminho.read_bytes()
            invalido = copy.deepcopy(self.setor)
            invalido['subsetores'][0]['barreiras'][0]['custo'] = 0
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
        self.assertEqual(contar_barreiras(self.setor), 4)
        self.assertEqual(custo_total(self.setor), sum(r['custo'] for r in self.registros))
        self.assertEqual(contar_por_tipo(self.setor, 'rampa_inclinada'), 4)

    def test_folhas_vazias_caminhos_achatamento_e_resumo(self):
        folha = {'nome': 'Folha vazia', 'barreiras': [], 'subsetores': []}
        self.assertEqual(custo_total(folha), 0)
        self.assertEqual(contar_barreiras(folha), 0)
        self.assertEqual(contar_por_tipo(folha, 'Rampa'), 0)
        self.assertEqual(profundidade(folha), 1)
        self.assertEqual(achatar(folha), [])
        primeiro = self.registros[0]
        self.assertEqual(caminho_da_barreira(self.setor, primeiro['codigo']), primeiro['caminho'])
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
        self.assertIn('4 barreiras', saida)
        self.assertIn(f'R$ {custo_total(self.setor):.2f}', saida)
        formatada = io.StringIO()
        with contextlib.redirect_stdout(formatada):
            resumo_hierarquico(folha, formatar_custo=lambda valor: f'R${valor:.0f}')
        self.assertIn('Folha vazia: 0 barreiras | R$0', formatada.getvalue())


if __name__ == '__main__':
    unittest.main()
