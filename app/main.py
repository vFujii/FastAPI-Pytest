from fastapi import FastAPI
from app.model import Aluno, AlunoCreate
import app.crud as crud

app = FastAPI(title="API Alunos")

# Rota GET – Listar todos os alunos
@app.get("/alunos", response_model=list[Aluno])
def listar_alunos():
    return crud.get_all_alunos()

# Rota GET – Buscar aluno por ID
@app.get("/alunos/{aluno_id}", response_model=Aluno)
def buscar_aluno(aluno_id: int):
    return crud.get_aluno_by_id(aluno_id)

# Rota POST – Criar novo aluno
@app.post("/alunos", response_model=Aluno, status_code=201)
def criar_aluno(aluno: AlunoCreate):
    return crud.create_aluno(aluno)
