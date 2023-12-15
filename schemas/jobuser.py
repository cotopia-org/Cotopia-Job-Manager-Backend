from pydantic import BaseModel


class JobUser(BaseModel):
    id: int
    is_active: bool
    first_name: str | None = None
    last_name: str | None = None
    discord_user_id: int | None = None
    email: str
