from sqlmodel import Session, select
from models.expediente_model import ExpedienteModel
from models.expediente_estadoExpediente_model import Expediente_EstadoExpedienteModel
from models.propietario_model import PropietarioModel
from models.expediente_propietario_model import Expediente_PropietarioModel
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

def create(session: Session, expediente : ExpedienteModel, propietarios : list[dict]) -> ExpedienteModel :
    
    session.add(expediente)
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

def create_expediente_con_propietarios(session: Session, expediente : ExpedienteModel, propietarios : list[dict]) -> ExpedienteModel :
    
    session.add(expediente)
    session.commit()
    session.refresh(expediente)
 
    # Registrar el estado inicial en la tabla expediente_estadoexpediente
    nuevo_estado = Expediente_EstadoExpedienteModel(
        idExpediente=expediente.idExpediente,
        idEstadoExpediente=8, # estado incial por defecto 
        fechaCambioEstado= datetime.now()
    )
    session.add(nuevo_estado)

    #Crear propietarios y asociarlos a la tabla expediente_propietario
    for p in propietarios:
        # Buscar si ya existe un propietario con ese CUIL
        existing_propietario = session.exec(select(PropietarioModel).where(PropietarioModel.cuil_cuit == p.cuil_cuit)).first()
        
        if not existing_propietario:
            #Registrar Propietario
            session.add(p)
            session.commit()
            session.refresh(p)
        else: 
            # Actualizar datos del propietario existente
            existing_propietario.nombre = p.nombre
            existing_propietario.apellido = p.apellido
            existing_propietario.domicilio = p.domicilio
             # ... asignar los demás campos que quieras actualizar
            session.add(existing_propietario)  # opcional en SQLModel
            session.commit()
            session.refresh(p)       
            
        #Registar la relacion Expedeinte_Propietario
        nuevo_ExpProp = Expediente_PropietarioModel(
            idExpediente=expediente.idExpediente,
            idPropietario=p.idPropietario, # estado incial por defecto 
            fechaCambioPropietario= datetime.now()
        )
    
        # Asociar propietarios al expediente (relación N a N)
        session.add(nuevo_ExpProp)
                
    session.commit()
        
   # session.refresh(expediente)
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
                               