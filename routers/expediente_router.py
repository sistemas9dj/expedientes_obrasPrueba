from fastapi import APIRouter, Depends, Body, Form, Request
from typing import List
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import RedirectResponse,JSONResponse
from config.conexion import get_session
from fastapi.templating import Jinja2Templates
from datetime import datetime
from fastapi import status

from models.expediente_model import ExpedienteModel
#from models.tipoObra_model import TipoObraModel
from models.profesional_model import ProfesionalModel
from models.expediente_profesional_model import Expediente_ProfesionalModel
#from models.estadoExpediente_model import EstadoExpedienteModel
#from models.expediente_estadoExpediente_model import Expediente_EstadoExpedienteModel
from models.propietario_model import PropietarioModel

from services.expediente_service import ExpedienteService
from services.profesional_service import ProfesionalService
from services.tipoObra_service import TipoObraService
from services.estadoExpediente_service import EstadoExpedienteService

router = APIRouter()

templates = Jinja2Templates(directory="templates")

# -------------------------------
# LISTAR EXPEDIENTES
# -------------------------------
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

# -------------------------------
# AGREGAR EXPEDIENTE (GET)
# -------------------------------
@router.get("/agregar_expediente", response_model=ExpedienteModel)
async def agregar_expediente_get(request: Request, session: Session = Depends(get_session)):
     return templates.TemplateResponse("agregar_expediente.html",{"request":request})

# -------------------------------
# AGREGAR EXPEDIENTE (POST)
# -------------------------------                                      
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
        anioMesaEntrada = int(anioMesaEntrada) if anioMesaEntrada else None
        #armar nro de entrada....debe ser consecutivos por año. 
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

                    nro_calle_int = int(partes[5]) if partes[5] else None
                    area_celular_int = int(partes[8]) if  partes[8] else None
                    nro_celular_int = int(partes[9]) if partes[9] else None
                    figuraPpal_int = int(partes[3]) if partes[3] else 0

                    propietario = PropietarioModel(
                        cuil_cuit = partes[0],
                        apellido = partes[1],
                        nombre = partes[2],
                        figuraPpal = partes[3],
                        calle = partes[4],
                        nroCalle = nro_calle_int,# partes[5],
                        piso = partes[6],
                        nroDpto = partes[7],
                        areaCelular = area_celular_int, #partes[8],
                        nroCelular = nro_celular_int,#partes[9],
                        email = partes[10]
                    )
                    valoresPropietarios.append({
                        "propietario": propietario,
                        "figuraPpal": figuraPpal_int
                    })
                    
    
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

        # Procesar profesionales
        valoresExpedientesProfesionales = []
        for i in range(1, idFila + 1):  # recorre prof1...profN
            valor = (await request.form()).get(f"prof{i}", "").strip()
            # valor esperado: "idProfesional/contactoPpal"

            if valor:
                partes = valor.split("/")
                if len(partes) >= 2:

                    expProfesional = Expediente_ProfesionalModel(
                        idProfesional = int(partes[0]) if partes[0] else None,
                        contactoPpal = partes[1],
                       # fechaIngresoSistema=datetime.now() 
                    )
                    valoresExpedientesProfesionales.append(expProfesional)
                    
    
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
        

        exito = service.crear_expediente(nuevo_expediente, valoresPropietarios, valoresExpedientesProfesionales)  
        
        if "/" not in exito:
            # No contiene "/"
            parte1=""
        else:
            # Contiene "/"
            parte1, parte2 = exito.split("/")

        if parte1 == "duplicado":
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"error": "El Cuil/Cuit " + parte2 + " ingresado ya fue asignado a un Propietario. Verifique la información."}
            )
        
        else:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Expediente agregado exitosamente"}
            )

# ---------------------------------------
# OBTENER PROPIETARIOS DE UN EXPEDIENTE
# ---------------------------------------
#Retorna solo los propietarios de un expediente determinado. Relacion N a N
@router.get("/expediente/{idExpediente}/propietarios", response_model=List[PropietarioModel])
def get_propietarios_expediente(idExpediente: int, session: Session = Depends(get_session)):
    service = ExpedienteService(session)
    return service.get_propietarios(idExpediente)

# ---------------------------------------
# OBTENER PROFESIONALES DE UN EXPEDIENTE
# ---------------------------------------
#Retorna solo los propietarios de un expediente determinado. Relacion N a N
@router.get("/expediente/{idExpediente}/profesionales", response_model=List[ProfesionalModel])
def get_profesionales_expediente(idExpediente: int, session: Session = Depends(get_session)):
    service = ExpedienteService(session)
    return service.get_profesionales(idExpediente)

