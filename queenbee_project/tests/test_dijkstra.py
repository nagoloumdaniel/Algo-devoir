"""Tests unitaires de Dijkstra : cas normaux (T-W9), cas limites (T-W10),
chemin (T-W3) et coût (T-W4)."""

import math

import pytest

from src.dijkstra import (
    build_graph,
    dijkstra,
    dijkstra_naive,
    format_duration,
    path_cost,
    reconstruct_path,
    shortest_path,
)
from src.site_graph import SITE_GRAPH


@pytest.fixture
def sample_graph():
    """Graphe non orienté de 6 noeuds dont les plus courts chemins depuis A sont connus :
    A=0, C=2, B=3 (A-C-B), D=8 (A-C-B-D), E=10 (…-D-E), F=12 (…-E-F)."""
    return build_graph([
        ("A", "B", 4), ("A", "C", 2), ("B", "C", 1), ("B", "D", 5), ("C", "D", 8),
        ("C", "E", 10), ("D", "E", 2), ("D", "F", 6), ("E", "F", 2),
    ])


EXPECTED_FROM_A = {"A": 0, "B": 3, "C": 2, "D": 8, "E": 10, "F": 12}


# ---------------------------------------------------------------------- #
# Cas normaux
# ---------------------------------------------------------------------- #
def test_distances_connues(sample_graph):
    distances, _ = dijkstra(sample_graph, "A")
    assert distances == pytest.approx(EXPECTED_FROM_A)


def test_chemin_connu(sample_graph):
    result = shortest_path(sample_graph, "A", "F")
    assert result["reachable"] is True
    assert result["path"] == ["A", "C", "B", "D", "E", "F"]
    assert result["total_cost"] == 12
    assert result["hop_count"] == 5


def test_cout_du_chemin_egal_a_la_distance(sample_graph):
    for target, expected in EXPECTED_FROM_A.items():
        result = shortest_path(sample_graph, "A", target)
        assert path_cost(sample_graph, result["path"]) == pytest.approx(expected)
        assert result["total_cost"] == pytest.approx(expected)


def test_chemin_commence_a_la_source_et_finit_a_la_cible(sample_graph):
    for source in sample_graph:
        for target in sample_graph:
            path = shortest_path(sample_graph, source, target)["path"]
            assert path[0] == source and path[-1] == target


def test_symetrie_graphe_non_oriente(sample_graph):
    for u in sample_graph:
        du, _ = dijkstra(sample_graph, u)
        for v in sample_graph:
            dv, _ = dijkstra(sample_graph, v)
            assert du[v] == pytest.approx(dv[u])


def test_inegalite_triangulaire(sample_graph):
    """Pour toute arête (u, v) : d(v) <= d(u) + w(u, v). Sinon un relâchement a été oublié."""
    distances, _ = dijkstra(sample_graph, "A")
    for u, neighbors in sample_graph.items():
        for v, w in neighbors.items():
            assert distances[v] <= distances[u] + w + 1e-9


def test_graphe_oriente():
    graph = build_graph([("A", "B", 1), ("B", "C", 1), ("C", "A", 1)], directed=True)
    distances, _ = dijkstra(graph, "B")
    assert distances == {"A": 2, "B": 0, "C": 1}


def test_format_liste_de_couples():
    graph = {"A": [("B", 2), ("C", 5)], "B": [("C", 1)], "C": []}
    assert shortest_path(graph, "A", "C")["path"] == ["A", "B", "C"]


def test_arete_multiple_garde_la_plus_courte():
    graph = build_graph([("A", "B", 9), ("A", "B", 2)])
    assert graph["A"]["B"] == 2


def test_poids_flottants_precision():
    graph = build_graph([("A", "B", 0.1), ("B", "C", 0.2)])
    result = shortest_path(graph, "A", "C")
    assert result["total_cost"] == 0.3        # arrondi à 2 décimales


def test_arret_anticipe_donne_la_meme_distance(sample_graph):
    full, _ = dijkstra(sample_graph, "A")
    early, _ = dijkstra(sample_graph, "A", target="D")
    assert early["D"] == full["D"]


