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






