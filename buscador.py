from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import json

class Buscador(object):
    URLS_IMPORTANTES = [] #salva sites em que o processo precisa ser pesquisado
    #opcoes que fazem o navegador carregar em segundo plano
    options = Options()
    options.add_argument("--headless")

    def __init__(self, numeroDigitoAno, JTRNumero, foroNumero):
        try:
            self.numeroDigitoAno = numeroDigitoAno #guarda para preencher formulario
            self.foroNumero = foroNumero #guarda para preencher formulario

            f = open('lista_tribunais.json','r') #abre arquivo contendo tribunais cadastrados
            tribunais = json.loads(f.read()) #salva na variavel para verificação
            f.close() #fecha arquivo
            #para cada tribunal na lista de tribunais cadastrados
            for tribunal in tribunais["Tribunais"]:
                if (JTRNumero==tribunal["Codigo"]): #caso o processo pertença aquele tribunal
                    #salvamos a lista de sites em que precisamos pesquisar o processo
                    self.URLS_IMPORTANTES = tribunal["Sites"]
            if not self.URLS_IMPORTANTES: #caso o processo nao pertenca a nenhum tribunal
                print("Tribunal nao registrado")
        except Exception as e:
            print("deu ruim no buscador")
            print(e)

    #funcao que retorna o grau e o hmtl da primeira instancia de um processo
    def getPrimeiraInstancia(self):
        try:
            #executa navegador atraves da webdriver
            fogo = webdriver.Firefox(firefox_options=self.options)
            fogo.get(self.URLS_IMPORTANTES[0]["URL"]) #pega url referente ao site da primeira instancia

            #encontra o formulario que deve ser preenchido
            formulario_numeroDigito = fogo.find_element_by_id('numeroDigitoAnoUnificado')
            formulario_foroNumero = fogo.find_element_by_id('foroNumeroUnificado')
            #envia numeros do processo para preencher os formularios
            formulario_numeroDigito.send_keys(self.numeroDigitoAno)
            formulario_foroNumero.send_keys(self.foroNumero)
            #encontra o botao de pesquisa
            botao = fogo.find_element_by_name("pbEnviar")
            botao.click() #clica no botao para pesquisar e carregar nova pagina

            #recebe pagina contendo as informações do processo pesquisado
            html = fogo.page_source
            
            return (self.URLS_IMPORTANTES[0]["Grau"],html)

        except Exception as e:
            print("Nao foi possivel pegar primeira instancia do processo")
            print(e)

    #funcao que retorna o grau e o hmtl da primeira instancia de um processo
    def getSegundaInstancia(self):
        try:
            #executa navegador atraves da webdriver
            fogo = webdriver.Firefox(firefox_options=self.options)
            fogo.get(self.URLS_IMPORTANTES[1]["URL"]) #pega url referente ao site da segunda instancia

            #encontra o formulario que deve ser preenchido
            formulario_numeroDigito = fogo.find_element_by_id('numeroDigitoAnoUnificado')
            formulario_foroNumero = fogo.find_element_by_id('foroNumeroUnificado')
            #envia numeros do processo para preencher os formularios
            formulario_numeroDigito.send_keys(self.numeroDigitoAno)
            formulario_foroNumero.send_keys(self.foroNumero)
            #encontra o botao de pesquisa
            botao = fogo.find_element_by_name("pbEnviar")
            botao.click() #clica no botao para pesquisar e carregar nova pagina

            #recebe pagina contendo as informações do processo pesquisado
            html = fogo.page_source
            
            return (self.URLS_IMPORTANTES[1]["Grau"],html)
            
        except Exception as e:
            print("Nao foi possivel pegar segunda instancia do processo")
            print(e)