def test_format_duration():
    assert format_duration(17.5) == "17 min 30 sec"
    assert format_duration(0) == "0 min 0 sec"
    assert format_duration(math.inf) == "inaccessible"


# ---------------------------------------------------------------------- #
# Cas limites
# ---------------------------------------------------------------------- #
def test_graphe_non_connexe():
    graph = build_graph([("A", "B", 1), ("C", "D", 1)])
    distances, predecessors = dijkstra(graph, "A")
    assert distances["C"] == math.inf and distances["D"] == math.inf
    assert predecessors["C"] is None
    assert reconstruct_path(predecessors, "A", "D", distances) is None
    result = shortest_path(graph, "A", "D")
    assert result == {"reachable": False, "path": None, "total_cost": None, "hop_count": None}


def test_cycles_terminent():
    graph = build_graph([("A", "B", 1), ("B", "C", 1), ("C", "A", 1), ("C", "D", 1)])
    assert shortest_path(graph, "A", "D")["path"] == ["A", "C", "D"]


def test_boucle_sur_soi_meme():
    graph = {"A": {"A": 5, "B": 1}, "B": {}}
    distances, _ = dijkstra(graph, "A")
    assert distances == {"A": 0, "B": 1}


def test_source_egale_cible(sample_graph):
    result = shortest_path(sample_graph, "C", "C")
    assert result["path"] == ["C"]
    assert result["total_cost"] == 0
    assert result["hop_count"] == 0


def test_graphe_vide_leve_une_erreur_propre():
    with pytest.raises(ValueError):
        dijkstra({}, "A")


def test_graphe_a_un_seul_noeud():
    distances, predecessors = dijkstra({"A": {}}, "A")
    assert distances == {"A": 0}
    assert predecessors == {"A": None}


def test_noeud_isole():
    graph = build_graph([("A", "B", 1)])
    graph["Z"] = {}
    assert shortest_path(graph, "A", "Z")["reachable"] is False


def test_noeud_present_seulement_en_destination():
    graph = {"A": {"B": 3}}          # B n'a pas d'entrée propre
    distances, _ = dijkstra(graph, "A")
    assert distances["B"] == 3


def test_source_inexistante(sample_graph):
    with pytest.raises(ValueError):
        dijkstra(sample_graph, "INCONNU")


def test_cible_inexistante(sample_graph):
    with pytest.raises(ValueError):
        shortest_path(sample_graph, "A", "INCONNU")


def test_poids_negatif_refuse():
    with pytest.raises(ValueError):
        dijkstra({"A": {"B": -1}, "B": {}}, "A")


# ---------------------------------------------------------------------- #
# T-W12 : version naïve — mêmes résultats que la version avec tas
# ---------------------------------------------------------------------- #
def test_naif_sur_le_graphe_exemple(sample_graph):
    distances, _ = dijkstra_naive(sample_graph, "A")
    assert distances == pytest.approx(EXPECTED_FROM_A)
    result = shortest_path(sample_graph, "A", "F", use_heap=False)
    assert result["path"] == ["A", "C", "B", "D", "E", "F"]


def test_tas_et_naif_identiques_sur_tout_le_site():
    """Depuis chaque noeud du site, les deux versions donnent les mêmes distances."""
    for source in SITE_GRAPH:
        d_heap, _ = dijkstra(SITE_GRAPH, source)
        d_naive, _ = dijkstra_naive(SITE_GRAPH, source)
        for node in SITE_GRAPH:
            assert d_heap[node] == pytest.approx(d_naive[node]), (source, node)


def test_naif_graphe_non_connexe():
    graph = build_graph([("A", "B", 1), ("C", "D", 1)])
    distances, _ = dijkstra_naive(graph, "A")
    assert distances["C"] == math.inf
    assert shortest_path(graph, "A", "D", use_heap=False)["reachable"] is False


def test_naif_source_inexistante(sample_graph):
    with pytest.raises(ValueError):
        dijkstra_naive(sample_graph, "INCONNU")