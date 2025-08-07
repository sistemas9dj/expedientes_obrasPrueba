from fastapi import APIRouter, Depends, Body, Form, Request
from typing import List, Optional
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import RedirectResponse, HTMLResponse
from config.conexion import get_session
from fastapi.templating import Jinja2Templates
from datetime import datetime

from models.expediente import Expediente
from models.tipoObra import TipoObra
from models.profesional import Profesional
from models.estadoExpediente import EstadoExpediente
from models.expediente_estadoExpediente import Expediente_EstadoExpediente


router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/expedientes", response_model=List[Expediente])
async def get_expedientes(request: Request, session: Session = Depends(get_session)):

    expedientes = session.exec(
        select(Expediente)
        .options(
            selectinload(Expediente.tipoObra),
            selectinload(Expediente.estados).selectinload(Expediente_EstadoExpediente.estado)
        )
        .order_by(Expediente.fechaIngresoSistema)
        ).all()
    
    tiposObras = session.exec(
        select(TipoObra).order_by(TipoObra.nombre)
    ).all()

    profesionales = session.exec(
        select(Profesional).order_by(Profesional.apellido)
    ).all()

    estadosExpedientes = session.exec(
        select(EstadoExpediente).order_by(EstadoExpediente.nombre)
    ).all()

    # Extraer el último estado por expediente
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
     
    return templates.TemplateResponse("listar_expedientes.html", { 
        "request": request,
        "expedientes": expedientes_con_estado,
        "tiposObras": tiposObras,
        "profesionales": profesionales,
        "estadosExpedientes": estadosExpedientes
    })

@router.get("/agregar_expediente", response_model=Expediente)
async def agregar_expediente_get(request: Request, session: Session = Depends(get_session)):
     return templates.TemplateResponse("agregar_expediente.html",{"request":request})
                                      
@router.post("/agregar_expediente", response_model=Expediente)
async def agregar_expediente_post(
    # request: Request,
    anioMesaEntrada : int = Form(...),
    nroExpedienteMesaEntrada: str = Form(...),
    nroPartida : str = Form(...),
    sucesion : int = Form(...),
    observaciones : str = Form(...),
    idTipoObra : int = Form(...),
    
    session: Session = Depends(get_session)
    ):
    try:
        #armar nro de entrada....debe ser consecutivos por año. 
        nroEntrada = 1
        anioMesaEntrada = int(anioMesaEntrada) if anioMesaEntrada else None

        fechaIngresoSistema = datetime.now()
        fechaUltimaMod = datetime.now()
    
        nuevo_expediente = Expediente(
            nroEntrada=nroEntrada,
            anioMesaEntrada=anioMesaEntrada,
            nroExpedienteMesaEntrada=nroExpedienteMesaEntrada,
            nroPartida=nroPartida,
            sucesion=sucesion,
            observaciones=observaciones,
            idTipoObra=idTipoObra,
            fechaIngresoSistema=fechaIngresoSistema,
            fechaUltimaMod=fechaUltimaMod  
        )
        
        session.add(nuevo_expediente)
        session.flush()  # OBTENÉS el id sin hacer commit
   
        # Registrar el estado inicial en la tabla intermedia
        nuevo_estado = Expediente_EstadoExpediente(
                idExpediente=nuevo_expediente.idExpediente,
                idEstadoExpediente=8, # estado incial por defecto 
                fechaCambioEstado= datetime.now()
            )

        session.add(nuevo_estado)
        session.commit()

        return RedirectResponse("/expedientes", status_code=303)
    except SQLAlchemyError as e:
        session.rollback()
        raise Exception(f"Error al insertar expediente y estado: {e}")

@router.put("/expediente/{idExpediente}", response_model=Expediente)
async def update_expediente(
    idExpediente: int,
    expediente_data: dict = Body(...),
    session: Session = Depends(get_session)
):
    expediente = session.get(Expediente, idExpediente)
    if not expediente:
        return {"error": "Expediente no encontrado"}

    # Helper para convertir campos vacíos a None
    def clean_int(value):
        return int(value) if isinstance(value, int) or (isinstance(value, str) and value.strip().isdigit()) else None
    
    fechaUltimaMod = datetime.now()

    expediente.anioMesaEntrada = expediente_data["anioMesaEntrada"]
    expediente.nroExpedienteMesaEntrada = expediente_data["nroExpedienteMesaEntrada"]
    expediente.nroPartida = expediente_data["nroPartida"]
    expediente.fechaUltimaMod = fechaUltimaMod
    expediente.idTipoObra = clean_int(expediente_data.get("idTipoObra"))
    expediente.sucesion = clean_int(expediente_data.get("sucesion"))
    expediente.observaciones = clean_int(expediente_data.get("observaciones"))   

    #Agregar Nuevo estado si es que cambio
    idEstadoExpediente = clean_int(expediente_data.get("idEstadoExpedienteNuevo"))
    idEstadoExpedienteActual = clean_int(expediente_data.get("idEstadoExpedienteActual"))

    print(f"Estado Nuevo: {idEstadoExpediente}")
    print(f"Estado Actual: {idEstadoExpedienteActual}")

    if idEstadoExpediente is not None and idEstadoExpediente != idEstadoExpedienteActual:
        nuevo_estado_relacion = Expediente_EstadoExpediente(
        idExpediente=expediente.idExpediente,
        idEstadoExpediente=idEstadoExpediente,
        fechaCambioEstado=datetime.now()
    )
        session.add(nuevo_estado_relacion)
   

    session.add(expediente)
    session.commit()
    session.refresh(expediente)
    
    return expediente


@router.delete("/expediente/{idExpediente}")
async def delete_expediente(
    idExpediente: int,
    session: Session = Depends(get_session)
):
    expediente = session.get(Expediente, idExpediente)
    if not expediente:
        return {"error": "Expediente no encontrado"}
    
    session.delete(expediente)
    session.commit()
    
    return {"message": "Expediente eliminado exitosamente"}