# -------------------------------
# ACTUALIZAR EXPEDIENTE
# -------------------------------
@router.put("/expediente/{idExpediente}", response_model=ExpedienteModel)
async def update_expediente(
    idExpediente: int,
    expediente_data: dict = Body(...),
    session: Session = Depends(get_session)
):
    fechaUltimaMod = datetime.now()

    expediente = ExpedienteModel(
        idExpediente = idExpediente,
        nroEntrada=expediente_data["nroEntrada"],
        anioMesaEntrada=expediente_data["anioMesaEntrada"],
        nroExpedienteMesaEntrada=expediente_data["nroExpedienteMesaEntrada"],
        nroPartida=expediente_data["nroPartida"],
        sucesion=expediente_data["sucesion"],
        observaciones=expediente_data["observaciones"],
        idTipoObra=expediente_data["idTipoObra"],
        fechaUltimaMod=fechaUltimaMod  
    )

    service = ExpedienteService(session)

    #Leer estado anterios
    idEstadoExpedienteAnterior=expediente_data["IDESTADOEXPEDIENTEEditHIDDEN"]
    #Leer el nuevo estado
    idEstadoExpedienteNuevo=expediente_data["idEstadoexpedienteEdit"]

#    print("""==============================================================""")
#    print("""PROPIETARIOS ROUTER""")
#    print("""==============================================================""")
   
    valoresPropietarios = []
    for valor in expediente_data.get("propietarios", []):  # recorre prop1...propN
        # valor esperado: "cuil/apellido/nombre/figuraPpal/calle/nroCalle/piso/dpto/areaCel/nroCel/email"
        partes = valor.split("/")
        if len(partes) >= 11:

                propietario = PropietarioModel(
                    cuil_cuit = partes[0],
                    apellido = partes[1],
                    nombre = partes[2],
                    figuraPpal = partes[3],
                    calle = partes[4],
                    nro_calle_int = int(partes[5]) if partes[5] not in (None, "", "null") else None,
                    piso = partes[6],
                    nroDpto = partes[7],
                    area_celular_int = int(partes[8]) if partes[8] not in (None, "", "null") else None,
                    nro_celular_int = int(partes[9]) if partes[9] not in (None, "", "null") else None,
                    email = partes[10]
                )
                valoresPropietarios.append(propietario)
    
 
    #print("Cantidad de propietarios router:!!!!!!!!", len(valoresPropietarios))

        print("""==============================================================""")
        print("""   PROFESIONALES ROUTER""")
        print("""==============================================================""")
    #Leer cantidad de propietarios
   # idFila: int = int(expediente_data["idFilaProfEdit"])  # cantProFESIONALES

    valoresProfesionales = []
    for valor in expediente_data.get("profesionales", []):  # recorre prop1...propN
        # valor esperado: "idProfesional/contactoPpal"
        partes = valor.split("/")
        if len(partes) >= 2:

                profesional = ProfesionalModel(
                    idProfesional = int(partes[0]) if partes[0] not in (None, "", "null") else None,
                    contactoPpal = partes[1]
                )
                valoresProfesionales.append(profesional)

    exito = service.actualizar_expediente(expediente,idEstadoExpedienteAnterior,idEstadoExpedienteNuevo,valoresPropietarios,valoresProfesionales)
    
    if exito == "noExiste":
        return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={"error": "Expediente no encontrado."}
                )
    else:    
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Expediente actualizado exitosamente"}
        )

# -------------------------------
# ELIMINAR EXPEDIENTE
# -------------------------------
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


# -------------------------------------------------
# FUNCION AUXILIAR: ACTUALIZAR PROPIETARIOS N a N
# -------------------------------------------------
'''def actualizar_propietarios(session: Session, idExpediente: int, lista_propietarios: list[dict]):
    # Relaciones actuales
    relaciones_actuales = session.exec(
        select(Expediente_PropietarioModel).where(Expediente_PropietarioModel.idExpediente == idExpediente)
    ).all()
    ids_actuales = [r.idPropietario for r in relaciones_actuales]

    # IDs enviados
    ids_enviados = [p.get('idPropietario') for p in lista_propietarios if p.get('idPropietario')]

    # Eliminar relaciones que ya no están
    for r in relaciones_actuales:
        if r.idPropietario not in ids_enviados:
            session.delete(r)

    # Agregar nuevos propietarios o relaciones
    for p in lista_propietarios:
        idP = p.get('idPropietario')
        propietario = None
        if idP:
            propietario = session.get(PropietarioModel, idP)

        if not propietario:
            propietario = PropietarioModel(**p)
            session.add(propietario)
            session.flush()  # Para generar idPropietario

        # Agregar relación si no existía
        existe_relacion = session.exec(
            select(Expediente_PropietarioModel)
            .where(Expediente_PropietarioModel.idExpediente == idExpediente)
            .where(Expediente_PropietarioModel.idPropietario == propietario.idPropietario)
        ).first()

        if not existe_relacion:
            relacion = Expediente_PropietarioModel(
                idExpediente=idExpediente,
                idPropietario=propietario.idPropietario
            )
            session.add(relacion)
'''