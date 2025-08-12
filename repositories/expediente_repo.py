from sqlmodel import Session, select
from models.expediente_model import ExpedienteModel
from models.expediente_estadoExpediente_model import Expediente_EstadoExpedienteModel
from typing import List, Optional
from sqlalchemy.orm import selectinload
from datetime import datetime
from sqlalchemy import func

#Funcion para generar el nro de entrada consecutivo por año del expediente
def get_next_nro_entrada(session: Session, anioMesaEntrada: int) -> int:
    max_nro = session.query(func.max(ExpedienteModel.nroEntrada))\
                     .filter(ExpedienteModel.anioMesaEntrada == anioMesaEntrada)\
                     .scalar()
    return (max_nro or 0) + 1

def get_all(session: Session) -> List[ExpedienteModel]:
    return session.exec(select(ExpedienteModel)
                                .options(
                                    selectinload(ExpedienteModel.tipoObra),
                                    selectinload(ExpedienteModel.estados).selectinload(Expediente_EstadoExpedienteModel.estado)
                                )
                                .order_by(ExpedienteModel.fechaIngresoSistema)
                                ).all()

def get_by_id(session: Session, id: int) -> Optional[ExpedienteModel]:
    return session.get(ExpedienteModel , id)

def create(session: Session, expediente : ExpedienteModel) -> ExpedienteModel :
    session.add(expediente)
    #session.commit()
    session.flush()  # OBTENÉS el id sin hacer commit

    # Registrar el estado inicial en la tabla expediente_estadoexpediente
    nuevo_estado = Expediente_EstadoExpedienteModel(
        idExpediente=expediente.idExpediente,
        idEstadoExpediente=8, # estado incial por defecto 
        fechaCambioEstado= datetime.now()
    )

    session.add(nuevo_estado)
    session.commit()
        
    session.refresh(expediente)
    return expediente 

def update(session: Session, expediente : ExpedienteModel, idEstadoExpediente:int) -> ExpedienteModel:
    session.add(expediente )
    session.commit()

    #Actualizar la relacion Expedeinte_estadoExpediente si cambio el estado del expediente
    if idEstadoExpediente is not None: 
         # Registrar el estado inicial en la tabla expediente_estadoexpediente
        nuevo_estado = Expediente_EstadoExpedienteModel(
            idExpediente=expediente.idExpediente,
            idEstadoExpediente=idEstadoExpediente,  
            fechaCambioEstado= datetime.now()
        )

        session.add(nuevo_estado)
    
    session.commit()
    session.refresh(expediente )
    return expediente 

def delete(session: Session, expediente : ExpedienteModel):  #creeria que no se puede eliminar un expedeinte ingresado o bien ver cuando!!!!! En proceso de analisis
    #session.delete(expediente )
    #session.commit()

    return expediente
                               