from sqlmodel import Session, select
from models.inspector import Inspector
from typing import List, Optional

def get_all(session: Session) -> List[Inspector]:
    return session.exec(select(Inspector).order_by(Inspector.apellido)).all()

def get_by_id(session: Session, id: int) -> Optional[Inspector]:
    return session.get(Inspector, id)

def create(session: Session, inspector: Inspector) -> Inspector:
    session.add(inspector)
    session.commit()
    session.refresh(inspector)
    return inspector

def update(session: Session, inspector: Inspector) -> Inspector:
    session.add(inspector)
    session.commit()
    session.refresh(inspector)
    return inspector

def delete(session: Session, inspector: Inspector):
    session.delete(inspector)
    session.commit()