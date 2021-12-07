import unittest
import os

from src.ferramentas import (
    valida_pdf,
    cria_diretorio,
    gera_md5_hash,
    salva_arquivo
)


class TesteValidaPdf(unittest.TestCase):
    def test_nada_acontece_quando_pdf_e_valido(self):
        pdf = b'%PDF...'
        self.assertIsNone(valida_pdf(pdf))

    def test_obtem_system_exit_quando_pdf_e_invalido(self):
        pdf = b'%JPG...'
        with self.assertRaises(SystemExit):
            valida_pdf(pdf)


class TesteCriaDiretorio(unittest.TestCase):
    def setUp(self):
        self.nome_diretorio = 'diretorio_de_teste'

    def test_cria_diretorio_quando_nao_existe(self):
        self.assertIsNone(cria_diretorio(self.nome_diretorio))
        lista_de_diretorios = os.listdir()
        self.assertIn(self.nome_diretorio, lista_de_diretorios)

    def test_nada_faz_quando_diretorio_ja_existe(self):
        self.assertIsNone(cria_diretorio(self.nome_diretorio))
        lista_de_diretorios = os.listdir()
        self.assertIn(self.nome_diretorio, lista_de_diretorios)

    def tearDown(self):
        os.rmdir(self.nome_diretorio)


class TesteGeraMd5Hash(unittest.TestCase):
    def setUp(self):
        with open('testes/dados/teste_gera_md5_hash/arquivo_1.pdf', 'rb') as arquivo:
            self.arquivo_1 = arquivo.read()

        with open('testes/dados/teste_gera_md5_hash/arquivo_2.pdf', 'rb') as arquivo:
            self.arquivo_2 = arquivo.read()

    def test_valida_md5_arquivo_1(self):
        md5_arquivo_1 = '0214f422c814f45775b460b205761552'
        md5_gerado_pelo_metodo = gera_md5_hash(self.arquivo_1)
        self.assertEqual(md5_gerado_pelo_metodo, md5_arquivo_1)

    def test_valida_md5_arquivo_2(self):
        md5_arquivo_2 = 'ec7995461aea41d8f253672d2c64aec5'
        md5_gerado_pelo_metodo = gera_md5_hash(self.arquivo_2)
        self.assertEqual(md5_gerado_pelo_metodo, md5_arquivo_2)


class TesteSalvaArquivo(unittest.TestCase):
    def setUp(self):
        self.nome_arquivo = 'arquivo_de_teste.pdf'
        self.conteudo_arquivo = b'%PDF...'

    def test_salva_arquivo(self):
        salva_arquivo(self.conteudo_arquivo, self.nome_arquivo)
        lista_de_diretorios_e_arquivos = os.listdir()
        self.assertIn(self.nome_arquivo, lista_de_diretorios_e_arquivos)

    def tearDown(self):
        os.remove(self.nome_arquivo)


if __name__ == '__main__':
    unittest.main()
