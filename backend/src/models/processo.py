import json

class Processo(object):
    STATUS = "" #informa o erro ou se esta tudo correto
    OBJETO = { #objeto para armazenar informações do processo
        "Numero_processo": {
            "Completo": '', #salva o numedo do processo passado para facilitar a visualização
            #separação feita para facilitar a busca pelo tribunal correto e preencher informações
            "numeroDigitoAnoUnificado": "", 
            "JTRNumeroUnificado": "",
            "foroNumeroUnificado": ""
        },
        "Dados_processo": {
            "Juiz": [ #uma lista pois há processos em há varios juizes (exemplo: 0000010-96.2014.8.12.0049)
            ],
            "Classe": "",
            "Area": "",
            "Assunto": "",
            "Distribuicao": "",
            "Valor_acao": 0.0
        },
        "Partes_processo":[
            {
                "Tipo": "", #qual o tipo/label do individuo/instituição na parte do processo
                "Nome": '', #nome referente ao individuo/instituição 
                "Agregados": [ #outros individuos/intituições associados ao individuo/instituiçao na parte do processo
                    {
                        "Tipo": "", #tipo/label do associado
                        "Nome": "" #nome do associado
                        }
                ]
            }
        ],
        "Movimentacoes_processo":[ #algumas das movimentações possuiem apenas data e status
            {
                "Data": "",
                "Status": "",
                "Resumo": ""
            }
        ]
    }
    

    def __init__(self, numero_processo):
        aux = numero_processo.split('.') #separa para facilitar outros processos (checar tribunal, prencher form)
        
        if len(aux)==5: #verifica formato do numero do processo
            self.OBJETO["Numero_processo"]["Completo"] = numero_processo
            self.OBJETO["Numero_processo"]["numeroDigitoAnoUnificado"] = aux[0] + '.' +aux[1]
            self.OBJETO["Numero_processo"]["JTRNumeroUnificado"] = aux[2] + '.' +aux[3]
            self.OBJETO["Numero_processo"]["foroNumeroUnificado"] = aux[-1].split('\n')[0]

            self.STATUS = "OK" #processo pronto para os devidas armazenamentos (preencherProcesso) 
            
            if (self.formatoInvalido()): #caso possua um formato invalido
                print('Processo inválido:\nO processo possui formato invalido')
                self.STATUS = "Formato invalido" #modifica status indicando o erro
           
            tribunal = self.foraDoEscopo()
            if tribunal=='ERROR': #caso o processo pertenca a um tribunal nao cadastrado
                print("Processo fora do escopo do desafio:\nO processo não pertence a nenhum tribunal especificado")
                self.STATUS = "Tribunal invalido" #modifica status indicando o erro
        else:
            self.STATUS = "Formato invalido"


    def preencheProcesso(self, dados_processo, partes_processo=[], movimentacoes_processo=[]):
        try:
            self.OBJETO["Dados_processo"] = dados_processo
            self.OBJETO["Partes_processo"] = partes_processo
            self.OBJETO["Movimentacoes_processo"] = movimentacoes_processo
        except:
            print("Nao foi possivel preencher o processo")

    def getJsonProcesso(self):
        try:
            processo = json.dumps(self.OBJETO)
            return processo
        except:
            print("Nao foi possivel retornar processo")

    #verifica se o documento possui formato valido
    def formatoInvalido(self):
        if (len(self.OBJETO["Numero_processo"]["numeroDigitoAnoUnificado"])!=15 or len(self.OBJETO["Numero_processo"]["JTRNumeroUnificado"])!=4 or len(self.OBJETO["Numero_processo"]["foroNumeroUnificado"])!=4):
            return True
        else:
            return False

# processo nao deve ter acesso a arquivos do tribunal
# vou importar o tribunal aq e testar com a funcao "getSigla()"
    def foraDoEscopo(self):
        f = open('lista_tribunais.json','r')
        tribunais = json.loads(f.read())
        f.close()
        nome='ERROR'
        for tribunal in tribunais["Tribunais"]:
            if (self.OBJETO["Numero_processo"]["JTRNumeroUnificado"]==tribunal["Codigo"]):
                return tribunal["Nome"]
        return nome
        
#testar e terminar, caso precise, essa funcao
    def __str__(self):
        if (self.formatoInvalido()):
            return 'iae Processo inválido:\nO processo possui formato invalido'
       
        tribunal = self.foraDoEscopo()
        if tribunal=='ERROR':
            return "Processo fora do escopo do desafio:\nO processo não pertence a nenhum tribunal especificado"
        

        return tribunal