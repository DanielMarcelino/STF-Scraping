import unittest

import requests

from unittest.mock import patch
from src.request_get import RequestGet


class TesteRequestGet(unittest.TestCase):
    def setUp(self) -> None:
        self.url = 'http://www.teste.ts'

    @patch('requests.get')
    def test_executa_requisicao_com_a_mesma_url_passada_para_obtem_response(self, mock_requests_get):
        mock_requests_get.return_value.status_code = 200
        instancia_de_requisicao = RequestGet()
        instancia_de_requisicao.obtem_response(self.url)
        mock_requests_get.assert_called_once_with(self.url, headers=instancia_de_requisicao.headers)

    @patch('requests.get')
    def test_retorna_resposta_da_requisicao_quando_tudo_ok(self, mock_requests_get):
        mock_requests_get.return_value.status_code = 200
        resposta_da_requisicao = b'pagina html, arquivo pdf etc...'
        mock_requests_get.return_value.content = resposta_da_requisicao
        instancia_de_requisicao = RequestGet()
        retorno_obtido = instancia_de_requisicao.obtem_response(self.url)
        self.assertEqual(resposta_da_requisicao, retorno_obtido)

    @patch('requests.get')
    def test_obtem_system_exit_quando_ocorre_http_error(self, mock_requests_get):
        mock_requests_get.side_effect = requests.exceptions.HTTPError
        instancia_de_requisicao = RequestGet()
        with self.assertRaises(SystemExit):
            instancia_de_requisicao.obtem_response(self.url)

    @patch('requests.get')
    def test_obtem_system_exit_quando_ocorre_invalid_url(self, mock_requests_get):
        mock_requests_get.side_effect = requests.exceptions.HTTPError
        instancia_de_requisicao = RequestGet()
        with self.assertRaises(SystemExit):
            instancia_de_requisicao.obtem_response(self.url)

    @patch('requests.get')
    def test_obtem_system_exit_quando_corre_connection_error(self, mock_requests_get):
        mock_requests_get.side_effect = requests.exceptions.HTTPError
        instancia_de_requisicao = RequestGet()
        with self.assertRaises(SystemExit):
            instancia_de_requisicao.obtem_response(self.url)

    @patch('requests.get')
    def test_obtem_system_exit_quando_status_code_maior_ou_igual_500(self, mock_requests_get):
        mock_requests_get.return_value.status_code = 500
        instancia_de_requisicao = RequestGet()
        with self.assertRaises(SystemExit):
            instancia_de_requisicao.obtem_response(self.url)


if __name__ == '__main__':
    unittest.main()
