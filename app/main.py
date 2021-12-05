from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, SQLModel, select

from db import engine, get_session
from models import Task, TaskCreate, TaskUpdate


app = FastAPI(debug=True)


@app.on_event("startup")
def on_startup() -> None:
    from config import settings
    print(settings.DATABASE_URI)
    SQLModel.metadata.create_all(engine)


@app.get("/health")
async def healthcheck() -> str:
    return "OK"


@app.get("/tasks", response_model=list[Task])
async def get_tasks_list(db: Session = Depends(get_session)) -> list[Task]:
    db_query = select(Task).where(Task.is_archived == False, Task.parent_id == None)
    tasks = db.exec(db_query).all()
    return tasks


@app.post("/tasks", response_model=Task)
async def create_task(task: TaskCreate, db: Session = Depends(get_session)) -> Task:
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int, db: Session = Depends(get_session)) -> Task:
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task is not found"
        )
    return task


@app.put("/tasks/{task_id}")
async def update_task(
    task_id: int, task: TaskUpdate, db: Session = Depends(get_session)
) -> None:
    db_task = db.get(Task, task_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task is not found"
        )
    if db_task.is_archived:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Task is already archived"
        )
    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.get("/tasks/{task_id}/tasks", response_model=list[Task])
async def get_subtasks(task_id: int, db: Session = Depends(get_session)) -> list[Task]:
    tasks = db.exec(select(Task).where(Task.parent_id == task_id)).all()
    return tasks
