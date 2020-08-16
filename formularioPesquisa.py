from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class FormularioPesquisa(FlaskForm):
    numero_processo = StringField('Numero do Processo', validators=[DataRequired()])
    consultar = SubmitField("Consultar")