from sqlmodel import SQLModel, Field
from typing import Optional

class Propietario(SQLModel, table=True):
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
    