from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime

class estado_Usuario (str, Enum):
    activo= "activo"
    inactivo = "inactivo"
    eliminado = "eliminado"


class Usuario (SQLModel, table= True):
    __tablename__ = "usuarios"
    id : Optional[int]=Field(default=None, primary_key=True)
    nombre : str
    email : str
    estado : estado_Usuario = Field(default=estado_Usuario.activo)
    premium : bool = False


# Modelo de Tarea
class EstadoTarea(str, Enum):
    pendiente = "Pendiente"
    en_ejecucion = "En ejecución"
    realizada = "Realizada"
    cancelada = "Cancelada"


class Tarea(SQLModel, table=True):
    __tablename__ = "tareas"
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    fecha_creacion: datetime
    fecha_modificacion: datetime
    estado: EstadoTarea
    usuario_id: int = Field(foreign_key="usuarios.id")

class EstadoTarea(str, Enum):
    pendiente = "Pendiente"
    en_ejecucion = "En ejecución"
    realizada = "Realizada"
    cancelada = "Cancelada"

# Modelo para crear tareas (entrada)
class TareaCreate(SQLModel):
    nombre: str
    descripcion: str
    estado: EstadoTarea
    usuario_id: int
