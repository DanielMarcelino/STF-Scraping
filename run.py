import argparse

from src.request_get import RequestGet
from src.pdf_downloader import PDFDownloader
from src.stf import STFScraper


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
    instancia_de_requisicao = RequestGet()
    instancia_de_busca = STFScraper(instancia_de_requisicao)
    lista_urls_pdf = instancia_de_busca.obtem_lista_urls_pdfs(data_publicacao)
    instancia_de_download_pdf = PDFDownloader(instancia_de_requisicao)
    instancia_de_download_pdf.efetua_download(lista_urls_pdf)
    lista_md5 = instancia_de_download_pdf.obtem_log_md5()

    for md5 in lista_md5:
        print(md5)


if __name__ == "__main__":
    main()
