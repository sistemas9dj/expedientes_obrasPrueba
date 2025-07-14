from fastapi import APIRouter, Depends, Body, Form
from typing import List
from sqlmodel import Session, select
from models.inspector import Inspector
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Request
from config.conexion import get_session
from config.conexion import session_dep 
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/inspectores", response_model=List[Inspector])
async def get_inspectores(request: Request, session: Session = Depends(get_session)):
    inspectores = session.exec(select(Inspector).order_by(Inspector.apellido)).all()
   
    return templates.TemplateResponse("listar_inspectores.html", { 
        "request": request,
        "inspectores": inspectores
    })

@router.get("/agregar_inspector", response_model=Inspector)
async def agregar_inspector_get(request: Request, session: Session = Depends(get_session)):
    return templates.TemplateResponse("agregar_inspector.html",{"request":request})
                                      
@router.post("/agregar_inspector", response_model=Inspector)
async def agregar_inspector_post(
    nombre : str = Form(...),
    apellido: str = Form(...),
    session: Session = Depends(get_session)
):
    nuevo_inspector = Inspector(
        nombre=nombre,
        apellido=apellido)
    
    session.add(nuevo_inspector)
    session.commit()
    session.refresh(nuevo_inspector)
    return RedirectResponse("/inspectores", status_code=303)

@router.put("/inspector/{idInspector}", response_model=Inspector)
async def update_inspector(
    idInspector: int,
    inspector_data: dict = Body(...),
    session: Session = Depends(get_session)
):
    inspector = session.get(Inspector, idInspector)
    if not inspector:
        return {"error": "Inspector no encontrado"}
    
    inspector.nombre = inspector_data["nombre"]
    inspector.apellido = inspector_data.get("apellido", "")
    
    session.add(inspector)
    session.commit()
    session.refresh(inspector)
    
    return inspector

@router.delete("/inspector/{idInspector}")
async def delete_inspector(
    idInspector: int,
    session: Session = Depends(get_session)
):
    inspector = session.get(Inspector, idInspector)
    if not inspector:
        return {"error": "Inspector no encontrado"}
    
    session.delete(inspector)
    session.commit()
    
    return {"message": "Inspector eliminado exitosamente"}



