from datetime import datetime

from bs4 import BeautifulSoup

from src.request_get import RequestGet
from src.exceptions import data_invalida, diario_nao_publicado


class STFScraper:
    URL_BASE = 'https://www.stf.jus.br/portal/diariojusticaeletronico/'
    PATH_URL = 'montarDiarioEletronico.asp?tp_pesquisa=0&dataP='

    def __init__(self, custom_response: RequestGet) -> None:
        self.custom_response = custom_response

    def obtem_lista_urls_pdfs(self, data: str) -> list:
        self._valida_data(data)
        lista_urls_pdfs = self._obtem_urls_dos_pdfs_da_pagina_html(data)
        return lista_urls_pdfs[:]

    def _obtem_urls_dos_pdfs_da_pagina_html(self, data: str) -> list:
        pagina_html = self._obtem_pagina_html(data)
        pagina_html = BeautifulSoup(pagina_html, 'html.parser')
        anchors = pagina_html.select('a[target]')
        lista_urls_pdfs = [(f'{STFScraper.URL_BASE}{anchor.get("href").strip()}')for anchor in anchors]
        if len(lista_urls_pdfs) == 0:
            diario_nao_publicado()
        return lista_urls_pdfs

    def _obtem_pagina_html(self, data: str) -> bytes:
        url = f'{STFScraper.URL_BASE}{STFScraper.PATH_URL}{data}'
        pagina_html = self.custom_response.obtem_response(url)
        return pagina_html

    def _valida_data(self, data: str) -> None:
        try:
            datetime.strptime(data, '%d-%m-%Y')
        except Exception:
            data_invalida()
