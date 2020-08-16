import json
import requests
from backend.src.extrator import Extrator

class Refinador(object):
    DADOS_REFINADOS = {}
    PARTES_REFINADAS = []
    MOVIMENTACOES_REFINADOS = []
    def __init__(self, conteudo_dados, conteudo_partes, conteudo_movimentacoes):
        self.refinaDados(conteudo_dados)
        self.refinaPartes(conteudo_partes)
        self.refinaMovimentacoes(conteudo_movimentacoes)

    def refinaDados(self, conteudo_dados):
        try:
            guarda_dados = {}
            processo_juiz = []
            processo_distribuicao = ''
            processo_classe = ''
            processo_area = ''
            processo_acao = 0.0
            processo_assunto = ''
            for elemento in conteudo_dados:
                conteudo = elemento.split(":")
                label = conteudo[0].strip()
                if label == "Classe":
                    processo_classe = conteudo[1].strip()
                elif label == "Área":
                    processo_area = conteudo[-1].strip()
                elif label == "Assunto":
                    processo_assunto = (conteudo[1].strip())
                elif label == "Juiz":
                    processo_juiz.append(conteudo[1].strip())
                elif label == "Valor da ação":
                    processo_acao = float(conteudo[1].split("R$")[-1].replace(".",'').replace(',', '.').strip())
                elif label == "Distribuição":
                    for item in range(1,len(conteudo)-1):
                        processo_distribuicao += conteudo[item].strip()+":"
                    processo_distribuicao += conteudo[-1]
                elif len(conteudo)== 1:
                    processo_distribuicao += ("\n"+label)
                elif conteudo[1].split()[0] == 'JUIZ':
                    junta = ''
                    for item in range(1,len(conteudo[1].split())):
                        junta += conteudo[1].split()[item]+" "
                    processo_juiz.append(junta.strip())

            guarda_dados = {
                "Classe": processo_classe,
                "Area": processo_area,
                "Assunto": processo_assunto,
                "Distribuicao": processo_distribuicao,
                "Juiz": processo_juiz,
                "Valor_acao": processo_acao
            }
            self.DADOS_REFINADOS = guarda_dados
        except:
            print("Nao foi possivel refinar dados")

    def getDados(self):
        try:
            return self.DADOS_REFINADOS
        except:
            print("Nao foi possivel pegar dados do processo")

    def refinaPartes(self, conteudo_partes):
        try:
            guarda_partes = []
            for elemento in conteudo_partes:
                principal_obj = {"Tipo": "", "Nome": "", "Agregados": []}
                conteudo = elemento.split("|")
                # print(conteudo)
                principal_obj["Tipo"] = conteudo[0]
                principal_obj["Nome"] = conteudo[1]
                # print(principal_obj)
                lista_agregados = conteudo[2].split(",")
                # print(len(lista_agregados))
                indice = 0
                while indice < len(lista_agregados) and len(lista_agregados)>1:
                    agregados = {"Tipo":"", "Nome": ""}
                    agregados["Tipo"] = lista_agregados[indice]
                    agregados["Nome"] = lista_agregados[indice+1]
                    principal_obj["Agregados"].append(agregados)
                    indice+=2
                # print(principal_obj)
                guarda_partes.append(principal_obj)
            self.PARTES_REFINADAS = guarda_partes

        except Exception as e:
            print("Nao foi possivel refinar partes do processo")
            print(e)

    def getPartes(self):
        try:
            return self.PARTES_REFINADAS
        except:
            print("Nao foi possivel pegar partes do processo")

    def refinaMovimentacoes(self, conteudo_movimentacoes):
        try:
            guarda_movimentacoes = []
            for elemento in conteudo_movimentacoes:
                conteudo = elemento.split("|")
                guarda_movimentacoes.append(
                    {
                        "Data":conteudo[0],
                        "Status":conteudo[1],
                        "Resumo":conteudo[2]
                    }
                )
            self.MOVIMENTACOES_REFINADOS = guarda_movimentacoes
        except Exception as e:
            print("Nao foi possivel refinar movimentacoes")
            print(e)

    def getMovimentacoes(self):
        try:
            return self.MOVIMENTACOES_REFINADOS
        except:
            print("Nao foi possivel pegar movimentacoes do processo")
