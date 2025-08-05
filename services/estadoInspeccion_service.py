from sqlmodel import Session
from typing import List, Optional
from models.estadoInspeccion import EstadoInspeccion
from repositories import estadoInspeccion_repo

class EstadoInspeccionService:
    def __init__(self, session: Session):
        self.session = session

    def listar_estados(self) -> List[EstadoInspeccion]:
        return estadoInspeccion_repo.get_all(self.session)  

    def obtener__estado_por_id(self, id: int) -> Optional[EstadoInspeccion]:
        return estadoInspeccion_repo.get_by_id(self.session, id)

    def crear_estado(self, nuevoEstado: EstadoInspeccion) -> EstadoInspeccion:
        return estadoInspeccion_repo.create(self.session, nuevoEstado)

    def actualizar_estado(self, updateEstado: EstadoInspeccion) -> Optional[EstadoInspeccion]:
        estado = estadoInspeccion_repo.get_by_id(self.session, updateEstado.idEstadoInspeccion)
        if not estado:
            return None
        estado.nombre = updateEstado.nombre
        estado.descripcion = updateEstado.descripcion
        return estadoInspeccion_repo.update(self.session, estado)

    def eliminar_estado(self, id: int) -> bool:
        estado = estadoInspeccion_repo.get_by_id(self.session, id)
        if not estado:
            return False
        estadoInspeccion_repo.delete(self.session, estado)
        return True