from sqlmodel import Session, select
from models.tipoObra import TipoObra
from typing import List, Optional

def get_all(session: Session) -> List[TipoObra]:
    return session.exec(select(TipoObra).order_by(TipoObra.nombre)).all()

def get_by_id(session: Session, id: int) -> Optional[TipoObra]:
    return session.get(TipoObra, id)

def create(session: Session, estado: TipoObra) -> TipoObra:
    session.add(estado)
    session.commit()
    session.refresh(estado)
    return estado

def update(session: Session, estado: TipoObra) -> TipoObra:
    session.add(estado)
    session.commit()
    session.refresh(estado)
    return estado

def delete(session: Session, estado: TipoObra):
    session.delete(estado)
    session.commit()