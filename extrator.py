import requests
from bs4 import BeautifulSoup
import json

class Extrator(object):
    HTML_PAGINA = '' #guarda html recebido
    DADOS_PROCESSO = [] #separa tabela de dados do processo
    PARTES_PROCESSO = [] #separa tabela de partes do processo
    MOVIMENTACOES_PROCESSO = [] #separa tabela de movimentacoes do processo
    STATUS = True

    def __init__(self, html_pagina):
        self.coletarProcesso(html_pagina)

    def coletarProcesso(self,html_pagina):
        try:
            sopa = BeautifulSoup(html_pagina, 'html.parser')
            self.extrairDadosProcesso(sopa)
            self.extrairPartesProcesso(sopa)
            self.extrairMovimentacoesProcesso(sopa)
        except Exception as e:
            self.STATUS = False
            print("Não foi possivel acessar a pagina")
            print(e)

    def extrairDadosProcesso(self, sopa):
        try:
            self.DADOS_PROCESSO = []
            dados_processo = sopa.find(class_='secaoFormBody', id='').prettify()
            soupa = BeautifulSoup(dados_processo, 'html.parser').tr
            irmaos = soupa.find_next_siblings()
            for irmao in irmaos:
                junta=''
                for indice in irmao.get_text().split():
                    junta += indice+' '
                self.DADOS_PROCESSO.append(junta.strip())


        except Exception as e:
            self.STATUS = False
            print("Nao foi possivel coletar dados do processo")
            print(e)
    
    def extrairPartesProcesso(self, sopa):
        try:
            self.PARTES_PROCESSO = []
            partes_processo = sopa.find(id='tableTodasPartes').prettify()
            soupa = BeautifulSoup(partes_processo, 'html.parser').tr
            filho = BeautifulSoup(soupa.prettify(), 'html.parser').td
            filhos = filho.find_next_sibling()
            irmaos = soupa.find_next_siblings()
            junta = ''
            junta += filho.span.text.replace(":", ":|").strip()

            junta += filhos.text.strip().split('\n')[0].strip()+"|"
            for indice in range(1, len(filhos.text.strip().split('\n'))):
                conteudo = filhos.text.strip().split('\n')
                if conteudo[indice]:
                    junta+= (conteudo[indice].strip()+"'")

            tratamento = junta.replace("''", "','")
            self.PARTES_PROCESSO.append(tratamento)

            for irmao in irmaos:
                filho = BeautifulSoup(irmao.prettify(), 'html.parser').td
                filhos = filho.find_next_sibling()
                junta = ''
                junta += filho.span.text.replace(":", ":|").strip()
                junta += filhos.text.strip().split('\n')[0].strip()+"|"
                for indice in range(1, len(filhos.text.strip().split('\n'))):
                    conteudo = filhos.text.strip().split('\n')
                    if conteudo[indice]:
                        junta+= (conteudo[indice].strip()+"'")

                tratamento = junta.replace("''", "','").replace("'", '')
                self.PARTES_PROCESSO.append(tratamento)
        except Exception as e:
            self.STATUS = False
            print("Nao foi possivel coletar partes do processo")
            print(e)
    
    def extrairMovimentacoesProcesso(self, sopa):
        try:
            self.MOVIMENTACOES_PROCESSO = []
            movimentacoes_processo = sopa.find('tbody', id='tabelaTodasMovimentacoes').prettify()
            soupa = BeautifulSoup(movimentacoes_processo, 'html.parser').tr
            irmaos = soupa.find_next_siblings()
            junta = ''
            data = soupa.td.get_text().strip()
            status = str(soupa.find_all('td')[2].get_text().strip()).split('\n')[0]
            resumo = soupa.find('span').get_text().strip()
            junta = data+'| '+status+'| '+resumo+'\n'
            self.MOVIMENTACOES_PROCESSO.append(junta.strip())

            for irmao in irmaos:
                junta = ''
                #print('\n'+irmao.prettify()+'\n')
                data = (irmao.td.get_text().strip())
                status = (str(irmao.find_all('td')[2].get_text().strip()).split('\n')[0])
                resumo = (irmao.find('span').get_text().strip())

                junta = data+'| '+status+'| '+resumo+'\n'
                #print(junta)
                self.MOVIMENTACOES_PROCESSO.append(junta.strip())
        except Exception as e:
            self.STATUS = False
            print("Nao foi possivel coletar movimentações do processo")
            print(e)