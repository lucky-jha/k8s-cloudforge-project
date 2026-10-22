from app import app


def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_index():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"CloudForge" in response.data

def test_info():
    client = app.test_client()
    response = client.get("/api/info")
    assert response.status_code == 200
    assert response.get_json()["service"] == "cloudforge-app"