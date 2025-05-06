from contextlib import asynccontextmanager
from http.client import HTTPException
from typing import List

from fastapi import FastAPI, Depends
from sqlmodel import Session
from data.models import *
from sqlmodel.ext.asyncio.session import AsyncSession
from operations.operations_db import *

from utils.connection_db import init_db, get_session
# LIFESPAN: Se ejecuta una vez al inicio del servidor
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

# SOLO una instancia de FastAPI
app = FastAPI(lifespan=lifespan)

# ENDPOINT DE PRUEBA
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# ENDPOINT PARA CREAR USUARIO
@app.post("/usuarios")
async def crear_usuario( nuevo_usuario: Usuario, session: AsyncSession = Depends(get_session)):
    session.add(nuevo_usuario)
    await session.commit()
    await session.refresh(nuevo_usuario)
    return nuevo_usuario


@app.get("/usuarios", response_model=List[Usuario])
async def listar_usuarios(session: AsyncSession = Depends(get_session)):
    return await obtener_todos_usuarios(session)

@app.get("/usuarios/{usuario_id}", response_model=Usuario)
async def get_usuario(usuario_id: int, session: AsyncSession = Depends(get_session)):
    usuario = await obtener_usuario_por_id(usuario_id, session)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.put("/usuarios/{usuario_id}/estado", response_model=Usuario)
async def update_estado_usuario(usuario_id: int, nuevo_estado: estado_Usuario, session: AsyncSession = Depends(get_session)):
    usuario = await actualizar_estado_usuario(usuario_id, nuevo_estado, session)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.put("/usuarios/{usuario_id}/premium", response_model=Usuario)
async def convertir_en_premium(usuario_id: int, session: AsyncSession = Depends(get_session)):
    usuario = await hacer_usuario_premium(usuario_id, session)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.get("/usuarios/estado/activo", response_model=List[Usuario])
async def listar_usuarios_activos(session: AsyncSession = Depends(get_session)):
    return await get_usuarios_activos(session)

@app.get("/usuarios/estado/activo/premium", response_model=List[Usuario])
async def listar_usuarios_activos_premium(session: AsyncSession = Depends(get_session)):
    return await obtener_usuarios_premium_activos(session)


#Endpoints de Tarea

# Crear nueva tarea
@app.post("/tareas", response_model=Tarea)
async def crear_tarea(nueva_tarea: Tarea, session: AsyncSession = Depends(get_session)):
    try:
        session.add(nueva_tarea)
        await session.commit()
        await session.refresh(nueva_tarea)
        return nueva_tarea
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear tarea: {str(e)}")

@app.get("/tareas", response_model=List[Tarea])
async def listar_todas_tareas(session: AsyncSession = Depends(get_session)):
    return await obtener_todas_tareas(session)

@app.get("/tareas/{tarea_id}", response_model=Tarea)
async def obtener_tarea_por_id(tarea_id: int, session: AsyncSession = Depends(get_session)):
    tarea = await obtener_tarea_por_id(tarea_id, session)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea

@app.put("/tareas/{tarea_id}/estado", response_model=Tarea)
async def actualizar_estado(tarea_id: int, nuevo_estado: EstadoTarea, session: AsyncSession = Depends(get_session)):
    tarea = await actualizar_estado_tarea(tarea_id, nuevo_estado, session)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea

@app.get("/tareas/usuario/{usuario_id}", response_model=List[Tarea])
async def listar_tareas_por_usuario(usuario_id: int, session: AsyncSession = Depends(get_session)):
    return await obtener_tareas_por_usuario(usuario_id, session)

@app.get("/tareas/estado/realizada", response_model=List[Tarea])
async def listar_tareas_realizadas(session: AsyncSession = Depends(get_session)):
    tareas = await obtener_tareas_realizadas(session)
    if not tareas:
        raise HTTPException(status_code=404, detail="No hay tareas realizadas")
    return tareas

@app.get("/tareas/estado/{estado}", response_model=List[Tarea])
async def listar_tareas_por_estado(estado: EstadoTarea, session: AsyncSession = Depends(get_session)):
    return await obtener_tareas_por_estado(estado, session)