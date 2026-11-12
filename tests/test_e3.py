import contextlib
import copy
import csv
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from coleta import (NUMEROS, TEXTOS, gravar_inventario, importar_ficha_campo,
                    ler_inventario, montar_arvore, validar_registro, validar_setor)
from ordenacao import bubble_sort, calcular_indices, indice_prioridade
from recursao import (achatar, caminho_da_barreira, contar_barreiras, contar_por_tipo,
                      custo_total, profundidade, resumo_hierarquico)

BASE = Path(__file__).resolve().parents[1]


class E3(unittest.TestCase):
    def setUp(self):
        self.setor = ler_inventario(BASE / 'tests/fixtures/demonstracao.json')
        self.registro = copy.deepcopy(self.setor['subsetores'][0]['barreiras'][0])

    def test_invalid_values(self):
        for campo, valores in {'custo': [0, -1, float('nan'), float('inf'), True],
                               'gravidade': [0, 6, 2.5, True],
                               'pessoas_dia': [-1, 1.5, False],
                               'medida': [-1], 'data_coleta': ['2026-02-30'],
                               'codigo': ['B01'], 'descricao': ['']}.items():
            for valor in valores:
                with self.subTest(campo=campo, valor=valor):
                    r = dict(self.registro)
                    r[campo] = valor
                    self.assertTrue(validar_registro(r))
        self.assertTrue(validar_registro(None))
        self.assertTrue(validar_setor({'nome': 'X'}))

    def test_duplicate_global_and_environment(self):
        self.setor['subsetores'][1]['barreiras'][0]['codigo'] = self.registro['codigo']
        self.assertTrue(any('repetido' in e for e in validar_setor(self.setor)))
        self.setor['subsetores'][1]['barreiras'][0]['ambiente'] = 'Outro'
        self.assertTrue(any('ambiente' in e for e in validar_setor(self.setor)))

    def test_json_roundtrip_and_reject_before_write(self):
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / 'inventario.json'
            gravar_inventario(arquivo, self.setor)
            self.assertEqual(ler_inventario(arquivo), self.setor)
            original = arquivo.read_bytes()
            self.setor['subsetores'][0]['barreiras'][0]['custo'] = 0
            with self.assertRaises(ValueError):
                gravar_inventario(arquivo, self.setor)
            self.assertEqual(arquivo.read_bytes(), original)
            arquivo.write_text('{')
            with self.assertRaises(ValueError):
                ler_inventario(arquivo)

    def test_csv_tree_and_line_errors(self):
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / 'ficha.csv'
            campos = ('caminho', 'referencia_norma') + TEXTOS + NUMEROS
            registros = achatar(self.setor)
            with arquivo.open('w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=campos, delimiter=';')
                writer.writeheader()
                writer.writerows(registros)
            lidos, erros = importar_ficha_campo(arquivo)
            self.assertEqual(erros, [])
            execucao = subprocess.run([sys.executable, str(BASE / 'main.py'), '--ficha', str(arquivo)],
                                      capture_output=True, text=True)
            self.assertEqual(execucao.returncode, 0, execucao.stderr)
            self.assertIn('Conferência: OK', execucao.stdout)
            self.assertEqual(montar_arvore(lidos), self._com_caminhos(self.setor))
            with arquivo.open('a', encoding='utf-8') as f:
                f.write(';'.join(['inválido'] * len(campos)) + '\n')
            lidos, erros = importar_ficha_campo(arquivo)
            self.assertEqual(len(lidos), 4)
            self.assertTrue(erros)
            arquivo.write_text('codigo\nB01\n')
            self.assertTrue(importar_ficha_campo(arquivo)[1])

    def _com_caminhos(self, setor):
        resultado = copy.deepcopy(setor)
        for no in resultado['subsetores']:
            for r in no['barreiras']:
                r['caminho'] = resultado['nome'] + '/' + no['nome']
        return resultado

    def test_recursive_unbalanced_tree(self):
        self.setor['subsetores'][1]['subsetores'].append(
            {'nome': 'Subambiente vazio', 'barreiras': [], 'subsetores': []})
        self.assertEqual(contar_barreiras(self.setor), 4)
        self.assertEqual(custo_total(self.setor), 8500)
        self.assertEqual(contar_por_tipo(self.setor, 'rampa_inclinada'), 4)
        self.assertEqual(contar_por_tipo(self.setor, 'ausente'), 0)
        self.assertEqual(profundidade(self.setor), 3)
        self.assertEqual(caminho_da_barreira(self.setor, 'DEMO-TESTE-99'), None)
        self.assertEqual(caminho_da_barreira(self.setor, 'DEMO-TESTE-01'),
                         self.setor['nome'] + '/Entrada')
        original = copy.deepcopy(self.setor)
        planos = achatar(self.setor)
        planos[0]['custo'] = -1
        self.assertEqual(self.setor, original)
        saida = io.StringIO()
        with contextlib.redirect_stdout(saida):
            resumo_hierarquico(self.setor)
        self.assertIn('8500.00', saida.getvalue())
        self.assertIn('    Subambiente vazio', saida.getvalue())

    def test_ranking_numeric_and_ties(self):
        pesos = {'gravidade': 0.6, 'alcance': 0.4}
        self.assertAlmostEqual(indice_prioridade(self.registro, pesos), 1.4)
        registros = achatar(self.setor)
        calcular_indices(registros, pesos)
        original = copy.deepcopy(registros)
        ranking, comparacoes, trocas = bubble_sort(registros)
        self.assertEqual([r['codigo'] for r in ranking],
                         ['DEMO-TESTE-02', 'DEMO-TESTE-04', 'DEMO-TESTE-01', 'DEMO-TESTE-03'])
        self.assertEqual(registros, original)
        crescente = bubble_sort(registros, crescente=True)[0]
        self.assertEqual([r['codigo'] for r in crescente],
                         ['DEMO-TESTE-03', 'DEMO-TESTE-01', 'DEMO-TESTE-04', 'DEMO-TESTE-02'])
        self.assertEqual((comparacoes, trocas), (6, 3))
        self.assertGreater(comparacoes, 0)
        self.assertGreater(trocas, 0)
        for crescente in (True, False):
            empatados = [{'codigo': 'B', 'indice': 1}, {'codigo': 'A', 'indice': 1}]
            self.assertEqual(bubble_sort(empatados, crescente=crescente)[0][0]['codigo'], 'A')
        self.assertEqual(bubble_sort([]), ([], 0, 0))
        self.assertEqual(bubble_sort([{'codigo': 'A', 'indice': 1}])[1:], (0, 0))
        for pesos in ({'gravidade': 0, 'alcance': 0}, {'gravidade': -1, 'alcance': 1}):
            with self.assertRaises(ValueError):
                indice_prioridade(self.registro, pesos)

    def test_operational_inventory_contains_pilot_records_and_demo_stays_separate(self):
        operacional = achatar(ler_inventario(BASE / 'dados/inventario.json'))
        self.assertEqual(len(operacional), 15)
        self.assertEqual({r['codigo_piloto'] for r in operacional},
                         {f'B{i:02}' for i in range(1, 16)})
        demonstracao = json.loads((BASE / 'tests/fixtures/demonstracao.json').read_text(encoding='utf-8'))
        registros = achatar(demonstracao)
        codigos = [registro['codigo'] for registro in registros]
        self.assertEqual(len(registros), 4)
        self.assertEqual(len(set(codigos)), 4)

    def test_menu_full_flow_and_recovery(self):
        with tempfile.TemporaryDirectory() as pasta:
            ausente = str(Path(pasta) / 'ausente.json')
            roteiro = f'5\n99\n1\n2\n{ausente}\n4\n5\n6\n7\n0\n'
            result = subprocess.run([sys.executable, str(BASE / 'main.py')],
                                    input=roteiro, text=True, capture_output=True, cwd=pasta)
            self.assertEqual(result.returncode, 0, result.stderr)
            for esperado in ('Carregue um inventário primeiro', 'Opção inválida',
                             'Não foi possível executar', 'Estrutura válida',
                             'RESUMO HIERÁRQUICO', 'RANKING', 'Persistência JSON',
                             'Arquivo fornecido', 'Conferência: OK'):
                self.assertIn(esperado, result.stdout)

    def test_menu_json_csv_and_eof(self):
        with tempfile.TemporaryDirectory() as pasta:
            ficha = Path(pasta) / 'ficha.csv'
            with ficha.open('w', encoding='utf-8', newline='') as arquivo:
                writer = csv.DictWriter(arquivo, fieldnames=('caminho', 'referencia_norma') + TEXTOS + NUMEROS,
                                        delimiter=';')
                writer.writeheader()
                writer.writerows(achatar(self.setor))
            roteiro = f'2\n{BASE / "tests/fixtures/demonstracao.json"}\n4\n3\n{ficha}\n7\n'
            result = subprocess.run([sys.executable, str(BASE / 'main.py')],
                                    input=roteiro, text=True, capture_output=True, cwd=pasta)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('Estrutura válida', result.stdout)
            self.assertIn('Conferência: OK', result.stdout)
            self.assertIn('Encerrando o menu', result.stdout)
            self.assertNotIn('Não foi possível executar', result.stdout)

    def test_missing_inventory_fails_from_other_directory(self):
        with tempfile.TemporaryDirectory() as pasta:
            result = subprocess.run([sys.executable, str(BASE / 'main.py'), '--inventario',
                                     str(Path(pasta) / 'ausente.json')], capture_output=True)
            self.assertEqual(result.returncode, 1)


if __name__ == '__main__':
    unittest.main()
