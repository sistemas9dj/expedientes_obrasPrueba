from sqlmodel import SQLModel, Field

class InspectorModel(SQLModel, table=True):
    __tablename__ = "Inspector"
    
    idInspector: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, nullable=False)
    apellido: str | None = Field(default=None, nullable=True)