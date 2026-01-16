from sqlmodel import Session, select
from sqlalchemy import delete as sa_delete

from models.expediente_model import ExpedienteModel
from models.expediente_estadoExpediente_model import Expediente_EstadoExpedienteModel
from models.expediente_propietario_model import Expediente_PropietarioModel
from models.expediente_profesional_model import Expediente_ProfesionalModel
from models.expediente_tipoObra_model import Expediente_TipoObraModel
from models.profesional_model import ProfesionalModel
from models.propietario_model import PropietarioModel

from repositories import propietario_repo

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
                                    # Cargar TipoExpediente
                                    selectinload(ExpedienteModel.tipoExpediente),

                                    #CARGAR Estados Expedientes
                                    selectinload(ExpedienteModel.estados)
                                        .selectinload(Expediente_EstadoExpedienteModel.estado),

                                    #Cargar Tipos de Obras
                                    selectinload(ExpedienteModel.tipos)
                                        .selectinload(Expediente_TipoObraModel.tipos)                                        

                                )
                                .order_by(ExpedienteModel.fechaIngresoSistema)
                                ).all()

def get_by_id(session: Session, id: int) -> Optional[ExpedienteModel]:
    return session.get(ExpedienteModel , id)

def get_propietarios(session: Session, idExpediente: int):
        # Buscar relaciones en la tabla intermedia
        relaciones = session.exec(
            select(Expediente_PropietarioModel).where(Expediente_PropietarioModel.idExpediente == idExpediente)
        ).all()

        if not relaciones:
            return []

        # Extraer los ids de propietarios
        ids_propietarios = [rel.idPropietario for rel in relaciones]

        # Buscar propietarios con esos IDs
        propietarios = propietario_repo.get_by_all_id(session,ids_propietarios)
       
        return propietarios

def get_profesionales(session: Session, idExpediente: int):
    stmt = (
        select(ProfesionalModel, Expediente_ProfesionalModel.contactoPpal)
        .join(Expediente_ProfesionalModel,
              ProfesionalModel.idProfesional == Expediente_ProfesionalModel.idProfesional)
        .where(Expediente_ProfesionalModel.idExpediente == idExpediente)
    )

    resultados = session.exec(stmt).all()

    lista = []

    for prof, contactoPpal in resultados:
        print( contactoPpal )
        lista.append({
            "idProfesional": prof.idProfesional,
            "nombre": prof.nombre,
            "apellido": prof.apellido,
            "matricula": prof.matricula,
            "contactoPpal": contactoPpal
        })

    return lista

def get_ultimo_estado_by_expediente(session, idExpediente: int) -> Expediente_EstadoExpedienteModel:
    return session.exec(
                select(Expediente_EstadoExpedienteModel)
                .where(Expediente_EstadoExpedienteModel.idExpediente == idExpediente)
                .order_by(Expediente_EstadoExpedienteModel.fechaCambioEstado.desc())
                .limit(1)).first()


