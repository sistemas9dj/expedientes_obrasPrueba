from sqlmodel import Session
from typing import List, Optional

from models.expediente_model import ExpedienteModel

from repositories import expediente_repo, propietario_repo

class ExpedienteService:
    # Helper para convertir campos vacíos a None
    def clean_int(value):
        return int(value) if isinstance(value, int) or (isinstance(value, str) and value.strip().isdigit()) else None
    
    def obtener_proximo_nro_entrada(self, anioMesaEntrada: int) -> int:
        return expediente_repo.get_next_nro_entrada(self.session, anioMesaEntrada)
    
    def __init__(self, session: Session):
        self.session = session

    def listar_expedientes(self) -> List[ExpedienteModel]:

        expedientes=expediente_repo.get_all(self.session)

        # Extraer el último estado asignado por expediente y generar un nuevo objeto expedientes con los datos extraidos de expediente 
        # agregados el id del ultimo estado y la fecha de la ultima modficacion del estado para mostrar en al tabla, ya que es una relacion n a n
        expedientes_con_estado = []
        for exp in expedientes:
            if exp.estados:
                ultimo_estado_obj = sorted(exp.estados, key=lambda e: e.fechaCambioEstado)[-1].estado
                ultimo_estado_id = ultimo_estado_obj.idEstadoExpediente
                ultimo_estado_nombre = ultimo_estado_obj.nombre
            else:
                ultimo_estado_id = None
                ultimo_estado_nombre = "Sin estado"
            
            expedientes_con_estado.append({
                "expediente": exp,
                "ultimo_estado_id": ultimo_estado_id,
                "ultimo_estado_nombre": ultimo_estado_nombre
            })

        return  expedientes_con_estado

    def obtener_expediente_por_id(self, id: int) -> Optional[ExpedienteModel]:
        return expediente_repo.get_by_id(self.session, id)

    #Obtener propietarios del Expedeinte. relacion N a N
    def get_propietarios(self, idExpediente: int):
        return expediente_repo.get_propietarios(self.session,idExpediente)

    #Obtener profesionales del Expediente. relacion N a N
    def get_profesionales(self, idExpediente: int):
        return expediente_repo.get_profesionales(self.session,idExpediente)
    
    def crear_expediente(self, nuevoExpediente: ExpedienteModel, propietarios_data: list[dict], expedientesProfesionales_data: list[dict]) -> Optional[ExpedienteModel]:
        #Validar que no exista un propietario con el Cuil ingresado
        for p_dict in propietarios_data:
            p = p_dict["propietario"]
            propietario = propietario_repo.get_by_cuit_distintApellido(self.session, p.apellido, p.cuil_cuit)
            if propietario:
                return "duplicado/" +  p.cuil_cuit 
        
        return expediente_repo.create_expediente_completo(self.session,nuevoExpediente, propietarios_data, expedientesProfesionales_data) 
       
    def actualizar_expediente(self, updateExpediente: ExpedienteModel, idEstadoExpediente:int, idEstadoExpNuevo:int,propietarios_data: list[dict],profesionales_data: list[dict]) -> Optional[ExpedienteModel]:
        
        expediente = expediente_repo.get_by_id(self.session, updateExpediente.idExpediente)
        if not expediente:
            return "noExiste"
        
        # Actualizar campos manualmente
        expediente.idTipoObra = updateExpediente.idTipoObra
        expediente.nroExpedienteMesaEntrada = updateExpediente.nroExpedienteMesaEntrada
        expediente.anioMesaEntrada = updateExpediente.anioMesaEntrada
        expediente.nroPartida = updateExpediente.nroPartida
        expediente.sucesion = updateExpediente.sucesion
        expediente.observaciones = updateExpediente.observaciones

        return expediente_repo.update_expediente_con_propietarios(self.session, expediente, idEstadoExpediente, idEstadoExpNuevo,propietarios_data, profesionales_data)        
            
    def eliminar_expediente(self, id: int) -> bool:
        expediente = expediente_repo.get_by_id(self.session, id)
        if not expediente:
            return False
        
        # Verificar si hay Expedientes que usen este Estado
        #expedientes = session.exec(
        #    select(Expediente).where(Expediente.idInspector == idInspector)
        #).all()

        #if expedientes:
        #    return {
        #        "error": "No se puede eliminar el Estado de Expediente porque está asociado a uno o más expedientes."
        #    }

        expediente_repo.delete(self.session, expediente)
        return True