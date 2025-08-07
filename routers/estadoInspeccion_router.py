from fastapi import APIRouter, Depends, Form, Body, Request
from sqlmodel import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from config.conexion import get_session
from services.estadoInspeccion_service import EstadoInspeccionService
from models.estadoInspeccion import EstadoInspeccion
from typing import List

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/estadosInspecciones", response_model=List[EstadoInspeccion])
async def listar(request: Request, session: Session = Depends(get_session)):
    service = EstadoInspeccionService(session)  # ✅ instanciás la clase
    estados = service.listar_estados()  # ✅ usás el método de instancia
    return templates.TemplateResponse("listar_estadosInspecciones.html", {
        "request": request,
        "estadosInspecciones": estados
    })

@router.get("/agregar_estadoExpediente", response_model=EstadoInspeccion)
async def agregar(nombre: str = Form(...), descripcion: str = Form(...), session: Session = Depends(get_session)):
    service = EstadoInspeccionService(session)
    service.crear_estado(nombre, descripcion)
    return RedirectResponse("/estadosInspecciones", status_code=303)

@router.post("/agregar_estadoInspeccion", response_model=EstadoInspeccion)
async def agregar_estadoInspeccion_post(
    nombre : str = Form(...),
    descripcion: str = Form(...),
    session: Session = Depends(get_session)
):
    nuevo_estadoInspeccion = EstadoInspeccion(
        nombre=nombre,
        descripcion=descripcion)
    
    service = EstadoInspeccionService(session)
    service.crear_estado(nuevo_estadoInspeccion)
    return RedirectResponse("/estadosInspecciones", status_code=303)


@router.put("/estadoInspeccion/{idEstadoInspeccion}", response_model=EstadoInspeccion)
async def update_estadoInspeccion(
    idEstadoInspeccion: int,
    estadoInspeccion_data: dict = Body(...),
    session: Session = Depends(get_session)
):
    estadoInspeccion = session.get(EstadoInspeccion, idEstadoInspeccion)
    if not estadoInspeccion:
        return {"error": "Estado de Inspeccion no encontrado"}
    
    update_estado = EstadoInspeccion(
        idEstadoInspeccion = idEstadoInspeccion,
        nombre = estadoInspeccion_data["nombre"],
        descripcion = estadoInspeccion_data.get("descripcion", "")
    )
    
    service = EstadoInspeccionService(session)
    service.actualizar_estado(update_estado)
    return update_estado

@router.delete("/estadoInspeccion/{idEstadoInspeccion}")
async def delete_estadoExpediente(
    idEstadoInspeccion: int,
    session: Session = Depends(get_session)
):
    service = EstadoInspeccionService(session)
    exito = service.eliminar_estado(idEstadoInspeccion)
    if not exito:
        return {"error": "Estado no encontrado"}
    return {"message": "Estado Inspección eliminado exitosamente"}

