from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
def test_register_success():
    response = client.post("/register", json={"username": "testuser", "password": "1234"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
def test_login_success():
    client.post("/register", json={"username": "testuser2", "password": "1234"})
    response = client.post("/login", json={"username": "testuser2", "password": "1234"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
def test_login_wrong_password():
    client.post("/register", json={"username": "testuser3", "password": "1234"})
    response = client.post("/login", json={"username": "testuser3", "password": "4321"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
def test_get_appointments_unauthorized():
    response = client.get("/appointments")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
def test_forbidden_appointment_access():
    client.post("/register", json={"username": "testuser4", "password": "1234"})
    login_response1 = client.post("/login", json={"username": "testuser4", "password": "1234"})
    client.post("/register", json={"username": "testuser5", "password": "1234"})
    login_response2 = client.post("/login", json={"username": "testuser5", "password": "1234"})
    token = login_response1.json()["access_token"]
    headers1 = {"Authorization": f"Bearer {token}"}
    appointment_response = client.post(
    "/appointments",
    json={
        "title": "test",
        "start_time": "2026-01-01T10:00:00",
        "end_time": "2026-01-01T11:00:00"
    },
    headers=headers1
)    
    assert appointment_response.status_code == 200
    token2 = login_response2.json()["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}
    appointment_id = appointment_response.json()["id"]
    response = client.get(f"/appointments/{appointment_id}", headers=headers2)
    assert response.status_code == 403