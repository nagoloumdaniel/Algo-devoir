"""
Benchmark comparatif : Dijkstra avec tas binaire vs version naïve O(|V|²) (T-W11, T-W13).

    python -m src.benchmark                    # graphes clairsemés (degré moyen ~6)
    python -m src.benchmark --density dense    # graphes denses (|E| ~ |V|²/4)

Pour chaque taille : 3 graphes aléatoires connexes (3 graines), chaque version est
chronométrée avec time.perf_counter(), on calcule moyenne et écart-type, on vérifie
que les deux versions donnent exactement les mêmes distances, et on compte les
opérations élémentaires. Résultats : tableau Markdown + CSV + graphique PNG.
"""

import argparse
import csv
import math
import random
import statistics
import time
from pathlib import Path

from src.dijkstra import dijkstra, dijkstra_naive, normalize_graph

try:
    from config.settings import BENCHMARK_SIZES
except ImportError:
    BENCHMARK_SIZES = [20, 50, 100, 200, 500, 1000]

SEEDS = [1, 2, 3]
REPEATS = 3          # on garde le meilleur de 3 exécutions pour limiter le bruit


def random_connected_graph(n, density="sparse", seed=0):
    """Graphe non orienté connexe de n noeuds, poids aléatoires dans [1, 20].

    Un arbre couvrant aléatoire garantit la connexité, puis on ajoute des arêtes :
      - sparse : ~3n arêtes au total (degré moyen ~6), cas réaliste d'un réseau de pistes
      - dense  : chaque paire reliée avec probabilité 0.5, soit |E| ~ n²/4
    """
    rng = random.Random(seed)
    graph = {i: {} for i in range(n)}

    def add(u, v):
        if u != v and v not in graph[u]:
            w = round(rng.uniform(1, 20), 2)
            graph[u][v] = w
            graph[v][u] = w

    for v in range(1, n):                    # arbre couvrant
        add(v, rng.randrange(v))
    if density == "dense":
        for u in range(n):
            for v in range(u + 1, n):
                if rng.random() < 0.5:
                    add(u, v)
    else:
        target_edges = 3 * n
        edges = n - 1
        while edges < target_edges and n > 1:
            u, v = rng.randrange(n), rng.randrange(n)
            if u != v and v not in graph[u]:
                add(u, v)
                edges += 1
    return graph


def count_edges(graph):
    return sum(len(nbrs) for nbrs in graph.values()) // 2


def time_function(func, graph, source):
    """Meilleur temps sur REPEATS exécutions, en ms. Le graphe est déjà normalisé
    (normalize=False) : seul l'algorithme est chronométré, pas la copie du graphe."""
    best = math.inf
    for _ in range(REPEATS):
        t0 = time.perf_counter()
        func(graph, source, normalize=False)
        best = min(best, time.perf_counter() - t0)
    return best * 1000           # en millisecondes


def run_benchmark(sizes=BENCHMARK_SIZES, density="sparse"):
    rows = []
    for n in sizes:
        heap_times, naive_times, heap_ops, naive_ops, edge_counts = [], [], [], [], []
        for seed in SEEDS:
            graph = normalize_graph(random_connected_graph(n, density, seed))
            edge_counts.append(count_edges(graph))

            # Vérification : les deux versions doivent donner les mêmes distances.
            s_heap, s_naive = {}, {}
            d_heap, _ = dijkstra(graph, 0, stats=s_heap)
            d_naive, _ = dijkstra_naive(graph, 0, stats=s_naive)
            for node in graph:
                if not math.isclose(d_heap[node], d_naive[node]):
                    raise AssertionError(f"Résultats différents (n={n}, seed={seed}, noeud={node})")

            heap_ops.append(s_heap["comparisons"] + s_heap["relaxations"])
            naive_ops.append(s_naive["comparisons"] + s_naive["relaxations"])
            heap_times.append(time_function(dijkstra, graph, 0))
            naive_times.append(time_function(dijkstra_naive, graph, 0))

        rows.append({
            "n": n,
            "edges": round(statistics.mean(edge_counts)),
            "heap_ms": statistics.mean(heap_times),
            "heap_std": statistics.stdev(heap_times),
            "naive_ms": statistics.mean(naive_times),
            "naive_std": statistics.stdev(naive_times),
            "speedup": statistics.mean(naive_times) / statistics.mean(heap_times),
            "heap_ops": round(statistics.mean(heap_ops)),
            "naive_ops": round(statistics.mean(naive_ops)),
        })
    return rows


def to_markdown(rows, density):
    lines = [
        f"### Graphes {'denses' if density == 'dense' else 'clairsemés'}",
        "",
        "| Noeuds | Arêtes | Tas (ms) | Naïf (ms) | Rapport naïf/tas | Opérations tas | Opérations naïf |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in rows:
        lines.append(
            f"| {r['n']} | {r['edges']} | {r['heap_ms']:.3f} ± {r['heap_std']:.3f} "
            f"| {r['naive_ms']:.3f} ± {r['naive_std']:.3f} | {r['speedup']:.2f} "
            f"| {r['heap_ops']:,} | {r['naive_ops']:,} |".replace(",", " "))
    return "\n".join(lines)


def save_csv(rows, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def save_plot(rows, path, density):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    sizes = [r["n"] for r in rows]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.errorbar(sizes, [r["heap_ms"] for r in rows], yerr=[r["heap_std"] for r in rows],
                marker="o", capsize=3, label="Dijkstra + tas binaire  O((V+E) log V)")
    ax.errorbar(sizes, [r["naive_ms"] for r in rows], yerr=[r["naive_std"] for r in rows],
                marker="s", capsize=3, label="Dijkstra naïf  O(V²)")
    ax.set_xlabel("Nombre de noeuds |V|")
    ax.set_ylabel("Temps d'exécution (ms)")
    ax.set_title(f"Benchmark Dijkstra — graphes {'denses' if density == 'dense' else 'clairsemés'}")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Benchmark Dijkstra tas vs naïf")
    parser.add_argument("--density", choices=["sparse", "dense"], default="sparse")
    parser.add_argument("--sizes", type=int, nargs="+", default=None)
    parser.add_argument("--out", default="docs/benchmark", help="dossier de sortie")
    args = parser.parse_args(argv)

    sizes = args.sizes or (BENCHMARK_SIZES if args.density == "sparse"
                           else [20, 50, 100, 200, 500])
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    rows = run_benchmark(sizes, args.density)
    table = to_markdown(rows, args.density)
    print(table)
    (out / f"resultats_{args.density}.md").write_text(table + "\n", encoding="utf-8")
    save_csv(rows, out / f"resultats_{args.density}.csv")
    save_plot(rows, out / f"benchmark_{args.density}.png", args.density)
    print(f"\nFichiers écrits dans {out}/")


if __name__ == "__main__":
    main()