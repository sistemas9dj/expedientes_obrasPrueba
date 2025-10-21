from sqlmodel import Session, select
from models.expediente_model import ExpedienteModel
from models.expediente_estadoExpediente_model import Expediente_EstadoExpedienteModel
from models.propietario_model import PropietarioModel
from models.expediente_propietario_model import Expediente_PropietarioModel
from models.expediente_profesional_model import Expediente_ProfesionalModel

from repositories import propietario_repo, profesional_repo

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

def get_propietarios(session: Session, idExpediente: int):
        # 1) Buscar relaciones en la tabla intermedia
        relaciones = session.exec(
            select(Expediente_PropietarioModel).where(Expediente_PropietarioModel.idExpediente == idExpediente)
        ).all()

        if not relaciones:
            return []

        # 2) Extraer los ids de propietarios
        ids_propietarios = [rel.idPropietario for rel in relaciones]

        # 3) Buscar propietarios con esos IDs
        propietarios = propietario_repo.get_by_all_id(session,ids_propietarios)
        #propietarios = session.exec(
        #    select(PropietarioModel).where(PropietarioModel.idPropietario.in_(ids_propietarios))
        #).all()

        return propietarios

def get_profesionales(session: Session, idExpediente: int):
        # 1) Buscar relaciones en la tabla intermedia
        relaciones = session.exec(
            select(Expediente_ProfesionalModel).where(Expediente_ProfesionalModel.idExpediente == idExpediente)
        ).all()

        if not relaciones:
            return []

        # 2) Extraer los ids de profesionales
        ids_profesionales = [rel.idProfesional for rel in relaciones]

        # 3) Buscar propietarios con esos IDs
        profesionales = profesional_repo.get_by_all_id(session,ids_profesionales)
      
        return profesionales

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

def create_expediente_completo(session: Session, expediente : ExpedienteModel, propietarios : list[dict], expedientesProfesionales : list[dict]) -> ExpedienteModel :
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
    for p_dict in propietarios:

        p = p_dict["propietario"]
        figuraPpal = p_dict["figuraPpal"]
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
                email=p.email
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
            
            session.commit()
            session.refresh(existing_propietario)
            prop_id = existing_propietario.idPropietario       
            
        #Registar la relacion Expediente_Propietario
        nuevo_ExpProp = Expediente_PropietarioModel(
            idExpediente=expediente.idExpediente,
            idPropietario=prop_id,
            figuraPpal=figuraPpal,
            fechaCambioPropietario= datetime.now()
        )
    
        # Asociar propietarios al expediente (relación N a N)
        session.add(nuevo_ExpProp)

        #Crear relacion expediente_profesional
        for p in expedientesProfesionales:
            #Registar la relacion Expediente_Profesional
            nuevo_ExpProf = Expediente_ProfesionalModel(
                idExpediente=expediente.idExpediente,
                idProfesional=p.idProfesional,
                contactoPpal=p.contactoPpal,
                fechaIngresoSistema= datetime.now()
            )
        
            # Asociar propietarios al expediente (relación N a N)
            session.add(nuevo_ExpProf)
                
    session.commit()
    return "exito" 

#-----------------------------------------------------------------------------------------------------
#Actualiza solamente el expediente y el estado. No se tiene en cuenta las tablas relacionadas
# ---------------------------------------------------------------------------------------------------- 
def update(session: Session, expediente : ExpedienteModel, idEstadoExpediente:int) -> ExpedienteModel:
    session.add(expediente )
    session.commit()

    #Actualizar la relacion Expediente_estadoExpediente si cambio el estado del expediente
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

def update_expediente_con_propietarios(session: Session, expediente : ExpedienteModel, idEstadoExpediente:int,idEstadoExpedienteNuevo:int, propietarios : list[dict], profesionales : list[dict]) -> ExpedienteModel:
    session.add(expediente)
    session.commit()

    # 1) Registrar el estado en la tabla expediente_estadoexpediente si es que se modifico
    if idEstadoExpediente != idEstadoExpedienteNuevo:
        nuevo_estado = Expediente_EstadoExpedienteModel(
            idExpediente=expediente.idExpediente,
            idEstadoExpediente=idEstadoExpedienteNuevo, 
            fechaCambioEstado= datetime.now()
        )
        session.add(nuevo_estado)

    # 2) Crear o modificar propietarios 
    for p in propietarios:

        # Buscar si ya existe un propietario con ese CUIL. 
        # SI EXISTE SOLO SE ACTUALIZAN LOS DATOS. A ESTA ALTURA SE VERIFICO QUE EL APELLIDO COINCIDE.
        cuil = p.cuil_cuit
        #existing_propietario = session.exec(select(PropietarioModel).where(PropietarioModel.cuil_cuit == cuil)).first()
        existing_propietario = propietario_repo.get_by_cuit(session,cuil)
        

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
                email=p.email
            )
            session.add(nuevo_propietario)
            session.commit()
            session.refresh(nuevo_propietario)
            prop_id = nuevo_propietario.idPropietario

            # 3) Registar la relacion Expediente_Propietario
            nuevo_ExpProp = Expediente_PropietarioModel(
                idExpediente=expediente.idExpediente,
                idPropietario=prop_id,
                figuraPpal=p.figuraPpal,
                fechaCambioPropietario= datetime.now()
            )
            session.add(nuevo_ExpProp)

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
             
            session.commit()
            session.refresh(existing_propietario)
            prop_id = existing_propietario.idPropietario       

            # 3)En esta instancia puede pasar que:
            #   3.a. el propietario ya fue relacionado con el expediente, en tal caso se hace nada
            #   3.b. el propietario no esta relacionado y debe relacionarse
            
            #Consulto si esta relacionado o no
            expedientesPropietarios = session.exec(
               select(Expediente_PropietarioModel).where((Expediente_PropietarioModel.idPropietario == prop_id) and (Expediente_PropietarioModel.idExpediente == expediente.idExpediente))
            ).all()

            if expedientesPropietarios is None:
                # 3.b.el propietario no esta relacionado y debe relacionarse.
                # Registar la relacion Expediente_Propietario
                nuevo_ExpProp = Expediente_PropietarioModel(
                    idExpediente=expediente.idExpediente,
                    idPropietario=prop_id,
                    figuraPpal = p.figuraPpal,
                    fechaCambioPropietario= datetime.now()
                )
    
                # Asociar propietarios al expediente (relación N a N)
                session.add(nuevo_ExpProp)

    # 3) Crear relacion expediente_profesional 
    # 3.1 Eliminar todas las relaciones para ese expediente y agregar sola las relaciones activas en esta instancia 
    expediente_profesional = Expediente_ProfesionalModel(
        idExpediente = expediente.idExpediente
    )
    session.delete(expediente_profesional)

    # 3.2 Para cada profesional de la lista creo la relacion 
    for p in profesionales:
        expediente_profesional = Expediente_ProfesionalModel(
            idExpediente = expediente.idExpediente,
            idProfesional = p.idprofesional,
            contactoPpal = p.contactoPpal,
            fechaIngresoSistema= datetime.now()
        )
        # Asociar propietarios al expediente (relación N a N)
        session.add(expediente_profesional)

                 
    session.commit()
    session.refresh(expediente)
    return "exito" 

def delete(session: Session, expediente : ExpedienteModel):  #creeria que no se puede eliminar un expedeinte ingresado o bien ver cuando!!!!! En proceso de analisis
    #session.delete(expediente )
    #session.commit()

    return expediente
                               