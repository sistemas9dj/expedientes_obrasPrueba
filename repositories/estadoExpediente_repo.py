from sqlmodel import Session, select
from models.estadoExpediente import EstadoExpediente
from typing import List, Optional

def get_all(session: Session) -> List[EstadoExpediente]:
    return session.exec(select(EstadoExpediente).order_by(EstadoExpediente.nombre)).all()

def get_by_id(session: Session, id: int) -> Optional[EstadoExpediente]:
    return session.get(EstadoExpediente, id)

def create(session: Session, estado: EstadoExpediente) -> EstadoExpediente:
    session.add(estado)
    session.commit()
    session.refresh(estado)
    return estado

def update(session: Session, estado: EstadoExpediente) -> EstadoExpediente:
    session.add(estado)
    session.commit()
    session.refresh(estado)
    return estado

def delete(session: Session, estado: EstadoExpediente):
    session.delete(estado)
    session.commit()