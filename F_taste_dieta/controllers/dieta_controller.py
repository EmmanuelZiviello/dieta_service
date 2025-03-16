from flask import request
from flask_restx import Resource, fields
from flask_jwt_extended import get_jwt_identity
from F_taste_dieta.namespaces import nutrizionista_ns,paziente_ns
from F_taste_dieta.utils.jwt_custom_decorators import nutrizionista_required,paziente_required
from F_taste_dieta.schemas.paziente import PazienteSchema
from F_taste_dieta.services.dieta_service import DietaService


pietanza_model = nutrizionista_ns.model('pietanza', {
    'quantita' : fields.Integer(required=True),
    'unita_misura': fields.String(required=True),
    'nome_alimento': fields.String(required=True)
}, strict = True)

pasto_model = nutrizionista_ns.model('pasto',{
    'nota' : fields.String(required=True),
    'pietanze' : fields.List(fields.Nested(pietanza_model, required=True),required=True)
}, strict = True)

dieta_giornaliera = nutrizionista_ns.model('diete_giornaliere', {
    'giorno': fields.String(required=True),
    'colazione': fields.Nested(pasto_model, required=True),
    'spuntino_1': fields.Nested(pasto_model, required=True),
    'pranzo': fields.Nested(pasto_model, required=True),
    'spuntino_2': fields.Nested(pasto_model, required=True),
    'cena': fields.Nested(pasto_model, required=True)
}, strict = True)

put_piano_giornaliero_request_model = nutrizionista_ns.model('get_dieta', {
     "id_paziente" : fields.String('id_paziente', required=True),
     "piano_giornaliero" : fields.Nested(dieta_giornaliera, required=True)
}, strict = True)

dieta_request_model = nutrizionista_ns.model('dieta model for get delete and post', {
     "id_paziente" : fields.String('id_paziente', required=True)
}, strict = True)


class DietaController(Resource):
    #da provare
    @nutrizionista_required()
    @nutrizionista_ns.doc("ricevi la dieta del paziente", params={'id_paziente': 'PAZ1234'})
    def get(self):
        request_args = request.args
        email_nutrizionista = get_jwt_identity()

        if "id_paziente" not in request_args:
            return {"error": "Il campo id_paziente è obbligatorio."}, 400

        return DietaService.get_dieta_paziente(request_args['id_paziente'], email_nutrizionista)
    
    #da provare
    @nutrizionista_required()
    @nutrizionista_ns.expect(put_piano_giornaliero_request_model)
    @nutrizionista_ns.doc('modifica dieta giornaliera')
    def put(self):
        request_json = request.get_json()
        email_nutrizionista = get_jwt_identity()
        return DietaService.modifica_piano_giornaliero(request_json, email_nutrizionista)
    
    #da provare
    @nutrizionista_required()
    @nutrizionista_ns.expect(dieta_request_model)
    @nutrizionista_ns.doc("elimina la dieta del paziente")
    def delete(self):
        request_json = request.get_json()
        email_nutrizionista = get_jwt_identity()
        return DietaService.elimina_dieta(request_json, email_nutrizionista)
    

    #da provare
    @nutrizionista_required()
    @nutrizionista_ns.expect(dieta_request_model)
    @nutrizionista_ns.doc('crea una dieta per il paziente')
    def post(self):
        request_json = request.get_json()
        email_nutrizionista = get_jwt_identity()
        return DietaService.crea_dieta(request_json, email_nutrizionista)
    

class DietaPazienteController(Resource):
    
    #da provare
    @paziente_required()
    @paziente_ns.doc("ricevi la dieta del paziente")
    def get(self):
        identity = get_jwt_identity()
        return  DietaService.ricevi_dieta(identity)
