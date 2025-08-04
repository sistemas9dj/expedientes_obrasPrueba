from sqlmodel import Session, select
from models.estadoInspeccion import EstadoInspeccion
from typing import List, Optional

def get_all(session: Session) -> List[EstadoInspeccion]:
    return session.exec(select(EstadoInspeccion).order_by(EstadoInspeccion.nombre)).all()

def get_by_id(session: Session, id: int) -> Optional[EstadoInspeccion]:
    return session.get(EstadoInspeccion, id)

def create(session: Session, estado: EstadoInspeccion) -> EstadoInspeccion:
    session.add(estado)
    session.commit()
    session.refresh(estado)
    return estado

def update(session: Session, estado: EstadoInspeccion) -> EstadoInspeccion:
    session.add(estado)
    session.commit()
    session.refresh(estado)
    return estado

def delete(session: Session, estado: EstadoInspeccion):
    session.delete(estado)
    session.commit()