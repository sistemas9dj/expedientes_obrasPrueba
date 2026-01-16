from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, func
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models.expediente_estadoExpediente_model import Expediente_EstadoExpedienteModel


class UsuarioModel(SQLModel, table=True):
    __tablename__ = "Usuario"
    
    idUsuario: int | None = Field(default=None, primary_key=True)
    usuario: str = Field(index=True, nullable=False)
    clave: str = Field(default=None, nullable=False)
    activo: int = Field(default=1, nullable=False)
    idRol: int = Field(default=1, nullable=False) # por el momento este valor no se usa, todos los usuarios hacen todo
    fechaUltimoLogin: datetime = Field(sa_column=Column(DateTime, server_default=func.now(), onupdate=func.now()))

    # RELACIÓN
    cambios_estado: List["Expediente_EstadoExpedienteModel"] = Relationship(back_populates="usuario")