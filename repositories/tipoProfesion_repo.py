from sqlmodel import Session, select
from models.tipoProfesion import TipoProfesion
from typing import List, Optional


def get_all(session: Session) -> List[TipoProfesion]:
    return session.exec(select(TipoProfesion).order_by(TipoProfesion.nombre)).all()

def get_by_id(session: Session, id: int) -> Optional[TipoProfesion]:
    return session.get(TipoProfesion, id)

def create(session: Session, tipo: TipoProfesion) -> TipoProfesion:
    session.add(tipo)
    session.commit()
    session.refresh(tipo)
    return tipo

def update(session: Session, tipo: TipoProfesion) -> TipoProfesion:
    session.add(tipo)
    session.commit()
    session.refresh(tipo)
    return tipo

def delete(session: Session, tipo: TipoProfesion):
    session.delete(tipo)
    session.commit()