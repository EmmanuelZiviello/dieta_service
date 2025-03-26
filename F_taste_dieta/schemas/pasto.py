from marshmallow import fields

# from flaskr import db
from F_taste_dieta.ma import ma
from F_taste_dieta.models.pasto import PastoModel
from F_taste_dieta.schemas.pietanza import PietanzaSchema


class PastoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PastoModel
        load_instance = True
        
        


    pietanze = fields.Nested(PietanzaSchema, many = True, dump_only = True, exclude = ['id_pietanza'])