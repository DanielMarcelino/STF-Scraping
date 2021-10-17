from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup

class Data:
    def __init__(self, data: str):
        self.__data = data

    def __checa_tamanho(self):
        return len(self.__data) == 10

    def __checa_separador(self):
        try:
            separador_1 = self.__data[2] == '-'
            separador_2 = self.__data[5] == '-'
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
        if self.__checa_tamanho() and self.__checa_separador() and self.__checa_dia() and self.__checa_mes() and \
                self.__checa_ano():
            return True
        else:
            return False

    def data_formatada(self):
        return self.__data.replace("-", "/")

class Diario:
    def __init__(self, data: str):
        self.__url_pdf = []
        self.__data = data
        self.__html = ""
        self.__headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'}

    def __verifica_url(self, url):
        try:
            request = Request(url, headers=self.__headers)
            response = urlopen(request)
            return  response.read()
        except HTTPError as error:
            print(error.status, error.reason)
            exit()
        except URLError as error:
            print(error.reason)
            exit()

    def checa_existencia_de_diario(self):
        try:
            url = 'https://www.stf.jus.br/portal/diariojusticaeletronico/montarDiarioEletronico.asp?tp_pesquisa=0&dataP='
            url = url + self.__data
            self.__html = self.__verifica_url(url)
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
        self.__html = BeautifulSoup(self.__html, 'html.parser')

    def get_url_pdf(self):
        self.__trata_html()
        self.__html = self.__html.findAll('a', target='_blank')
        links = []
        for link in self.__html:
            links.append(str(link).replace('<a href="', '').replace(
                '" target="_blank"><img border="0" src="imagem/ico_pdf_integral.jpg"/></a>', ''))
        return links





