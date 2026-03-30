from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
    senha_hash = Column(String) 
    termos = relationship("TermoBusca", back_populates="dono")

class TermoBusca(Base):
    __tablename__ = "termos_busca"
    id = Column(Integer, primary_key=True, index=True)
    
    palavra_chave = Column(String) 
    ativo = Column(Boolean, default=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    dono = relationship("Usuario", back_populates="termos")
    vagas = relationship("Vaga", back_populates="termo_origem")

class Vaga(Base):
    __tablename__ = "vagas"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    link = Column(String, unique=True)
    data_descoberta = Column(DateTime, default=datetime.utcnow)
    notificado = Column(Boolean, default=False)
    termo_id = Column(Integer, ForeignKey("termos_busca.id"))
    termo_origem = relationship("TermoBusca", back_populates="vagas")