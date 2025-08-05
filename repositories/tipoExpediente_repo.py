from sqlmodel import Session, select
from models.tipoExpediente import TipoExpediente
from typing import List, Optional

def get_all(session: Session) -> List[TipoExpediente]:
    return session.exec(select(TipoExpediente).order_by(TipoExpediente.nombre)).all()

def get_by_id(session: Session, id: int) -> Optional[TipoExpediente]:
    return session.get(TipoExpediente, id)

def create(session: Session, estado: TipoExpediente) -> TipoExpediente:
    session.add(estado)
    session.commit()
    session.refresh(estado)
    return estado

def update(session: Session, estado: TipoExpediente) -> TipoExpediente:
    session.add(estado)
    session.commit()
    session.refresh(estado)
    return estado

def delete(session: Session, estado: TipoExpediente):
    session.delete(estado)
    session.commit()