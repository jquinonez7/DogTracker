from pydantic import BaseModel
from typing import Optional

class DogCreate(BaseModel):
    user_id: int
    name: str
    breed: Optional[str] = None
    sex: Optional[str] = None
    age: Optional[str] = None

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str


# Pydantic Model that will be used in the 
# token endpoint for the response
class Token(BaseModel):
    access_token: str
    token_type: str
