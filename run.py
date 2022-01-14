import argparse
import calendar

from src.request_get import RequestGet
from src.pdf_downloader import PDFDownloader
from src.stf import STFScraper


def obtem_data_args() -> str:
    parser = argparse.ArgumentParser(
        prog='stf-scraping.py',
        description='Baixa os Diários oficiais do STF publicados em uma determinada data.'
    )
    parser.add_argument('data_informada', metavar='Data', type=str, help='Data de publicação (MM-AAAA).')
    args = parser.parse_args()
    return args.data_informada


def main():
    data_publicacao = obtem_data_args()
    mes = int(data_publicacao.split('-')[0])
    ano = int(data_publicacao.split('-')[1])
    quantidade_de__dias_no_mes = calendar.monthrange(ano, mes)[1]
    
    lista_urls = []
    instancia_de_busca = STFScraper()

    for dia in range(1, quantidade_de__dias_no_mes + 1):
        urls = instancia_de_busca.obtem_lista_urls_pdfs(f'{dia}/{mes}/{ano}')
        if urls:
            lista_urls.extend(urls)

    instancia_de_download_pdf = PDFDownloader()
    for url in lista_urls:
        instancia_de_download_pdf.efetua_download(url)

if __name__ == "__main__":
    main()
