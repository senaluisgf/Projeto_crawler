import os
import json

class Tribunais(object):
    #variavel que ira armazenar a lista de todos os tribunais cadastrados
    TRIBUNAIS_OBJETO = {
        "Tribunais": [
            {
                "Nome": "", #Nome por extenso do tribunal
                "Sigla": "", #sigla referente ao tribunal
                "Codigo": "", #Codigo referente ao tribunal
                "Sites": [ #armazena em uma lista todos os sites do dominio referente ao tribunal
                    {
                        "Grau": "", #Grau/relacao do processo
                        "URL": "" #Endereco do site referente ao grau do processo no tribunal
                    }
                ]
            }
        ]
    }

    #Construtor da classe que ira receber o primeiro tribunal passado e cadastra-lo
    #O parametro lista_paginas deve receber uma lista de diretorios respeitando o formato do modelo acima
    def __init__(self, nome_tribunal, sigla_tribunal, codigo_tribunal, lista_paginas= []):
        self.TRIBUNAIS_OBJETO["Tribunais"][0]["Nome"] = nome_tribunal
        self.TRIBUNAIS_OBJETO["Tribunais"][0]["Sigla"] = sigla_tribunal
        self.TRIBUNAIS_OBJETO["Tribunais"][0]["Codigo"] = codigo_tribunal
        self.TRIBUNAIS_OBJETO["Tribunais"][0]["Sites"] = lista_paginas

        #assim que o tribunal for cadastrado, é executada a função que armazena os tribunais cadastrado em disco
        self.salvarLista()
        #apos o armazenamento é criada uma pasta referente ao tribunal
        self.criarPastaTribunal(sigla_tribunal)

    #salva todos os tribunais na lista em um arquivo json para gerenciamento de processos e controle dos arquivos
    def salvarLista(self):
        f = open('lista_tribunais.json','w')
        f.write(json.dumps(self.TRIBUNAIS_OBJETO))
        f.close()
    
    #Adiciona um tribunal a lista de tribunais
    def addTribunal(self, nome_tribunal, sigla_tribunal, codigo_tribunal, lista_paginas=[]):
        try:
            tribunal_objeto = {
                "Nome": "",
                "Sigla": "",
                "Codigo": ""
            }

            tribunal_objeto["Nome"] = nome_tribunal
            tribunal_objeto["Sigla"] = sigla_tribunal
            tribunal_objeto["Codigo"] = codigo_tribunal
            tribunal_objeto["Sites"] = lista_paginas

            self.TRIBUNAIS_OBJETO["Tribunais"].append(tribunal_objeto) #adiciona tribunal na lista
            
            self.salvarLista() #reescreve o arquivo que armazena os tribunais adicionando o tribunal atual
            self.criarPastaTribunal(sigla_tribunal) #cria uma pasta para este tribunal
        except:
            print("Nao foi possivel Adicionar Tribunal à lista")

    #lista tribunais cadastrados
    def listarTribunais(self):
        lista_tribunais = []
        for tribunal in self.TRIBUNAIS_OBJETO["Tribunais"]:
            lista_tribunais.append(tribunal)
        return lista_tribunais

    #cria pasta referente ao tribunal passado (sigla)
    def criarPastaTribunal(self, pasta):
        try:
            if not os.path.exists(pasta): #verifica se a pasta ja existe
                    os.mkdir(pasta) #caso nao exista, a pasta é criada
        except:
            print("nao foi possivel criar pasta para "+pasta)

    #Cria um arquivo referente a instancia de um processo e salva este processo no tribunal ao qual ele pertence
    #por padrao, a funcao nao atualiza caso o arquivo do processo ja exista
    def criaArquivoProcesso(self, nome_arquivo, informacoes_arquivo, atualizar=False):
        try:
            aux = nome_arquivo.split('.') #separa o numero para encontrar o codigo do tribunal (embutido no processo)
            codigo_tribunal = aux[2] + '.' +aux[3] #salva este codigo do tribunal para vereficaçoes
            sigla = self.getSiglaTribunal(codigo_tribunal) #recebe a sigla do tribunal ao qual o processo pertence

            if sigla != 'ERROR': #caso o processo pertence a um tribunal nao cadastrado
                #indica o nome que o arquivo ira conter ao ser armazenado
                arquivo = './'+sigla+'/'+nome_arquivo+'.json'
               
                #verefica se o arquivo nao existe ou o arquivo deve ser atualizado
                if not os.path.isfile(arquivo) or atualizar:
                    f = open(arquivo, 'w')
                    f.write(informacoes_arquivo)
                    f.close()
            else:
                #provalmente nem chega aqui porque as classes buscador e processo ja verificam este problema
                print("processo fora do escopo")
        except:
            print("Nao foi possivel criar arquivo para o processo "+nome_arquivo)

    #dado um codigo de um tribunal, retorna sua sigla caso exista
    def getSiglaTribunal(self, codigo_tribunal):
        try:
            #para cada tribunal na lista
            for tribunal in self.TRIBUNAIS_OBJETO["Tribunais"]:
                #verifica se o codigo passado é o msm do tribunal checado
                if tribunal["Codigo"] == codigo_tribunal:
                    return tribunal["Sigla"] #caso seja, retorna a sigla do tribunal
            return 'ERROR' #caso percorra todos os tribunais e nao ache um que corresponde, retorna "ERROR"
        except:
            print("Nao foi possivel checar sigla")

#adicionar uma maneira q dado o codigo do tribunal eu retorne a lista de sites