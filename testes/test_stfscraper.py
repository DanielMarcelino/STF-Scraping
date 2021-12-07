import unittest

from unittest.mock import patch
from src.request_get import RequestGet
from src.stf import STFScraper


class TesteStfScraper(unittest.TestCase):
    @patch('src.request_get.RequestGet')
    def setUp(self, mock_request_get) -> None:
        self.instancia_stf_scraper = STFScraper(RequestGet())

    def test_nada_acontece_quando_a_data_esta_correta(self):
        data = '15-09-2021'
        self.assertIsNone(self.instancia_stf_scraper._valida_data(data))

    def test_obtem_system_exit_quando_a_data_esta_incorreta(self):
        data = '32-09-2021'
        with self.assertRaises(SystemExit):
            self.assertIsNone(self.instancia_stf_scraper._valida_data(data))

    def test_obtem_system_exit_quando_a_data_contem_separador_inesperado(self):
        data = '15/09/2021'
        with self.assertRaises(SystemExit):
            self.assertIsNone(self.instancia_stf_scraper._valida_data(data))

    @patch('src.request_get.RequestGet.obtem_response')
    def test_metodo_obtem_pagina_html_executa_requisicao_com_a_url_correta(self, mock_obtem_response):
        data = '15-09-2021'
        url_esperada = f'{STFScraper.URL_BASE}{STFScraper.PATH_URL}{data}'
        self.instancia_stf_scraper._obtem_pagina_html(data)
        mock_obtem_response.assert_called_once_with(url_esperada)

    @patch('src.request_get.RequestGet.obtem_response', return_value=b'%HTML...')
    def test_metodo_obtem_pagina_html_retorna_valor_esperado(self, mock_obtem_response):
        data = '15-09-2021'
        retorno_esperado = b'%HTML...'
        retorno_obtido = self.instancia_stf_scraper._obtem_pagina_html(data)
        self.assertEqual(retorno_esperado, retorno_obtido)

    @patch('src.stf.STFScraper._obtem_pagina_html')
    def test_metodo_obtem_lista_urls_pdfsretona_lista_de_urls_quando_exitem_diarios_na_pagina(
        self,
        mock_obtem_pagina_html
    ):
        data = '15-09-2021'
        with open('testes/dados/teste_stf_scraper/pagina_html_com_diarios.html', 'rb') as arquivo:
            pagina_html = arquivo.read()
        mock_obtem_pagina_html.return_value = pagina_html
        lista_urls_obtida = self.instancia_stf_scraper.obtem_lista_urls_pdfs(data)
        lista_urls_esperada = [
            (
                'https://www.stf.jus.br/portal/diariojusticaeletronico/'
                'verDiarioEletronico.asp?seq=757262601&data=14/09/2021&ano=2021&numero=184'
            ),
            (
                'https://www.stf.jus.br/portal/diariojusticaeletronico/'
                'verDiarioEletronico.asp?seq=757260925&data=14/09/2021&ano=2021&numero=183'
            )
        ]
        self.assertEqual(lista_urls_esperada, lista_urls_obtida)

    @patch('src.stf.STFScraper._obtem_pagina_html')
    def test_metodo_obtem_lista_urls_pdfs_obtem_system_exit_quando_nao_exitem_diarios_na_pagina(
        self,
        mock_obtem_pagina_html
    ):
        data = '15-09-2021'
        with open('testes/dados/teste_stf_scraper/pagina_html_sem_diarios.html', 'rb') as arquivo:
            pagina_html = arquivo.read()
        mock_obtem_pagina_html.return_value = pagina_html
        with self.assertRaises(SystemExit):
            self.instancia_stf_scraper.obtem_lista_urls_pdfs(data)


if __name__ == '__main__':
    unittest.main()
