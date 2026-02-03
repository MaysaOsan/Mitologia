from fastapi import FastAPI, HTTPException, Depends, Form
from datetime import date
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from typing import Annotated
from contextlib import asynccontextmanager
from sqlmodel import Session, select

from data.db import init_db, get_session
from models.seres import Ser

import uvicorn

@asynccontextmanager 
async def lifespan(application: FastAPI): #esta función se ejecuta antes de que el servidor se inicie
    init_db()
    yield

SessionDep = Annotated[Session, Depends(get_session)] #se usa para inyectar la sesión en las funciones

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

## Página Web
#página de inicio
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    mensaje = "Bienvenido a la aplicación de series de mitología"
    return templates.TemplateResponse("index.html", {"request": request, "mensaje": mensaje})
#página de lista de series
@app.get("/seres", response_class=HTMLResponse)
async def listar_seres(request: Request, session: SessionDep):
    seres = session.exec(select(Ser)).all()
    return templates.TemplateResponse("seres.html", {"request":request, "seres": seres})

##Paginas Web para crear, editar y eliminar un Ser
#página de crear un nuevo ser
@app.get("/seres/crearSer", response_class=HTMLResponse)
async def crear_ser_form(request: Request):
    return templates.TemplateResponse("crear_ser.html", {"request": request})

@app.post("/seres/crearSer", response_class=HTMLResponse)
async def crear_ser(
    request: Request,
    session: SessionDep,
    nombre: str = Form(...),
    raza: str = Form(...),
    titulo: str = Form(None),
    esDios: bool = Form(False),
    fechaDeCreacion: date = Form(None)
):
    nuevo_ser = Ser(
        nombre=nombre,
        raza=raza,
        titulo=titulo,
        esDios=esDios,
        fechaDeCreacion=fechaDeCreacion
    )

    session.add(nuevo_ser)
    session.commit()
    session.refresh(nuevo_ser)

    return templates.TemplateResponse(
        "detalle_seres.html",
        {"request": request, "ser": nuevo_ser}
    )

#página de moficiar un ser
@app.get("/seres/editar/{ser_id}", response_class=HTMLResponse)
async def editar_ser_form(ser_id: int, request: Request, session: SessionDep):
    ser = session.get(Ser, ser_id)
    if not ser:
        raise HTTPException(status_code=404, detail="No se encontro el ser")
    return templates.TemplateResponse("editar_ser.html", {"request": request, "ser": ser})

@app.post("/seres/editar/{ser_id}", response_class=HTMLResponse)
async def editar_ser(
    request: Request,
    session: SessionDep, 
    ser_id: int,
    nombre: str = Form(...),
    raza: str = Form(...),
    titulo: str = Form(None),
    esDios: bool = Form(False),
    fechaDeCreacion: date = Form(None)
):
    ser = session.get(Ser, ser_id)
    if not ser:
        raise HTTPException(status_code=404, detail="No se encontro el ser")
    ser.nombre = nombre
    ser.raza = raza
    ser.titulo = titulo
    ser.esDios = esDios
    ser.fechaDeCreacion = fechaDeCreacion
    session.commit()
    session.refresh(ser)
    return templates.TemplateResponse(
        "detalle_seres.html",
        {"request": request, "ser": ser}
    )

#página de eliminar un ser
@app.get("/seres/eliminar/{ser_id}", response_class=HTMLResponse)
async def eliminar_ser_form(ser_id: int, request: Request, session: SessionDep):
    ser = session.get(Ser, ser_id)
    if not ser:
        raise HTTPException(status_code=404, detail="No se encontro el ser")
    return templates.TemplateResponse("eliminar_ser.html", {"request": request, "ser": ser})

@app.post("/seres/eliminar/{ser_id}", response_class=HTMLResponse)
async def eliminar_ser(
    ser_id: int,
    request: Request,
    session: SessionDep 
):
    ser = session.get(Ser, ser_id)
    if not ser:
        raise HTTPException(status_code=404, detail="No se encontro el ser")
    session.delete(ser)
    session.commit()
    return templates.TemplateResponse(
        "seres.html",
        {"request": request, "seres": session.exec(select(Ser)).all()})

#página de detalle de una serie dinámica // RECO: que vaya al final.Rutas "fijas" arriba, rutas dinámicas abajo
@app.get("/seres/{ser_id}", response_class=HTMLResponse)
async def buscar_ser_por_id(ser_id: int, request: Request, session: SessionDep):
    ser_encontrado = session.get(Ser, ser_id)
    if not ser_encontrado:
        raise HTTPException(status_code=404, detail="No se encontro el ser")
    return templates.TemplateResponse("detalle_seres.html", {"request": request, "ser": ser_encontrado})


## Servicios web basados en REST

@app.get("/api/seres", response_model=list[Ser])
async def api_lista_seres(session: SessionDep):
    return session.exec(select(Ser)).all()


@app.post("/api/seres", response_model=Ser, status_code=201)
async def api_añadir_ser(ser: Ser, session: SessionDep):
    session.add(ser)
    session.commit()
    session.refresh(ser)
    return ser

@app.put("/api/seres/{ser_id}", response_model=Ser)
async def api_actualizar_ser(ser_id: int, ser_actualizado: Ser, session: SessionDep):
    ser = session.get(Ser, ser_id)
    if not ser: 
        raise HTTPException(status_code=404, detail="No se encontro el ser")

    if ser_actualizado.nombre:
        ser.nombre = ser_actualizado.nombre
    if ser_actualizado.raza:
        ser.raza = ser_actualizado.raza
    if ser_actualizado.titulo:
        ser.titulo = ser_actualizado.titulo
    if ser_actualizado.esDios is not None:
        ser.esDios = ser_actualizado.esDios
    if ser_actualizado.fechaDeCreacion: 
        ser.fechaDeCreacion = ser_actualizado.fechaDeCreacion
    session.commit()
    session.refresh(ser)
    return ser

@app.delete("/api/seres/{ser_id}", status_code=204)
async def api_eliminar_ser(ser_id: int, session: SessionDep):
    ser = session.get(Ser, ser_id)
    if not ser:
        raise HTTPException(status_code=404, detail="No se encontro el ser")
    session.delete(ser)
    session.commit()
    return None


## Ejecutar

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)