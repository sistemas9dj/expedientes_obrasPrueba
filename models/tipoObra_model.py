from sqlmodel import SQLModel, Field

class TipoObraModel(SQLModel, table=True):
    __tablename__ = "TipoObra"
    
    idTipoObra: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, nullable=False)
    descripcion: str | None = Field(default=None, nullable=True)