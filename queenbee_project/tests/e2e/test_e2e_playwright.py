"""Tests E2E (Playwright) de l'API QueenBee via Swagger UI et le client HTTP.

Lance un vrai serveur uvicorn, pilote un vrai navigateur Chromium, vérifie les
réponses et enregistre des captures d'écran nommées dans docs/captures/.

    python -m pytest tests/e2e -v
"""

import json
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest

playwright_sync = pytest.importorskip("playwright.sync_api")
sync_playwright = playwright_sync.sync_playwright

ROOT = Path(__file__).resolve().parents[2]
CAPTURES = ROOT / "docs" / "captures"
ENDPOINT = "/api/v1/routing/emergency-path"


def _free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="module")
def base_url():
    port = _free_port()
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "src.api:app", "--port", str(port), "--log-level", "warning"],
        cwd=ROOT)
    url = f"http://127.0.0.1:{port}"
    for _ in range(60):
        try:
            socket.create_connection(("127.0.0.1", port), timeout=0.5).close()
            break
        except OSError:
            time.sleep(0.25)
    yield url
    proc.terminate()
    proc.wait(timeout=10)


@pytest.fixture(scope="module")
def browser_page(base_url):
    CAPTURES.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto(f"{base_url}/docs")
        page.wait_for_selector(".opblock-post .opblock-summary", timeout=30000)
        yield page
        browser.close()


def _shot(page, name):
    page.screenshot(path=str(CAPTURES / name))


def _execute_in_swagger(page, body):
    """Ouvre l'opération POST, remplace le corps JSON et clique sur Execute."""
    block = page.locator(".opblock-post")
    if "is-open" not in (block.get_attribute("class") or ""):
        page.locator(".opblock-post .opblock-summary").click()
    page.wait_for_selector("button.try-out__btn")
    if "cancel" not in (page.locator("button.try-out__btn").first.get_attribute("class") or ""):
        page.locator("button.try-out__btn").first.click()
    page.wait_for_selector(".body-param__text")
    page.locator(".body-param__text").fill(json.dumps(body, indent=2))
    page.locator("button.execute").click()
    page.wait_for_selector(".live-responses-table tbody .response-col_status", timeout=10000)
    return page.locator(".live-responses-table tbody .response-col_status").first.inner_text().strip()


def test_01_swagger_ui_documente_l_endpoint(browser_page):
    page = browser_page
    assert page.locator(".opblock-post .opblock-summary").count() == 1
    assert ENDPOINT in page.locator(".opblock-summary-path").inner_text()
    _shot(page, "01_swagger_documentation_endpoint.png")


def test_02_swagger_chemin_nominal_200(browser_page):
    page = browser_page
    status = _execute_in_swagger(page, {"coordinator_id": "C01", "target_hive_id": "H07",
                                        "urgence_niveau": "critique"})
    assert status.startswith("200")
    body = page.locator(".live-responses-table .microlight").first.inner_text()
    data = json.loads(body)
    assert data["status"] == "success" and data["path"][0] == "BASE_NORD" and data["path"][-1] == "H07"
    assert data["total_cost"] == 17.5
    page.locator(".live-responses-table").scroll_into_view_if_needed()
    _shot(page, "02_swagger_requete_nominale_200_succes.png")


def test_03_swagger_ruche_inexistante_404(browser_page):
    page = browser_page
    status = _execute_in_swagger(page, {"coordinator_id": "C01", "target_hive_id": "H99"})
    assert status.startswith("404")
    page.locator(".live-responses-table").scroll_into_view_if_needed()
    _shot(page, "03_swagger_ruche_inexistante_404.png")


def test_04_swagger_identifiant_invalide_422(browser_page):
    page = browser_page
    status = _execute_in_swagger(page, {"coordinator_id": "ZZZ", "target_hive_id": "H07"})
    assert status.startswith("422")
    page.locator(".live-responses-table").scroll_into_view_if_needed()
    _shot(page, "04_swagger_identifiant_invalide_422.png")


def test_05_swagger_ruche_isolee_statut_error(browser_page):
    page = browser_page
    status = _execute_in_swagger(page, {"coordinator_id": "C02", "target_hive_id": "H13"})
    assert status.startswith("200")
    data = json.loads(page.locator(".live-responses-table .microlight").first.inner_text())
    assert data["status"] == "error" and data["path"] == [] and data["total_cost"] is None
    page.locator(".live-responses-table").scroll_into_view_if_needed()
    _shot(page, "05_swagger_ruche_isolee_aucun_itineraire.png")


def test_06_schemas_openapi_visibles(browser_page):
    page = browser_page
    page.locator("section.models").scroll_into_view_if_needed()
    if "is-open" not in (page.locator("section.models").get_attribute("class") or ""):
        page.locator("section.models h4 button").click()
    page.get_by_text("EmergencyPathRequest").first.wait_for(timeout=5000)
    _shot(page, "06_swagger_schemas_pydantic.png")


def test_07_api_http_cas_nominal_et_methodes(base_url, browser_page):
    ctx = browser_page.context.request
    ok = ctx.post(base_url + ENDPOINT, data={"coordinator_id": "C02", "target_hive_id": "H12"})
    assert ok.status == 200
    data = ok.json()
    assert set(["total_cost", "path", "calculation_time_ms"]) <= set(data)
    assert data["calculation_time_ms"] >= 0 and data["path"][-1] == "H12"
    assert ctx.get(base_url + ENDPOINT).status == 405
    assert ctx.post(base_url + ENDPOINT, data={"coordinator_id": "C01"}).status == 422
    assert ctx.post(base_url + ENDPOINT, data={"coordinator_id": "C09", "target_hive_id": "H01"}).status == 404


def test_08_openapi_json_et_capture_reponse_brute(base_url, browser_page):
    page = browser_page.context.browser.new_page(viewport={'width': 1000, 'height': 700})
    page.goto(base_url + "/openapi.json")
    spec = json.loads(page.inner_text("body"))
    assert ENDPOINT in spec["paths"] and "post" in spec["paths"][ENDPOINT]
    _shot(page, "07_openapi_json_contrat_api.png")
    page.close()
