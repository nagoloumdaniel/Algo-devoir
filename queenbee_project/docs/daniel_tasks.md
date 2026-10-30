# Tâches de Daniel - Dijkstra (DevOps)

## Phase 1 : Architecture API (Jours 1-2)

### T-D1 : Endpoint REST
- **But** : `POST /api/v1/routing/emergency-path`
- **Détails** : FastAPI; modèle Pydantic entrée; routage URL; documentation OpenAPI
- **Tests** : Schéma valide; champs obligatoires erreur; type incorrect erreur; GET 405

### T-D2 : Modèles Pydantic
- **But** : Schéma entrée/sortie
- **Détails** : `coordinator_id`/`target_hive_id`; champs optionnels `urgence_niveau`/`metadata`; docs OpenAPI; validators
- **Tests** : Validation réussie; champs obligatoires erreur; type incorrect; métadonnées optionnelles

### T-D3 : Validation identifiants
- **But** : Valider coordonneur/ruche
- **Détails** : Format ID; existence base de données; gestion cas edge
- **Tests** : Valide accepté; invalide rejeté; ruche inexistante 404; format faux rejeté

### T-D4 : Routage URL FastAPI
- **But** : Configurer API FastAPI
- **Détails** : Préfixe `/api/v1/routing`; méthode POST; documentation auto; tags operations
- **Tests** : Route accessible; autres méthodes erreurs; Swagger UI dispo

---

## Phase 2 : Intégration et API (Jours 3-4)

### T-D5 : Intégrer Dijkstra
- **But** : Intégrer code Wissam comme fonction interne
- **Tests** : Intégration valide résultats corrects; erreurs gestionnées; format JSON cohérent

### T-D6 : Gérer erreurs/cases edge
- **But** : Graphe non connexe/identifiants inexistants etc.
- **Tests** : Non connexe gestion adéquate; identifiant inexistant 404; vide pas crash; cycles corrects

### T-D7 : Formatter réponse JSON
- **But** : `total_cost`, `path`, `calculation_time_ms`
- **Détails** : `total_cost` float 2 décimales; `path` liste identifiants; `calculation_time_ms` ms; `status` "success"/"error"; JSON sérialisable
- **Tests** : Structure JSON complète; chemin inexistant defaults; timing positif; sérialisation sans erreur

### T-D8 : Documentation OpenAPI
- **But** : Documenter endpoint
- **Détails** : FastAPI génère docs; descriptions champs; exemples requêtes/réponses; tags operations
- **Tests** : `/docs` accessible; champs ont descriptions; exemples présents; schémas valides OpenAPI

---

## Phase 3 : Benchmark et Analyse (Jours 5-6)

### T-D8 : Benchmarks performance
- **But** : Mesurer performances deux implémentations
- **Détails** : Graphes aléatoires tailles 20/50/100/200/500/1000 nœuds 3 graines; chronométrer deux versions Dijkstra `time.perf_counter()`; moyenne écart-type 3 graphes; comparer résultats
- **Tests** : 5 tailles graphe; version Tas plus rapide seuil; écarts-types raisonnables; temps positif fini

### T-D9 : Graphiques comparaison
- **But** : Visualiser performances
- **Tests** : Graphique généré sans erreur; axes étiquetés; légende présente; données correspondances tableau

### T-D10 : Note complexité Grand O
- **But** : Analyse formelle
- **Détails** : O((|V|+|E|)log|V|) avec Tas; comparaison O(|V|)²; justifier choix implémentaire; cas edge; cas pratiques
- **Tests** : Analyse présente sections; mathématique correcte; justifications raisonnables; cas pratiques

### T-D11 : Analyser résultats
- **But** : Interpréter benchmarks justifier choix
- **Détails** : Seuils seuils Tas avantageux; facteurs densité graphe poids type processeur; comparer théories complexité; tableau résultats; graphique comparaison; limitations conditions langage; conclusions recommandations
- **Tests** : Analyse présente sections; complexité correcte; justifications raisonnables; mention cas pratiques; recommandations actionnables

---

## Phase 4 : Document PDF final (Jour 7)

### T-D12 : Mettre en page PDF
- **But** : Document complet
- **Détails** : Page degarde noms/prénoms; section implémentation Min-Heap; section tests résultats; section analyse complexité; mise en page professionnelle; < 5 Mo
- **Tests** : PDF ouvre sans erreur; page degarde présentes; toutes sections; taille < 5 Mo; mise en page cohérente

### T-D13 : Respecter limite < 5 Mo
- **But** : Taille fichier
- **Tests** : Taille vérifiée < 5 Mo; PDF lisible; toutes informations essentielles présentes

### T-D14 : Préparer Pronote
- **But** : Déposer sur Pronote
- **Tests** : Les deux étudiants déposent avec succès; fichiers identiques; métadonnées visibles; dépôt confirmé par email

### T-D15 : Traçabilité noms/prénoms
- **But** : Garantir traçabilité notation
- **Tests** : Noms visibles en entête; système accepte dépôt; emails confirmation reçus; fichiers identiques contenu