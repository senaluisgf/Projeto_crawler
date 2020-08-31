from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import json

# opcoes que fazem o navegador carregar em segundo plano
options = Options()
# options.add_argument("--headless")

raposa_fogo = webdriver.Firefox(firefox_options=options)

class Buscador(object):
    URLS_IMPORTANTES = [] #salva sites em que o processo precisa ser pesquisado

    def __init__(self, numero_processo, lista_links):
        self.numero_processo = numero_processo
        self.URLS_IMPORTANTES = lista_links

    def coletaPaginas(self):
        htmlPaginas = []

        for elemento in self.URLS_IMPORTANTES:
            htmlPaginas.append((elemento['grau'], self.extraiHTML(elemento['url'])))

        return htmlPaginas

    def extraiHTML(self, link):
        try:
            # executa navegador atraves da webdriver
            raposa_fogo.get(link)

            # encontra o formulario que deve ser preenchido
            formulario_numeroDigito = raposa_fogo.find_element_by_id('numeroDigitoAnoUnificado')
            # encontra o botao de pesquisa
            botao = raposa_fogo.find_element_by_name("pbEnviar")

            # preenche formulario
            formulario_numeroDigito.send_keys(self.numero_processo)

            # clica no botao para pesquisar e carregar nova pagina
            botao.click()

            #recebe pagina contendo as informações do processo pesquisado
            html = raposa_fogo.page_source
            
            return html

        except Exception as e:
            print("Nao foi possivel extrair html da pagina")
            print(e)

# busca = Buscador('123', [{'grau':'1o','url':'https://www.youtube.com/'}])
# print(busca.coletaPaginas())