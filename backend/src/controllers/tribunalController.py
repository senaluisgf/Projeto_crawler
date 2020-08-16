import json

from backend.src.models.tribunal import Tribunais

class TribunalController():
    def getTribunais(self):
        lista_tribunais = Tribunais('alagoas','tjal','123')
        return lista_tribunais.listarTribunais()