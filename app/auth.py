from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from .models import User
from .database import init_db, get_session

# Secret key used to sign JWTs.
# In a real app, this should come from an environment variable, not be hard-coded.
SECRET_KEY = "9bcc186dae486c3134ad4eb7dc7b0917660f77c41de4ce953666939f2ad4f0f1"

# Algorithm used to sign tokens. HS256 is standard for symmetric keys.
ALGORITHM = "HS256"

# How long a login should last (in minutes)
# 60 * 24 * 30  = 30 days
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30  # 30 days

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

#creates secure password hashing system using bcrypt that can use throughout app
password_hasher = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

#turn plain-text password into a secure hashed password for the database.
def hash_password(password: str) -> str:
    # bcrypt only supports passwords up to 72 bytes.
    # To be safe, we cut any longer password down before hashing.
    if len(password) > 72:
        password = password[:72]

    return password_hasher.hash(password)


#check if plain-text password matches the hashed password from database.
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hasher.verify(plain_password, hashed_password)


# this function will create the token
# for particular data
def create_access_token(data: dict):
    to_encode = data.copy()
    
    # expire time of the token
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    # return the generated token
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    with get_session() as session:
        user = session.query(User).filter(User.email == email).first()

    if user is None:
        raise credentials_exception

    return user
