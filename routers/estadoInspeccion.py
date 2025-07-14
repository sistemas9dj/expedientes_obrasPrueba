from fastapi import APIRouter, Depends, Body, Form
from typing import List
from sqlmodel import Session, select
from models.estadoInspeccion import EstadoInspeccion
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Request
from config.conexion import get_session
from config.conexion import session_dep 
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/estadosInspecciones", response_model=List[EstadoInspeccion])
async def get_estadoInspecciones(request: Request, session: Session = Depends(get_session)):
    estadosInspecciones = session.exec(select(EstadoInspeccion).order_by(EstadoInspeccion.nombre)).all()
   
    return templates.TemplateResponse("listar_estadosInspecciones.html", { 
        "request": request,
        "estadosInspecciones": estadosInspecciones
    })

@router.get("/agregar_estadoInspeccion", response_model=EstadoInspeccion)
async def agregar_estadoInspeccion_get(request: Request, session: Session = Depends(get_session)):
    return templates.TemplateResponse("agregar_estadoInspeccion.html",{"request":request})
                                      
@router.post("/agregar_estadoInspeccion", response_model=EstadoInspeccion)
async def agregar_estadoInspeccion_post(
    nombre : str = Form(...),
    descripcion: str = Form(...),
    session: Session = Depends(get_session)
):
    nuevo_estadoInspeccion = EstadoInspeccion(
        nombre=nombre,
        descripcion=descripcion)
    
    session.add(nuevo_estadoInspeccion)
    session.commit()
    session.refresh(nuevo_estadoInspeccion)
    return RedirectResponse("/estadosInspecciones", status_code=303)

@router.put("/estadoInspeccion/{idEstadoInspeccion}", response_model=EstadoInspeccion)
async def update_estadoInspeccion(
    idEstadoInspeccion: int,
    estadoInspeccion_data: dict = Body(...),
    session: Session = Depends(get_session)
):
    estadoInspeccion = session.get(EstadoInspeccion, idEstadoInspeccion)
    if not estadoInspeccion:
        return {"error": "Estado de la Inspeccion no encontrado"}
    
    estadoInspeccion.nombre = estadoInspeccion_data["nombre"]
    estadoInspeccion.descripcion = estadoInspeccion_data.get("descripcion", "")
    
    session.add(estadoInspeccion)
    session.commit()
    session.refresh(estadoInspeccion)
    
    return estadoInspeccion

@router.delete("/estadoInspeccion/{idEstadoInspeccion}")
async def delete_estadoInspeccion(
    idEstadoInspeccion: int,
    session: Session = Depends(get_session)
):
    estadoInspeccion = session.get(EstadoInspeccion, idEstadoInspeccion)
    if not estadoInspeccion:
        return {"error": "Estado Inspeccion no encontrado"}
    
    session.delete(estadoInspeccion)
    session.commit()
    
    return {"message": "Estado Inspeccion eliminado exitosamente"}

