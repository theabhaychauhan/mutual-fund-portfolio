from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True
