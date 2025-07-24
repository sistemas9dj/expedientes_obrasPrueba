from fastapi import APIRouter, Depends, Body, Form
from typing import List
from sqlmodel import Session, select
from models.tipoObra import TipoObra
from fastapi.responses import RedirectResponse
from fastapi import Request
from config.conexion import get_session
from config.conexion import session_dep 
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/tiposObras", response_model=List[TipoObra])
async def get_tiposObras(request: Request, session: Session = Depends(get_session)):
    tiposObras = session.exec(select(TipoObra).order_by(TipoObra.nombre)).all()
   
    return templates.TemplateResponse("listar_tiposObras.html", { 
        "request": request,
        "tiposObras": tiposObras
    })

@router.get("/agregar_tipoObra", response_model=TipoObra)
async def agregar_tipoObra_get(request: Request, session: Session = Depends(get_session)):
    return templates.TemplateResponse("agregar_tipoObra.html",{"request":request})
                                      
@router.post("/agregar_tipoObra", response_model=TipoObra)
async def agregar_tipoObra_post(
    nombre : str = Form(...),
    descripcion: str = Form(...),
    session: Session = Depends(get_session)
):
    nuevo_tipoObra = TipoObra(
        nombre=nombre,
        descripcion=descripcion)
    
    session.add(nuevo_tipoObra)
    session.commit()
    session.refresh(nuevo_tipoObra)
    return RedirectResponse("/tiposObras", status_code=303)

@router.put("/tipoObra/{idTipoObra}", response_model=TipoObra)
async def update_tipoObra(
    idTipoObra: int,
    tipoObra_data: dict = Body(...),
    session: Session = Depends(get_session)
):
    tipoObra = session.get(TipoObra, idTipoObra)
    if not tipoObra:
        return {"error": "Tipo de Obra no encontrado"}
    
    tipoObra.nombre = tipoObra_data["nombre"]
    tipoObra.descripcion = tipoObra_data.get("descripcion", "")
    
    session.add(tipoObra)
    session.commit()
    session.refresh(tipoObra)
    
    return tipoObra

@router.delete("/tipoObra/{idTipoObra}")
async def delete_tipoObra(
    idTipoObra: int,
    session: Session = Depends(get_session)
):
    tipoObra = session.get(TipoObra, idTipoObra)
    if not tipoObra:
        return {"error": "Tipo Obra no encontrado"}
    
    session.delete(tipoObra)
    session.commit()
    
    return {"message": "Tipo Obra eliminado exitosamente"}

