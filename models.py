from app import db

class Tribunal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    sigla = db.Column(db.String(10),index=True ,unique=True)
    codigo = db.Column(db.String(10), index=True, unique=True)
    sites = db.relationship('Site', backref='tribunal', lazy='dynamic')
    processos = db.relationship('Processo', backref='tribunal', lazy="dynamic")

    def __repr__(self):
        return 'Tribunal: {}({})'.format(self.nome, self.sigla)

class Processo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(30), index=True, unique=True)
    juiz = db.Column(db.String(50))
    classe = db.Column(db.String(50))
    area = db.Column(db.String(30))
    assunto = db.Column(db.String(30))
    distribuição = db.Column(db.String(100))
    valor_acao = db.Column(db.Float)
    tribunal_id = db.Column(db.Integer, db.ForeignKey('tribunal.id'))

    def __repr__(self):
        return 'Processo: {} | Juiz: {}'.format(self.numero, self.juiz)

class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grau = db.Column(db.String(20))
    url = db.Column(db.String(45))
    tribunal_id = db.Column(db.Integer, db.ForeignKey('tribunal.id'))

    def __repr__(self):
        return 'Grau {} Site {}'.format(self.grau, self.url)