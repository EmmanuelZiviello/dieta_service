from F_taste_dieta.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from F_taste_dieta.models.alimento import AlimentoModel

class PietanzaModel(Base):
    __tablename__ = "pietanza"

    id_pietanza = Column(Integer, primary_key=True)
    unita_misura = Column(String(45))
    quantita = Column(Integer)
    fk_pasto = Column(Integer, ForeignKey("pasto.id_pasto", onupdate="CASCADE", ondelete = "CASCADE"), nullable=False)
    fk_alimento = Column(Integer, ForeignKey("alimento.codice_alimento", onupdate="CASCADE", ondelete = "CASCADE"), nullable=False) # nullable = False/TRUE?
    pasto = relationship("PastoModel", back_populates = 'pietanze', lazy = True)
    alimento = relationship("AlimentoModel", back_populates = 'pietanze', lazy = True)

    def __init__(self, unita_misura, quantita):
        self.unita_misura = unita_misura
        self.quantita = quantita

    def __repr__(self):
        return "PietanzaModel(fk_alimento: %s , quantita: %s, unita_misura: %s, fk_pasto=%s)" % (self.fk_alimento, self.quantita,self.unita_misura, self.fk_pasto)

    def __json__(self):
        return {'fk_pasto': self.fk_pasto, 'fk_alimento': self.fk_alimento, 'quantita': self.quantita, 'unita_misura': self.unita_misura}
