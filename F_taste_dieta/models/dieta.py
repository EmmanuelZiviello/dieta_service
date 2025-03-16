from datetime import datetime
from F_taste_dieta.db import Base
from F_taste_dieta.models.pasto import PastoModel
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint, TIMESTAMP
from sqlalchemy.orm import relationship

class DietaModel(Base):
    __tablename__ = "dieta"

    id_dieta = Column(Integer, primary_key=True)
    data = Column(TIMESTAMP)
    id_paziente = Column(String(7), nullable=False, unique=True)  # Eliminata la ForeignKey
    pasti_dieta = relationship("PastoModel", back_populates = 'dieta', lazy=True, cascade='delete')

    def __init__(self, id_paziente, data = datetime.now()):
        self.id_paziente = id_paziente
        self.data = data
        
    def __repr__(self):
        return 'DietaModel(id_paziente=%s, data=%s, id_dieta=%s)' % (self.id_paziente, self.data, self.id_dieta)

    def __json__(self):
        return { 'id_paziente': self.id_paziente, 'data': self.data, 'id_dieta': self.id_dieta }

