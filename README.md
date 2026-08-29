# Booking API
 
A secure REST API for managing appointments, built with FastAPI. Users can register, authenticate, and manage their own appointments — with ownership-based authorization and automatic double-booking prevention.
 
**Live demo:** https://booking-api-gtv0.onrender.com/docs
**Repository:** https://github.com/vaytrix911/Booking_API
 
## Features
 
- **JWT Authentication** — secure register/login flow with bcrypt password hashing
- **Ownership-based Authorization** — users can only view, edit, or delete their own appointments
- **Double-booking prevention** — automatically rejects appointments that overlap with an existing one for the same user
- **Full CRUD** — create, list, retrieve, update (PATCH), and delete appointments
- **Input validation** — enforced via Pydantic schemas (e.g. end time must be after start time)
- **Automated tests** — pytest suite covering auth success/failure, unauthorized access, and forbidden (cross-user) access attempts
## Tech Stack
 
- **FastAPI** — web framework
- **SQLAlchemy** — ORM
- **SQLite** — database
- **Pydantic** — request/response validation
- **python-jose** — JWT encoding/decoding
- **passlib (bcrypt)** — password hashing
- **pytest** — testing
- **Render** — deployment
## Project Structure
 
```
app/
├── main.py           # FastAPI app entrypoint, router registration
├── database.py        # DB engine, session, Base
├── models.py           # SQLAlchemy models (User, Appointment)
├── schemas.py          # Pydantic request/response schemas
├── security.py         # Password hashing, JWT creation
├── dependencies.py     # get_current_user (JWT verification)
└── routers/
    ├── auth.py          # /register, /login
    └── appointments.py  # Appointment CRUD
 
tests/
├── test_auth.py
└── test_appointments.py
```
 
## API Endpoints
 
| Method | Endpoint | Description | Auth Required |
|--------|----------|--------------|----------------|
| POST | `/register` | Create a new user account | No |
| POST | `/login` | Authenticate and receive a JWT | No |
| POST | `/appointments` | Create a new appointment | Yes |
| GET | `/appointments` | List the current user's appointments | Yes |
| GET | `/appointments/{id}` | Get a specific appointment | Yes (owner only) |
| PATCH | `/appointments/{id}` | Update a specific appointment | Yes (owner only) |
| DELETE | `/appointments/{id}` | Delete a specific appointment | Yes (owner only) |
 
## Security Notes
 
- Passwords are never stored in plain text — hashed with bcrypt before saving
- JWTs are short-lived and signed with a secret key stored in environment variables (never committed to source control)
- `owner_id` on appointments is always derived from the authenticated user's token, never trusted from client input, preventing ownership spoofing
- Attempting to access another user's appointment returns `403 Forbidden`; missing/invalid authentication returns `401 Unauthorized`
## Running Locally
 
```bash
git clone https://github.com/vaytrix911/Booking_API.git
cd Booking_API
pip install -r requirements.txt
 
# Create a .env file with:
# SECRET_KEY=your-secret-key
# ALGORITHM=HS256
# DATABASE_URL=sqlite:///./booking.db
 
uvicorn app.main:app --reload
```
 
Visit `http://127.0.0.1:8000/docs` for interactive API documentation.
 
## Running Tests
 
```bash
pytest
```
 
## Possible Future Improvements
 
- PostgreSQL support for persistent production storage
- Appointment status field (confirmed / cancelled / completed)
- Pagination for the appointments list endpoint
- Rate limiting on login attempts
 
