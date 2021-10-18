from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import hashlib
import sys


class Data:
    def __init__(self, data: str):
        self.__data = data

    def __checa_tamanho(self):
        return len(self.__data) == 10

    def __checa_separador(self):
        try:
            separador_1 = (self.__data[2] == '-') or (self.__data[2] == '/')
            separador_2 = (self.__data[5] == '-') or (self.__data[5] == '/')
            return separador_1 and separador_2
        except:
            return False

    def __checa_dia(self):
        try:
            dia = "{}{}".format(self.__data[0], self.__data[1])
            dia = int(dia)
            return 0 < dia <= 31
        except:
            return False

    def __checa_mes(self):
        try:
            mes = "{}{}".format(self.__data[3], self.__data[4])
            mes = int(mes)
            return 0 < mes <= 12
        except:
            return False

    def __checa_ano(self):
        try:
            ano = "{}{}{}{}".format(self.__data[6], self.__data[7], self.__data[8], self.__data[9])
            ano = int(ano)
            return 0 < ano <= 9999
        except:
            return False

    def valida_data(self):
        if self.__checa_tamanho() and self.__checa_separador() and self.__checa_dia() and self.__checa_mes() and  self.__checa_ano():
            return True
        else:
            return False

    def data_formatada(self):
        return self.__data.replace("-", "/")


class Diario:
    def __init__(self, data):
        self.__data = data
        self.__lista_url_pdf = []
        self.__html = ""
        self.__headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'}
        self.__lista_binarios_pdf = []
        self.__lista_md5 = []



    def __verifica_url_captura_response(self, url):
        try:
            request = Request(url, headers=self.__headers)
            response = urlopen(request)
            return  response.read()
        except HTTPError as error:
            print(error.status, error.reason)
            exit()
        except URLError as error:
            print(error.reason, "\nVerifique sua conexão com a internet.")
            exit()

    def __checa_existencia_de_diario(self):
        try:
            url = 'https://www.stf.jus.br/portal/diariojusticaeletronico/montarDiarioEletronico.asp?tp_pesquisa=0&dataP='
            url = url + self.__data
            self.__html = self.__verifica_url_captura_response(url)
            return self.__html != b"0|"
        except:
            return False

    def __trata_html(self):
        self.__html = self.__html.decode('utf-8')
        self.__html = self.__html.split()
        self.__html = " ".join(self.__html)
        self.__html = self.__html.replace('> <', '><')
        self.__html = self.__html.replace('" ', '"')
        self.__html = self.__html.replace(' "', '"')

    def get_url_pdf(self):
        self.__trata_html()
        self.__html = BeautifulSoup(self.__html, 'html.parser')
        self.__html = self.__html.findAll('a', target='_blank')
        for link in self.__html:
            link = str(link)
            link = link.replace('<a href="', '')
            link = link.replace('" target="_blank"><img border="0" src="imagem/ico_pdf_integral.jpg"/></a>', '')
            link = link.replace('amp;', '')
            self.__lista_url_pdf.append(link)
        return self.__lista_url_pdf

    def __gera_lista_arquivos_binarios_pdf(self):
        for url in self.__lista_url_pdf:
            prefixo_url = 'http://www.stf.jus.br/portal/diariojusticaeletronico/'
            url = prefixo_url + url
            self.__lista_binarios_pdf.append(self.__verifica_url_captura_response(url))

    def __get_md5(self, pdf):
        md5 = hashlib.md5()
        md5.update(pdf)
        return str(md5.hexdigest())

    def get_lista_pdf_md5(self):
        self.__gera_lista_arquivos_binarios_pdf()
        for pdf in self.__lista_binarios_pdf:
            md5 = self.__get_md5(pdf)
            self.__lista_md5.append(md5)
        return self.__lista_md5

    def baixa_pdf_renomeado_com_md5(self):
        i = 0
        for pdf in self.__lista_binarios_pdf:
            with open(self.__lista_md5[i] + ".pdf", "wb") as arquivo:
                arquivo.write(pdf)
            i += 1

    def inicia_busca(self):
        if not self.__checa_existencia_de_diario():
            return False

        self.get_url_pdf()

        return True

def main(args):
    try:
        data_publicacao = Data(args[1])
    except:
        print("Nenhuma data foi informada.")
        exit()

    if not data_publicacao.valida_data():
        print("Data inválida!", end="\n\n")
        print("-- Instrução --")
        print("Formato da data: DD-MM-AAAA")
        print("Separadores esperados: '-' ou '/'")
        exit()

    busca_diario = Diario(data_publicacao.data_formatada())

    if not busca_diario.inicia_busca():
        print("Não há diários publicados na data informada.")
        exit()

    lista_md5 = busca_diario.get_lista_pdf_md5()

    busca_diario.baixa_pdf_renomeado_com_md5()

    for md5 in lista_md5:
        print(md5)


if __name__ == "__main__":
    sys.exit(main(sys.argv))




