#Relacion N a N entre Expedeinte y Esatdo Expediente. 
#Esta relacion Guarda los distintos estados por los que pasa el Expediente y registra las fecha
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, func
from datetime import datetime
from typing import Optional, TYPE_CHECKING


#if TYPE_CHECKING:
#   from models.expediente_model import ExpedienteModel
#   from models.propietario_model import PropietarioModel

class Expediente_PropietarioModel(SQLModel, table=True):
    __tablename__ = "Expediente_Propietario"
    
    idExpediente: int = Field(foreign_key="Expediente.idExpediente", primary_key=True)
    idPropietario: int = Field(foreign_key="Propietario.idPropietario", primary_key=True)
    figuraPpal: int | None = Field(default=1, nullable=True) 

    fechaCambioPropietario: datetime = Field(
        sa_column=Column(DateTime, server_default=func.now())
    )



    # Relaciones con back_populates. Relacion N a N
    # Forward references (clases referenciadas como string)
#    expediente: Optional["ExpedienteModel"] = Relationship(back_populates="propietario")
#    propietario: Optional["PropietarioModel"] = Relationship(back_populates="expediente")
    
# Resolver forward references
#Expediente_PropietarioModel.update_forward_refs()   


