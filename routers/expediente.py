from fastapi import APIRouter, Depends, Body, Form
from typing import List, Optional
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from models.expediente import Expediente
from models.tipoObra import TipoObra
from models.profesional import Profesional
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Request
from config.conexion import get_session
from fastapi.templating import Jinja2Templates

from datetime import datetime


router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/expedientes", response_model=List[Expediente])
async def get_expedientes(request: Request, session: Session = Depends(get_session)):

    expedientes = session.exec(
        select(Expediente)
        .options(selectinload(Expediente.tipoObra))  # ✅ esta es la relación
        .order_by(Expediente.fechaIngresoSistema)
    ).all()
    
    tiposObras = session.exec(
        select(TipoObra).order_by(TipoObra.nombre)
    ).all()

    profesionales = session.exec(
        select(Profesional).order_by(Profesional.apellido)
    ).all()

    return templates.TemplateResponse("listar_expedientes.html", { 
        "request": request,
        "expedientes": expedientes,
        "tiposObras": tiposObras,
        "profesionales": profesionales
    })

@router.get("/agregar_expediente", response_model=Expediente)
async def agregar_expediente_get(request: Request, session: Session = Depends(get_session)):
    
    print(" Llegó al endpoint /agregar_expediente por get")
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

    print(" Llegó al endpoint /agregar_expediente")
    print(f"anioMesaEntrada: {anioMesaEntrada}")
    print(f"nroExpedienteMesaEntrada: {nroExpedienteMesaEntrada}")
      
    #armar nro de entrada....debe ser consecutivos por año. 
    nroEntrada = 1
    idEstadoExpediente=8,
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
        idEstadoExpediente=idEstadoExpediente,
        idTipoObra=idTipoObra,
        fechaIngresoSistema=fechaIngresoSistema,
        fechaUltimaMod=fechaUltimaMod  
    )
    
    session.add(nuevo_expediente)
    session.commit()
    session.refresh(nuevo_expediente)
    return RedirectResponse("/expedientes", status_code=303)


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
    expediente.idTipoExpediente = clean_int(expediente_data.get("idTipoExpediente"))
    
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
