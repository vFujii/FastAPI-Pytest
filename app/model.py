from pydantic import BaseModel, EmailStr


class Aluno(BaseModel):
    id: int
    nome: str
    email: EmailStr


class AlunoCreate(BaseModel):
    nome: str
    email: EmailStr
