from fastapi import APIRouter, Depends, Body, Form
from typing import List, Optional
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from models.profesional import Profesional
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Request
from config.conexion import get_session
from fastapi.templating import Jinja2Templates
from models.tipoProfesion import TipoProfesion


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/profesionales", response_model=List[Profesional])
async def get_profesionales(request: Request, session: Session = Depends(get_session)):

    profesionales = session.exec(
        select(Profesional)
        .options(selectinload(Profesional.tipoProfesion))  # ✅ esta es la relación
        .order_by(Profesional.apellido)
    ).all()
    
    tiposProfesiones = session.exec(
        select(TipoProfesion).order_by(TipoProfesion.nombre)
    ).all()
   
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
    
    request: Request,
    cuil_cuit : str = Form(...),
    nombre : str = Form(...),
    apellido: str = Form(...),
    razonSocial : str = Form(default=None),
    calle : str = Form(default=None),
    nroCalle : Optional[str] = Form(None),
    nroDpto : str = Form(default=None),
    piso : str = Form(default=None),
    areaCelular : Optional[str] = Form(None),
    nroCelular : Optional[str] = Form(None),
    matricula : str = Form(default=None),
    email : str = Form(default=None),
    idTipoProfesion : int = Form(...),  # debe ser int
    
    
    session: Session = Depends(get_session)
):
    
    # Validar CUIL duplicado
    profesional_existente = session.exec(
        select(Profesional).where(Profesional.cuil_cuit == cuil_cuit)
    ).first()
    
    if profesional_existente:
        return HTMLResponse(content="""
            <script>
              alert("verifique el Cuil/Cuit. Ya existe un profesional registrado con ese CUIL.");
              history.back();  // vuelve al formulario sin cerrar el modal
            </script>
        """, status_code=200)

    nro_calle_int = int(nroCalle) if nroCalle else None
    area_celular_int = int(areaCelular) if areaCelular else None
    nro_celular_int = int(nroCelular) if nroCelular else None

    nuevo_profesional = Profesional(
        cuil_cuit = cuil_cuit,
        nombre  = nombre,
        apellido = apellido,
        razonSocial  = razonSocial,
        calle  = calle,
        nroCalle  = nro_calle_int,
        nroDpto  = nroDpto,
        piso  = piso,
        areaCelular  = area_celular_int,
        nroCelular  = nro_celular_int,
        matricula  = matricula,
        email  = email,
        idTipoProfesion = idTipoProfesion   
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

    # Helper para convertir campos vacíos a None
    def clean_int(value):
        return int(value) if isinstance(value, int) or (isinstance(value, str) and value.strip().isdigit()) else None
    
    profesional.cuil_cuit = profesional_data["cuil_cuit"]
    profesional.nombre = profesional_data["nombre"]
    profesional.apellido = profesional_data["apellido"]
    profesional.razonSocial = profesional_data.get("razonSocial")
    profesional.calle = profesional_data.get("calle")
    profesional.nroCalle = clean_int(profesional_data.get("nroCalle"))
    profesional.nroDpto = profesional_data.get("nroDpto")
    profesional.piso = profesional_data.get("piso")
    profesional.areaCelular = clean_int(profesional_data.get("areaCelular"))
    profesional.nroCelular = clean_int(profesional_data.get("nroCelular"))
    profesional.matricula = profesional_data.get("matricula")
    profesional.email = profesional_data.get("email")
    profesional.idTipoProfesion = clean_int(profesional_data.get("idTipoProfesion"))
    
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
