from fastapi import APIRouter, Depends, Body, Form
from typing import List
from sqlmodel import Session, select
from models.profesional import Profesional
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Request
from config.conexion import get_session
from config.conexion import session_dep 
from fastapi.templating import Jinja2Templates
from models.tipoProfesion import TipoProfesion

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/profesionales", response_model=List[Profesional])
async def get_profesionales(request: Request, session: Session = Depends(get_session)):
    profesionales = session.exec(select(Profesional).order_by(Profesional.apellido)).all()
    tiposProfesiones = session.exec(select(TipoProfesion).order_by(TipoProfesion.nombre)).all()
   
    return templates.TemplateResponse("listar_profesionales.html", { 
        "request": request,
        "profesionales": profesionales,
         "tiposProfesiones": tiposProfesiones
    })

@router.get("/agregar_profesional", response_model=Profesional)
async def agregar_profesional_get(request: Request, session: Session = Depends(get_session)):
    return templates.TemplateResponse("agregar_profesional.html",{"request":request})
                                      
@router.post("/agregar_profesional", response_model=Profesional)
async def agregar_profesional_post(
    cuil_cuit : str = Form(...),
    nombre : str = Form(...),
    apellido: str = Form(...),
    razonSocial : str = Form(...),
    calle : str = Form(...),
    nroCalle : int = Form(...),
    nroDpto : str = Form(...),
    piso : str = Form(...),
    areaCelular : int = Form(...),
    nroCelular : int = Form(...),
    matricula : str = Form(...),
    email : str = Form(...),
    session: Session = Depends(get_session)
):
    nuevo_profesional = Profesional(
        cuil_cuit = cuil_cuit,
        nombre  = nombre,
        apellido = apellido,
        razonSocial  = razonSocial,
        calle  = calle,
        nroCalle  = nroCalle,
        nroDpto  = nroDpto,
        piso  = piso,
        areaCelular  = areaCelular,
        nroCelular  = nroCelular,
        matricula  = matricula,
        email  = email   
        )
    
    session.add(nuevo_profesional)
    session.commit()
    session.refresh(nuevo_profesional)
    return RedirectResponse("/profesionales", status_code=303)

@router.put("/profesional/{idProfesional}", response_model=Profesional)
async def update_profesional(
    idProfesional: int,
    profesional_data: dict = Body(...),
    session: Session = Depends(get_session)
):
    profesional = session.get(Profesional, idProfesional)
    if not profesional:
        return {"error": "Profesional no encontrado"}
    
    profesional.cuil_cuit = profesional_data["cuil_cuit"]
    profesional.nombre = profesional_data["nombre"]
    profesional.apellido = profesional_data["apellido"]
    profesional.razonSocial = profesional_data.get("razonSocial", "")
    profesional.calle = profesional_data.get("calle", "")
    profesional.nroCalle = profesional_data.get("nroCalle", "")
    profesional.nroDpto = profesional_data.get("nroDpto", "")
    profesional.piso = profesional_data.get("piso", "")
    profesional.areaCelular = profesional_data.get("areaCelular")
    profesional.nroCelular = profesional_data.get("nroCelular")
    profesional.matricula = profesional_data.get("matricula", "")
    profesional.email = profesional_data.get("email", "")
    
    session.add(profesional)
    session.commit()
    session.refresh(profesional)
    
    return profesional

@router.delete("/profesional/{idProfesional}")
async def delete_profesional(
    idProfesional: int,
    session: Session = Depends(get_session)
):
    profesional = session.get(Profesional, idProfesional)
    if not profesional:
        return {"error": "Profesional no encontrado"}
    
    session.delete(profesional)
    session.commit()
    
    return {"message": "Profesional eliminado exitosamente"}
