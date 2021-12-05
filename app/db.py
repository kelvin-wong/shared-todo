import typing

from sqlmodel import Session, create_engine

from models import *
from config import settings


engine = create_engine(settings.DATABASE_URI)


def get_session() -> typing.Generator:
    with Session(engine) as session:
        yield session
