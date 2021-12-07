from typing import List

from src.ferramentas import (
    cria_diretorio,
    salva_arquivo,
    valida_pdf,
    gera_md5_hash
)
from src.request_get import RequestGet
from src.exceptions import url_invalida_ou_indisponivel


class PDFDownloader:
    DIRETORIO_PRINCIPAL = 'diarios'

    def __init__(self, instancia_de_requisicao: RequestGet) -> None:
        self.instancia_de_requisicao = instancia_de_requisicao
        cria_diretorio(nome_diretorio=PDFDownloader.DIRETORIO_PRINCIPAL)
        self.log_md5 = []

    def obtem_log_md5(self) -> list:
        return self.log_md5[:]

    def efetua_download(self, lista_urls_pdfs: List[str]) -> list:
        self._lista_vazia(lista_urls_pdfs)
        for url in lista_urls_pdfs:
            self._baixa_pdf(url)

    def _baixa_pdf(self, url: str) -> None:
        binario_pdf = self.instancia_de_requisicao.obtem_response(url)
        valida_pdf(binario_pdf)
        md5_pdf = gera_md5_hash(binario_pdf)
        salva_arquivo(
            binario=binario_pdf,
            nome=f'{md5_pdf}.pdf',
            caminho=f'{PDFDownloader.DIRETORIO_PRINCIPAL}/'
        )
        self._insere_md5_no_log(md5_pdf)

    def _lista_vazia(self, lista_urls_pdfs: List[str]) -> bool:
        if not lista_urls_pdfs:
            url_invalida_ou_indisponivel()

    def _insere_md5_no_log(self, md5: str) -> None:
        self.log_md5.append(md5)
