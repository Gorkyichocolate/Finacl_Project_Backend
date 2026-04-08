from pydantic import BaseModel, EmailStr

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: str | None = None


class UserInDB(User):
    hashed_password: str
