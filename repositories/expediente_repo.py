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
    #Crea un expediente sin propietarios y son profesionales
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
    #Crea un expedeinte completo, es decir, agrega las relaciones con estadoExpedeinte, propietariosExpedientes y ProfesionalesExpedientes
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
        # Buscar si ya existe un propietario con ese CUIL. sI EXISTE SOLO SE ACTUALIZAN LOS DATOS. A ESTA ALTURA SE VERIFICO QUE EL APELLIDO COINCIDE.
        cuil = p.cuil_cuit
        existing_propietario = session.exec(select(PropietarioModel).where(PropietarioModel.cuil_cuit == cuil)).first()

        if existing_propietario is None:
            #Registrar nuevo Propietario
            nuevo_propietario = PropietarioModel(
                cuil_cuit=p.cuil_cuit,
                nombre=p.nombre,
                apellido=p.apellido,
                calle=p.calle,
                nroCalle=p.nroCalle,
                piso=p.piso,
                nroDpto=p.nroDpto,
                areaCelular=p.areaCelular,
                nroCelular=p.nroCelular,
                email=p.email,
                figuraPpal=p.figuraPpal
            )
            session.add(nuevo_propietario)
            session.commit()
            session.refresh(nuevo_propietario)
            prop_id = nuevo_propietario.idPropietario
        else: 
           # Actualizar propietario existente
            existing_propietario.nombre = p.nombre
            existing_propietario.calle = p.calle
            existing_propietario.nroCalle = p.nroCalle
            existing_propietario.piso = p.piso
            existing_propietario.nroDpto = p.nroDpto
            existing_propietario.areaCelular = p.areaCelular 
            existing_propietario.nroCelular = p.nroCelular 
            existing_propietario.email = p.email
            existing_propietario.figuraPpal = p.figuraPpal
  
            session.commit()
            session.refresh(existing_propietario)
            prop_id = existing_propietario.idPropietario       
            
        #Registar la relacion Expedeinte_Propietario
        nuevo_ExpProp = Expediente_PropietarioModel(
            idExpediente=expediente.idExpediente,
            idPropietario=prop_id,
            fechaCambioPropietario= datetime.now()
        )
    
        # Asociar propietarios al expediente (relación N a N)
        session.add(nuevo_ExpProp)
                
    session.commit()
    return "exito" 

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
                               