from typing import List
from sqlmodel import SQLModel, Field

class TipoProfesionModel(SQLModel, table=True):
    __tablename__ = "TipoProfesion"
    
    idTipoProfesion: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, nullable=False)
    descripcion: str | None = Field(default=None, nullable=True)

    