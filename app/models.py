import enum
import typing

from sqlmodel import Column, Enum, Field, SQLModel


class Status(int, enum.Enum):
    TODO = 0
    DOING = 1
    COMPLETED = 2


class Task(SQLModel):
    id: typing.Optional[int] = Field(default=None, primary_key=True)
    parent_id: typing.Optional[int] = Field(default=None)
    name: str
    status: int = Field(sa_column=Column(Enum(Status), default=Status.TODO))
    is_archived: bool = False

    class Config:
        table = True


class TaskCreate(SQLModel):
    parent_id: typing.Optional[int] = Field(default=None)
    name: str
    status: int = Status.TODO


class TaskUpdate(SQLModel):
    parent_id: typing.Optional[int] = None
    name: typing.Optional[str] = None
    status: typing.Optional[int] = None
