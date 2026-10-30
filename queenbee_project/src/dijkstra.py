"""
Algorithme de Dijkstra — projet QueenBee, cas d'usage UC-C01 (interventions d'urgence).

Contenu (tâches de Wissam) :
    T-W1  dijkstra()            Dijkstra avec file de priorité (tas binaire maison)
    T-W3  reconstruct_path()    reconstitution du chemin optimal source -> cible
    T-W4  shortest_path()       distance / temps cumulé + nombre d'étapes
          format_duration()     formatage "X min Y sec"
    T-W12 dijkstra_naive()      version naïve O(|V|²) sans tas (recherche linéaire)

Aucune bibliothèque de graphes (NetworkX, SciPy...) n'est utilisée.

Format du graphe
----------------
Liste d'adjacence sous forme de dictionnaire. Deux variantes sont acceptées :
    {"A": {"B": 4.0, "C": 2.0}, ...}           dict de dict
    {"A": [("B", 4.0), ("C", 2.0)], ...}       dict de listes de couples
Une liste d'arêtes peut être convertie avec build_graph().
Les poids doivent être >= 0 (condition de validité de Dijkstra).
"""

import argparse
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
# T-W12 : version naïve sans tas  —  O(|V|²)
# ====================================================================== #
def dijkstra_naive(graph, source, target=None, stats=None, normalize=True):
    """Même résultat que dijkstra(), mais le minimum est cherché par parcours linéaire.

    Chacune des |V| itérations parcourt tous les noeuds non visités pour trouver
    le plus proche : O(|V|) par itération, donc O(|V|²) au total, plus O(|E|)
    pour les relâchements. Aucune file de priorité.
    """
    if normalize:
        graph = normalize_graph(graph)
    _check_node(graph, source, "source")
    if target is not None:
        _check_node(graph, target, "cible")

    distances = {node: INFINITY for node in graph}
    predecessors = {node: None for node in graph}
    distances[source] = 0.0
    unvisited = set(graph)
    comparisons, relaxations = 0, 0

    while unvisited:
        # Recherche linéaire du noeud non visité de distance minimale.
        node, best = None, INFINITY
        for candidate in unvisited:
            comparisons += 1
            if distances[candidate] < best:
                node, best = candidate, distances[candidate]
        if node is None:             # tous les restants sont inaccessibles
            break
        unvisited.remove(node)
        if node == target:
            break
        for neighbor, weight in graph[node].items():
            if neighbor not in unvisited:
                continue
            relaxations += 1
            new_dist = best + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                predecessors[neighbor] = node

    if stats is not None:
        stats.update({
            "comparisons": comparisons,
            "relaxations": relaxations,
            "visited": len(graph) - len(unvisited),
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
        return None

    path = []
    node = target
    while node is not None:
        path.append(node)
        if node == source:
            path.reverse()
            return path
        node = predecessors[node]
        if len(path) > len(predecessors):    # garde-fou contre une table corrompue
            raise RuntimeError("Cycle détecté dans la table des prédécesseurs")
    return None                              # la remontée n'a pas atteint la source


# ====================================================================== #
# T-W4 : distance / temps cumulé
# ====================================================================== #
def path_cost(graph, path):
    """Recalcule le coût d'un chemin en additionnant le poids de ses arêtes.

    Sert de vérification croisée avec distances[cible].
    """
    graph = normalize_graph(graph)
    total = 0.0
    for u, v in zip(path, path[1:]):
        if v not in graph[u]:
            raise ValueError(f"L'arête {u}->{v} n'existe pas")
        total += graph[u][v]
    return total


def format_duration(minutes):
    """Formate une durée exprimée en minutes en "X min Y sec".

    >>> format_duration(12.5)
    '12 min 30 sec'
    >>> format_duration(0)
    '0 min 0 sec'
    """
    if minutes is None or minutes == INFINITY:
        return "inaccessible"
    total_seconds = round(minutes * 60)
    return f"{total_seconds // 60} min {total_seconds % 60} sec"


def shortest_path(graph, source, target, use_heap=True):
    """Calcule le meilleur itinéraire source -> cible et le coût associé.

    Renvoie un dictionnaire :
        reachable  : bool
        path       : liste ordonnée des noeuds, ou None si inaccessible
        total_cost : coût total arrondi à 2 décimales, ou None si inaccessible
        hop_count  : nombre d'arêtes parcourues, ou None si inaccessible
    """
    algorithm = dijkstra if use_heap else dijkstra_naive
    distances, predecessors = algorithm(graph, source, target)
    path = reconstruct_path(predecessors, source, target, distances)
    if path is None:
        return {"reachable": False, "path": None, "total_cost": None, "hop_count": None}
    return {
        "reachable": True,
        "path": path,
        "total_cost": round(distances[target], 2),
        "hop_count": len(path) - 1,
    }


# ====================================================================== #
# Point d'entrée en ligne de commande :  python -m src.dijkstra --help
# ====================================================================== #
def main(argv=None):
    from src.site_graph import SITE_GRAPH

    parser = argparse.ArgumentParser(
        description="Plus court chemin (Dijkstra + tas binaire) sur le site de démo QueenBee.")
    parser.add_argument("--source", default="BASE_NORD", help="noeud de départ")
    parser.add_argument("--target", default="H07", help="noeud d'arrivée (ruche)")
    parser.add_argument("--naive", action="store_true", help="utiliser la version O(|V|²)")
    args = parser.parse_args(argv)

    result = shortest_path(SITE_GRAPH, args.source, args.target, use_heap=not args.naive)
    if not result["reachable"]:
        print(f"Aucun chemin entre {args.source} et {args.target}.")
        return 1
    print("Chemin   :", " -> ".join(result["path"]))
    print("Durée    :", format_duration(result["total_cost"]),
          f"({result['total_cost']} min)")
    print("Étapes   :", result["hop_count"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())