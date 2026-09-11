from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Maquina(Base):
    __tablename__ = "maquinas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)           # Ex: "Escavadeira CAT 320"
    tipo = Column(String(50), nullable=False)             # Ex: "Escavadeira", "Retro", "Patrol"
    placa_serie = Column(String(50), unique=True)         # Placa ou número de série
    ano = Column(Integer)
    horimetro = Column(Float, default=0)                  # Horímetro atual
    status = Column(String(20), default="Ativa")          # Ativa / Em manutenção / Inativa
    criado_em = Column(DateTime, default=datetime.utcnow)

    manutencoes = relationship("Manutencao", back_populates="maquina")


class Mecanico(Base):
    __tablename__ = "mecanicos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(20))
    especialidade = Column(String(100))                   # Ex: "Motor", "Hidráulica"
    criado_em = Column(DateTime, default=datetime.utcnow)

    manutencoes = relationship("Manutencao", back_populates="mecanico")


class Manutencao(Base):
    __tablename__ = "manutencoes"

    id = Column(Integer, primary_key=True, index=True)
    maquina_id = Column(Integer, ForeignKey("maquinas.id"), nullable=False)
    mecanico_id = Column(Integer, ForeignKey("mecanicos.id"), nullable=False)
    data = Column(DateTime, default=datetime.utcnow)
    tipo_servico = Column(String(100))                    # Ex: "Preventiva", "Corretiva"
    descricao = Column(Text)                              # Descrição do serviço realizado
    horimetro_atual = Column(Float)
    custo_total = Column(Float, default=0)                # <--- ADICIONADO
    criado_em = Column(DateTime, default=datetime.utcnow)

    maquina = relationship("Maquina", back_populates="manutencoes")
    mecanico = relationship("Mecanico", back_populates="manutencoes")
    pecas = relationship("PecaUsada", back_populates="manutencao")


class PecaUsada(Base):
    __tablename__ = "pecas_usadas"

    id = Column(Integer, primary_key=True, index=True)
    manutencao_id = Column(Integer, ForeignKey("manutencoes.id"), nullable=False)
    nome = Column(String(150), nullable=False)            # Ex: "Filtro de óleo"
    quantidade = Column(Integer, default=1)
    valor_unitario = Column(Float, default=0)
    criado_em = Column(DateTime, default=datetime.utcnow)

    manutencao = relationship("Manutencao", back_populates="pecas")
