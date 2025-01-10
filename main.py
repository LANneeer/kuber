from fastapi import FastAPI, BackgroundTasks
from celery import Celery
from pydantic import BaseModel

app = FastAPI()

celery_app = Celery(broker="amqp://rabbitmq", backend="redis://redis:6379/0")


# Models
class Task(BaseModel):
    name: str


@app.get("/")
def main_page():
    return {"message": "hello world"}


@app.post("/task")
def create_task(task: Task, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_celery_task, task.name)
    return {"message": "Task created", "name": task.name}


@celery_app.task
def run_celery_task(name: str):
    print(f"Processing task: {name}")
    return f"Processed task: {name}"
