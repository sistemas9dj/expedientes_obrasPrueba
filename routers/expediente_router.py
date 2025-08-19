from fastapi import APIRouter, Depends, Body, Form, Request
from typing import List, Optional
from sqlmodel import Session, select
#from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import RedirectResponse
from config.conexion import get_session
from fastapi.templating import Jinja2Templates
from datetime import datetime
import json


from models.expediente_model import ExpedienteModel
from models.tipoObra_model import TipoObraModel
from models.profesional_model import ProfesionalModel
from models.estadoExpediente_model import EstadoExpedienteModel
from models.expediente_estadoExpediente_model import Expediente_EstadoExpedienteModel
from models.propietario_model import PropietarioModel

from services.expediente_service import ExpedienteService
from services.profesional_service import ProfesionalService
from services.tipoObra_service import TipoObraService
from services.estadoExpediente_service import EstadoExpedienteService

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/expedientes", response_model=List[ExpedienteModel])
async def get_expedientes(request: Request, session: Session = Depends(get_session)):

    service = ExpedienteService(session)  # ✅ instanciás la clase
    expedientes = service.listar_expedientes()  # ✅ usás el método de instancia

    service = TipoObraService(session)  # ✅ instanciás la clase
    tipoObras = service.listar_tipoObras()  # ✅ usás el método de instancia

    service = ProfesionalService(session)  # ✅ instanciás la clase
    profesionales = service.listar_profesionales()  # ✅ usás el método de instancia

    service = EstadoExpedienteService(session)  # ✅ instanciás la clase
    estadosExpedientes = service.listar_estados()  # ✅ usás el método de instancia

    return templates.TemplateResponse("listar_expedientes.html", { 
        "request": request,
        "expedientes": expedientes,
        "tiposObras": tipoObras,
        "profesionales": profesionales,
        "estadosExpedientes": estadosExpedientes
    })

@router.get("/agregar_expediente", response_model=ExpedienteModel)
async def agregar_expediente_get(request: Request, session: Session = Depends(get_session)):
     return templates.TemplateResponse("agregar_expediente.html",{"request":request})
                                      
@router.post("/agregar_expediente", response_model=ExpedienteModel)
async def agregar_expediente_post(
    request: Request,
    anioMesaEntrada : int = Form(...),
    nroExpedienteMesaEntrada: str = Form(...),
    nroPartida : str = Form(...),
    sucesion : int = Form(...),
    observaciones : str = Form(...),
    idTipoObra : int = Form(...),
    idFila: int = Form(...),  # cantPropietarios

    session: Session = Depends(get_session)
    ):
        service = ExpedienteService(session)  # ✅ instanciás la clase
        #armar nro de entrada....debe ser consecutivos por año. 
      #  nroEntrada = 1
        anioMesaEntrada = int(anioMesaEntrada) if anioMesaEntrada else None
        nroEntrada = service.obtener_proximo_nro_entrada(anioMesaEntrada)

        #fechaIngresoSistema = datetime.now()
        fechaUltimaMod = datetime.now()

         # Procesar propietarios
        valoresPropietarios = []
        for i in range(1, idFila + 1):  # recorre prop1...propN
            valor = (await request.form()).get(f"prop{i}", "").strip()
            # valor esperado: "cuil/apellido/nombre/figuraPpal/calle/nroCalle/piso/dpto/areaCel/nroCel/email"

            if valor:
                partes = valor.split("/")
                if len(partes) >= 11:
                    propietario = PropietarioModel(
                        cuil_cuit = partes[0],
                        apellido = partes[1],
                        nombre = partes[2],
                        figuraPpal = partes[3],
                        calle = partes[4],
                        nroCalle = partes[5],
                        piso = partes[6],
                        dpto = partes[7],
                        areaCelular = partes[8],
                        nroCelular = partes[9],
                        email = partes[10]
                    )
                    valoresPropietarios.append(propietario)
    
        nuevo_expediente = ExpedienteModel(
            nroEntrada=nroEntrada,
            anioMesaEntrada=anioMesaEntrada,
            nroExpedienteMesaEntrada=nroExpedienteMesaEntrada,
            nroPartida=nroPartida,
            sucesion=sucesion,
            observaciones=observaciones,
            idTipoObra=idTipoObra,
        #    fechaIngresoSistema=fechaIngresoSistema,
            fechaUltimaMod=fechaUltimaMod  
        )
                        
        service.crear_expediente(nuevo_expediente, valoresPropietarios)  # ✅ usás el método de instancia
        
        return RedirectResponse("/expedientes", status_code=303)
   

@router.put("/expediente/{idExpediente}", response_model=ExpedienteModel)
async def update_expediente(
    idExpediente: int,
    expediente_data: dict = Body(...),
    session: Session = Depends(get_session)
):
    expediente = session.get(ExpedienteModel, idExpediente)
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
    expediente.sucesion = clean_int(expediente_data.get("sucesion"))
    expediente.observaciones = clean_int(expediente_data.get("observaciones"))   

    #Agregar Nuevo estado si es que cambio
    idEstadoExpediente = clean_int(expediente_data.get("idEstadoExpNuevo"))
    idEstadoExpedienteActual = clean_int(expediente_data.get("idEstadoExpActual"))

    idEstadoExpedienteNuevo = idEstadoExpediente if idEstadoExpediente is not None and idEstadoExpediente != idEstadoExpedienteActual else None
    
    service = ExpedienteService(session)  # ✅ instanciás la clase
    service.actualizar_expediente(expediente, idEstadoExpedienteNuevo)

    #Agregar Propietarios
    idFilasPropietario = clean_int(expediente_data.get("idFila"))

    for i in range(1, idFilasPropietario):  
        valor = expediente_data.get(f"prop{i}", "").strip()  # prop1, prop2, etc.
        #de la forma  valor= cuil_cuit + "/" + apellido + "/" + nombre + "/" + figuraPpal + "/" + calle + "/" + nroCalle + "/" +piso+ "/" +dpto+ "/" +areaCelular+ "/" +nroCelular+ "/" +email;
         

    if valor:
        # Extraer curso y el resto después de la primera "/"
        pos = valor.find("/")
        if pos != -1:
            cuil = valor[:pos]
            resto = valor[pos + 1:]

            # Extraer idArea hasta la próxima "/"
            pos2 = resto.find("/")
            if pos2 != -1:
                apellido = resto[:pos2]
                resto = valor[pos2 + 2:]
            else:
                apellido = resto  # si no hay más "/"

                        # Extraer idArea hasta la próxima "/"
            pos3 = resto.find("/")
            if pos3 != -1:
                nombre = resto[:pos3]
                resto = valor[pos3 + 3:]
            else:
                nombre = resto  # si no hay más "/"
    
            #sql_insert_PostulanteCurso(idPostulante, curso, idArea)

    return expediente


@router.delete("/expediente/{idExpediente}")
async def delete_expediente(
    idExpediente: int,
    session: Session = Depends(get_session)
):
    service = ExpedienteService(session)  # ✅ instanciás la clase
    exito = service.eliminar_expediente(idExpediente)
    if not exito:
        return {"error": "Expediente no encontrado"}
      
    return {"message": "Expediente eliminado exitosamente"}


