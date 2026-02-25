from fastapi import FastAPI
from models import User

app = FastAPI()

user = User(
    name="Egor Evtushenko",
    id=1
)

@app.get("/users")
async def users():
    return user
