#Relacion N a N entre Expedeinte y Esatdo Expediente. 
#Esta relacion Guarda los distintos estados por los que pasa el Expediente y registra las fecha
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, func
from datetime import datetime
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from models.expediente_model import ExpedienteModel
    from models.estadoExpediente_model import EstadoExpedienteModel
    from models.usuario_model import UsuarioModel

class Expediente_EstadoExpedienteModel(SQLModel, table=True):
    __tablename__ = "Expediente_EstadoExpediente"
    
    idRelacion: int | None = Field(default=None, primary_key=True)
   
    idExpediente: int = Field(foreign_key="Expediente.idExpediente", nullable=False)
    idEstadoExpediente: int = Field(foreign_key="EstadoExpediente.idEstadoExpediente", nullable=False)
    idUsuario: int = Field(foreign_key="Usuario.idUsuario", nullable=False)

    fechaCambioEstado: datetime = Field(
        sa_column=Column(DateTime, server_default=func.now())
    )

    observaciones: str | None = Field(default=None, nullable=True)

    # Relaciones con back_populates. Relacion N a N
    # Forward references (clases referenciadas como string)
    expediente: Optional["ExpedienteModel"] = Relationship(back_populates="estados")
    estado: Optional["EstadoExpedienteModel"] = Relationship(back_populates="expedientes")
    usuario: Optional["UsuarioModel"] = Relationship(back_populates="cambios_estado")


    