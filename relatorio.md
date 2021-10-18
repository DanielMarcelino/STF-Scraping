# Relatório de Desenvolvimento

O principal objetivo, além de desenvolver a solução para o enunciado da proposta de sistema, era fazê-lo de forma ótima. Isto é, obter uma solução simples que facilitasse o desenvolvimento e execução do script. A premissa inicial foi evitar o uso de frameworks que necessitem um processo complexo de instalação e configuração e priorizar os pacotes built-in que a linguagem python dispoẽ.

## Dificuldades encontradas
Dentre os desafios em alcançar a solução da proposta, o principal obstáculo foi lidar com a página de diários do Supremo Tribunal Federal. A página oferece duas formas de se buscar um diário oficial: por seleção manual, na interface em forma de calendário e via formulário. A seleção manual é baseada em java script, esse caminho exigiria a aplicação de uma biblioteca complexa no projeto. A segunda via, por formulário, pareceu mais atraente aos planos de desenvolvimento da solução. No entanto, ainda seria  relativamente complicado lidar com o formulário da página. 


## Métodos
Investindo tempo em investigar por outras formas de requisitar os diários da página e usando uma ferramenta de desenvolvedor presente no navegador web, foi possível encontrar um método que satisfez a necessidade de simplificar o desenvolvimento da solução.

A investigação revelou que o bloco em que os diários são exibidos é um módulo importado através de uma url (https://www.stf.jus.br/portal/diariojusticaeletronico/montarDiarioEletronico.asp?tp_pesquisa=0&dataP=15/09/2021). É possível requisitar a lista de diários, na data desejada, apenas modificando a data contida na url. Descoberto isso, foi usada a biblioteca urllib para capturar o código html da página pela response e extrair a url de cada arquivo PDF contida na página através dos recursos do pacote Beautiful Soup.

O restante das funções que o script deveria realizar para concluir a solução do problema proposto não representaram dificuldades quanto ao desenvolvimento.

O desenvolvimento foi conduzido  por testes.  Métodos de testes automáticos foram desenvolvidos antes das classes que seriam testadas. Com isso, as classes sofreram constantes refatorações até passarem nos testes.


## Fontes de Pesquisa

- [Your First Web Scraper - Web Scraping with Python](https://www.oreilly.com/library/view/web-scraping-with/9781491910283/ch01.html)

- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

- [21.5. urllib — URL handling modules](https://docs.python.org/3.6/library/urllib.html)

- [Create MD5 Hash of a File in Python](https://debugpointer.com/create-md5-hash-of-a-file-in-python/)



