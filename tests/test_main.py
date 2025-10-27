from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_all_alunos_success():
    response = client.get("/alunos")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "nome" in data[0]
    
def test_get_aluno_by_id_success():
    response = client.get("/alunos/1")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == 1
    
def test_create_student_success():
    response = client.post(
        "/alunos",
        json={
            "nome": "Ana Luisa",
            "email": "analuisa@examplo.com",
        },
    )
    data = response.json()
    assert response.status_code == 201
    assert data["nome"] == "Ana Luisa"


def test_get_aluno_by_id_not_found():
    response = client.get("/alunos/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Aluno não encontrado"}

def test_create_aluno_duplicate_email():
    client.post(
        "/alunos",
        json={"nome": "Nicolle Vitalino Fujii", "email": "nicollefujii@examplo.com"},
    )
    response = client.post(
        "/alunos",
        json={"nome": "Nicole Luzia Vitalino", "email": "nicollefujii@examplo.com"},
    )
    assert response.status_code == 400
    assert "Já existe" in response.json()["detail"]
