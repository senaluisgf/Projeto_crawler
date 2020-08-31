#!/usr/bin/python3

from flask import Flask, jsonify, request, render_template, redirect, url_for, flash #biblioteca para gerar api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json #biblioteca para manipulacao e conversao de objetos'.json'
import re

from backend.src.controllers.processController import ProcessController
from backend.src.controllers.tribunalController import TribunalController

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
from forms import FormularioPesquisa, FormularioCadastroTribunal

# guarda a expressao regular que extrai o codigo do tribunal de dentro do numero do processo
expressao_codigo = re.compile(r'\.[0-9]\.[0-9]{2}')

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'Tribunal':Tribunal, 'Processo':Processo, 'Site':Site}

# rota inicial da nossa API
# ainda preciso processar o numero usando regex e retornar a pesquisa do backend
@app.route('/', methods=['GET', 'post'])
def home():
    form = FormularioPesquisa()
    if form.validate_on_submit():
        processo = Processo.query.filter_by(numero=form.numero_processo.data).first()
        if processo:
            tribunal = Tribunal.query.get(processo.tribunal_id)
            return (
                redirect(
                    url_for(
                        'getProcesso',
                        sigla_tribunal=tribunal.sigla,
                        numero_processo=processo.numero
                    )
                )
            )
        codigo_tribunal = expressao_codigo.findall(form.numero_processo.data)[0][1:]
        # print("Home: codigo tribunal - "+codigo_tribunal)
        flash("Processo nao esta no banco")
    return render_template('pagina_inicial.html', form=form)

@app.route('/tribunais', methods=['GET', 'POST'])
def listarTribunais():
    tribunais = Tribunal.query.all()
    return render_template('lista_de_tribunais.html', lista_tribunais=tribunais)

@app.route('/tribunais/new', methods=['GET', 'POST'])
def cadastrarTribunal():
    form = FormularioCadastroTribunal()
    if form.validate_on_submit():
        tribunal_novo = Tribunal(nome=form.nome.data, sigla=form.sigla.data, codigo=form.codigo.data)
        site_novo = Site(grau=form.grau_1.data, url=form.site_1.data, tribunal=tribunal_novo)
        # print(tribunal_novo)
        # print(site_novo)
        db.session.add(tribunal_novo)
        db.session.add(site_novo)
        db.session.commit()
        flash("Tribunal cadastrado com sucesso!")
        return redirect(url_for('tribunais'))
    return render_template('cadastro_tribunal.html', title='Cadastro', form=form)

@app.route('/tribunais/<string:sigla_tribunal>')
def listarProcessosTribunal(sigla_tribunal):
    tribunal = Tribunal.query.filter_by(sigla=sigla_tribunal).first_or_404()
    lista_processos = Processo.query.filter_by(tribunal_id=tribunal.id)
    return render_template('pagina_do_tribunal.html', tribunal=tribunal, lista_processos=lista_processos)

# rota para que o usuario possa obter informacoes do processo que deseja
@app.route('/tribunais/<string:sigla_tribunal>/<string:numero_processo>')
def getProcesso(sigla_tribunal, numero_processo):
    processo = Processo.query.filter_by(numero=numero_processo).first()
    tribunal = Tribunal.query.filter_by(sigla=sigla_tribunal).first()
    return render_template('pagina_do_processo.html',title='Processo', tribunal=tribunal, processo=processo)

# deixa nosso server rodando
if __name__ == '__main__':
    app.run(debug=True)