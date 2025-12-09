from typing import Optional, List
from datetime import datetime, date
from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    """
    App user (account). Holds login identity.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)  # unique constraint: no duplicate accounts
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    # Reverse link: one user can have many dogs
    dogs: List["Dog"] = Relationship(back_populates="owner")

# table=True → makes a database table named 'dog'
class Dog(SQLModel, table=True):
    # id → primary key (unique for each dog)
    # Optional[int] → starts as None until saved
    # Field(..., primary_key=True) → lets SQLite auto-assign 1, 2, 3, …
    id: Optional[int] = Field(default=None, primary_key=True)
    # Foreign key: which user owns this dog.
    # - integer that must match an existing User.id
    # - enforces “this dog must belong to a real user”
    user_id: int = Field(foreign_key="user.id", index=True)
    name: str
    #optional info
    breed: Optional[str] = None
    dob: Optional[date] = None
    sex: Optional[str] = None     # e.g., "M", "F", "Other"
    avatar_url: Optional[str] = None
    notes: Optional[str] = None
     # Reverse link back to the user
    owner: Optional[User] = Relationship(back_populates="dogs")
 
