# Desafio_JusBrasil
Jusbrasil - Desafio Backend Engineer | Data

#Requisitos
bibliotecas:
  flask
  selenium
arquivos:
  Copiar arquivo geckodriver da pasta "src" do a pasta "/bin" de sua máquina

##Estrutura do JSON:
Optei por organizar o json da seguinte forma

\{ 
    "Numero_processo": \{
        "Completo": '', #salva o numedo do processo passado para facilitar a visualização
        #separação feita para facilitar a busca pelo tribunal correto e preencher informações
        "numeroDigitoAnoUnificado": "", 
        "JTRNumeroUnificado": "",
        "foroNumeroUnificado": ""
    \},
    "Dados_processo": \{
        "Juiz": [ #uma lista pois há processos em há varios juizes (exemplo: 0000010-96.2014.8.12.0049)
        ],
        "Classe": "",
        "Area": "",
        "Assunto": "",
        "Distribuicao": "",
        "Valor_acao": 0.0
    \},
    "Partes_processo":[
        \{
            "Tipo": "", #qual o tipo/label do individuo/instituição na parte do processo
            "Nome": '', #nome referente ao individuo/instituição 
            "Agregados": [ #outros individuos/intituições associados ao individuo/instituiçao na parte do processo
                \{
                    "Tipo": "", #tipo/label do associado
                    "Nome": "" #nome do associado
                    \}
            ]
        \}
    ],
    "Movimentacoes_processo":[ #algumas das movimentações possuiem apenas data e status
        \{
            "Data": "",
            "Status": "",
            "Resumo": ""
        \}
    ]
\}