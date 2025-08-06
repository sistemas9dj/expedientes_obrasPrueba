from sqlmodel import Session, select
from models.tipoObra import TipoObra
from typing import List, Optional

def get_all(session: Session) -> List[TipoObra]:
    return session.exec(select(TipoObra).order_by(TipoObra.nombre)).all()

def get_by_id(session: Session, id: int) -> Optional[TipoObra]:
    return session.get(TipoObra, id)

def create(session: Session, tipo: TipoObra) -> TipoObra:
    session.add(tipo)
    session.commit()
    session.refresh(tipo)
    return tipo

def update(session: Session, tipo: TipoObra) -> TipoObra:
    session.add(tipo)
    session.commit()
    session.refresh(tipo)
    return tipo

def delete(session: Session, tipo: TipoObra):
    session.delete(tipo)
    session.commit()