from sqlmodel import SQLModel, Field, Relationship
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.expediente_estadoExpediente_model import Expediente_EstadoExpedienteModel

class EstadoExpedienteModel(SQLModel, table=True):
    __tablename__ = "EstadoExpediente"
    
    idEstadoExpediente: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, nullable=False)
    descripcion: str | None = Field(default=None, nullable=True)

    #relacion N a N
    expedientes: List["Expediente_EstadoExpedienteModel"] = Relationship(back_populates="estado")

  