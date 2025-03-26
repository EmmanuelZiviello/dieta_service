# from flaskr import db
from F_taste_dieta.ma import ma
from F_taste_dieta.models.dieta import DietaModel
from marshmallow import fields

class DietaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DietaModel
        load_instance = True
    #non sicuro,vedere i controller cosa richiedono
    id_paziente = fields.String(required=True)  # Ora è solo un campo stringa ed è richiesto anche nello schema
        