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

    def obtener_profesional_por_id(self, id: int) -> Optional[Profesional]:
        return profesional_repo.get_by_id(self.session, id)

    def crear_profesional(self, nuevoProfesional: Profesional) -> Profesional:
        return profesional_repo.create(self.session, nuevoProfesional)
    
    def actualizar_profesional(self, updateProfesional: Profesional) -> Optional[Profesional]:
        
        profesionales = profesional_repo.get_by_cuit(self.session,updateProfesional.idProfesional,updateProfesional.cuil_cuit)
        
        if profesionales is not None:
            return "cuilRepetido"
            #return HTMLResponse(content="""
            #    <script>
            #    alert("verifique el Cuil/Cuit. Ya existe un profesional registrado con ese CUIL.");
            #    history.back();  // vuelve al formulario sin cerrar el modal
            #    </script>
            #""", status_code=200)

        profesional = profesional_repo.get_by_id(self.session, updateProfesional.idProfesional)
        if not profesional:
            return "noExiste"
        
        return profesional_repo.update(self.session, updateProfesional)

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