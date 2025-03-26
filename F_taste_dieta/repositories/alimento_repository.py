from F_taste_dieta.models.alimento import AlimentoModel
from F_taste_dieta.db import get_session


class AlimentoRepository:
    
    @staticmethod
    def get_alimento_by_id(id_alimento, session=None):
        session=session or get_session('dietitian') 
        result = session.query(AlimentoModel).filter(AlimentoModel.codice_alimento == id_alimento).one()
        return result
    
    @staticmethod
    def get_alimento_by_name(nome, session=None):
        session=session or get_session('dietitian')
        result = session.query(AlimentoModel).filter(AlimentoModel.nome_alimento == nome).one()
        return result

    @staticmethod
    def get_all_alimenti(session=None):
        session=session or get_session('dietitian')
        result = session.query(AlimentoModel).all()
        return result
