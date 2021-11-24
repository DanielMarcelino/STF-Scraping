import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
import hashlib
import argparse

class Excecoes(Exception):
    def DataInvalida() -> None:
        pass

    def URLInvalidaOuIndisponivel() -> None:
        pass
    
    def IndisponibilidadeTemporaria() -> None:
        pass

    def DiarioNaoPublicado() -> None:
        pass

    def ArquivoIncompativelComFormatoPDF() -> None:
        pass

    def ImpossibilidadeEmSalvarPDF() -> None:
        pass

class Scraper:
    def __init__(self, data:str) -> None:
        self.__valida_data(data)
        self._lista_urls_pdfs = self.__obtem_urls_dos_pdfs_da_pagina_html(data)

    prefixo_url = 'https://www.stf.jus.br/portal/diariojusticaeletronico/'
    posfixo_url = 'montarDiarioEletronico.asp?tp_pesquisa=0&dataP='
    headers = {'user-agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}

    def __valida_data(self, data:str)  -> None:
        try:
            datetime.strptime(data, '%d-%m-%Y')
        except:
            raise Excecoes.DataInvalida()

    @property
    def lista_urls_pdf(self) -> list:
        return self._lista_urls_pdfs[:]

    def __obtem_urls_dos_pdfs_da_pagina_html(self, data:str) -> list:
        pagina_html = self.__obtem_pagina_html(data)
        pagina_html = BeautifulSoup(pagina_html, 'html.parser')
        links = pagina_html.find_all('a', target='_blank')
        lista_urls_pdfs = [(f'{Scraper.prefixo_url}{link.get("href")}') for link in links]
        if len(lista_urls_pdfs) == 0:
            raise Excecoes.DiarioNaoPublicado()
        return lista_urls_pdfs

    def __obtem_pagina_html(self, data:str) -> str:
        url = f'{Scraper.prefixo_url}{Scraper.posfixo_url}{data}'
        pagina_html = self.__obtem_response(url)
        pagina_html = self.__sanitiza_html(pagina_html)
        return pagina_html
        
    def __obtem_response(self, url:str) -> str:
        try:
            response = requests.get(url, headers = Scraper.headers)
        except:
            raise Excecoes.URLInvalidaOuIndisponivel()
        if response.status_code >= 500:
            raise Excecoes.IndisponibilidadeTemporaria()
        return response.text

    def __sanitiza_html(self, pagina_html:bytes) -> str:
        pagina_html = re.sub(r'[\n|\t|\r]', '', pagina_html)
        return pagina_html

class PDFDownloader:
    def __init__(self, lista_urls_pdf:list) -> None:
        self._lista_md5_pdfs = self.__obtem_arquivos_pdfs(lista_urls_pdf)

    def __obtem_arquivos_pdfs(self, lista_urls_pdfs:list) -> list:
        if not lista_urls_pdfs:
            raise Excecoes.URLInvalidaOuIndisponivel()
        lista_md5_pdfs = []
        for url in lista_urls_pdfs:
            binario_pdf = self.__obtem_response(url)
            self.__verifica_compatibilidade_de_aquivo_PDF(binario_pdf)
            md5_pdf = self.__obtem_md5_pdf(binario_pdf)
            self.__salva_arquivo_pdf(binario_pdf, md5_pdf)
            lista_md5_pdfs.append(md5_pdf)
        return lista_md5_pdfs

    def __verifica_compatibilidade_de_aquivo_PDF(self, binario_pdf:bytes) -> None:
        if not binario_pdf.startswith(b'%PDF'):
            raise Excecoes.ArquivoIncompativelComFormatoPDF()

    def __obtem_response(self, url:str) -> str:
        try:
            response = requests.get(url, headers = Scraper.headers)
        except:
            raise Excecoes.URLInvalidaOuIndisponivel()
        if response.status_code >= 500:
            raise Excecoes.IndisponibilidadeTemporaria()
        return response.content

    def __salva_arquivo_pdf(self, binario_pdf:bytes, nome_arquivo:str) -> None:
        try:
            with open(f'{nome_arquivo}.pdf', 'wb') as arquivo_pdf:
                arquivo_pdf.write(binario_pdf)
        except:
            raise Excecoes.ImpossibilidadeEmSalvarPDF()

    def __obtem_md5_pdf(self, binario_pdf:bytes) -> str:
        md5_pdf = hashlib.md5()
        md5_pdf.update(binario_pdf)
        return str(md5_pdf.hexdigest())

    def imprime_log_md5_pdfs(self) -> None:
        for md5 in self._lista_md5_pdfs:
            print(md5)

def obtem_data_args() -> str:
    parser = argparse.ArgumentParser(prog='stf-scraping.py', description='Baixa os Diários oficiais do STF publicados em uma determinada data.')
    parser.add_argument('data_informada', metavar = 'Data', type = str, help = 'Data de publicação (DD-MM-AAAA).')
    args = parser.parse_args()
    return  args.data_informada

def main():
    data_publicacao = obtem_data_args()
    
    busca = Scraper(data_publicacao)
    lista_urls_pdf = busca.lista_urls_pdf

    baixa_pdf = PDFDownloader(lista_urls_pdf)
    baixa_pdf.imprime_log_md5_pdfs()

if __name__ == "__main__":
    main()