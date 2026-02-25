from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Numbers(BaseModel):
    num1: int
    num2: int

@app.get("/")
async def root():
    return {"message": "Добро пожаловать в моёприложение FastAPI!"}

@app.post("/calcul")
async def calcul(numbers: Numbers):
    result = numbers.num1 + numbers.num2
    return {"result": result}

