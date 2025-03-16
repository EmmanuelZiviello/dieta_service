from F_taste_dieta.repositories.alimento_repository import AlimentoRepository
from F_taste_dieta.schemas.alimento import AlimentoSchema
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
