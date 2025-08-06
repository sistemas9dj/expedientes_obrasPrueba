from sqlmodel import Session, select
from models.tipoExpediente import TipoExpediente
from typing import List, Optional

def get_all(session: Session) -> List[TipoExpediente]:
    return session.exec(select(TipoExpediente).order_by(TipoExpediente.nombre)).all()

def get_by_id(session: Session, id: int) -> Optional[TipoExpediente]:
    return session.get(TipoExpediente, id)

def create(session: Session, tipo: TipoExpediente) -> TipoExpediente:
    session.add(tipo)
    session.commit()
    session.refresh(tipo)
    return tipo

def update(session: Session, tipo: TipoExpediente) -> TipoExpediente:
    session.add(tipo)
    session.commit()
    session.refresh(tipo)
    return tipo

def delete(session: Session, tipo: TipoExpediente):
    session.delete(tipo)
    session.commit()