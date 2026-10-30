"""
Service de calcul d'itinéraire d'urgence (UC-C01).

Couche métier appelée par l'endpoint REST (src/api.py). Elle ne dépend pas de
FastAPI, ce qui permet de la tester directement et de garder l'API "fine".

Entrée : identifiant du coordinateur + identifiant de la ruche à risque.
Sortie : dictionnaire JSON-sérialisable (format de sortie de T-W7).
"""

import re
import time

from src.dijkstra import dijkstra, format_duration, reconstruct_path
from src.site_graph import COORDINATORS, HIVES, SITE_GRAPH

ALGORITHM_VERSION = "dijkstra-minheap-1.0"

COORDINATOR_ID_PATTERN = re.compile(r"^C\d{2}$")   # ex. C01
HIVE_ID_PATTERN = re.compile(r"^H\d{2}$")          # ex. H07


class InvalidIdentifierError(ValueError):
    """Identifiant mal formé  -> HTTP 400."""


class UnknownResourceError(LookupError):
    """Coordinateur ou ruche inexistant  -> HTTP 404."""


def normalize_id(value, field_name):
    """Supprime les espaces et met en majuscules ("h07 " -> "H07")."""
    if not isinstance(value, str):
        raise InvalidIdentifierError(f"{field_name} doit être une chaîne de caractères")
    return value.strip().upper()


def compute_emergency_path(coordinator_id, target_hive_id,
                           graph=SITE_GRAPH, coordinators=COORDINATORS, hives=HIVES):
    """Calcule l'itinéraire optimal du coordinateur vers la ruche en alerte.

    Lève InvalidIdentifierError (400) ou UnknownResourceError (404).
    Si la ruche existe mais n'est pas accessible, renvoie status="error"
    avec les valeurs par défaut (path vide, total_cost None).
    """
    coordinator_id = normalize_id(coordinator_id, "coordinator_id")
    target_hive_id = normalize_id(target_hive_id, "target_hive_id")

    if not COORDINATOR_ID_PATTERN.match(coordinator_id):
        raise InvalidIdentifierError(
            f"coordinator_id '{coordinator_id}' invalide (format attendu : CXX, ex. C01)")
    if not HIVE_ID_PATTERN.match(target_hive_id):
        raise InvalidIdentifierError(
            f"target_hive_id '{target_hive_id}' invalide (format attendu : HXX, ex. H07)")
    if coordinator_id not in coordinators:
        raise UnknownResourceError(f"Coordinateur '{coordinator_id}' inconnu")
    if target_hive_id not in hives or target_hive_id not in graph:
        raise UnknownResourceError(f"Ruche '{target_hive_id}' inconnue")

    start_node = coordinators[coordinator_id]

    # Seul l'algorithme est chronométré (pas la validation ni la sérialisation).
    t0 = time.perf_counter()
    distances, predecessors = dijkstra(graph, start_node, target_hive_id)
    path = reconstruct_path(predecessors, start_node, target_hive_id, distances)
    elapsed_ms = (time.perf_counter() - t0) * 1000

    response = {
        "coordinator_id": coordinator_id,
        "target_hive_id": target_hive_id,
        "start_node": start_node,
        "calculation_time_ms": round(elapsed_ms, 4),
        "algorithm_version": ALGORITHM_VERSION,
    }
    if path is None:
        response.update({
            "status": "error",
            "message": f"Aucun itinéraire praticable vers la ruche {target_hive_id}",
            "total_cost": None,
            "total_cost_formatted": None,
            "path": [],
            "hop_count": 0,
        })
    else:
        total = round(distances[target_hive_id], 2)
        response.update({
            "status": "success",
            "message": None,
            "total_cost": total,
            "total_cost_formatted": format_duration(total),
            "path": path,
            "hop_count": len(path) - 1,
        })
    return response