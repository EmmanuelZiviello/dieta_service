# from flaskr import db
from F_taste_dieta.ma import ma
from F_taste_dieta.models.dieta import DietaModel

class DietaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DietaModel
        load_instance = True
        include_relationships = True