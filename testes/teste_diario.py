import sys
sys.path.insert(0, '..')
from stf_scraping import Diario

# É nescessario conexão á internet para realizar os testes abaixo
def test_valida_existencia_de_diario_para_03_05_2019():
    diario = Diario("03/05/2019")
    assert diario.checa_existencia_de_diario() == True

def test_invalida_existencia_de_diario_para_16_11_2021():
    diario = Diario("16/10/2021")
    assert diario.checa_existencia_de_diario() == False

def test_obtem_erro_interno_quando_uma_data_em_formato_inesperado_quebra_a_pagina():
    diario = Diario("16/10/20021")
    assert diario.checa_existencia_de_diario() == False

def test_obtem_uma_url_de_pdf_na_data_04_10_2021():
    diario = Diario("04/10/2021")
    assert diario.checa_existencia_de_diario() == True
    assert len(diario.get_url_pdf()) == 1

def test_obtem_duas_urls_de_pdf_na_data_16_10_2020():
    diario = Diario("16/10/2020")
    assert diario.checa_existencia_de_diario() == True
    assert len(diario.get_url_pdf()) == 2

def test_obtem_tres_urls_de_pdf_na_data_04_11_2019():
    diario = Diario("04/11/2019")
    assert diario.checa_existencia_de_diario() == True
    assert len(diario.get_url_pdf()) == 3

def test_obtem_nenhuma_url_de_pdf_na_data_12_10_2021():
    diario = Diario("12/10/2021")
    assert diario.checa_existencia_de_diario() == False
    assert len(diario.get_url_pdf()) == 0