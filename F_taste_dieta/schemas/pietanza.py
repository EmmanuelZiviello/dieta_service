from marshmallow import ValidationError, fields, validates

# from flaskr import db
from F_taste_dieta.ma import ma
from F_taste_dieta.models.pietanza import PietanzaModel
from F_taste_dieta.schemas.alimento import AlimentoSchema

class PietanzaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PietanzaModel
        load_instance = True
        
    unita_misura = fields.String()
    alimento = fields.Nested(AlimentoSchema, many = False, only=['nome_alimento'], dump_only = True)

    @validates('unita_misura')
    def is_a_correct_unita_misura(self, value):
        
        if value not in ['unita', 'gr', 'porzione', 'ml', 'cl', 'tazza']:
            raise ValidationError("unita di misura non valida")