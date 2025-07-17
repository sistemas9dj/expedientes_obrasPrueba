from fastapi import APIRouter, Depends, Body, Form
from typing import List
from sqlmodel import Session, select
from models.tipoProfesion import TipoProfesion
from fastapi.responses import RedirectResponse, HTMLResponse,JSONResponse
from fastapi import Request
from config.conexion import get_session
from config.conexion import session_dep 
from fastapi.templating import Jinja2Templates
from models.profesional import Profesional

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/tiposProfesiones", response_model=List[TipoProfesion])
async def get_tiposProfesiones(request: Request, session: Session = Depends(get_session)):
    tiposProfesiones = session.exec(select(TipoProfesion).order_by(TipoProfesion.nombre)).all()
   
    return templates.TemplateResponse("listar_tiposProfesiones.html", { 
        "request": request,
        "tiposProfesiones": tiposProfesiones
    })

@router.get("/agregar_tipoProfesion", response_model=TipoProfesion)
async def agregar_tipoProfesion_get(request: Request, session: Session = Depends(get_session)):
    return templates.TemplateResponse("agregar_tipoProfesion.html",{"request":request})
                                      
@router.post("/agregar_tipoProfesion", response_model=TipoProfesion)
async def agregar_tipoProfesion_post(
    nombre : str = Form(...),
    descripcion: str = Form(...),
    session: Session = Depends(get_session)
):
    nuevo_tipoProfesion = TipoProfesion(
        nombre=nombre,
        descripcion=descripcion)
    
    session.add(nuevo_tipoProfesion)
    session.commit()
    session.refresh(nuevo_tipoProfesion)
    return RedirectResponse("/tiposProfesiones", status_code=303)

@router.put("/tipoProfesion/{idTipoProfesion}", response_model=TipoProfesion)
async def update_tipoProfesion(
    idTipoProfesion: int,
    tipoProfesion_data: dict = Body(...),
    session: Session = Depends(get_session)
):
    tipoProfesion = session.get(TipoProfesion, idTipoProfesion)
    if not tipoProfesion:
        return {"error": "Tipo de Profesion no encontrado"}
    
    tipoProfesion.nombre = tipoProfesion_data["nombre"]
    tipoProfesion.descripcion = tipoProfesion_data.get("descripcion", "")
    
    session.add(tipoProfesion)
    session.commit()
    session.refresh(tipoProfesion)
    
    return tipoProfesion

@router.delete("/tipoProfesion/{idTipoProfesion}")
async def delete_tipoProfesion(
    idTipoProfesion: int,
    session: Session = Depends(get_session)
):
    tipoProfesion = session.get(TipoProfesion, idTipoProfesion)
    if not tipoProfesion:
        return {"error": "Tipo Profesion no encontrado"}
    
    # Validar que el tipo de profesion no este asignado algun profesional
    profesionales = session.exec(
        select(Profesional).where(Profesional.idTipoProfesion == idTipoProfesion)
    ).first()
    
    if profesionales is not None:
        return JSONResponse(
        content={"error": "No se puede eliminar el Tipo de Profesión porque está asignado a uno o más profesionales."},
        status_code=400
        )
    
    session.delete(tipoProfesion)
    session.commit()
    
    return {"message": "Tipo Profesion eliminado exitosamente"}

