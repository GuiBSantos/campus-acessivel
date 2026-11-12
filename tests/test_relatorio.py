"""Conferências e rastreabilidade das saídas E3."""

import copy
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from coleta import ler_inventario
from relatorio import (conferir_inventario, exportar_relatorio, gerar_relatorio,
                       matriz_ambiente_tipo, origem_campo, reais, texto_ranking)
from recursao import achatar

BASE = Path(__file__).resolve().parents[1]


class Relatorio(unittest.TestCase):
    def setUp(self):
        self.setor = ler_inventario(BASE / 'tests/fixtures/demonstracao.json')
        self.pesos = {'gravidade': 1, 'pessoas_dia': 1}

    def test_format_and_estimate_provenance(self):
        self.assertEqual(reais(134460), 'R$ 134.460,00')
        self.assertEqual(reais(0), 'R$ 0,00')
        r = dict(achatar(self.setor)[0], coletado_por='Grupo', base_estimativa='Fluxo estimado sem contagem')
        self.assertIn('estimado', origem_campo(r, 'pessoas_dia'))
        self.assertEqual(origem_campo(r, 'medida'), 'não informada')
        r['origens'] = {'medida': 'medição de campo; ficha de 21/10/2026'}
        self.assertEqual(origem_campo(r, 'medida'), r['origens']['medida'])
        r['origens'] = {}
        r['unidade'] = 'm (hipótese, não medida)'
        self.assertIn('estimada', origem_campo(r, 'medida'))

    def test_counts_coverage_and_independent_totals(self):
        self.assertEqual(conferir_inventario(self.setor, 4), [])
        self.assertTrue(conferir_inventario(self.setor))
        with patch('relatorio.custo_total', return_value=8501):
            self.assertTrue(any('Custos' in e for e in conferir_inventario(self.setor, 4)))
        with patch('relatorio.contar_barreiras', return_value=5):
            self.assertTrue(any('Contagem' in e for e in conferir_inventario(self.setor, 4)))
        registros = achatar(self.setor)
        self.setor['subsetores'][1]['barreiras'][0]['codigo'] = registros[0]['codigo']
        self.assertTrue(any('repetido' in e for e in conferir_inventario(self.setor, 4)))

    def test_pilot_coverage_even_with_unique_final_codes(self):
        for i in range(15):
            r = dict(self.setor['subsetores'][0]['barreiras'][0],
                     codigo=f'ES-TESTE-{i+1:02}', codigo_piloto=f'B{i+1:02}', ambiente='Raiz')
            if i == 0:
                setor = dict(nome='Raiz', barreiras=[], subsetores=[])
            setor['barreiras'].append(r)
        self.assertEqual(len(conferir_inventario(setor)), 2)  # Falta cobertura e hierarquia.
        setor['barreiras'][1]['codigo_piloto'] = 'B01'
        erros = conferir_inventario(setor)
        self.assertTrue(any('B01' in e for e in erros))
        self.assertTrue(any('B02' in e for e in erros))

    def test_matrix_homonymous_rooms_are_distinct(self):
        for no in self.setor['subsetores'][:2]:
            registros_locais = no['barreiras']
            no['barreiras'] = []
            for registro in registros_locais:
                registro['ambiente'] = 'Portas'
            no['subsetores'] = [dict(nome='Portas', barreiras=registros_locais, subsetores=[])]
        registros = achatar(self.setor)
        ambientes, tipos, matriz = matriz_ambiente_tipo(registros)
        self.assertEqual(sum(sum(linha) for linha in matriz), 4)
        self.assertEqual(len(ambientes), 3)

    def test_report_retains_sources_and_does_not_overwrite(self):
        r = self.setor['subsetores'][0]['barreiras'][0]
        r['coletado_por'] = 'Grupo'
        r['base_estimativa'] = 'Hipótese: preço por placa, sem cotação.'
        original = copy.deepcopy(self.setor)
        texto = gerar_relatorio(self.setor, self.pesos, 4)
        for esperado in ('R$ 8.500,00', 'Hipótese: preço por placa, sem cotação.',
                         'não informada', 'fictício', 'Grav.', 'Pessoas/dia',
                         '4 códigos únicos', 'MATRIZ AMBIENTE × TIPO'):
            self.assertIn(esperado, texto)
        self.assertEqual(self.setor, original)
        with tempfile.TemporaryDirectory() as pasta:
            destino = Path(pasta) / 'relatorio.txt'
            exportar_relatorio(destino, self.setor, self.pesos, 4)
            self.assertEqual(destino.read_text(encoding='utf-8'), texto)
            with self.assertRaises(FileExistsError):
                exportar_relatorio(destino, self.setor, self.pesos, 4)
            result = subprocess.run([sys.executable, str(BASE / 'main.py')],
                                    input=f'1\n8\n{Path(pasta) / "menu.txt"}\n0\n',
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('Relatório salvo', result.stdout)
            self.assertIn('estimado', (Path(pasta) / 'menu.txt').read_text(encoding='utf-8'))
