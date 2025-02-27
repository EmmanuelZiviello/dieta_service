from F_taste_dieta.models.dieta import DietaModel
from F_taste_dieta.db import get_session

class DietaRepository:
    
    @staticmethod
    def find_dieta_by_id_paziente(id_paziente, session=None):
        session=session or get_session('dietitian')
        result = session.query(DietaModel).filter_by(fk_paziente=id_paziente).first()
        return result
    
    @staticmethod
    def get_pasti_dieta(dieta,session=None):
        session=session or get_session('dietitian')
        return dieta.pasti_dieta

    @staticmethod
    def delete_dieta(dieta, session=None) -> bool:
        session=session or get_session('dietitian')
        if dieta:
            session.delete(dieta)
            session.commit()
            return True
        return False
    

    @staticmethod
    def add_dieta(dieta: "DietaModel", session=None):
        session=session or get_session('dietitian')
        session.add(dieta)
        session.commit()