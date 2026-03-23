import pytest
from fastapi.testclient import TestClient
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the API app (to be implemented)
try:
    from api import app
except ImportError:
    app = None

@pytest.mark.skipif(app is None, reason="API app not implemented yet")
def test_suggest_move_api_valid_fen(monkeypatch):
    client = TestClient(app)
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    response = client.post("/suggest-move", json={"fen": fen})
    assert response.status_code == 200
    data = response.json()
    assert "move" in data
    assert isinstance(data["move"], str)
    assert len(data["move"]) in (4, 5)

@pytest.mark.skipif(app is None, reason="API app not implemented yet")
def test_suggest_move_api_invalid_fen(monkeypatch):
    client = TestClient(app)
    response = client.post("/suggest-move", json={"fen": "invalid-fen"})
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Invalid FEN" in data["detail"]

@pytest.mark.skipif(app is None, reason="API app not implemented yet")
def test_suggest_move_api_missing_fen(monkeypatch):
    client = TestClient(app)
    response = client.post("/suggest-move", json={})
    assert response.status_code == 422  # FastAPI validation error
