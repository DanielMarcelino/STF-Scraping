# ⚖️ STF Scraping

## 📋️ Descrição

Este é um simples script que baixa e retorna os hash MD5 dos diários oficiais do Supremo Tribunal Federal filtrados pela data de publicação.

### 🛠 Tecnologias

Os seguintes recursos foram usadas na construção do projeto:
- [Python 3.6](https://www.python.org/downloads/release/python-360/)
- [Beautiful Soupp](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Pytest](https://docs.pytest.org/en/6.2.x/)


### ▶️ Como executar o script
Antes de executar, caso não tenha em sua máquina, é necessário instalar o pacote Beautiful Soup:
```bash
# Instale o Beautiful Soup
$ pip install beautifulsoup4
```
Em seguida, clone o repositório:

```bash
# Clone este repositório
$ git clone https://github.com/DanielMarcelino/STF-Scraping.git
```

Por fim, execute o script com o seguinte comando:

```bash
# Execute o script
$ python stf_scraping.py <data>
```
O input da data é feito por meio de argumento de linha de comando. A data deve seguir o seguinte formato: `DD-MM-AAAA`.

A data admite dois tipos de caracteres separadores diferentes: `-` e `/`. Caso a data informada não satisfaça os requisitos o script não executará a busca de diário. Se não houver diários publicados na data informada, uma mensagem será exibida no terminal.
#### Exemplo de execução
A execução do script com a data de busca igual à `15-09-2021` retorna o seguinte resultado:
```bash
$ python stf_scraping.py 15-09-2021
ec7995461aea41d8f253672d2c64aec5
0214f422c814f45775b460b205761552
```

Cada linha do resultado corresponde ao hash MD5 de cada arquivo PDF de diário oficial que foi encontrado com a data de publicação equivalente a informada ao script. Durante a execução, os arquivos são baixados e nomeados com nomes correspondentes a sua hash MD5 e salvos no diretório em que o script foi executado.

O tempo de resposta do script é relativo ao tamanho dos arquivos PDF, quantidade e latência da conexão com o site do Supremo Tribunal Federal.


#### Execução dos testes
Antes de executar os testes, caso não tenha o pacote Pytest,  será nescessario instalá-lo seguindo o passo à seguir:
```bash
# Instalar Pytest
$ pip install -U pytest
```
Após instalar o Pytest, vá ao diretório `testes/` e execute o seguite comando no terminal: 
```bash
# Testes automáticos
$ pytest teste_data.py teste_diario.py 
```



