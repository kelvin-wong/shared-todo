import threading

from sqlmodel import Session, select

from db import get_session
from models import Status, Task


WAIT_TIME_SECONDS = 3 * 60


def archive_tasks() -> None:
    print('Archive completed tasks')
    session: Session = next(get_session())
    completed_tasks = session.exec(
        select(Task).where(
            Task.is_archived == False, Task.status == Status.COMPLETED
        )
    ).all()
    for task in completed_tasks:
        task.is_archived = True
    session.commit()


def start_service() -> None:
    ticker = threading.Event()
    archive_tasks()
    while not ticker.wait(WAIT_TIME_SECONDS):
        archive_tasks()


if __name__ == "__main__":
    start_service()
