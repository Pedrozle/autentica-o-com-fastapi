from pydantic import BaseModel


class User(BaseModel):
    name: str
    username: str
    email: str
    email_seg: str
    password: str
    perfil: int


class Login(BaseModel):
    email: str
    password: str


class Autenticatable(BaseModel):
    username: str
    token: str


class UpdateLogin(BaseModel):
    username: str
    perfil: int
