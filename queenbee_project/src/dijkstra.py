"""
Algorithme de Dijkstra — projet QueenBee, cas d'usage UC-C01 (interventions d'urgence).

Contenu (tâches de Wissam) :
    T-W1  dijkstra()            Dijkstra avec file de priorité (tas binaire maison)

Aucune bibliothèque de graphes (NetworkX, SciPy...) n'est utilisée.

Format du graphe
----------------
Liste d'adjacence sous forme de dictionnaire. Deux variantes sont acceptées :
    {"A": {"B": 4.0, "C": 2.0}, ...}           dict de dict
    {"A": [("B", 4.0), ("C", 2.0)], ...}       dict de listes de couples
Une liste d'arêtes peut être convertie avec build_graph().
Les poids doivent être >= 0 (condition de validité de Dijkstra).
"""

import math

from src.min_heap import BinaryHeap

INFINITY = math.inf


# ====================================================================== #
# Construction / normalisation du graphe
# ====================================================================== #
def build_graph(edges, directed=False):
    """Construit une liste d'adjacence {u: {v: poids}} à partir d'arêtes (u, v, poids).

    Si ``directed`` est False, chaque arête est ajoutée dans les deux sens
    (une piste se parcourt dans les deux sens). En cas d'arêtes multiples
    entre deux mêmes noeuds, on garde la plus courte.

    >>> build_graph([("A", "B", 3)])
    {'A': {'B': 3.0}, 'B': {'A': 3.0}}
    """
    graph = {}

    def add(u, v, w):
        graph.setdefault(u, {})
        graph.setdefault(v, {})
        if v not in graph[u] or w < graph[u][v]:
            graph[u][v] = w

    for u, v, weight in edges:
        weight = float(weight)
        if weight < 0:
            raise ValueError(f"Poids négatif interdit sur l'arête {u}-{v} : {weight}")
        add(u, v, weight)
        if not directed:
            add(v, u, weight)
    return graph


def normalize_graph(graph):
    """Renvoie une copie du graphe au format {u: {v: poids}} et la valide.

    - accepte les voisins sous forme de dict ou de liste de couples ;
    - ajoute comme noeuds isolés les sommets qui n'apparaissent qu'en destination ;
    - rejette les poids négatifs (Dijkstra serait faux).
    """
    if graph is None:
        raise ValueError("Le graphe ne peut pas être None")
    normalized = {}
    for u, neighbors in graph.items():
        items = neighbors.items() if isinstance(neighbors, dict) else neighbors
        normalized.setdefault(u, {})
        for v, weight in items:
            weight = float(weight)
            if weight < 0:
                raise ValueError(f"Poids négatif interdit sur l'arête {u}->{v} : {weight}")
            normalized.setdefault(v, {})
            if v not in normalized[u] or weight < normalized[u][v]:
                normalized[u][v] = weight
    return normalized


def _check_node(graph, node, role):
    if node not in graph:
        raise ValueError(f"Le noeud {role} '{node}' n'existe pas dans le graphe")


# ====================================================================== #
# T-W1 : Dijkstra avec tas binaire  —  O((|V| + |E|) log |V|)
# ====================================================================== #
def dijkstra(graph, source, target=None, stats=None, normalize=True):
    """Plus courts chemins depuis ``source`` avec une file de priorité (Min-Heap).

    Paramètres
    ----------
    graph  : liste d'adjacence (voir en-tête du module)
    source : noeud de départ
    target : optionnel ; si fourni, on s'arrête dès que la cible est extraite
             du tas (sa distance est alors définitive)
    stats  : dict optionnel rempli avec des compteurs d'opérations
    normalize : si False, le graphe est supposé déjà au format {u: {v: poids>=0}}
             (évite la copie O(|V|+|E|) ; utilisé par le benchmark pour ne
             chronométrer que l'algorithme)

    Renvoie
    -------
    (distances, predecessors)
        distances[v]    : coût minimal source -> v (math.inf si inaccessible)
        predecessors[v] : noeud précédent sur le meilleur chemin (None pour la
                          source et les noeuds inaccessibles)

    Principe
    --------
    Le tas contient des couples (distance provisoire, noeud). À chaque tour on
    extrait le noeud de plus petite distance : comme les poids sont >= 0, cette
    distance ne peut plus diminuer, le noeud est donc "définitif" (visited).
    On relâche ensuite ses arêtes sortantes.

    Plutôt qu'une opération decrease-key, on utilise la "suppression paresseuse" :
    quand une distance s'améliore on ré-insère le noeud ; les anciennes entrées
    périmées sont ignorées à l'extraction. Le tas contient au plus |E| + 1
    entrées, donc chaque opération coûte O(log |E|) = O(log |V|).
    """
    if normalize:
        graph = normalize_graph(graph)
    _check_node(graph, source, "source")
    if target is not None:
        _check_node(graph, target, "cible")

    distances = {node: INFINITY for node in graph}
    predecessors = {node: None for node in graph}
    distances[source] = 0.0

    visited = set()
    heap = BinaryHeap()
    counter = 0                      # départage les égalités de distance
    heap.insert((0.0, counter, source))
    pushes, pops, relaxations = 1, 0, 0

    while not heap.is_empty():
        current_dist, _, node = heap.extract_min()
        pops += 1

        if node in visited:          # entrée périmée (suppression paresseuse)
            continue
        visited.add(node)

        if node == target:           # arrêt anticipé : distance de la cible définitive
            break

        for neighbor, weight in graph[node].items():
            if neighbor in visited:
                continue
            relaxations += 1
            new_dist = current_dist + weight
            if new_dist < distances[neighbor]:       # relâchement
                distances[neighbor] = new_dist
                predecessors[neighbor] = node
                counter += 1
                heap.insert((new_dist, counter, neighbor))
                pushes += 1

    if stats is not None:
        stats.update({
            "heap_pushes": pushes,
            "heap_pops": pops,
            "relaxations": relaxations,
            "comparisons": heap.comparisons,
            "visited": len(visited),
        })
    return distances, predecessors

# ====================================================================== #
# T-W3 : reconstitution du chemin optimal
# ====================================================================== #
def reconstruct_path(predecessors, source, target, distances=None):
    """Renvoie la liste ordonnée [source, ..., target], ou None s'il n'y a pas de chemin.

    On part de la cible et on remonte les prédécesseurs jusqu'à la source
    (predecessors[source] vaut None), puis on inverse la liste. O(longueur du chemin).
    """
    if source not in predecessors:
        raise ValueError(f"Le noeud source '{source}' n'existe pas dans le graphe")
    if target not in predecessors:
        raise ValueError(f"Le noeud cible '{target}' n'existe pas dans le graphe")
    if source == target:
        return [source]
    if distances is not None and distances.get(target, INFINITY) == INFINITY:
        return None                              # cible inaccessible

    path = []
    node = target
    while node is not None:
        path.append(node)
        if node == source:
            path.reverse()
            return path
        node = predecessors[node]
        if len(path) > len(predecessors):        # garde-fou contre une boucle infinie
            raise RuntimeError("Cycle détecté dans la table des prédécesseurs")
    return None                                  # la remontée n'a pas atteint la source