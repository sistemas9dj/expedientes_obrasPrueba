from sqlmodel import Session
from typing import List, Optional
from models.tipoProfesion import TipoProfesion
from models.profesional import Profesional
from repositories import tipoProfesion_repo, profesional_repo

class TipoProfesionService:
    def __init__(self, session: Session):
        self.session = session

    def listar_tipoProfesiones(self) -> List[TipoProfesion]:
        return tipoProfesion_repo.get_all(self.session)  

    def obtener_tipoProfesion_por_id(self, id: int) -> Optional[TipoProfesion]:
        return tipoProfesion_repo.get_by_id(self.session, id)

    def crear_tipoProfesion(self, nuevoTipoProfesion: TipoProfesion) -> TipoProfesion:
        return tipoProfesion_repo.create(self.session, nuevoTipoProfesion)

    def actualizar_tipoProfesion(self, updateTipoProfesion: TipoProfesion) -> Optional[TipoProfesion]:
        tipoProfesion = tipoProfesion_repo.get_by_id(self.session, updateTipoProfesion.idTipoProfesion)
        if not tipoProfesion:
            return None
        tipoProfesion.nombre = updateTipoProfesion.nombre
        tipoProfesion.descripcion = updateTipoProfesion.descripcion
        return tipoProfesion_repo.update(self.session, tipoProfesion)

    def eliminar_tipoProfesion(self, id: int) -> str:
        tipoProfesion = tipoProfesion_repo.get_by_id(self.session, id)
        if not tipoProfesion:
            return "no existe"  # No encontrado

        profesionales = profesional_repo.get_by_idTipoProefesion(self.session, tipoProfesion.idTipoProfesion) 

        if profesionales is not None:
            return "relacionado"  #existen profesionales con el tipo de profesion
        else:
            tipoProfesion_repo.delete(self.session, tipoProfesion)
            return "exito"
       
     