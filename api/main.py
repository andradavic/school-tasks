from fastapi import FastAPI
from app.endpoints import login, tasks

app = FastAPI()

app.include_router(login.router)
app.include_router(tasks.router)