from F_taste_dieta.repositories.dieta_repository import DietaRepository
from F_taste_dieta.repositories.pasto_repository import PastoRepository
from F_taste_dieta.repositories.alimento_repository import AlimentoRepository
from F_taste_dieta.models.dieta import DietaModel
from F_taste_dieta.models.paziente import PazienteModel
from F_taste_dieta.schemas.pasto import PastoSchema
from F_taste_dieta.schemas.pietanza import PietanzaSchema
from sqlalchemy.orm import scoped_session

def get_giorni():
    return ['lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato', 'domenica']

def get_restructured_pietanza(pietanza):
    pietanza['nome_alimento'] = pietanza['alimento']['nome_alimento']
    del pietanza['alimento']
    return pietanza

def get_meals_of_the_day(giorno, id_dieta, session):
    pasti = PastoSchema(many=True, exclude=['giorno', 'id_pasto']).dump(
        PastoRepository.get_pasti_del_giorno(id_dieta, giorno, session)
    )
    
    piano_giornaliero = {'giorno': giorno}
    
    for pasto in pasti:
        tipo_pasto = pasto.pop('tipo_pasto')
        piano_giornaliero[tipo_pasto] = pasto
        for pietanza in pasto['pietanze']:
            pietanza = get_restructured_pietanza(pietanza)
    
    return piano_giornaliero

def get_dieta(id_paziente, session: scoped_session):
    response = DietaRepository.find_dieta_by_id_paziente(id_paziente, session)
    if not response:
        return None
    
    dieta = {'data': str(response.data), 'diete_giornaliere': []}
    
    for giorno in get_giorni():
        dieta['diete_giornaliere'].append(get_meals_of_the_day(giorno, response.id_dieta, session))
    
    return dieta

def create_dieta(paziente: "PazienteModel", session) -> "DietaModel":
    dieta = DietaModel(paziente.id_paziente)
    dieta.paziente = paziente
    DietaRepository.add_dieta(dieta, session)  # Usa il repository per gestire l'inserimento
    return dieta

def get_names_of_meals():
    return ['colazione' , 'spuntino_1', 'pranzo', 'spuntino_2', 'cena']

def delete_dieta(id_paziente, session):
    dieta = DietaRepository.find_dieta_by_id_paziente(id_paziente, session)
    return DietaRepository.delete_dieta(dieta, session)

def create_piano_giornaliero(piano_giornaliero, dieta, session):
    pasti = []
    pasti_del_giorno = get_names_of_meals()

    # Elimina i pasti precedenti di quel giorno per evitare duplicati
    delete_previous_pasti(piano_giornaliero['giorno'], dieta.id_dieta, session)

    for tipo_pasto in pasti_del_giorno:
        if tipo_pasto in piano_giornaliero and len(piano_giornaliero[tipo_pasto]) > 0:
            pasto = create_pasto(piano_giornaliero['giorno'], piano_giornaliero[tipo_pasto], tipo_pasto, dieta, session)
            pasti.append(pasto)

    # Aggiunge i nuovi pasti e le pietanze associate
    session.add_all(pasti)
    for pasto in pasti:
        session.add_all(pasto.pietanze)

    session.commit()

def create_pasto(giorno, pasto_s, tipo_pasto, dieta, session):
   
    pasto = PastoRepository.create_pasto(giorno, pasto_s['nota'], tipo_pasto, dieta, session)
    
    for pietanza_s in pasto_s['pietanze']:
        pietanza = create_pietanza(pietanza_s, session)
        pasto.pietanze.append(pietanza)
    
    return pasto

def create_pietanza(pietanza_s, session):
    nome_alimento = pietanza_s.pop('nome_alimento')  # Estrae e rimuove la chiave dal dizionario
    pietanza = PietanzaSchema(only=['unita_misura', 'quantita']).load(pietanza_s, session=session)

    alimento = AlimentoRepository.get_alimento_by_name(nome_alimento, session)
    pietanza.alimento = alimento
    
    return pietanza

def delete_previous_pasti(giorno, id_dieta, session):
    pasti = PastoRepository.get_pasti_del_giorno(id_dieta, giorno, session)
    PastoRepository.delete_pasti(pasti, session)

def check_existing_dieta(id_paziente, session):
    return DietaRepository.find_dieta_by_id_paziente(id_paziente, session) is not None



def whats_in_there():
    breakpoint()