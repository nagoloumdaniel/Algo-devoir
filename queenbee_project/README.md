# QueenBee — Dijkstra (itinéraires d'urgence UC-C01)

Calcul du plus court chemin à source unique (Dijkstra, tas binaire codé à la main) pour envoyer
un coordinateur régional vers une ruche en alerte critique. Exposé via une API REST FastAPI.
Projet Mastère 1 INGETIS / ITIS — spécialité Développement / DevOps.

**Binôme :** Daniel Nagoloum TALLA et Wissam AIT EL HADI.

## Contenu
- `src/min_heap.py` : tas binaire (min-heap) redimensionnable, sans `heapq`
- `src/dijkstra.py` : Dijkstra avec tas, version naïve O(|V|²), reconstitution du chemin, coût
- `src/api.py`, `src/routing_service.py`, `src/site_graph.py` : `POST /api/v1/routing/emergency-path`
- `src/benchmark.py` : benchmark tas vs naïf (CSV, tableaux, graphiques dans `docs/benchmark/`)
- `tests/` : tests unitaires pytest ; `tests/e2e/` : tests E2E Playwright (captures dans `docs/captures/`)
- `docs/analyse_complexite.md` : note de complexité ; `docs/Compte_Rendu_QueenBee_Dijkstra.pdf` : rapport final

## Utilisation
```bash
pip install fastapi uvicorn pydantic pytest httpx matplotlib playwright pygments markdown-it-py
playwright install chromium

uvicorn src.api:app --reload          # API + Swagger UI sur http://127.0.0.1:8000/docs
python -m pytest tests --ignore=tests/e2e   # tests unitaires
python -m pytest tests/e2e            # tests E2E (lance le serveur, pilote Chromium, enregistre les captures)
python -m src.benchmark               # benchmark
python scripts/build_report.py        # régénère le PDF du compte rendu
```

## Exemple
```bash
curl -X POST http://127.0.0.1:8000/api/v1/routing/emergency-path \
  -H "Content-Type: application/json" \
  -d '{"coordinator_id": "C01", "target_hive_id": "H07"}'
```
Réponse : `status`, `total_cost` (minutes), `path` (points de passage), `calculation_time_ms`, `hop_count`.
Codes : 200, 400/404 (identifiant invalide/inconnu), 422 (corps invalide), 405 (mauvaise méthode).
