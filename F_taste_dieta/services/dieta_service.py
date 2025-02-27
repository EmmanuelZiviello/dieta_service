from F_taste_dieta.db import get_session
from F_taste_dieta.repositories.paziente_repository import PazienteRepository
from F_taste_dieta.repositories.nutrizionista_repository import NutrizionistaRepository
from F_taste_dieta.repositories.dieta_repository import DietaRepository
from F_taste_dieta.utils.dieta_utils import check_existing_dieta,get_dieta,create_piano_giornaliero,get_giorni,delete_dieta,create_dieta
from F_taste_dieta.utils.management_utils import check_nutrizionista


class DietaService:
    @staticmethod
    def get_dieta_paziente(id_paziente, email_nutrizionista):
        session = get_session('dietitian')

        paziente = PazienteRepository.find_by_id(id_paziente, session)
        if paziente is None:
            session.close()
            return {'message': 'paziente non presente nel db'}, 404
        
        nutrizionista = NutrizionistaRepository.find_by_email(email_nutrizionista, session)
        if nutrizionista is None:
            session.close()
            return {'message': 'nutrizionista non presente nel db'}, 404

        if check_nutrizionista(paziente, nutrizionista):
            if check_existing_dieta(paziente.id_paziente, session):
                dieta = get_dieta(paziente.id_paziente, session)
                session.close()
                return dieta, 200 
            else:
                session.close()
                return {'message': 'il paziente non ha la dieta'}, 404
        else:
            session.close()
            return {'message': 'paziente non seguito'}, 403
        



    @staticmethod
    def modifica_piano_giornaliero(request_json, email_nutrizionista):
        session = get_session('dietitian')

        paziente = PazienteRepository.find_by_id(request_json['id_paziente'], session)
        if paziente is None:
            session.close()
            return {'message': 'id paziente non presente nel db'}, 404

        nutrizionista = NutrizionistaRepository.find_by_email(email_nutrizionista, session)
        if nutrizionista is None:
            session.close()
            return {'message': 'email nutrizionista non presente nel db'}, 404

        if check_nutrizionista(paziente, nutrizionista):
            if check_existing_dieta(paziente.id_paziente, session):
                dieta = DietaRepository.find_dieta_by_id_paziente(paziente.id_paziente, session)
                piano_giornaliero = request_json['piano_giornaliero']

                if piano_giornaliero['giorno'] not in get_giorni():
                    session.close()
                    return {'message': 'giorno della settimana non corretto'}, 400

                try:
                    create_piano_giornaliero(piano_giornaliero, dieta, session)
                except Exception as e:
                    session.close()
                    raise e

                session.close()
                return {'message': 'piano giornaliero aggiunto correttamente'}, 200
            else:
                session.close()
                return {'message': 'dieta non presente nel db'}, 404
        else:
            session.close()
            return {'message': 'paziente non seguito'}, 403
        


    
    @staticmethod
    def elimina_dieta(request_json, email_nutrizionista):
        session = get_session('dietitian')

        paziente = PazienteRepository.find_by_id(request_json['id_paziente'], session)
        if paziente is None:
            session.close()
            return {'message': 'id paziente non presente nel db'}, 404

        nutrizionista = NutrizionistaRepository.find_by_email(email_nutrizionista, session)
        if nutrizionista is None:
            session.close()
            return {'message': 'email nutrizionista non presente nel db'}, 404

        if check_nutrizionista(paziente, nutrizionista):
            if check_existing_dieta(paziente.id_paziente, session):
                if delete_dieta(paziente.id_paziente, session):
                    session.commit()
                    session.close()
                    return {'message': 'dieta eliminata con successo'}, 200
                else:
                    session.close()
                    return {'message':'dieta non presente'},400
            else:
                session.close()
                return {'message': 'il paziente non ha la dieta'}, 404
        else:
            session.close()
            return {'message': 'paziente non seguito'}, 403
        


    @staticmethod
    def crea_dieta(request_json, email_nutrizionista):
        session = get_session('dietitian')

        # Verifica paziente
        paziente = PazienteRepository.find_by_id(request_json['id_paziente'], session)
        if paziente is None:
            session.close()
            return {'message': 'id paziente non presente nel db'}, 404

        # Verifica nutrizionista
        nutrizionista = NutrizionistaRepository.find_by_email(email_nutrizionista, session)
        if nutrizionista is None:
            session.close()
            return {'message': 'email nutrizionista non presente nel db'}, 404

        # Controllo se il nutrizionista segue il paziente
        if not check_nutrizionista(paziente, nutrizionista):
            session.close()
            return {'message': 'non segui questo paziente'}, 403

        # Controllo se il paziente ha già una dieta
        if check_existing_dieta(paziente.id_paziente, session):
            session.close()
            return {'message': 'il paziente ha gia la dieta'}, 409

        # Creazione della dieta
        dieta = create_dieta(paziente,session)
        if dieta is None:
            session.close()
            return {'message':"errore creazione dieta"},400
        session.close()

        return {'message': 'dieta creata con successo'}, 201
    

    @staticmethod
    def ricevi_dieta(identity):
        session = get_session('patient')

        # Verifica paziente
        paziente = PazienteRepository.find_by_id(identity, session)
        if paziente is None:
            session.close()
            return {'message': 'id paziente non presente nel db'}, 404

        # Verifica se esiste una dieta
        if check_existing_dieta(paziente.id_paziente, session):
            dieta = get_dieta(paziente.id_paziente, session)
            session.close()
            return dieta, 200
        else:
            session.close()
            return {}, 204