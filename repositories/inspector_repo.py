from sqlmodel import Session, select
from models.inspector import Inspector
from typing import List, Optional

def get_all(session: Session) -> List[Inspector]:
    return session.exec(select(Inspector).order_by(Inspector.apellido)).all()

def get_by_id(session: Session, id: int) -> Optional[Inspector]:
    return session.get(Inspector, id)

def create(session: Session, estado: Inspector) -> Inspector:
    session.add(estado)
    session.commit()
    session.refresh(estado)
    return estado

def update(session: Session, estado: Inspector) -> Inspector:
    session.add(estado)
    session.commit()
    session.refresh(estado)
    return estado

def delete(session: Session, estado: Inspector):
    session.delete(estado)
    session.commit()