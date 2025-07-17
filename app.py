from fastapi import FastAPI, APIRouter, Request, HTTPException, Depends
from fastapi.staticfiles import StaticFiles

from routers.estadoExpediente import router 
from routers.inspector import router 
from routers.estadoExpediente import router as estadoExpedienteRouter
from routers.estadoInspeccion import router as estadoInspeccionRouter
from routers.inspector import router as inspectorRouter
from routers.tipoExpediente import router as tipoExpedienteRouter
from routers.tipoObra import router as tipoObraRouter
from routers.tipoProfesion import router as tipoProfesionRouter
from routers.profesional import router as profesionalRouter

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

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



@app.get("/", response_class=HTMLResponse)
async def get_estadosExpedientes(request: Request):
    return templates.TemplateResponse("layouts/layout.html", {"request": request})


