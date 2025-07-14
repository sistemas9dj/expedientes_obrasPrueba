from fastapi import APIRouter, Depends, Body, Form
from typing import List
from sqlmodel import Session, select

#from models.expediente import Expediente  # Asegurate de importar el modelo
from models.estadoExpediente import EstadoExpediente

from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Request
from config.conexion import get_session
from config.conexion import session_dep 
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/estadosExpedientes", response_model=List[EstadoExpediente])
async def get_estadoExpedientes(request: Request, session: Session = Depends(get_session)):
    estadosExpedientes = session.exec(select(EstadoExpediente).order_by(EstadoExpediente.nombre)).all()
   
    return templates.TemplateResponse("listar_estadosExpedientes.html", { 
        "request": request,
        "estadosExpedientes": estadosExpedientes
    })

@router.get("/agregar_estadoExpediente", response_model=EstadoExpediente)
async def agregar_estadoExpediente_get(request: Request, session: Session = Depends(get_session)):
    return templates.TemplateResponse("agregar_estadoExpediente.html",{"request":request})
                                      
@router.post("/agregar_estadoExpediente", response_model=EstadoExpediente)
async def agregar_estadoExpediente_post(
    nombre : str = Form(...),
    descripcion: str = Form(...),
    session: Session = Depends(get_session)
):
    nuevo_estadoExpediente = EstadoExpediente(
        nombre=nombre,
        descripcion=descripcion)
    
    session.add(nuevo_estadoExpediente)
    session.commit()
    session.refresh(nuevo_estadoExpediente)
    return RedirectResponse("/estadosExpedientes", status_code=303)

@router.put("/estadoExpediente/{idEstadoExpediente}", response_model=EstadoExpediente)
async def update_estadoExpediente(
    idEstadoExpediente: int,
    estadoExpediente_data: dict = Body(...),
    session: Session = Depends(get_session)
):
    estadoExpediente = session.get(EstadoExpediente, idEstadoExpediente)
    if not estadoExpediente:
        return {"error": "Estado del Expediente no encontrado"}
    
    estadoExpediente.nombre = estadoExpediente_data["nombre"]
    estadoExpediente.descripcion = estadoExpediente_data.get("descripcion", "")
    
    session.add(estadoExpediente)
    session.commit()
    session.refresh(estadoExpediente)
    
    return estadoExpediente

  

@router.delete("/estadoExpediente/{idEstadoExpediente}")
async def delete_estadoExpediente(
    idEstadoExpediente: int,
    session: Session = Depends(get_session)
):
    estadoExpediente = session.get(EstadoExpediente, idEstadoExpediente)
    if not estadoExpediente:
        return {"error": "Estado Expediente no encontrado"}

    # Verificar si hay Expedientes que usen este Estado
    #expedientes = session.exec(
    #    select(Expediente).where(Expediente.idEstadoExpediente == idEstadoExpediente)
    #).all()

    #if expedientes:
    #    return {
    #        "error": "No se puede eliminar el Estado de Expediente porque está asociado a uno o más expedientes."
    #    }

    session.delete(estadoExpediente)
    session.commit()

    return {"message": "Estado Expediente eliminado exitosamente"}

