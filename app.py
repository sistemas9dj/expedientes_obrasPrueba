from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from routers.estadoExpediente_router import router as estadoExpedienteRouter
from routers.estadoInspeccion_router import router as estadoInspeccionRouter
from routers.inspector_router import router as inspectorRouter
from routers.tipoExpediente_router import router as tipoExpedienteRouter
from routers.tipoObra_router import router as tipoObraRouter
from routers.tipoProfesion_router import router as tipoProfesionRouter
from routers.profesional_router import router as profesionalRouter
from routers.expediente_router import router as expedienteRouter

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# ----------------------
# IMPORTAR MODELOS (REGISTRA RELACIONES)
# ----------------------
import models  # ⚡ Importante: registra todos los modelos antes de crear tablas

app = FastAPI()

# Montar la carpeta "static"
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(estadoExpedienteRouter, prefix="", tags=["estadosExpedientes"])
app.include_router(estadoInspeccionRouter, prefix="", tags=["estadosInspecciones"])
app.include_router(inspectorRouter, prefix="", tags=["inspectores"])
app.include_router(tipoExpedienteRouter, prefix="", tags=["tiposExpedientes"])
app.include_router(tipoObraRouter, prefix="", tags=["tiposObras"])
app.include_router(tipoProfesionRouter, prefix="", tags=["tiposProfesiones"])
app.include_router(profesionalRouter, prefix="", tags=["profesionales"])
app.include_router(expedienteRouter, prefix="", tags=["expedientes"])

@app.get("/enConstruccion", response_class=HTMLResponse)
async def en_construccion(request: Request):
    return templates.TemplateResponse("enConstruccion.html", {"request": request})

@app.get("/", response_class=HTMLResponse)
async def get_estadosExpedientes(request: Request):
    return templates.TemplateResponse("layouts/layout.html", {"request": request})



