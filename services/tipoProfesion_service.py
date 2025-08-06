from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from typing import List, Optional
from models.tipoProfesion import TipoProfesion
from models.profesional import Profesional
from repositories import tipoProfesion_repo
from fastapi import HTTPException

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
        #if not tipoProfesion:
        #   raise HTTPException(
        #        status_code=404,
        #        detail="Tipo de Profesión no encontrado."
        #    )
        if not tipoProfesion:
            print("❌ Tipo de Profesión no encontrado")
            return "no existe"  # No encontrado

        # Validar que el tipo de profesion no este asignado algun profesional
        profesionales = self.session.exec(
                           select(Profesional).where(Profesional.idTipoProfesion == tipoProfesion.idTipoProfesion)
                        ).first()
    
        if profesionales is not None:
            print("❌ Tipo de Profesión en profesional")
            #return "No se puede eliminar el Tipo de Profesión porque está asignado a uno o más profesionales."
            return "relacionado"  #existen profesionales con el tipo de profesion
        else:
            print("❌ Borrando tipo")
            tipoProfesion_repo.delete(self.session, tipoProfesion)
            return "exito"
       
     