from sqlmodel import SQLModel, Field, Relationship
#from typing import List, TYPE_CHECKING

#if TYPE_CHECKING:
#    from models.expediente_model import ExpedienteModel
#    from models.expediente_propietario_model import Expediente_PropietarioModel

class PropietarioModel(SQLModel, table=True):
    __tablename__ = "Propietario"
    
    idPropietario: int | None = Field(default=None, primary_key=True)
    cuil_cuit: str 
    nombre: str 
    apellido: str 
    calle: str | None = Field(default=None, nullable=True)
    nroCalle: int | None = Field(default=None, nullable=True) 
    nroDpto: str | None = Field(default=None, nullable=True)
    piso: str | None = Field(default=None, nullable=True)
    areaCelular: int | None = Field(default=None, nullable=True) 
    nroCelular: int | None = Field(default=None, nullable=True)
    email: str | None = Field(default=None, nullable=True)
    #figuraPpal: int | None = Field(default=1, nullable=True) 
    
    #Relacion N a N
    #expedientes: List["Expediente_PropietarioModel"] = Relationship(back_populates="propietario")

  # Relación N a N con Expedientes usando tabla intermedia
  #  expedientes: List["ExpedienteModel"] = Relationship(
  #      back_populates="propietarios",
  #      link_model=Expediente_PropietarioModel
  #  )
# Resolver forward references
#PropietarioModel.update_forward_refs()    

    #orm_mode = True,permite que FastAPI va a poder convertir automáticamente los objetos SQLAlchemy en JSON válido.
    class Config:
            orm_mode = True