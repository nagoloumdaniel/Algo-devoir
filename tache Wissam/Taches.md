# Tâches de Wissam - Dijkstra (DevOps)

## Phase 1 : Algorithmique (Jours 1-3)

### T-W1 : Dijkstra Min-Heap Python
- **But** : Implémenter Dijkstra sans bibliothèque tierce
- **Détails** : Classe `MinHeap` (heapify/bubble_up/down/extract_min/insert); dictionnaires `distances` (source→coût, source=0) et `predecessors`; gestion cible non atteinte
- **Tests** : Graphe 4 nœuds vérification; distance source→source=0; cohérence
- **Finitions** : Commentaires/docstring; noms variables significatifs; gestion infini; perf 10/50/100 nœuds

### T-W2 : Tas binaire de zéro
- **But** : `BinaryHeap` structure redimensionnable
- **Détails** : `heapify(arr)` O(n), `insert` O(log n), `extract_min` O(log n), `get_min()`, `size()`, redimensionnement, `__str__`
- **Tests** : `heapify` propriété tas; `insert` taille/propriété; `extract_min` bon élément; `get_min` sans modif; redimensionnement éléments préservés
- **Finitions** : Assertions verbeuses; `__repr__`; capacité max avant redimensionnement; doc méthodes avec exemple

### T-W3 : Chemin optimal (parent tracking)
- **But** : Suite ordonnée nœuds source→cible
- **Détails** : Cible→`predecessors`; suivre chaîne jusqu'à source (`predecessors[source]=None`); inverser liste; calculer étapes; vérifier chemin inexistant
- **Tests** : Chemin connu correspondance; sans chemin None/échec; source=cible [source]; graphe déconnecté comportement
- **Finitions** : Edge source/cible inexistantes; type cohérent liste/None; comments code; formats graphe (dict/list)

### T-W4 : Distance/temps cumulé
- **But** : Additionner poids arêtes chemin reconstitué
- **Détails** : `distances[cible]` distance totale; optionnel recalculer arêtes; convertir unité (secondes→minutes, mètres→km); formater 2 décimales; inclure étapes (hop count)
- **Tests** : Graphe connu Somme poids; source=cible distance=0; chemin inexistant comportement; poids flottants précision
- **Finitions** : Dictionnaire/tuple (distance, étapes); formatage "X min Y sec"; vérification cohérence; précision flottants

---

## Phase 2 : API REST (Jours 4-5)

### T-W5 : Endpoint `POST /api/v1/routing/emergency-path`
- **But** : Endpoint FastAPI POST renvoie Dijkstra
- **Détails** : Route `@app.post`; modèle Pydantic entrée `coordinator_id`/`target_hive_id`; extraire corps JSON; appeler Dijkstra T-W1; erreurs 400/404; JSON standardisé
- **Tests** : POST valides code 200 JSON; POST données manquantes code 422/FastAPI ou 400; identifiant ruche inexistant code 404; GET code 405 méthode non autorisée
- **Finitions** : Descriptions schemas Pydantic auto-doc; exemple requête erreur; logger requêtes; endpoint casse IDs

### T-W6 : Schéma entrée `{ "coordinator_id": "string", "target_hive_id": "string" }`
- **But** : Validation données entrantes
- **Détails** : Pydantic `BaseModel`; `coordinator_id` chaîne regex format ID; `target_hive_id` chaîne "HXX"; champs optionnels `urgence_niveau` (enum), `metadata` (dict); docs OpenAPI; validators coordonneur base
- **Tests** : Validation réussie passe; champs obligatoires erreur; type incorrect erreur; métadonnées optionnelles acceptées/rejetées
- **Finitions** : `example` champ Pydantic; alias API externe; `model_dump()` dict; sérialisation JSON

### T-W7 : Schéma sortie `{ "total_cost": number, "path": [node_ids], "calculation_time_ms": number }`
- **But** : Sortie standardisée coordinateur régional
- **Détails** : `total_cost` float 2 décimales; `path` liste identifiants source→cible; `calculation_time_ms` ms (`time.perf_counter()`); optionnel `hop_count`; `algorithm_version` string; JSON sérialisable; valeurs par défaut chemin inexistant
- **Tests** : Structure JSON complète; chemin inexistant defaults échec; timing positif; sérialisation JSON sans erreur
- **Finitions** : `jsonable_encoder`/`.model_dump()` Pydantic; champ `status` "success"/"error"; en-têtes `Content-Type: application/json`; diff sizes graphe perf sérialisation

---

## Phase 3 : Tests et Complexité (Jours 5-6)

### T-W9 : Tests cas normaux
- **But** : Suite pytest Dijkstra cas de base
- **Tests** : Fichier `test_dijkstra.py`; fixture `sample_graph` graphe 6-8 nœuds poidsKnown; plus court chemin entre n'importe deux nœuds; distance minimale; inégalité triangulaire

### T-W10 : Tests cas limites
- **But** : Graphe non connexe cycles source=cible graphe vide
- **Tests** : Non connexe distances infinity; cycles termine pas boucle infinime; source=cible distance=0 chemin [source]; vide pas crash; source inexistant ValueError; cible inexistante; isolé sans arêtes

### T-W11 : Complexité O((|V|+|E|)log|V|) Tas binaire
- **But** : Complexité théorique Dijkstra file priorité
- **Tests** : Benchmarks chronométrés tailles 10/50/100/500/1000 nœuds; croissance temps attendu; tracer croissance vs nœuds

### T-W12 : Version naïve O(|V|²) comparaison
- **But** : Version classique recherche linéaire minimum
- **Tests** : Résultat identique deux versions même chemin distance; petit graphe 10-20 rapide; grand graphe 500+ naïve beaucoup plus lente; cohérence deux versions mêmes edge

---

## Phase 4 : Benchmark (Jours 6-7)

### T-W13 : Benchmarks comparatifs
- **But** : Mesurer objectivement performances deux implémentations
- **Détails** : Graphes aléatoires tailles 20/50/100/200/500/1000 nœuds 3 graines; chronométrer deux versions `time.perf_counter()` microsecondes/ms; moyenne écart-type 3 graphes même taille; tableau récapitulatif; graphique taille vs temps
- **Tests** : Benchmark 5 tailles graphe; version Tas plus rapide seuil seuil; écarts-types raisonnables; temps positif fini

### T-W14 : Documenter résultats
- **But** : Interpréter résultats benchmarks
- **Tests** : Tableau bonnes lignes/colonnes; graphique sans erreur; tous temps positif nombre