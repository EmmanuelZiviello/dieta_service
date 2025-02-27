from F_taste_dieta.models.pasto import PastoModel
from F_taste_dieta.db import get_session

class PastoRepository:
    

    @staticmethod
    def get_pasti_del_giorno(fk_dieta, giorno, session=None):
        session = session or get_session('dietitian')
        result = session.query(PastoModel).filter_by(fk_dieta=fk_dieta, giorno=giorno).all()
        return result

    @staticmethod
    def delete_pasti(pasti: list[PastoModel], session=None):
        for pasto in pasti:
            session.delete(pasto)
        session.commit()

    @staticmethod
    def create_pasto(giorno, nota, tipo_pasto, dieta, session=None):
        session=session or get_session('dietitian')
        pasto = PastoModel(giorno, nota, tipo_pasto, dieta.id_dieta)
        pasto.dieta = dieta
        session.add(pasto)
        return pasto