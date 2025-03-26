from F_taste_dieta.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class AlimentoModel(Base):
    __tablename__ = "alimento"

    codice_alimento = Column(Integer, primary_key=True)
    nome_alimento = Column(String(600), unique=True, nullable=False)
    pietanze = relationship("PietanzaModel", back_populates = 'alimento', lazy = True, cascade='delete')

    def __repr__(self):
        return " nome: {0} codice :{1}".format(self.nome_alimento, self.codice_alimento)

    def __init__(self, codice_alimento, nome_alimento):
        self.codice_alimento = codice_alimento
        self.nome_alimento = nome_alimento

    def __repr__(self):
        return 'AlimentoModel(codice_alimento=%s, nome_alimento=%s)' % (self.codice_alimento, self.nome_alimento)

    def __json__(self):
        return { 'codice_alimento': self.codice_alimento, 'nome_alimento': self.nome_alimento }
