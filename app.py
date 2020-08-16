#!/usr/bin/python3

from flask import Flask, jsonify, request, render_template, redirect, url_for, flash #biblioteca para gerar api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json #biblioteca para manipulacao e conversao de objetos'.json'

from backend.src.controllers.processController import ProcessController
from backend.src.controllers.tribunalController import TribunalController

from formularioPesquisa import FormularioPesquisa
from config import Config

app = Flask(
    __name__,
    template_folder= "frontend/view/templates",
    static_folder= 'frontend/view/static'
)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Tribunal, Processo, Site

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'Tribunal':Tribunal, 'Processo':Processo, 'Site':Site}

#rota inicial da nossa API
@app.route('/', methods=['GET', 'post'])
def home():
    form = FormularioPesquisa()
    if form.validate_on_submit():
        flash("Processo {} foi solicitado".format(form.numero_processo.data))
        return (
            redirect(
                url_for(
                    'getProcesso',
                    sigla_tribunal='amendoim',
                    numero_processo=form.numero_processo.data
                )
            )
        )
    return render_template('homePage.html', form=form)

@app.route('/tribunais', methods=['GET', 'POST'])
def tribunais():
    tribunais = TribunalController()
    # tribunais = [{'name':'tjal'}, {'name':'tjms'}]
    return render_template('tribunalsListPage.html', lista_tribunais=tribunais.getTribunais())

@app.route('/tribunais/<string:sigla_tribunal>')
def listarProcessosTribunal(sigla_tribunal):
    tribunal = TribunalController()
    lista_processos = ['121','12321','44444']
    return render_template('tribunalPage.html', tribunal=tribunal.getTribunais()[0], lista_processos=lista_processos)

#rota para que o usuario possa obter informacoes do processo que deseja
@app.route('/tribunais/<string:sigla_tribunal>/<string:numero_processo>')
def getProcesso(sigla_tribunal, numero_processo):
    # processo = ProcessController.getProcesso(numero_processo)
    processo =  numero_processo
    tribunal = sigla_tribunal
    return render_template('processPage.html',title='Processo', sigla_tribunal=tribunal, numero_processo=processo)

#deixa nosso server rodando
if __name__ == '__main__':
    app.run(debug=True)