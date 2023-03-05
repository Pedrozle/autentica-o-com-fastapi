import pytest
import requests


def test_connection():
    data = {"email": "pedrozle@outlook.com", "password": "str1"}
    response = requests.post("http://localhost:8000/login", json=data)
    assert response.status_code == 401
    assert response.json() == {"logado": False, "motivo": "senha incorreta"}


def test_login_success():
    data = {"email": "pedrozle@outlook.com", "password": "str"}
    response = requests.post("http://localhost:8000/login", json=data)
    assert response.status_code == 200
    assert response.json() == {
        "logado": True,
        "username": "PEDROZLE",
        "perfil": 1,
        "autenticado": False,
    }


def test_login_incorrect_pwd():
    data = {"email": "pedrozle@outlook.com", "password": "str1"}
    response = requests.post("http://localhost:8000/login", json=data)
    assert response.status_code == 401
    assert response.json() == {"logado": False, "motivo": "senha incorreta"}


def test_login_not_found():
    data = {"email": "pedrozle@gmail.com", "password": "str"}
    response = requests.post("http://localhost:8000/login", json=data)
    assert response.status_code == 404
    assert response.json() == {"logado": False, "motivo": "usuario não encontrado"}
