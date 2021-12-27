from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime

engine = create_engine("sqlite:///database.db")
# type: ignore


class RegistroChuva(SQLModel, table=True):  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    bairro: str
    data: datetime
    chuva: float

    def save(self):
        SQLModel.metadata.create_all(engine)
        with Session(engine) as session:
            session.add(self)
            session.commit()

    @classmethod
    def select_registro(cls):
        with Session(engine) as session:
            return session.exec(select(cls)).all()
