from F_taste_dieta.db import get_session
from F_taste_dieta.repositories.paziente_repository import PazienteRepository
from F_taste_dieta.repositories.nutrizionista_repository import NutrizionistaRepository
from F_taste_dieta.repositories.dieta_repository import DietaRepository
from F_taste_dieta.utils.dieta_utils import check_existing_dieta,get_dieta,create_piano_giornaliero,get_giorni,delete_dieta,create_dieta
from F_taste_dieta.utils.management_utils import check_nutrizionista
from F_taste_dieta.utils.kafka_helpers import wait_for_kafka_response
from F_taste_dieta.kafka.kafka_producer import send_kafka_message


class DietaService:
    @staticmethod
    def get_dieta_paziente(id_paziente, email_nutrizionista):
        #invia tramite kafka per capire se è presente il paziente nel db e riceve status e id_nutrizionista
        message={"id_paziente":id_paziente}
        send_kafka_message("patient.existGet.request",message)
        response_paziente=wait_for_kafka_response(["patient.existGet.success", "patient.existGet.failed"])
        #controlli su response_paziente
        if response_paziente is None:
            return {"message": "Errore nella comunicazione con Kafka"}, 500
        
        if response_paziente.get("status_code") == "200":
            paziente_id_nutrizionista=response_paziente["id_nutrizionista"]
            if paziente_id_nutrizionista:
                #invia tramite kafka per capire se è presente il nutrizionista nel db e riceve il suo id
                message={"email_nutrizionista":email_nutrizionista}
                send_kafka_message("dietitian.existGet.request",message)
                response_nutrizionista=wait_for_kafka_response(["dietitian.existGet.success", "dietitian.existGet.failed"])
                #controlli su response_nutrizionista
                if response_nutrizionista is None:
                    return {"message": "Errore nella comunicazione con Kafka"}, 500
                
                if response_nutrizionista.get("status_code") == "200":
                    id_nutrizionista=response_nutrizionista["id_nutrizionista"]

                    if id_nutrizionista:
                    #   
                        if paziente_id_nutrizionista == id_nutrizionista:
                                session = get_session('dietitian')
                                if check_existing_dieta(id_paziente, session):
                                    dieta = get_dieta(id_paziente, session)
                                    session.close()
                                    return dieta, 200 
                                else:
                                    session.close()
                                    return {'message': 'il paziente non ha la dieta'}, 404
                        else:
                            return {'message': 'paziente non seguito'}, 403
                        
                    else:
                        return{"message":"Id nutrizionista mancante"}, 400
                    #
                elif response_nutrizionista.get("status_code") == "400":
                    return {"esito get_dieta_paziente":"Dati mancanti"}, 400
                elif response_nutrizionista.get("status_code") == "404":
                    return {"esito get_dieta_paziente":"Nutrizionista non presente nel db"}, 404
            
            return{"message":"Il paziente non è seguito da un nutrizionista"}, 403

            
        elif response_paziente.get("status_code") == "400":
            return {"esito get_dieta_paziente":"Dati mancanti"}, 400
        elif response_paziente.get("status_code") == "404":
            return {"esito get_dieta_paziente":"Paziente non presente nel db"}, 404

        

        
        
        

    @staticmethod
    def modifica_piano_giornaliero(s_paziente,email_nutrizionista):
        id_paziente=s_paziente["id_paziente"]
        #invia tramite kafka per capire se è presente il paziente nel db e riceve status e id_nutrizionista
        message={"id_paziente":id_paziente}
        send_kafka_message("patient.existGet.request",message)
        response_paziente=wait_for_kafka_response(["patient.existGet.success", "patient.existGet.failed"])
        #controlli su response_paziente
        if response_paziente is None:
            return {"message": "Errore nella comunicazione con Kafka"}, 500
        
        if response_paziente.get("status_code") == "200":
            paziente_id_nutrizionista=response_paziente["id_nutrizionista"]
            if paziente_id_nutrizionista:
                #invia tramite kafka per capire se è presente il nutrizionista nel db e riceve il suo id
                message={"email_nutrizionista":email_nutrizionista}
                send_kafka_message("dietitian.existGet.request",message)
                response_nutrizionista=wait_for_kafka_response(["dietitian.existGet.success", "dietitian.existGet.failed"])
                #controlli su response_nutrizionista
                if response_nutrizionista is None:
                    return {"message": "Errore nella comunicazione con Kafka"}, 500
                
                if response_nutrizionista.get("status_code") == "200":
                    id_nutrizionista=response_nutrizionista["id_nutrizionista"]

                    if id_nutrizionista:
                    #   
                        if paziente_id_nutrizionista == id_nutrizionista:
                                session = get_session('dietitian')
                                if check_existing_dieta(id_paziente, session):
                                    dieta=DietaRepository.find_dieta_by_id_paziente(id_paziente,session)
                                    piano_giornaliero=s_paziente["piano_giornaliero"]
                                    if piano_giornaliero["giorno"] not in get_giorni():
                                        session.close()
                                        return {'message': 'giorno della settimana non corretto'}, 400
                                    try:
                                        create_piano_giornaliero(piano_giornaliero,dieta,session)
                                    except Exception as e:
                                        session.close()
                                        raise e
                                    session.close()
                                    return {'message' : 'piano giornaliero aggiunto correttamente'}, 200

                                else:
                                    session.close()
                                    return {'message': 'il paziente non ha la dieta'}, 404
                        else:
                            return {'message': 'paziente non seguito'}, 403
                        
                    else:
                        return{"message":"Id nutrizionista mancante"}, 400
                    #
                elif response_nutrizionista.get("status_code") == "400":
                    return {"esito get_dieta_paziente":"Dati mancanti"}, 400
                elif response_nutrizionista.get("status_code") == "404":
                    return {"esito get_dieta_paziente":"Nutrizionista non presente nel db"}, 404
            
            return{"message":"Il paziente non è seguito da un nutrizionista"}, 403

            
        elif response_paziente.get("status_code") == "400":
            return {"esito get_dieta_paziente":"Dati mancanti"}, 400
        elif response_paziente.get("status_code") == "404":
            return {"esito get_dieta_paziente":"Paziente non presente nel db"}, 404

    '''
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
        '''

    @staticmethod
    def elimina_dieta(s_paziente,email_nutrizionista):
        id_paziente=s_paziente["id_paziente"]
         #invia tramite kafka per capire se è presente il paziente nel db e riceve status e id_nutrizionista
        message={"id_paziente":id_paziente}
        send_kafka_message("patient.existGet.request",message)
        response_paziente=wait_for_kafka_response(["patient.existGet.success", "patient.existGet.failed"])
        #controlli su response_paziente
        if response_paziente is None:
            return {"message": "Errore nella comunicazione con Kafka"}, 500
        
        if response_paziente.get("status_code") == "200":
            paziente_id_nutrizionista=response_paziente["id_nutrizionista"]
            if paziente_id_nutrizionista:
                #invia tramite kafka per capire se è presente il nutrizionista nel db e riceve il suo id
                message={"email_nutrizionista":email_nutrizionista}
                send_kafka_message("dietitian.existGet.request",message)
                response_nutrizionista=wait_for_kafka_response(["dietitian.existGet.success", "dietitian.existGet.failed"])
                #controlli su response_nutrizionista
                if response_nutrizionista is None:
                    return {"message": "Errore nella comunicazione con Kafka"}, 500
                
                if response_nutrizionista.get("status_code") == "200":
                    id_nutrizionista=response_nutrizionista["id_nutrizionista"]

                    if id_nutrizionista:
                    #   
                        if paziente_id_nutrizionista == id_nutrizionista:
                                session = get_session('dietitian')
                                if check_existing_dieta(id_paziente, session):
                                    if delete_dieta(id_paziente, session):
                                        session.close()
                                        return {'message' : 'Dieta eliminata con successo'}, 200 
                                    else:
                                        return {"message":"Errore eliminazione dieta"}, 400
                                else:
                                    session.close()
                                    return {'message': 'il paziente non ha la dieta'}, 404
                        else:
                            return {'message': 'paziente non seguito'}, 403
                        
                    else:
                        return{"message":"Id nutrizionista mancante"}, 400
                    #
                elif response_nutrizionista.get("status_code") == "400":
                    return {"esito get_dieta_paziente":"Dati mancanti"}, 400
                elif response_nutrizionista.get("status_code") == "404":
                    return {"esito get_dieta_paziente":"Nutrizionista non presente nel db"}, 404
            
            return{"message":"Il paziente non è seguito da un nutrizionista"}, 403

            
        elif response_paziente.get("status_code") == "400":
            return {"esito get_dieta_paziente":"Dati mancanti"}, 400
        elif response_paziente.get("status_code") == "404":
            return {"esito get_dieta_paziente":"Paziente non presente nel db"}, 404
        
    
    '''
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
        '''
        

    @staticmethod
    def crea_dieta(s_paziente,email_nutrizionista):
        id_paziente=s_paziente["id_paziente"]
        #invia tramite kafka per capire se è presente il paziente nel db e riceve status e id_nutrizionista
        message={"id_paziente":id_paziente}
        send_kafka_message("patient.existGet.request",message)
        response_paziente=wait_for_kafka_response(["patient.existGet.success", "patient.existGet.failed"])
        #controlli su response_paziente
        if response_paziente is None:
            return {"message": "Errore nella comunicazione con Kafka"}, 500
        
        if response_paziente.get("status_code") == "200":
            paziente_id_nutrizionista=response_paziente["id_nutrizionista"]
            if paziente_id_nutrizionista:
                #invia tramite kafka per capire se è presente il nutrizionista nel db e riceve il suo id
                message={"email_nutrizionista":email_nutrizionista}
                send_kafka_message("dietitian.existGet.request",message)
                response_nutrizionista=wait_for_kafka_response(["dietitian.existGet.success", "dietitian.existGet.failed"])
                #controlli su response_nutrizionista
                if response_nutrizionista is None:
                    return {"message": "Errore nella comunicazione con Kafka"}, 500
                
                if response_nutrizionista.get("status_code") == "200":
                    id_nutrizionista=response_nutrizionista["id_nutrizionista"]

                    if id_nutrizionista:
                    #   
                        if paziente_id_nutrizionista == id_nutrizionista:
                                session = get_session('dietitian')
                                if not check_existing_dieta(id_paziente, session):
                                    create_dieta(id_paziente, session)
                                    session.close()
                                    return {'message' : 'dieta creata con successo'}, 201 
                                else:
                                    session.close()
                                    return {'message': 'il paziente ha già la dieta'}, 404
                        else:
                            return {'message': 'paziente non seguito'}, 403
                        
                    else:
                        return{"message":"Id nutrizionista mancante"}, 400
                    #
                elif response_nutrizionista.get("status_code") == "400":
                    return {"esito get_dieta_paziente":"Dati mancanti"}, 400
                elif response_nutrizionista.get("status_code") == "404":
                    return {"esito get_dieta_paziente":"Nutrizionista non presente nel db"}, 404
            
            return{"message":"Il paziente non è seguito da un nutrizionista"}, 403

            
        elif response_paziente.get("status_code") == "400":
            return {"esito get_dieta_paziente":"Dati mancanti"}, 400
        elif response_paziente.get("status_code") == "404":
            return {"esito get_dieta_paziente":"Paziente non presente nel db"}, 404

    '''
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
    '''

    @staticmethod
    def ricevi_dieta(id_paziente):
        session = get_session('patient')

        # Verifica paziente
        #(credo la verifica paziente non sia necessaria banalmente perchè si cerca la dieta
        #tramite l'id nel jwt,inoltre la verifica del paziente esistente viene fatta prima di creare la dieta stessa)
        

        # Verifica se esiste una dieta
        if check_existing_dieta(id_paziente, session):
            dieta = get_dieta(id_paziente, session)
            session.close()
            return dieta, 200
        else:
            session.close()
            return {}, 204