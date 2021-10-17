import sys
sys.path.insert(0, '..')
from stf_scraping import Data

# Formato DD-MM-AAAA
# Separador "-"
# 0 < DIA < 31 / 0 < MES < 12 / 0 < ANO < 9999

def test_valida_data_que_respeita_o_formato_separador_intervalo():
    data = Data("01-01-0001")
    assert data.valida_data() == True


def test_valida_data_em_que_o_dia_esta_no_limite_maximo():
    data = Data("31-01-0001")
    assert data.valida_data() == True
    

def test_valida_data_em_que_o_mes_esta_no_limite_maximo():
    data = Data("31-12-0001")
    assert data.valida_data() == True
    

def test_valida_data_em_que_o_ano_esta_no_limite_maximo():
    data = Data("31-12-9999")
    assert data.valida_data() == True
    

def test_invalida_data_em_que_o_dias_esta_acima_do_limite_maximo():
    data = Data("32-12-9999")
    assert data.valida_data() == False

    
def test_invalida_data_em_que_o_mes_esta_acima_do_limite_maximo():
    data = Data("31-13-9999")
    assert data.valida_data() == False


def test_invalida_data_em_que_o_ano_esta_acima_do_limite_maximo():
    data = Data("31-12-10000")
    assert data.valida_data() == False


def test_invalida_data_em_que_o_dias_esta_abaixo_do_limite_maximo():
    data = Data("00-12-9999")
    assert data.valida_data() == False
    

def test_invalida_data_em_que_o_mes_esta_abaixo_do_limite_maximo():
    data = Data("31-00-9999")
    assert data.valida_data() == False


def test_invalida_data_em_que_o_ano_esta_abaixo_do_limite_maximo():
    data = Data("31-12-0000")
    assert data.valida_data() == False
    

def test_invalida_data_em_que_o_dia_contem_somente_uma_casa_decimal_sem_zero():
    data = Data("5-12-2021")
    assert data.valida_data() == False
    

def test_invalida_data_em_que_o_mes_contem_somente_uma_casa_decimal_sem_zero():
    data = Data("05-1-2021")
    assert data.valida_data() == False


def test_invalida_data_em_que_contem_separadores_inesperados():
    data = Data("05/12/2021")
    assert data.valida_data() == False


def test_invalida_data_em_que_contem_o_primeiro_separador_inesperado():
    data = Data("05/12-2021")
    assert data.valida_data() == False


def test_invalida_data_em_que_contem_o_segundo_separador_inesperado():
    data = Data("05-12/2021")
    assert data.valida_data() == False


def test_formata_data_corretamente():
    data = Data("05-12-2021")
    assert data.data_formatada() == "05/12/2021"
