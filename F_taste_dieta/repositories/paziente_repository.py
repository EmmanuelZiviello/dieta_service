from F_taste_dieta.db import get_session
from F_taste_dieta.models.paziente import PazienteModel
from sqlalchemy.exc import SQLAlchemyError

class PazienteRepository:

    @staticmethod
    def find_by_email(email, session=None):
        session = session or get_session('dietitian')
        return session.query(PazienteModel).filter_by(email=email).first()

    @staticmethod
    def find_by_id(id_paziente, session=None):
        session = session or get_session('dietitian')
        return session.query(PazienteModel).filter_by(id_paziente=id_paziente).first()

    @staticmethod
    def add(paziente, session=None):
        session = session or get_session('dietitian')
        session.add(paziente)
        session.commit()

    @staticmethod
    def delete(paziente, session=None):
        session = session or get_session('dietitian')
        session.delete(paziente)
        session.commit()


    