from fastapi import APIRouter, Depends, Body, Form
from typing import List
from sqlmodel import Session, select
from models.tipoExpediente import TipoExpediente
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Request
from config.conexion import get_session
from config.conexion import session_dep 
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/tiposExpedientes", response_model=List[TipoExpediente])
async def get_tiposExpedientes(request: Request, session: Session = Depends(get_session)):
    tiposExpedientes = session.exec(select(TipoExpediente).order_by(TipoExpediente.nombre)).all()
   
    return templates.TemplateResponse("listar_tiposExpedientes.html", { 
        "request": request,
        "tiposExpedientes": tiposExpedientes
    })

@router.get("/agregar_tipoExpediente", response_model=TipoExpediente)
async def agregar_tipoExpediente_get(request: Request, session: Session = Depends(get_session)):
    return templates.TemplateResponse("agregar_tipoExpediente.html",{"request":request})
                                      
@router.post("/agregar_tipoExpediente", response_model=TipoExpediente)
async def agregar_tipoExpediente_post(
    nombre : str = Form(...),
    descripcion: str = Form(...),
    session: Session = Depends(get_session)
):
    nuevo_tipoExpediente = TipoExpediente(
        nombre=nombre,
        descripcion=descripcion)
    
    session.add(nuevo_tipoExpediente)
    session.commit()
    session.refresh(nuevo_tipoExpediente)
    return RedirectResponse("/tiposExpedientes", status_code=303)

@router.put("/tipoExpediente/{idTipoExpediente}", response_model=TipoExpediente)
async def update_tipoExpediente(
    idTipoExpediente: int,
    tipoExpediente_data: dict = Body(...),
    session: Session = Depends(get_session)
):
    tipoExpediente = session.get(TipoExpediente, idTipoExpediente)
    if not tipoExpediente:
        return {"error": "Tipo del Expediente no encontrado"}
    
    tipoExpediente.nombre = tipoExpediente_data["nombre"]
    tipoExpediente.descripcion = tipoExpediente_data.get("descripcion", "")
    
    session.add(tipoExpediente)
    session.commit()
    session.refresh(tipoExpediente)
    
    return tipoExpediente

@router.delete("/tipoExpediente/{idTipoExpediente}")
async def delete_tipoExpediente(
    idTipoExpediente: int,
    session: Session = Depends(get_session)
):
    tipoExpediente = session.get(TipoExpediente, idTipoExpediente)
    if not tipoExpediente:
        return {"error": "Tipo Expediente no encontrado"}
    
    session.delete(tipoExpediente)
    session.commit()
    
    return {"message": "Tipo Expediente eliminado exitosamente"}

