from F_taste_dieta.repositories.alimento_repository import AlimentoRepository
from F_taste_dieta.schemas.alimento import AlimentoSchema
from F_taste_dieta.models.alimento import AlimentoModel
from F_taste_dieta.db import get_session

alimenti_schema = AlimentoSchema(many=True, only=['nome_alimento', 'codice_alimento'])

class AlimentoService:
    @staticmethod
    def get_all_alimenti():
        session=get_session('dietitian')
        alimenti = AlimentoRepository.get_all_alimenti(session)
        output_richiesta=alimenti_schema.dump(alimenti)
        session.close()
        return output_richiesta, 200
    
    @staticmethod
    def add(s_alimento):
        session=get_session('dietitian')
        codice=s_alimento.get("codice_alimento")
        nome=s_alimento.get("nome_alimento")
        alimento=AlimentoModel(codice,nome)
        AlimentoRepository.add(alimento,session)
        session.close()
        return {"esito add_alimento":"Alimento aggiunto con successo"}
