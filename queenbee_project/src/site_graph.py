"""
Graphe de démonstration d'un site QueenBee : maillage des pistes et accès.

Hypothèse de modélisation (à remplacer par les données réelles du CDC si besoin) :
    - sommets  : bases des coordinateurs (BASE_*), carrefours de pistes (J*), ruches (H**)
    - arêtes   : tronçons de piste praticables, non orientés
    - poids    : temps de trajet en MINUTES (moto / pick-up)

H13 est volontairement isolée (piste coupée) pour illustrer le cas "aucun chemin".
Le graphe contient des cycles (ex. BASE_NORD - J1 - J2 - BASE_NORD).
"""

from src.dijkstra import build_graph

# (noeud A, noeud B, temps en minutes)
SITE_EDGES = [
    # Bases des coordinateurs vers le réseau de pistes
    ("BASE_NORD", "J1", 4.0),
    ("BASE_NORD", "J2", 9.0),
    ("BASE_SUD", "J5", 3.5),
    ("BASE_SUD", "J6", 6.0),
    # Pistes principales entre carrefours
    ("J1", "J2", 3.0),
    ("J1", "J3", 7.5),
    ("J2", "J3", 2.5),
    ("J2", "J4", 8.0),
    ("J3", "J4", 4.0),
    ("J3", "J5", 11.0),
    ("J4", "J6", 5.0),
    ("J5", "J6", 4.5),
    # Accès aux ruches
    ("J1", "H01", 2.0),
    ("J1", "H02", 3.5),
    ("J2", "H03", 1.5),
    ("J3", "H04", 2.0),
    ("J3", "H05", 3.0),
    ("H04", "H05", 1.5),
    ("J4", "H06", 2.5),
    ("J4", "H07", 4.0),
    ("H06", "H07", 2.0),
    ("J5", "H08", 2.0),
    ("J5", "H09", 3.0),
    ("J6", "H10", 1.5),
    ("J6", "H11", 2.5),
    ("H10", "H12", 3.0),
]

SITE_GRAPH = build_graph(SITE_EDGES)
SITE_GRAPH["H13"] = {}           # ruche isolée : accès coupé

# Coordinateurs régionaux -> point de départ dans le graphe
COORDINATORS = {
    "C01": "BASE_NORD",
    "C02": "BASE_SUD",
}

# Ruches connues du site
HIVES = sorted(node for node in SITE_GRAPH if node.startswith("H"))