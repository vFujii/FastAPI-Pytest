from fastapi import HTTPException
from app.model import Aluno, AlunoCreate

alunos_db = [Aluno(id=1, nome="Nicolle", email="nicollefujii@exemplo.com")]


def get_all_alunos():
    return alunos_db


def get_aluno_by_id(aluno_id: int):
    for aluno in alunos_db:
        if aluno.id == aluno_id:
            return aluno
    raise HTTPException(status_code=404, detail="Aluno não encontrado")


def create_aluno(aluno: AlunoCreate):
    for a in alunos_db:
        if a.email == aluno.email:
            raise HTTPException(status_code=400, detail="Já existe")

    new_id = max(a.id for a in alunos_db) + 1 if alunos_db else 1
    new_aluno = Aluno(id=new_id, nome=aluno.nome, email=aluno.email)
    alunos_db.append(new_aluno)
    return new_aluno
