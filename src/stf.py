from datetime import datetime

from bs4 import BeautifulSoup
import requests


class STFScraper:
    HEADERS = {
            'user-agent': (
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
            )
        }
    URL_BASE = 'https://www.stf.jus.br/portal/diariojusticaeletronico/'
    PATH_URL = 'montarDiarioEletronico.asp?tp_pesquisa=0&dataP='

    def obtem_lista_urls_pdfs(self, data: str) -> list:
        pagina_html = self._obtem_pagina_html(data)
        if not pagina_html:
            return None
        pagina_html = BeautifulSoup(pagina_html, 'html.parser')
        anchors = pagina_html.select('a[target]')
        if not anchors:
            print(f'[{datetime.now()}] Não há diários publicados em {data}')
            return None
        lista_urls_pdfs = [(f'{STFScraper.URL_BASE}{anchor.get("href").strip()}') for anchor in anchors]
        print(f'[{datetime.now()}] Foram encontrados {len(lista_urls_pdfs)} diários publicados em {data}')
        return lista_urls_pdfs

    def _obtem_pagina_html(self, data: str) -> bytes:
        url = f'{STFScraper.URL_BASE}{STFScraper.PATH_URL}{data}'
        response = requests.get(url, headers=self.HEADERS)
        if response.status_code != 200:
            print(f'[{datetime.now()}] Erro {response.status_code} ao buscar diários na data {data}')
            return None
        return response.content

    # def _valida_data(self, data: str) -> None:
    #     try:
    #         datetime.strptime(data, '%d-%m-%Y')
    #     except Exception:
    #         data_invalida()
