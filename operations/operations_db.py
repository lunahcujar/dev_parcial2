from sqlmodel import Session, select
from data.models import Usuario
from utils.connection_db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from data.models import *
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

async def hacer_usuario_premium(usuario_id: int, session: AsyncSession):
    usuario_db = await session.get(Usuario, usuario_id)
    if not usuario_db:
        return None
    usuario_db.premium = True
    await session.commit()
    await session.refresh(usuario_db)
    return usuario_db


async def obtener_todos_usuarios(session: AsyncSession):
    result = await session.exec(select(Usuario))
    return result.all()

async def obtener_usuario_por_id(usuario_id: int, session: AsyncSession):
    return await session.get(Usuario, usuario_id)


async def actualizar_estado_usuario(usuario_id: int, nuevo_estado: estado_Usuario, session: AsyncSession):
    usuario = await session.get(Usuario, usuario_id)
    if not usuario:
        return None
    usuario.estado = nuevo_estado
    await session.commit()
    await session.refresh(usuario)
    return usuario

async def hacer_usuario_premium(usuario_id: int, session: AsyncSession):
    usuario_db = await session.get(Usuario, usuario_id)
    if not usuario_db:
        return None
    usuario_db.premium = True
    await session.commit()
    await session.refresh(usuario_db)
    return usuario_db


async def get_usuarios_activos(session: AsyncSession):
    query = select(Usuario).where(Usuario.estado == estado_Usuario.activo)
    result = await session.execute(query)
    return result.scalars().all()


async def obtener_usuarios_premium_activos(session: AsyncSession):
    consulta = select(Usuario).where(
        Usuario.estado == "activo",
        Usuario.premium == True
    )
    resultado = await session.exec(consulta)
    return resultado.all()




#operaciones Tarea

# Crear una nueva tarea
async def crear_tarea(tarea: Tarea, session: AsyncSession) -> Tarea:
    session.add(tarea)
    await session.commit()
    await session.refresh(tarea)
    return tarea

# Obtener todas las tareas
async def obtener_todas_tareas(session: AsyncSession) :
    result = await session.exec(select(Tarea))
    return result.all()

# Obtener tarea por ID
async def obtener_tarea_por_id(tarea_id: int, session: AsyncSession) :
    return await session.get(Tarea, tarea_id)

# Actualizar estado de una tarea
async def actualizar_estado_tarea(tarea_id: int, nuevo_estado: EstadoTarea, session: AsyncSession) :
    tarea = await session.get(Tarea, tarea_id)
    if not tarea:
        return None
    tarea.estado = nuevo_estado
    tarea.fecha_modificacion = datetime.utcnow()
    await session.commit()
    await session.refresh(tarea)
    return tarea

# Obtener tareas por usuario
async def obtener_tareas_por_usuario(usuario_id: int, session: AsyncSession):
    query = select(Tarea).where(Tarea.usuario_id == usuario_id)
    result = await session.exec(query)
    return result.all()

# Obtener tareas realizadas
async def obtener_tareas_realizadas(session: AsyncSession):
    query = select(Tarea).where(Tarea.estado == EstadoTarea.realizada)
    result = await session.exec(query)
    return result.all()

# Obtener tareas por estado
async def obtener_tareas_por_estado(estado: EstadoTarea, session: AsyncSession) :
    query = select(Tarea).where(Tarea.estado == estado)
    result = await session.exec(query)
    return result.all()