def create_expediente_completo(session: Session, expediente : ExpedienteModel, idEstadoExpediente:int, lista_tiposObras: list, propietarios : list[dict], expedientesProfesionales : list[dict], idUsuario: int) -> ExpedienteModel :
    #Crea un expediente completo, es decir, agrega las relaciones con estadoExpediente, propietariosExpedientes y ProfesionalesExpedientes
    session.add(expediente)
    session.flush() # obtener id sin commit
 
    # -----------------------------------------------------------------
    # Registrar el estado inicial en la tabla expediente_estadoexpediente
    # -----------------------------------------------------------------
    nuevo_estado = Expediente_EstadoExpedienteModel(
        idExpediente=expediente.idExpediente,
        idEstadoExpediente = idEstadoExpediente, 
        fechaCambioEstado = datetime.now(),
        idUsuario = idUsuario
    )
    session.add(nuevo_estado)

    # -----------------------------------------------------------------
    # Registrar los tipos de obras seleccioandos
    # -----------------------------------------------------------------
    for tipo in lista_tiposObras:
        nuevo_tipo = Expediente_TipoObraModel(
            idExpediente=expediente.idExpediente,
            idTipoObra=int(tipo),
            fechaAsignacion= datetime.now()
        )
        session.add(nuevo_tipo)

    # -----------------------------------------------------------------
    # Crear propietarios y asociarlos a la tabla expediente_propietario
    # -----------------------------------------------------------------
    for p_dict in propietarios:

        p = p_dict["propietario"]
        figuraPpal = p_dict["figuraPpal"]
        # Buscar si ya existe un propietario con ese CUIL. sI EXISTE SOLO SE ACTUALIZAN LOS DATOS. A ESTA ALTURA SE VERIFICO QUE EL APELLIDO COINCIDE.
        cuil = p.cuil_cuit
        existing_propietario = propietario_repo.get_by_cuit(session, cuil)

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
            session.flush() # obtener id sin commit
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
            
            session.flush()
            prop_id = existing_propietario.idPropietario       
            
        # -----------------------------------------------------------------
        # Crear propietarios 
        # -----------------------------------------------------------------
        nuevo_ExpProp = Expediente_PropietarioModel(
            idExpediente=expediente.idExpediente,
            idPropietario=prop_id,
            figuraPpal=figuraPpal,
            fechaCambioPropietario= datetime.now()
        )
    
        # Asociar propietarios al expediente (relación N a N)
        session.add(nuevo_ExpProp)

    # -----------------------------------------------------------------
    # Crear proesioanles y asociarlos a la tabla expediente_profesional
    # ----------------------------------------------------------------- 
    for p in expedientesProfesionales:
        #Registar la relacion Expediente_Profesional
        nuevo_ExpProf = Expediente_ProfesionalModel(
            idExpediente=expediente.idExpediente,
            idProfesional = p["idProfesional"],
            contactoPpal = p["contactoPpal"],
            fechaIngresoSistema= datetime.now()
        )
        
        # Asociar propietarios al expediente (relación N a N)
        session.add(nuevo_ExpProf)
                
    session.commit()
    session.refresh(expediente)
    
    return "exito" 

#-----------------------------------------------------------------------------------------------------
#Actualiza solamente el expediente y el estado. No se tiene en cuenta las tablas relacionadas
# ---------------------------------------------------------------------------------------------------- 
def update(session: Session, expediente : ExpedienteModel, idEstadoExpediente:int, idUsuario: int) -> ExpedienteModel:
    session.add(expediente )
   # session.commit()

    #Actualizar la relacion Expediente_estadoExpediente si cambio el estado del expediente
    if idEstadoExpediente is not None: 
         # Registrar el estado inicial en la tabla expediente_estadoexpediente
        nuevo_estado = Expediente_EstadoExpedienteModel(
            idExpediente=expediente.idExpediente,
            idEstadoExpediente=idEstadoExpediente,  
            fechaCambioEstado= datetime.now(),
            idUsuario = idUsuario
        )

        session.add(nuevo_estado)
    
    session.commit()
    session.refresh(expediente )
    return expediente 

