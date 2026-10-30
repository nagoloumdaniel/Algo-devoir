"""Tests HTTP de l'endpoint POST /api/v1/routing/emergency-path (T-W5, T-W6, T-W7).

Nécessite fastapi et httpx (voir requirements.txt).
"""

from fastapi.testclient import TestClient

from src.api import app

client = TestClient(app)
URL = "/api/v1/routing/emergency-path"


def test_post_valide_renvoie_200_et_le_chemin():
    response = client.post(URL, json={"coordinator_id": "C01", "target_hive_id": "H07"})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    body = response.json()
    assert body["status"] == "success"
    assert body["total_cost"] == 17.5
    assert body["path"] == ["BASE_NORD", "J1", "J2", "J3", "J4", "H07"]
    assert body["calculation_time_ms"] >= 0


def test_champs_optionnels_acceptes():
    response = client.post(URL, json={
        "coordinator_id": "C02", "target_hive_id": "H10",
        "urgence_niveau": "critique", "metadata": {"alerte": "anomalie_thermique"},
    })
    assert response.status_code == 200


def test_ids_en_minuscules_acceptes():
    response = client.post(URL, json={"coordinator_id": "c01", "target_hive_id": "h07"})
    assert response.status_code == 200


def test_champ_manquant_renvoie_422():
    response = client.post(URL, json={"coordinator_id": "C01"})
    assert response.status_code == 422


def test_mauvais_type_renvoie_422():
    response = client.post(URL, json={"coordinator_id": 1, "target_hive_id": "H07"})
    assert response.status_code == 422


def test_mauvais_format_renvoie_422():
    response = client.post(URL, json={"coordinator_id": "C01", "target_hive_id": "RUCHE7"})
    assert response.status_code == 422


def test_niveau_urgence_inconnu_renvoie_422():
    response = client.post(URL, json={"coordinator_id": "C01", "target_hive_id": "H07",
                                      "urgence_niveau": "apocalypse"})
    assert response.status_code == 422


def test_ruche_inexistante_renvoie_404():
    response = client.post(URL, json={"coordinator_id": "C01", "target_hive_id": "H99"})
    assert response.status_code == 404


def test_coordinateur_inexistant_renvoie_404():
    response = client.post(URL, json={"coordinator_id": "C09", "target_hive_id": "H01"})
    assert response.status_code == 404


def test_ruche_inaccessible_renvoie_status_error():
    response = client.post(URL, json={"coordinator_id": "C01", "target_hive_id": "H13"})
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "error"
    assert body["path"] == [] and body["total_cost"] is None


def test_get_renvoie_405():
    assert client.get(URL).status_code == 405


def test_documentation_openapi_disponible():
    assert client.get("/docs").status_code == 200
    schema = client.get("/openapi.json").json()
    assert URL in schema["paths"]