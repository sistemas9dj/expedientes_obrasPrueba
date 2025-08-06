from sqlmodel import Session
from typing import List, Optional
from models.profesional import Profesional
from repositories import profesional_repo

class ProfesionalService:
    # Helper para convertir campos vacíos a None
    def clean_int(value):
        return int(value) if isinstance(value, int) or (isinstance(value, str) and value.strip().isdigit()) else None
    
    def __init__(self, session: Session):
        self.session = session

    def listar_profesionales(self) -> List[Profesional]:
        return profesional_repo.get_all(self.session)  

    def obtener_inspector_por_id(self, id: int) -> Optional[Profesional]:
        return profesional_repo.get_by_id(self.session, id)

    def crear_inspector(self, nuevoInspector: Profesional) -> Profesional:
        return profesional_repo.create(self.session, nuevoInspector)
    
    def actualizar_profesional(self, updateProfesional: Profesional) -> Optional[Profesional]:
        profesional = profesional_repo.get_by_id(self.session, updateProfesional.idProfesional)
        if not profesional:
            return None
        profesional.nombre = updateProfesional.nombre
        profesional.apellido = updateProfesional.apellido

        profesional.cuil_cuit = updateProfesional.cuil_cuit
        profesional.nombre = updateProfesional.nombre
        profesional.apellido = updateProfesional.apellido
        profesional.razonSocial = updateProfesional.razonSocial
        profesional.calle = updateProfesional.calle
        profesional.nroCalle = clean_int(updateProfesional.nroCalle)
        profesional.nroDpto = updateProfesional.nroDpto
        profesional.piso = updateProfesional.piso
        profesional.areaCelular = clean_int(updateProfesional.areaCelular)
        profesional.nroCelular = clean_int(updateProfesional.nroCelular)
        profesional.matricula = updateProfesional.matricula
        profesional.email = updateProfesional.email
        profesional.idTipoProfesion = clean_int(updateProfesional.idTipoProfesion)


        return profesional_repo.update(self.session, profesional)

    def eliminar_profesional(self, id: int) -> bool:
        profesional = profesional_repo.get_by_id(self.session, id)
        if not profesional:
            return False
        
        # Verificar si hay Expedientes que usen este Estado
        #expedientes = session.exec(
        #    select(Expediente).where(Expediente.idInspector == idInspector)
        #).all()

        #if expedientes:
        #    return {
        #        "error": "No se puede eliminar el Estado de Expediente porque está asociado a uno o más expedientes."
        #    }

        profesional_repo.delete(self.session, profesional)
        return True