# DogTracker Backend

DogTracker is a FastAPI backend for a dog health-tracking application.
Right now the project includes authentication, database setup, and a basic API structure. The backend is fully functional on its own and serves as the foundation for the future frontend and full health-logging features.

## Features (Current)

### Authentication

* JWT-based login and authorization
* Password hashing
* `get_current_user` dependency for protected routes

### Database

* SQLModel models
* SQLite database (`dogtracker.db`)
* Session handling via `database.py`

### API Structure

* Modular routers under `/app/routers`
* `main.py` includes router registration and app creation
* Pydantic schemas for input/output validation

## How Authentication Works

1. User logs in with email/username + password.
2. Password is verified using hash functions in `auth.py`.
3. A JWT access token is generated with the user’s identity in the payload (`sub`).
4. Protected routes depend on `get_current_user`, which:

   * extracts the token
   * decodes it
   * validates it
   * loads the user from the database
5. If invalid, a 401 is raised.

## Future Plans

* Dog model + owner relationship
* CRUD routes for meals, symptoms, meds, and notes
* Frontend UI (React + Vite + Tailwind)
* Deployment to production
* Push notifications or alerts for health reminders
