from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    org_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: UUID | None = None
    org_id: UUID | None = None

class UserOut(BaseModel):
    id: UUID
    org_id: UUID
    email: str
    role: str

    class Config:
        from_attributes = True
