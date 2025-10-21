#Relacion N a N entre Expedeinte y Esatdo Expediente. 
#Esta relacion Guarda los distintos estados por los que pasa el Expediente y registra las fecha
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, func
from datetime import datetime
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from models.expediente_model import ExpedienteModel
    from models.estadoExpediente_model import EstadoExpedienteModel

class Expediente_EstadoExpedienteModel(SQLModel, table=True):
    __tablename__ = "Expediente_EstadoExpediente"
    
    idExpediente: int = Field(foreign_key="Expediente.idExpediente", primary_key=True)
    idEstadoExpediente: int = Field(foreign_key="EstadoExpediente.idEstadoExpediente", primary_key=True)

    fechaCambioEstado: datetime = Field(
        sa_column=Column(DateTime, server_default=func.now())
    )

    # Relaciones con back_populates. Relacion N a N
    # Forward references (clases referenciadas como string)
    expediente: Optional["ExpedienteModel"] = Relationship(back_populates="estados")
    estado: Optional["EstadoExpedienteModel"] = Relationship(back_populates="expedientes")
    
   