from sqlmodel import Session, select
from models.profesional import Profesional
from typing import List, Optional

def get_all(session: Session) -> List[Profesional]:
    return session.exec(select(Profesional).order_by(Profesional.apellido)).all()

def get_by_id(session: Session, id: int) -> Optional[Profesional]:
    return session.get(Profesional, id)

def create(session: Session, profesional: Profesional) -> Profesional:
    session.add(profesional)
    session.commit()
    session.refresh(profesional)
    return profesional

def update(session: Session, profesional: Profesional) -> Profesional:
    session.add(profesional)
    session.commit()
    session.refresh(profesional)
    return profesional

def delete(session: Session, profesional: Profesional):
    session.delete(profesional)
    session.commit()