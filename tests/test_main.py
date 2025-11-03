import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_user_data():
    return [
        {"id": 1, "name": "Alice Johnson", "email": "alice@example.com"},
        {"id": 2, "name": "Bob Smith", "email": "bob@example.com"},
    ]


@pytest.fixture
def mock_individual_user():
    return {"id": 1, "name": "Alice Johnson", "email": "alice@example.com"}


@pytest.fixture
def mock_success_requests(mocker):
    def _mock(data, status_code=200):
        mock_response = mocker.Mock()
        mock_response.status_code = status_code
        mock_response.json.return_value = data
        mocker.patch("requests.get", return_value=mock_response)
        return mock_response

    return _mock


@pytest.fixture
def mock_success_post_requests(mocker):
    def _mock(data, status_code=201):
        mock_response = mocker.Mock()
        mock_response.status_code = status_code
        mock_response.json.return_value = data
        mocker.patch("httpx.post", return_value=mock_response)
        return mock_response

    return _mock


@pytest.fixture
def mock_error_requests(mocker):
    def _mock(status_code=500):
        mock_response = mocker.Mock()
        mock_response.status_code = status_code
        mock_response.json.return_value = {"detail": "Erro simulado"}
        mocker.patch("requests.get", return_value=mock_response)
        return mock_response

    return _mock


def test_get_all_users_success(client, mock_user_data, mock_success_requests):
    mock_success_requests(mock_user_data)
    response = client.get("/users?limit=2")
    assert response.status_code == 200
    assert response.json() == mock_user_data


def test_get_user_by_id_success(client, mock_individual_user, mock_success_requests):
    mock_success_requests(mock_individual_user)
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Alice Johnson"


def test_post_user_success(client, mock_success_post_requests):
    new_user = {"id": 10, "name": "Charlie Brown", "email": "charlie@example.com"}
    mock_success_post_requests(new_user)
    response = client.post("/users", json=new_user)
    assert response.status_code == 201
    assert response.json()["name"] == "Charlie Brown"


def test_get_users_error(client, mock_error_requests):
    mock_error_requests(status_code=500)
    response = client.get("/users")
    assert response.status_code == 500
    assert "erro ao acessar api externa" in response.json()["detail"].lower()
