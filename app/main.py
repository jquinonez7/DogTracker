from fastapi import FastAPI, status, HTTPException
from .database import init_db, get_session
from .models import Dog
from .models import User
from .auth import hash_password, verify_password, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, create_access_token 
from .schemas import DogCreate
from .schemas import UserCreate
from .schemas import UserLogin
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from jose import JWTError, jwt



app = FastAPI(title = "Dog Health Tracker")

@app.get("/health") #run app.get
def health(): #define health 
    return {"ok": True}

@app.get("/dogs") #run app.get
def dogs(): #define dog
    with get_session() as session: #open database and close as leave block
        dogs_list = session.query(Dog).all() #assign the query result to dogs_list
        return dogs_list #return list of dogs

#decorator tells FastAPI, when GET request to /dogs/<some number> run the function below
@app.get("/dogs/{dog_id}")
#dog_id comes from the URL and is automatically converted to an int by FastAPI
def get_dog(dog_id: int):
    #opens a temporary connection (session) to the database.
    with get_session() as session:
        # This looks in the Dog table and finds ONE row
        # where the primary key (id) equals dog_id.
        # If no dog exists with that id, this returns None.
        dog = session.get(Dog, dog_id)
        if dog is None:
            raise HTTPException(status_code=404, detail="Dog not found")
        # This sends the dog back to the client as JSON.
        # FastAPI automatically converts the Dog object into JSON.
        return dog



@app.post("/dogs")
def create_dog(dog_data: DogCreate): #endpoint expects data from the user, data should follow  DogCreate schema.
    with get_session() as session: #open database session
        dog = Dog( #assigns that new Dog object to a variable named dog
           user_id=dog_data.user_id, #create new Dog user in memory
           name=dog_data.name, #create new Dog name in memory
           breed=dog_data.breed, #create new Dog breed in memory
           sex=dog_data.sex, #create new Dog sex in memory
           age=dog_data.age #create new Dog age in memory
        )
        session.add(dog) #adds new dog object
        session.commit() #saves the object
        session.refresh(dog) #gets ID from the database back into your dog object
        return dog

@app.delete("/dogs/{dog_id}") #delete dog function
def delete_dog(dog_id: int):
    with get_session() as session: #open database session
         dog = session.get(Dog, dog_id)
         if dog is None:
            raise HTTPException(status_code=404, detail="Dog not found")
         session.delete(dog)
         session.commit()
    return {"message": f"Dog {dog_id} successfully removed"}

@app.post("/auth/register")
def register(user_data: UserCreate):
    with get_session() as session:
        hashed_password = hash_password(user_data.password)

        user = User(
            email=user_data.email,
            password_hash=hashed_password,
        )

        session.add(user)

        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            # Email already exists
            raise HTTPException(
                status_code=400,
                detail="Email already registered",
            )

        session.refresh(user)
        return {"id": user.id, "email": user.email}

@app.post("/auth/login")
def login(user_data: UserLogin):
        with get_session() as session: #open database session
            user = session.query(User).filter(User.email == user_data.email).first() #assign the query result to user

        if not user: #check if user
            return {"error": "Invalid email or password"}

        if not verify_password(user_data.password, user.password_hash): #check if valid login
            return {"error": "Invalid email or password"}
        
        access_token = create_access_token(
            data={"sub": user.email}
            )
        return {
    "access_token": access_token,
    "token_type": "bearer",
    "id": user.id,
    "email": user.email
    }
