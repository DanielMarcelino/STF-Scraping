from datetime import datetime
from typing import List

import requests

from src.ferramentas import (
    cria_diretorio,
    salva_arquivo,
    valida_pdf,
    gera_md5_hash
)
from src.exceptions import url_invalida_ou_indisponivel


class PDFDownloader:
    DIRETORIO_PRINCIPAL = 'diarios'
    HEADERS = {
        'user-agent': (
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
        )
    }

    def __init__(self) -> None:
        cria_diretorio(nome_diretorio=PDFDownloader.DIRETORIO_PRINCIPAL)

    def efetua_download(self, url: str) -> list:
        self._baixa_pdf(url)

    def _baixa_pdf(self, url: str) -> None:
        response = requests.get(url, headers=self.HEADERS, timeout=30)
        url_split = url.split('=')
        data_diario = url_split[2][:10]
        numero_diario = url_split[4]
        if response.status_code != 200 :
            print(f'[{datetime.now()}] Erro {response.status_code} ao baixar diário nº {numero_diario} data {data_diario}')
            return
        md5_pdf = gera_md5_hash(response.content)
        salva_arquivo(
            binario=response.content,
            nome=f'{md5_pdf}.pdf',
            caminho=f'{PDFDownloader.DIRETORIO_PRINCIPAL}/'
        )
        print(f'[{datetime.now()}] Diário nº {numero_diario} data {data_diario} baixado com sucesso md5 = {md5_pdf}')
