"""Tests de la logique métier de l'endpoint (T-W5, T-W7) — sans serveur HTTP."""

import json

import pytest

from src.routing_service import (
    InvalidIdentifierError,
    UnknownResourceError,
    compute_emergency_path,
)

EXPECTED_KEYS = {
    "status", "message", "coordinator_id", "target_hive_id", "start_node", "total_cost",
    "total_cost_formatted", "path", "hop_count", "calculation_time_ms", "algorithm_version",
}


def test_itineraire_connu():
    result = compute_emergency_path("C01", "H07")
    assert result["status"] == "success"
    assert result["path"] == ["BASE_NORD", "J1", "J2", "J3", "J4", "H07"]
    assert result["total_cost"] == 17.5
    assert result["total_cost_formatted"] == "17 min 30 sec"
    assert result["hop_count"] == 5


def test_structure_json_complete_et_serialisable():
    result = compute_emergency_path("C02", "H04")
    assert set(result) == EXPECTED_KEYS
    json.dumps(result)                               # ne doit pas lever d'exception
    assert result["calculation_time_ms"] > 0


def test_ids_insensibles_a_la_casse_et_aux_espaces():
    assert compute_emergency_path(" c01 ", "h07")["total_cost"] == 17.5


def test_ruche_inaccessible_renvoie_les_valeurs_par_defaut():
    result = compute_emergency_path("C01", "H13")
    assert result["status"] == "error"
    assert result["path"] == []
    assert result["total_cost"] is None
    assert result["hop_count"] == 0
    assert result["message"]


@pytest.mark.parametrize("coordinator, hive", [("X01", "H01"), ("C01", "R01"), ("C1", "H01")])
def test_format_invalide(coordinator, hive):
    with pytest.raises(InvalidIdentifierError):
        compute_emergency_path(coordinator, hive)


def test_type_invalide():
    with pytest.raises(InvalidIdentifierError):
        compute_emergency_path(1, "H01")


def test_ruche_inexistante():
    with pytest.raises(UnknownResourceError):
        compute_emergency_path("C01", "H99")


def test_coordinateur_inexistant():
    with pytest.raises(UnknownResourceError):
        compute_emergency_path("C09", "H01")