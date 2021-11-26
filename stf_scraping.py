import hashlib
import argparse
import exceptions

import requests

from datetime import datetime
from bs4 import BeautifulSoup


class CustomResponse:
    def __init__(self) -> None:
        self.headers = {
            'user-agent': (
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
            )
        }

    def obtem_response(self, url):
        try:
            response = requests.get(url, headers=self.headers)
        except Exception:
            exceptions.url_invalida_ou_indisponivel()
        if response.status_code >= 500:
            exceptions.indisponibilidade_temporaria()
        return response.content


class Scraper:
    URL_BASE = 'https://www.stf.jus.br/portal/diariojusticaeletronico/'
    PATH_URL = 'montarDiarioEletronico.asp?tp_pesquisa=0&dataP='

    def __init__(self, data: str, custom_response: CustomResponse) -> None:
        self.__valida_data(data)
        self.custom_response = custom_response
        self._lista_urls_pdfs = self.__obtem_urls_dos_pdfs_da_pagina_html(data)

    def __valida_data(self, data: str) -> None:
        try:
            datetime.strptime(data, '%d-%m-%Y')
        except Exception:
            exceptions.data_invalida()

    @property
    def lista_urls_pdf(self) -> list:
        return self._lista_urls_pdfs[:]

    def __obtem_urls_dos_pdfs_da_pagina_html(self, data: str) -> list:
        pagina_html = self.__obtem_pagina_html(data)
        pagina_html = BeautifulSoup(pagina_html, 'html.parser')
        anchors = pagina_html.select('a[target]')
        lista_urls_pdfs = [(f'{Scraper.URL_BASE}{anchor.get("href").strip()}')for anchor in anchors]
        if len(lista_urls_pdfs) == 0:
            exceptions.diario_nao_publicado()
        return lista_urls_pdfs

    def __obtem_pagina_html(self, data: str) -> bytes:
        url = f'{Scraper.URL_BASE}{Scraper.PATH_URL}{data}'
        pagina_html = self.custom_response.obtem_response(url)
        return pagina_html


class PDFDownloader:
    def __init__(self, lista_urls_pdf: list,  custom_response: CustomResponse) -> None:
        self.custom_response = custom_response
        self._lista_md5_pdfs = self.__obtem_arquivos_pdfs(lista_urls_pdf)

    def __obtem_arquivos_pdfs(self, lista_urls_pdfs: list) -> list:
        if not lista_urls_pdfs:
            exceptions.url_invalida_ou_indisponivel()

        lista_md5_pdfs = []
        for url in lista_urls_pdfs:
            binario_pdf = self.custom_response.obtem_response(url)
            self.__verifica_compatibilidade_de_aquivo_PDF(binario_pdf)
            md5_pdf = self.__obtem_md5_pdf(binario_pdf)
            self.__salva_arquivo_pdf(binario_pdf, md5_pdf)
            lista_md5_pdfs.append(md5_pdf)
        return lista_md5_pdfs

    def __verifica_compatibilidade_de_aquivo_PDF(self, binario_pdf: bytes) -> None:
        if not binario_pdf.startswith(b'%PDF'):
            exceptions.arquivo_incompativel_com_formato_pdf()

    def __salva_arquivo_pdf(self, binario_pdf: bytes, nome_arquivo: str) -> None:
        try:
            with open(f'{nome_arquivo}.pdf', 'wb') as arquivo_pdf:
                arquivo_pdf.write(binario_pdf)
        except Exception:
            exceptions.impossibilidade_em_salvar_pdf()

    def __obtem_md5_pdf(self, binario_pdf: bytes) -> str:
        md5_pdf = hashlib.md5()
        md5_pdf.update(binario_pdf)
        return str(md5_pdf.hexdigest())

    def imprime_log_md5_pdfs(self) -> None:
        for md5 in self._lista_md5_pdfs:
            print(md5)


def obtem_data_args() -> str:
    parser = argparse.ArgumentParser(
        prog='stf-scraping.py',
        description='Baixa os Diários oficiais do STF publicados em uma determinada data.'
    )
    parser.add_argument('data_informada', metavar='Data', type=str, help='Data de publicação (DD-MM-AAAA).')
    args = parser.parse_args()
    return args.data_informada


def main():
    data_publicacao = obtem_data_args()
    custom_response = CustomResponse()
    busca = Scraper(data_publicacao, custom_response)
    lista_urls_pdf = busca.lista_urls_pdf
    baixa_pdf = PDFDownloader(lista_urls_pdf, custom_response)
    baixa_pdf.imprime_log_md5_pdfs()


if __name__ == "__main__":
    main()
