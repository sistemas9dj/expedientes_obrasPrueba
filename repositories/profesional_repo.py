from sqlmodel import Session, select
from models.profesional import Profesional
from typing import List, Optional
from sqlalchemy.orm import selectinload

def get_all(session: Session) -> List[Profesional]:
    return session.exec(select(Profesional)
                                .options(selectinload(Profesional.tipoProfesion))  # ✅ esta es la relación
                                .order_by(Profesional.apellido)).all()

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

def get_by_idTipoProefesion(session: Session, id: int) ->  Profesional:
    return session.exec(select(Profesional).where(Profesional.idTipoProfesion == id)).first()

def get_by_cuit(session: Session, id:int, cuil: int) -> List[Profesional]:
    return session.exec(select(Profesional).where(Profesional.idProfesional != id and Profesional.cuil_cuit == cuil)).all()
                                