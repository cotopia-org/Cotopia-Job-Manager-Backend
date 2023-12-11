from fastapi import FastAPI

from api import users
from db.db_setup import engine
from db.models import user

user.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Manager API",
    description="Better Than A Taskmanager",
    version="0.0.1",
    contact={
        "name": "Ali Kharrati",
        "email": "ali.kharrati@gmail.com",
    }
)

app.include_router(users.router)
