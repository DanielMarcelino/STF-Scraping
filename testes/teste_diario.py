import sys
sys.path.insert(0, '..')
from stf_scraping import Diario


# É nescessario conexão á internet para realizar os testes abaixo
def test_valida_existencia_de_diario_para_03_05_2019():
    diario = Diario("03-05-2019")
    assert diario._Diario__checa_existencia_de_diario() == True

def test_invalida_existencia_de_diario_para_16_11_2021():
    diario = Diario("16-10-2021")
    assert diario._Diario__checa_existencia_de_diario() == False

def test_obtem_erro_quando_uma_data_em_formato_inesperado_quebra_a_pagina():
    diario = Diario("16-10-20021")
    assert diario._Diario__checa_existencia_de_diario() == False

def test_obtem_uma_url_de_pdf_na_data_04_10_2021():
    diario = Diario("04-10-2021")
    assert diario._Diario__checa_existencia_de_diario() == True
    lista_url_pdf = diario.get_url_pdf()
    assert len(lista_url_pdf) == 1
    assert lista_url_pdf[0] == "verDiarioEletronico.asp?seq=757585726&data=01/10/2021&ano=2021&numero=197"

def test_obtem_duas_urls_de_pdf_na_data_16_10_2020():
    diario = Diario("16-10-2020")
    assert diario._Diario__checa_existencia_de_diario() == True
    lista_url_pdf = diario.get_url_pdf()
    assert len(lista_url_pdf) == 2
    assert lista_url_pdf[0] == "verDiarioEletronico.asp?seq=754124131&data=15/10/2020&ano=2020&numero=251"
    assert lista_url_pdf[1] == "verDiarioEletronico.asp?seq=754121625&data=15/10/2020&ano=2020&numero=250"

def test_obtem_tres_urls_de_pdf_na_data_04_11_2019():
    diario = Diario("04-11-2019")
    assert diario._Diario__checa_existencia_de_diario() == True
    lista_url_pdf = diario.get_url_pdf()
    assert len(lista_url_pdf) == 3
    assert lista_url_pdf[0] == "verDiarioEletronico.asp?seq=751305988&data=30/10/2019&ano=2019&numero=240"
    assert lista_url_pdf[1] == "verDiarioEletronico.asp?seq=751303782&data=30/10/2019&ano=2019&numero=239"
    assert lista_url_pdf[2] == "verDiarioEletronico.asp?seq=751296690&data=30/10/2019&ano=2019&numero=238"

def test_obtem_nenhuma_url_de_pdf_na_data_12_10_2021():
    diario = Diario("12-10-2021")
    assert diario._Diario__checa_existencia_de_diario() == False
    assert len(diario.get_url_pdf()) == 0

def test_obtem_um_arquivo_pdf_da_lista_de_url_na_data_04_10_2021():
    diario = Diario("04-10-2021")
    assert diario._Diario__checa_existencia_de_diario() == True
    assert len(diario.get_url_pdf()) == 1
    diario.get_lista_pdf_md5()
    assert len(diario._Diario__lista_binarios_pdf) == 1

def test_obtem_md5_de_2_pdfs_na_data_15_09_2021():
    diario = Diario("15-09-2021")
    assert diario._Diario__checa_existencia_de_diario() == True
    assert len(diario.get_url_pdf()) == 2
    lista_md5 = diario.get_lista_pdf_md5()
    assert lista_md5[0] == "ec7995461aea41d8f253672d2c64aec5"
    assert lista_md5[1] == "0214f422c814f45775b460b205761552"

def test_baixa_pdf_e_renomea_com_md5_para_data_15_09_2021():
    diario = Diario("15-09-2021")
    assert diario._Diario__checa_existencia_de_diario() == True
    assert len(diario.get_url_pdf()) == 2
    lista_md5 = diario.get_lista_pdf_md5()
    diario.baixa_pdf_renomeado_com_md5()
    try:
        for nome_pdf in lista_md5:
            with open(nome_pdf  + ".pdf", "rb") as arquivo:
                arquivo.read()
        assert True
    except:
        assert False
