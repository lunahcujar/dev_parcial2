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

