from os import getenv

from dotenv import load_dotenv
from sqlalchemy.orm import Session

from api.utils.users import create_user, get_user_by_email
from schemas.user import UserCreate


def get_user_id(db: Session, bots_data: dict):
    # we put <discord_id>@<guild_id>.discord  as email of users
    # we should check if it exist, if so return the id
    # if not, create user and return the id
    email = (
        str(bots_data["discord_id"])
        + "@"
        + str(bots_data["discord_guild"])
        + ".discord"
    )
    load_dotenv()
    password = getenv("DBUPW") + "@!"

    db_user = get_user_by_email(db=db, email=email)
    if db_user:
        return db_user.id
    else:
        our_user = UserCreate(email=email, password=password)
        db_user = create_user(db=db, user=our_user)
        return db_user.id
