from F_taste_dieta.db import Base
from F_taste_dieta.models.pietanza import PietanzaModel
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

class PastoModel(Base):
    __tablename__ = "pasto"

    id_pasto = Column(Integer, primary_key=True)
    tipo_pasto = Column(String(20))
    nota = Column(String(200))
    giorno = Column(String(15))
    fk_dieta = Column(Integer, ForeignKey("dieta.id_dieta", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    pietanze = relationship("PietanzaModel", back_populates='pasto', lazy=True, cascade='delete')
    dieta = relationship("DietaModel", back_populates='pasti_dieta', lazy=True)
    __table_args__ = (UniqueConstraint(fk_dieta, tipo_pasto, giorno, name='one_kind_of_meal_each_day'),)

    def __init__(self, giorno, nota, tipo_pasto, fk_dieta) -> "PastoModel":
        self.giorno = giorno
        self.nota = nota
        self.tipo_pasto = tipo_pasto
        self.fk_dieta = fk_dieta

    def __repr__(self):
        return "PastoModel(giorno:%s , tipo_pasto:%s , nota:%s)" % (self.giorno, self.tipo_pasto, self.nota)

    def __json__(self):
        return { 'giorno': self.giorno, 'tipo_pasto': self.tipo_pasto, 'fk_dieta': self.fk_dieta }
