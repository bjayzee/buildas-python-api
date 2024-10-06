from pydantic import BaseModel, ConfigDict


class CreateUser(BaseModel):
    username: str
    name: str
    email: str
    password: str

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: str
    password: str

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

    model_config = ConfigDict(from_attributes=True)