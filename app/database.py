from sqlmodel import SQLModel, create_engine, Session
from contextlib import contextmanager
import os
from .models import Dog, User  # <-- this line is important

#engine = “plug” to the database
#init_db() = “make sure my tables exist”
#get_session() = “open the database for a moment, do stuff, then close it”

# Use SQLite locally; swap to Postgres later by setting DATABASE_URL in env.
# this says where my database lives 
DB_URL = os.environ.get("DATABASE_URL", "sqlite:///./dogtracker.db")

# For SQLite, we need check_same_thread=False when used with async servers.
# this creates the connection and lets app talk to database
engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False} if DB_URL.startswith("sqlite") else {}
)

#makes sure values/tables exist in database
#called at start of app
def init_db() -> None:
    """Create tables from SQLModel metadata (no-op if they already exist)."""
    SQLModel.metadata.create_all(engine)

#helper function
#allows us to "borrow key" to database
@contextmanager
def get_session():
    """Provide a short-lived session. Always closes — even on errors."""
    with Session(engine) as session:
        yield session
