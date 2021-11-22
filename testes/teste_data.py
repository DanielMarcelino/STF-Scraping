import sys
sys.path.insert(0, '..')
from stf_scraping import valida_data

def test_valida_data_que_respeita_o_formato_separador_intervalo():
    data = "01-01-0001"
    assert valida_data(data)

def test_valida_data_em_que_o_dia_esta_no_limite_maximo():
    data = "31-01-0001"
    assert valida_data(data)

def test_valida_data_em_que_o_mes_esta_no_limite_maximo():
    data = "31-12-0001" 
    assert valida_data(data)

def test_valida_data_em_que_o_ano_esta_no_limite_maximo():
    data = "31-12-9999" 
    assert valida_data(data)

def test_invalida_data_em_que_o_dia_e_igual_a_zero():
    data = "0-12-2021" 
    assert not valida_data(data)

def test_invalida_data_em_que_o_mes_e_igual_a_zero():
    data = "01-00-2021" 
    assert not valida_data(data)

def test_invalida_data_em_que_o_ano_e_igual_a_zero():
    data = "01-01-00" 
    assert not valida_data(data)

def test_invalida_data_com_separador_inesperado():
    data = "01/01/2021" 
    assert not valida_data(data)
    
