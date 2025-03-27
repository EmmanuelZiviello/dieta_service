from flask_restx import Resource
from flask import request
from F_taste_dieta.namespaces import nutrizionista_ns
from F_taste_dieta.utils.jwt_custom_decorators import nutrizionista_required
from F_taste_dieta.schemas.alimento import AlimentoSchema
from F_taste_dieta.services.alimento_service import AlimentoService

alimenti_schema = AlimentoSchema(many=True, only=['nome_alimento', 'codice_alimento'])

class AlimentoController(Resource):

    @nutrizionista_required()
    @nutrizionista_ns.doc('ricevi la lista di alimenti inseribili nella dieta')
    def get(self):
        return AlimentoService.get_all_alimenti()
    
    @nutrizionista_ns.doc('debug per aggiungere alimenti nel db')
    def post(self):
        request_json = request.get_json()
        return AlimentoService.add(request_json)
        
