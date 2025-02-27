from F_taste_dieta.ma import ma
# from flaskr import db
from F_taste_dieta.models.alimento import AlimentoModel

class AlimentoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AlimentoModel
        load_instance = True
        include_fk = False

    