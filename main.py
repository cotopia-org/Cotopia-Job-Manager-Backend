from fastapi import FastAPI

from api import comments, jobs, users
from db.db_setup import engine
from db.models import comment, job, user

user.Base.metadata.create_all(bind=engine)
comment.Base.metadata.create_all(bind=engine)
job.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Manager API",
    description="Better Than A Taskmanager",
    version="0.42",
    contact={
        "name": "Ali Kharrati",
        "email": "ali.kharrati@gmail.com",
    },
)

app.include_router(users.router)
app.include_router(comments.router)
app.include_router(jobs.router)
