from datetime import datetime
from F_taste_dieta.db import Base
from F_taste_dieta.models.pasto import PastoModel
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint, TIMESTAMP
from sqlalchemy.orm import relationship

class DietaModel(Base):
    __tablename__ = "dieta"

    id_dieta = Column(Integer, primary_key=True)
    data = Column(TIMESTAMP)
    fk_paziente = Column(String(10),
                            ForeignKey("paziente.id_paziente", onupdate="CASCADE", ondelete="CASCADE"), 
                            nullable=False, 
                            unique = True)
    pasti_dieta = relationship("PastoModel", back_populates = 'dieta', lazy=True, cascade='delete')
    paziente = relationship("PazienteModel", back_populates='dieta_paziente', lazy=True)

    def __init__(self, fkpaziente, data = datetime.now()):
        self.fkpaziente = fkpaziente
        self.data = data
        
    def __repr__(self):
        return 'DietaModel(fk_paziente=%s, data=%s, id_dieta=%s)' % (self.fk_paziente, self.data, self.id_dieta)

    def __json__(self):
        return { 'fk_paziente': self.fk_paziente, 'data': self.data, 'id_dieta': self.id_dieta }

