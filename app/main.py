from fastapi import FastAPI
from app.routers import auth, appointments

app = FastAPI()

app.get("/")
def hello():
    return {"message":"hello bro"}
app.include_router(auth.router)
app.include_router(appointments.router)