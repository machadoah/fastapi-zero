from pydantic import BaseModel, ConfigDict, EmailStr

from fastapi_zero.models import TodoState


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    # o config_dict é um objeto que permite que você defina configurações para
    # o modelo ele é utilizado para definir que os atributos do modelo serão
    # convertidos para um dicionário e não para um objeto
    model_config = ConfigDict(from_attributes=True)


class UserDB(UserSchema):
    id: int


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState


class TodoPublic(TodoSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)
