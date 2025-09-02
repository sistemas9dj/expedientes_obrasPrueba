from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, func
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from models.tipoObra_model import TipoObraModel

if TYPE_CHECKING:
     from models.expediente_estadoExpediente_model import Expediente_EstadoExpedienteModel
     from models.expediente_profesional_model import Expediente_ProfesionalModel
#    from models.expediente_propietario_model import Expediente_PropietarioModel
     
class ExpedienteModel(SQLModel, table=True):
    __tablename__ = "Expediente"
    
    idExpediente: int | None = Field(default=None, primary_key=True)
    #El nro de expediente se forma con el nroEntrada + el anioMesa de Entrada
    nroEntrada: int # 3 digitos, se reinicia con cada año 
    anioMesaEntrada: int 
    nroExpedienteMesaEntrada: str | None = Field(default=None, nullable=True)
    nroPartida: str | None = Field(default=None, nullable=True)
    sucesion: int | None = Field(default=None, nullable=True)
    observaciones: str | None = Field(default=None, nullable=True)

    #fechaIngresoSistema: datetime | None = Field(default= None, nullable=True)
    fechaIngresoSistema: datetime = Field(
        sa_column=Column(DateTime, server_default=func.now())
    )
    fechaUltimaMod: datetime = Field(
        sa_column=Column(DateTime, server_default=func.now(), onupdate=func.now())
    )
   
    idTipoObra: int | None = Field(default=None, foreign_key="TipoObra.idTipoObra")

    # Relación con TipoObra 1 a n
    tipoObra: Optional[TipoObraModel] = Relationship()

    # Relación N a N (tabla intermedia Expediente_EstadoExpediente)
    estados: List["Expediente_EstadoExpedienteModel"] = Relationship(back_populates="expediente")
    # Relación N a N (tabla intermedia Expediente_Profesional)
    profesionales: List["Expediente_ProfesionalModel"] = Relationship(back_populates="expediente")
    
    # Relación N a N (tabla intermedia Expediente_Propietario)
    #propietarios: List["Expediente_PropietarioModel"] = Relationship(back_populates="expediente")
     
# Resolver forward references
#ExpedienteModel.update_forward_refs()   