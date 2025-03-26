from F_taste_dieta.models.paziente import PazienteModel
from F_taste_dieta.models.nutrizionista import NutrizionistaModel

def check_nutrizionista(paziente : PazienteModel, nutrizionista : NutrizionistaModel):
    if paziente.id_nutrizionista == nutrizionista.id_nutrizionista:
        return True
    return False