def update_expediente_con_propietarios(session: Session, expediente : ExpedienteModel, idEstadoExpediente:int,idEstadoExpedienteNuevo:int, propietarios : list[dict], profesionales : list[dict], idUsuario: int) -> ExpedienteModel:
    session.add(expediente)

    # -----------------------------------------------------------------
    # Registrar nuevo estado si cambió. Tabla expediente_estadoExpediente
    # -----------------------------------------------------------------
    if idEstadoExpediente != idEstadoExpedienteNuevo:
        nuevo_estado = Expediente_EstadoExpedienteModel(
            idExpediente=expediente.idExpediente,
            idEstadoExpediente=idEstadoExpedienteNuevo,
            fechaCambioEstado=datetime.now(),
            idUsuario=idUsuario
        )
        session.add(nuevo_estado)

    # -----------------------------------------------------------------
    # LIMPIAR relaciones de propietarios que ya no vienen. Tabla expediente_Propietario
    # -----------------------------------------------------------------
    ids_nuevos_cuil = [p["propietario"].cuil_cuit for p in propietarios]

    #Leer las relaciones cargadas en la DBpara el expedeinte
    relaciones_actuales = session.exec(
        select(Expediente_PropietarioModel)
        .where(Expediente_PropietarioModel.idExpediente == expediente.idExpediente)
    ).all()

    #Para cada propietario de la relacion de la DB ya cargados comparo si esta en la lista de los ingresados en el html
    for rel in relaciones_actuales:
        prop = session.get(PropietarioModel, rel.idPropietario)
        if prop.cuil_cuit not in ids_nuevos_cuil:
            session.delete(rel)

    # -----------------------------------------------------------------
    # Crear / actualizar propietarios y relaciones
    # -----------------------------------------------------------------
    for p_dict in propietarios:

        p = p_dict["propietario"]
        figuraPpal = p_dict["figuraPpal"]
        cuil = p.cuil_cuit

        existing_propietario = propietario_repo.get_by_cuit(session, cuil)

        if existing_propietario is None:
            # Crear propietario
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
            session.flush()
            prop_id = nuevo_propietario.idPropietario
        else:
            # Actualizar propietario existente
            existing_propietario.nombre = p.nombre
            existing_propietario.apellido = p.apellido
            existing_propietario.calle = p.calle
            existing_propietario.nroCalle = p.nroCalle
            existing_propietario.piso = p.piso
            existing_propietario.nroDpto = p.nroDpto
            existing_propietario.areaCelular = p.areaCelular
            existing_propietario.nroCelular = p.nroCelular
            existing_propietario.email = p.email
            session.flush()
            prop_id = existing_propietario.idPropietario

        # Verificar si ya existe la relación
        rel = session.exec(
            select(Expediente_PropietarioModel).where(
                (Expediente_PropietarioModel.idExpediente == expediente.idExpediente) &
                (Expediente_PropietarioModel.idPropietario == prop_id)
            )
        ).first()

        if rel:
            # Actualizar figura principal si cambió
            rel.figuraPpal = figuraPpal
            rel.fechaCambioPropietario = datetime.now()
        else:
            # Crear relación
            nueva_rel = Expediente_PropietarioModel(
                idExpediente=expediente.idExpediente,
                idPropietario=prop_id,
                figuraPpal=figuraPpal,
                fechaCambioPropietario=datetime.now()
            )
            session.add(nueva_rel)

    # -----------------------------------------------------------------
    # Crear / actualizar Profesionales y relaciones
    # -----------------------------------------------------------------
    # Leo los ids que se cargaron en el html
    ids_nuevos_prof = [p["idProfesional"] for p in profesionales]
    

    # Leo las relaciones cargadas en la db
    relaciones_actuales_prof = session.exec(
        select(Expediente_ProfesionalModel)
        .where(Expediente_ProfesionalModel.idExpediente == expediente.idExpediente)
    ).all()

    # Eliminar relaciones que ya no vienen desde el html
    for rel in relaciones_actuales_prof:
        if rel.idProfesional not in ids_nuevos_prof:
            session.delete(rel)

    # Agregar y Actualizar
    for p in profesionales:
        id_prof = p["idProfesional"]
        contactoPpal = p["contactoPpal"]

        # Buscar si ya existe la relación
        rel_existente = session.exec(
            select(Expediente_ProfesionalModel)
            .where(
                (Expediente_ProfesionalModel.idExpediente == expediente.idExpediente) &
                (Expediente_ProfesionalModel.idProfesional == id_prof)
            )
        ).first()

        if rel_existente:
            # Update si cambió algo
            rel_existente.contactoPpal = contactoPpal
            # rel_existente.fechaIngresoSistema = datetime.now()
        else:
            # Alta nueva relación
            nuevo_rel = Expediente_ProfesionalModel(
                idExpediente=expediente.idExpediente,
                idProfesional=id_prof,
                contactoPpal=contactoPpal,
                fechaIngresoSistema=datetime.now()
            )
            session.add(nuevo_rel)

    # -----------------------------------------------------------------
    # Commit final
    # -----------------------------------------------------------------
    session.commit()
    session.refresh(expediente)

    return "exito"

def delete(session: Session, expediente : ExpedienteModel):  #creeria que no se puede eliminar un expedeinte ingresado o bien ver cuando!!!!! En proceso de analisis
    #session.delete(expediente )
    #session.commit()

    return expediente
         