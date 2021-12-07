import os
import unittest

from unittest.mock import MagicMock, patch
from src.pdf_downloader import PDFDownloader
from src.request_get import RequestGet


class TestPdfDownloader(unittest.TestCase):
    def setUp(self) -> None:
        self.instancia_pdf_downloader = PDFDownloader(RequestGet)
        self.md5 = 'ec7995461aea41d8f253672d2c64aec5'
        self.url = 'http://www.urldeteste.com'

    def test_obtem_system_exit_quando_lista_de_urls_esta_vazia(self):
        lista_urls = []
        with self.assertRaises(SystemExit):
            self.instancia_pdf_downloader._lista_vazia(lista_urls)

    def test_nada_acontece_quando_lista_de_urls_nao_esta_vazia(self):
        lista_urls = ['http://www.urldeteste.com']
        self.assertIsNone(self.instancia_pdf_downloader._lista_vazia(lista_urls))

    def test_efetua_append_de_md5_no_log(self):
        self.instancia_pdf_downloader._insere_md5_no_log(self.md5)
        self.assertIn(self.md5, self.instancia_pdf_downloader.log_md5)

    def teste_obtem_lista_md5_inseridos_no_log(self):
        self.instancia_pdf_downloader._insere_md5_no_log(self.md5)
        self.assertIn(self.md5, self.instancia_pdf_downloader.obtem_log_md5())

    @patch('src.request_get.RequestGet.obtem_response', return_value=b'%PDF...')
    def test_executa_requisicao_de_pdf_com_a_mesma_url_passada_por_parametro(self, mock_requests):
        self.instancia_pdf_downloader._baixa_pdf(self.url)
        mock_requests.assert_called_once_with(self.url)

    @patch('builtins.open', return_value=MagicMock())
    @patch('src.ferramentas.gera_md5_hash', return_value='2689ae956d50e24c6d3652fa455bb776')
    @patch('src.request_get.RequestGet.obtem_response', return_value=b'%PDF...')
    def test_salva_o_pdf_com_os_parametros_corretos(self, mock_requests, mock_md5, mock_open):
        self.instancia_pdf_downloader._baixa_pdf(self.url)
        nome = f'{PDFDownloader.DIRETORIO_PRINCIPAL}/{mock_md5.return_value}.pdf'
        mock_open.assert_called_once_with(nome, 'wb')
        nome_arquivo = f'{PDFDownloader.DIRETORIO_PRINCIPAL}/2689ae956d50e24c6d3652fa455bb776.pdf'
        os.remove(nome_arquivo)

    @patch('src.pdf_downloader.PDFDownloader._baixa_pdf')
    def teste_efetua_download_com_parametros_corretos(self, mock_efetua_download):
        lista_urls = ['url1', 'url2', 'url3']
        self.instancia_pdf_downloader.efetua_download(lista_urls)
        mock_efetua_download.call_args_list == lista_urls


if __name__ == '__main__':
    unittest.main()
