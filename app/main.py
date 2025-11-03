from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel, EmailStr
import httpx

app = FastAPI()

BASE_URL = "https://jsonplaceholder.typicode.com/users"


class User(BaseModel):
    id: int
    name: str
    email: EmailStr


@app.get("/")
def root():
    return {"message": "Mocking and Fixture's testing endpoints "}


@app.get("/users")
def list_users(limit: int = 5):
    response = requests.get(BASE_URL)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro ao acessar API externa")
    users = response.json()
    return users[:limit]


@app.get("/users/{user_id}")
def get_user(user_id: int):
    response = requests.get(f"{BASE_URL}/{user_id}")
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro na API externa")
    return response.json()


@app.post("/users", status_code=201)
def post_user(user: User):
    response = httpx.post(BASE_URL, json=user.model_dump())
    if response.status_code not in (200, 201):
        raise HTTPException(status_code=502, detail="Erro ao criar usuário")
    return response.json()
