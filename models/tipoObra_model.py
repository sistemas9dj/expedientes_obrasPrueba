from sqlmodel import SQLModel, Field, Relationship
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.expediente_tipoObra_model import Expediente_TipoObraModel

class TipoObraModel(SQLModel, table=True):
    __tablename__ = "TipoObra"
    
    idTipoObra: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, nullable=False)
    descripcion: str | None = Field(default=None, nullable=True)

     #relacion N a N
    expedientes: List["Expediente_TipoObraModel"] = Relationship(back_populates="tipos")