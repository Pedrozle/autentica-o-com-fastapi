from pydantic import BaseModel


class User(BaseModel):
    name: str
    username: str
    email: str
    email_seg: str
    password: str
    perfil: int
