from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import comments, jobs, users, bot
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
    servers=[
        {
            "url": "https://jobs-api.cotopia.social",
            "description": "Staging environment",
        },
        {"url": "http://127.0.0.1:8000", "description": "Local environment"},
    ],
)

origins = [
    "https://jobs-api.cotopia.social",
    "https://jobs-api.cotopia.social/",
    "https://insight.cotopia.social/",
    "https://insight.cotopia.social",
    "http://localhost:8787/",
    "http://localhost:8787",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(comments.router)
app.include_router(jobs.router)
app.include_router(bot.router)
