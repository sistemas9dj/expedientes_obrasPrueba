from sqlmodel import SQLModel, Field

class Profesional(SQLModel, table=True):
    __tablename__ = "Profesional"
    
    idProfesional: int | None = Field(default=None, primary_key=True)
    cuil_cuit: str 
    nombre: str 
    apellido: str 
    razonSocial: str | None = Field(default=None, nullable=True) 
    calle: str | None = Field(default=None, nullable=True)
    nroCalle: int | None = Field(default=None, nullable=True)
    nroDpto: str | None = Field(default=None, nullable=True)
    piso: str | None = Field(default=None, nullable=True)
    areaCelular: int | None = Field(default=None, nullable=True) 
    nroCelular: int | None = Field(default=None, nullable=True)
    matricula: str | None = Field(default=None, nullable=True)
    email: str | None = Field(default=None, nullable=True)