import json

from backend.src.models.tribunal import Tribunais #cadastra e gerencia tribunais e salva processos em pastas de tribunais
from backend.src.models.processo import Processo #Armazena informacoes importantes,sobre o processo, que devem ser retornadas
from backend.src.buscador import Buscador #recebe numero do processo, verefica que tribunal ele pertence e retorna html do processo pesquisado
from backend.src.extrator import Extrator #recebe um html, isola tabelas importantes e retorda dados das tabelas
from backend.src.refinador import Refinador #pega dados das tabelas e coleta somente os dados desejados para o processo


class ProcessController():
    def getProcesso(numero_processo):
        sites_tjal = [
            {
                "Grau": "1_instancia",
                "URL": 'https://www2.tjal.jus.br/cpopg/open.do'
            },
            {
                "Grau": "2_instancia",
                "URL": 'https://www2.tjal.jus.br/cposg5/open.do'
            }
        ]

        #cadastrando tribunais
        tribunal_obj = Tribunais("Tribunal Justica Alagoas", "tjal", "8.02", lista_paginas=sites_tjal)

        #criando uma lista de processos vazia para adicionar jsons que iram ser retornados
        processos = []
        aux = numero_processo.split('.')
        numero_processo1 = aux[0] + '.' +aux[1]
        numero_processo2 = aux[2] + '.' +aux[3]
        numero_processo3 = aux[-1].split('\n')[0]

        #cria um objeto processo para organizar e armazenar informações da primeira instancia do processo
        processo_objeto = Processo(numero_processo)

        try:
            #verificar se o processo esta no escopo do desafio proposto
            if processo_objeto.STATUS=="OK":
                #variavel que irar receber o numero do processo dividido
                #procurar o tribunal correto em que o processo deve ser pesquisado
                busca = Buscador(numero_processo1, numero_processo2, numero_processo3)

                if busca.URLS_IMPORTANTES:#caso haja sites em que o processo deva ser pesquisado
                    #pega cada par ordenado de grau e html_pagina da primeira instancia do processo
                    (grau,html_pagina) = busca.getPrimeiraInstancia()

                    #fornesse o html_pagina pro extrator
                    #para isolar as tabelas da pagina que desejamos (dados, partes e movimentações do processo)
                    extrai = Extrator(html_pagina)

                    if extrai.STATUS: #caso o extrator tenha conseguido isolar as tabelas
                        #criamos uma variavel que irar pegar somente as informações que desejamos dentro dessas tabelas
                        refina = Refinador(extrai.DADOS_PROCESSO, extrai.PARTES_PROCESSO, extrai.MOVIMENTACOES_PROCESSO)
                    
                        dados_coletados = refina.getDados() #recebe apenas os dados desejados da tabela "Dados do Processo"
                        partes_coletadas = refina.getPartes() #recebe apenas os dados desejados da tabela "Partes do Processo"
                        movimentacoes_coletadas = refina.getMovimentacoes() #recebe apenas os dados desejados da tabela "Movimentações do Processo"

                        #apos o isolamento das tabelas e a coleta dos dados desejados
                        #podemos preencher o objeto processo com os valores coletados
                        processo_objeto.preencheProcesso(dados_processo=dados_coletados, partes_processo=partes_coletadas, movimentacoes_processo=movimentacoes_coletadas)
                        informacoes_coletadas = processo_objeto.getJsonProcesso() #pega informações da primeira instancia do processo

                        #lista de processos recebe um vetor contendo a primeira instancia do processo
                        processos = [{"Grau": grau, "Processo": json.loads(informacoes_coletadas)}]
                        #criamos um arquivo para salvar as informações coletadas sobre a primeira instancia do processo
                        tribunal_obj.criaArquivoProcesso(numero_processo+"_"+grau, informacoes_coletadas, atualizar=True)

                        #verifica se o processo pode estar em segundo grau
                        #caso esteja, repete passos para coletar segunda instancia
                        if len(busca.URLS_IMPORTANTES)>1:
                            #cria um objeto para guardar informações da segunda instancia do processo
                            processo_objeto = Processo(numero_processo)
                            #pega cada par ordenado de grau e html_pagina da segunda instancia do processo
                            (grau,html_pagina) = busca.getSegundaInstancia()

                            extrai = Extrator(html_pagina) #isola tabelas
                            if extrai.STATUS:
                                #coleta informacoes desejadas
                                refina = Refinador(conteudo_dados=extrai.DADOS_PROCESSO, conteudo_partes=extrai.PARTES_PROCESSO, conteudo_movimentacoes=extrai.MOVIMENTACOES_PROCESSO)
                                #separar informações coletadas para armazenagem
                                dados_coletados = refina.getDados()
                                partes_coletadas = refina.getPartes()
                                movimentacoes_coletadas = refina.getMovimentacoes()
                                #salva informações coletadas no objeto do processo
                                processo_objeto.preencheProcesso(dados_processo=dados_coletados, partes_processo=partes_coletadas, movimentacoes_processo=movimentacoes_coletadas)
                                informacoes_coletadas = processo_objeto.getJsonProcesso() #pega informações da segunda instancia do processo
                                
                                processos.append({"Grau": grau, "Processo": json.loads(informacoes_coletadas)}) #adiciona segunda intancia na lista
                                #cria outro arquivo para salvar segunda instancia do processo
                                tribunal_obj.criaArquivoProcesso(numero_processo+"_"+grau, informacoes_coletadas, atualizar=True)
                
                        return json.dumps(processos), 200
                    else:
                        return json.dumps({"error":"Este processo nao existe"})

            #caso pertenca a um tribunal nao cadastrado/inexistente
            elif processo_objeto.STATUS=="Tribunal invalido":
                return json.dumps({"error":"Este processo pertence a um tribunal inexistente ou nao cadastrado"}),404
            #caso o processo tenha um formato invalido
            else:
                return json.dumps({"error":"Este processo possui um formato invalido"}), 404

        except Exception as e:
            print(e)
            return json.dumps({"error":"Tempo limite de espera excedido"}), 404