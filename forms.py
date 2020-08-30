from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired
import re

from models import Tribunal

expressao = re.compile(r'[0-9]{7}\-[0-9]{2}\.[0-9]{4}\.[0-9]\.[0-9]{2}\.[0-9]{4}')

class FormularioPesquisa(FlaskForm):
    numero_processo = StringField('Numero do Processo', validators=[DataRequired()])
    consultar = SubmitField("Consultar")

    def validate_numero_processo(self, numero_processo):
        # print("validar numero: entrou")
        valido = expressao.match(numero_processo.data)
        # print("validar numero: "+str(valido))
        if valido is None:
            # print("Validar numero: if - formato invalido")
            raise ValidationError("Numero do processo possui formato invalido")

class FormularioCadastroTribunal(FlaskForm):
    nome = StringField("Nome do Tribunal", validators = [DataRequired()] )
    sigla = StringField("Sigla do Tribunal", validators = [DataRequired()])
    codigo = StringField("Codigo do Tribunal", validators = [DataRequired()])
    grau_1 = StringField("Grau:", validators = [DataRequired()])
    site_1 = StringField("URL:", validators = [DataRequired()])
    submit = SubmitField("Cadastrar")

    def validate_sigla(self, sigla):
        sigla  = Tribunal.query.filter_by(sigla=sigla.data).first()
        if sigla is not None:
            raise ValidationError("Já cadastramos um tribunal com esta sigla!")

    def validate_codigo(self, codigo):
        codigo = Tribunal.query.filter_by(codigo=codigo.data).first()
        if codigo is not None:
            raise ValidationError("já cadastramos um tribunal com este codigo!")