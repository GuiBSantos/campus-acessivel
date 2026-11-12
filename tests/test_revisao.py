import copy
import csv
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from busca import busca_sequencial, busca_binaria_iterativa, busca_binaria_recursiva
from coleta import alterar_barreira, importar_ficha_campo, ler_inventario, TEXTOS, NUMEROS
from ordenacao import bubble_sort, selection_sort, insertion_sort, confere_com_o_python
from recursao import achatar, melhor_pacote_exaustivo, pacote_guloso
from relatorio import conferir_inventario, texto_planos, texto_desempenho, texto_sensibilidade

BASE = Path(__file__).resolve().parents[1]
PESOS = {'gravidade': 0, 'pessoas_dia': 1}


class Revisao(unittest.TestCase):
    def setUp(self):
        self.setor = ler_inventario(BASE / 'tests/fixtures/demonstracao.json')
        self.modelo = achatar(self.setor)[0]

    def item(self, numero, custo, beneficio):
        return dict(self.modelo, codigo=f'TESTE-CASO-{numero:02}', custo=custo, pessoas_dia=beneficio)

    def test_ordenacoes_permutacoes_empates_imutabilidade_e_contadores(self):
        base = [{'codigo': 'C', 'indice': 1}, {'codigo': 'A', 'indice': 2},
                {'codigo': 'B', 'indice': 1}, {'codigo': 'D', 'indice': 3}]
        for entrada in itertools.permutations(base):
            original = copy.deepcopy(entrada)
            for chave in ('indice', 'codigo'):
                for crescente in (False, True):
                    resultados = [alg(entrada, chave, crescente) for alg in
                                  (bubble_sort, selection_sort, insertion_sort)]
                    self.assertEqual(resultados[0][0], resultados[1][0])
                    self.assertEqual(resultados[0][0], resultados[2][0])
                    self.assertTrue(confere_com_o_python(resultados[0][0], chave, crescente))
                    self.assertEqual(resultados[0][1], 6)
                    self.assertEqual(resultados[1][1], 6)
                    self.assertEqual(resultados[0][2], resultados[2][2])
            self.assertEqual(entrada, original)
        for alg in (bubble_sort, selection_sort, insertion_sort):
            self.assertEqual(alg([]), ([], 0, 0))
            self.assertEqual(alg(base[:1]), (base[:1], 0, 0))

    def test_buscas_intervalos_e_contadores(self):
        for tamanho in range(20):
            lista = [{'codigo': f'{i:03}'} for i in range(tamanho)]
            for alvo in range(tamanho + 1):
                codigo = f'{alvo:03}'
                esperado = alvo if alvo < tamanho else -1
                for busca in (busca_sequencial, busca_binaria_iterativa, busca_binaria_recursiva):
                    self.assertEqual(busca(lista, codigo)[0], esperado)
                self.assertEqual(busca_binaria_iterativa(lista, codigo), busca_binaria_recursiva(lista, codigo))
            self.assertEqual(busca_sequencial(lista, 'ausente')[1], tamanho)

    def test_exaustiva_contra_enumeracao_independente(self):
        itens = [self.item(1, 4, 7), self.item(2, 3, 5), self.item(3, 3, 5), self.item(4, 20, 40)]
        original = copy.deepcopy(itens)
        for teto in range(15):
            referencia = (0, 0, [])
            for mascara in range(1 << len(itens)):
                escolhidos = [item for i, item in enumerate(itens) if mascara & (1 << i)]
                custo = sum(item['custo'] for item in escolhidos)
                beneficio = sum(item['pessoas_dia'] for item in escolhidos)
                codigos = [item['codigo'] for item in escolhidos]
                if custo <= teto and (beneficio > referencia[0] or
                    (beneficio == referencia[0] and (custo, codigos) < (referencia[1], referencia[2]))):
                    referencia = beneficio, custo, codigos
            resultado = melhor_pacote_exaustivo(itens, teto, PESOS)
            self.assertEqual(resultado[:3], referencia)
            self.assertGreaterEqual(resultado[3], 1)
        self.assertEqual(itens, original)
        self.assertLess(pacote_guloso(itens, 6, PESOS)[0], melhor_pacote_exaustivo(itens, 6, PESOS)[0])

    def test_centavos_poda_chamadas_e_entradas_invalidas(self):
        itens = [self.item(1, .1, 1), self.item(2, .2, 2)]
        for algoritmo in (pacote_guloso, melhor_pacote_exaustivo):
            self.assertEqual(algoritmo(itens, .3, PESOS)[:2], (3, .3))
            for teto in (-1, float('nan'), float('inf'), .001):
                with self.assertRaises(ValueError):
                    algoritmo(itens, teto, PESOS)
        self.assertEqual(melhor_pacote_exaustivo([], 0, PESOS), (0, 0, [], 1))
        self.assertEqual(melhor_pacote_exaustivo(itens, 0, PESOS), (0, 0, [], 1))
        self.assertEqual(melhor_pacote_exaustivo(itens, 1, PESOS)[3], 7)
        muitos = [self.item(i, 1, 1) for i in range(21)]
        setor = dict(nome=self.modelo['ambiente'], barreiras=muitos, subsetores=[])
        self.assertIn('(>20)', texto_planos(setor, PESOS, [30]))

    def test_csv_do_caderno_e_coluna_extra(self):
        campos = ['caminho', 'referencia_norma'] + list(TEXTOS + NUMEROS)
        registro = dict(self.modelo, caminho='Raiz > ' + self.modelo['ambiente'], custo='1650,50', medida='12,3')
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / 'ficha.csv'
            with caminho.open('w', encoding='utf-8', newline='') as arquivo:
                writer = csv.DictWriter(arquivo, campos, delimiter=';', extrasaction='ignore')
                writer.writeheader()
                writer.writerow(registro)
            registros, erros = importar_ficha_campo(caminho)
            self.assertEqual(erros, [])
            self.assertEqual(registros[0]['custo'], 1650.5)
            self.assertEqual(registros[0]['medida'], 12.3)
            linhas = caminho.read_text().splitlines()
            linhas[1] += ';EXTRA'
            caminho.write_text('\n'.join(linhas) + '\n')
            self.assertTrue(importar_ficha_campo(caminho)[1])

    def test_crud_transacional_metadados_e_duplicidade(self):
        original = copy.deepcopy(self.setor)
        caminho = self.modelo['caminho']
        novo = self.item(99, 100, 10)
        novo['base_estimativa'] = 'Teste de preservação'
        criado = alterar_barreira(self.setor, 'cadastrar', registro=novo, caminho=caminho)
        self.assertEqual(len(achatar(criado)), len(achatar(original)) + 1)
        editado = alterar_barreira(criado, 'editar', novo['codigo'], {'custo': 200}, caminho)
        item = next(r for r in achatar(editado) if r['codigo'] == novo['codigo'])
        self.assertEqual(item['custo'], 200)
        self.assertEqual(item['base_estimativa'], 'Teste de preservação')
        removido = alterar_barreira(editado, 'remover', novo['codigo'])
        self.assertEqual(removido, original)
        with self.assertRaises(ValueError):
            alterar_barreira(criado, 'cadastrar', registro=novo, caminho=caminho)
        with self.assertRaises(ValueError):
            alterar_barreira(criado, 'editar', novo['codigo'], {'custo': -1}, caminho)
        self.assertEqual(self.setor, original)

    def test_menu_novos_fluxos_e_relatorios(self):
        codigo = 'SEM-REGISTRO-01'
        roteiro = f'1\n9\n{codigo}\nrecursiva\n10\n11\n1000;2000;5000;10000\n\n12\n13\nselection\n0\n'
        r = subprocess.run([sys.executable, str(BASE / 'main.py')], input=roteiro,
                           text=True, capture_output=True, timeout=20)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn('Não foi possível', r.stdout)
        for texto in ('Busca:', 'exaustivo', 'A1', 'A2', 'A5', 'Selection'):
            self.assertIn(texto, r.stdout)
        self.assertIn('A1', texto_desempenho(self.setor, PESOS))
        self.assertIn('gravidade dobrada', texto_sensibilidade(self.setor, PESOS))

    def test_cobertura_minima_nao_exige_exatamente_15(self):
        setor = copy.deepcopy(self.setor)
        base = achatar(setor)[0]
        for i in range(20):
            setor = alterar_barreira(setor, 'cadastrar', registro=dict(base, codigo=f'TESTE-NOVO-{i:02}'), caminho=base['caminho'])
        erros = conferir_inventario(setor)
        self.assertFalse(any('Quantidade elegivel' in erro for erro in erros))



if __name__ == '__main__':
    unittest.main()

