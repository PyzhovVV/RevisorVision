from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str


class UserCreate(BaseUser):
    password: str


class User(BaseUser):
    id: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'