# ROADMAP - PROJET QUEENBEE
## Spécialité : DÉVELOPPEMENT (DevOps)
## Algorithme : DIJKSTRA (Plus court chemin à source unique)

> **Projet fil rouge INGETIS-ITIS - Master 1**  
> **Cas d'usage :** UC-C01 - Interventions d'urgence (alerte critique sur ruche)  
> **Date de rendu :** 05/11/2026 sur Pronote (Travail à faire)  
> **Format :** Un seul fichier PDF par binôme (< 5 Mo)

---

## 🎯 OBJECTIF

Implémenter l'algorithme de calcul du plus court chemin à source unique (Dijkstra) pour les interventions d'urgence. Lorsqu'une ruche déclenche une alerte critique (chute brutale de poids, risque d'essaimage imminent, anomalie thermique), le coordinateur régional doit se rendre sur place dans les plus brefs délais. Dijkstra calcule l'itinéraire optimal sur le maillage des pistes et accès du site.

---

## 🛠️ STACK TECHNIQUE

| Domaine | Technologie | Usage |
|---------|-------------|-------|
| Langage | Python 3.x | Implémentation de l'algorithme et des tests |
| Backend API | Node.js/Express ou Python/FastAPI | Endpoint REST `/api/v1/routing/emergency-path` |
| Tests | pytest (Python) ou Jest (Node.js) | Tests unitaires |
| Documentation | Markdown / PDF | Rapport final et note d'analyse |

---

## 📋 CAHIER DES CHARGES ET ATTENDUS TECHNIQUES

### 1. Implémentation de l'algorithme
- [ ] T1.1 - Implémentation de Dijkstra utilisant obligatoirement une file de priorité (Tas binaire / Min-Heap)
- [ ] T1.2 - Reconstitution intégrale du chemin optimal (suite ordonnée des nœuds)
- [ ] T1.3 - Calcul de la distance/temps cumulé total du trajet
- [ ] T1.4 - Gestion des cas limites : graphe non connexe, cycles, nœud source = cible, graphe vide

### 2. Intégration API applicative (Architecture logicielle)
- [ ] T2.1 - Exposition de l'algorithme sous forme d'endpoint REST au sein du backend QueenBee
  - `POST /api/v1/routing/emergency-path`
- [ ] T2.2 - Entrée : Identifiant du coordinateur / point de départ, identifiant de la ruche cible à risque
- [ ] T2.3 - Sortie (JSON) : Coût total du trajet, séquence complète des points de passage, temps de calcul algorithmique

### 3. Analyse de complexité & Benchmark
- [ ] T3.1 - Formalisation mathématique de la complexité temporelle avec tas binaire : O((|V| + |E|) log |V|)
- [ ] T3.2 - Implémentation d'une version naïve sans tas binaire : O(|V|²)
- [ ] T3.3 - Comparaison argumentée et/ou benchmark mesuré entre les deux versions
- [ ] T3.4 - Analyse comparative des performances (temps d'exécution, nombre d'opérations)

---

## 🧪 JEUX DE TESTS & RÉSULTATS

- [ ] T4.1 - Code des tests unitaires démontrant le bon fonctionnement sur des cas normaux
- [ ] T4.2 - Tests sur des cas limites : graphe non connexe, cycles, nœud source = cible, graphe vide, graphe à un seul nœud
- [ ] T4.3 - Vérification de la reconstitution du chemin optimal
- [ ] T4.4 - Vérification du coût total et du temps de calcul

---

## 📄 MODALITÉS DE RENDU

Le rendu s'effectue directement sur **Pronote** (rubrique Travail à faire) au plus tard le **05/11/2026**.

### Format attendu : UN SEUL fichier PDF par binôme (taille max recommandée : < 5 Mo)

Structure du document PDF :

1. **Page de garde / En-tête**
   - Noms et prénoms des deux étudiants du binôme
   - Spécialité : Développement / DevOps

2. **Implémentation de l'Algorithme (Code source)**
   - Code source complet et commenté de Dijkstra (sans bibliothèques tierces de graphes)
   - Mise en page propre avec coloration/police à chasse fixe
   - Structures de données associées : File de priorité / Tas binaire (Min-Heap)

3. **Jeux de Tests & Résultats**
   - Code des tests unitaires démontrant le bon fonctionnement
   - Cas normaux et cas limites (graphe non connexe, cycles, etc.)

4. **Note d'Analyse de Complexité**
   - Démonstration formelle et justification rigoureuse de la complexité en notation Grand O
   - Analyse comparative des performances (Dijkstra avec tas vs version naïve)

> **Remarque Pronote :** Les deux étudiants du binôme déposent le même fichier PDF sur leur espace Pronote respectif pour garantir la traçabilité de la notation.

---

## ✅ CHECKLIST DE VALIDATION

- [ ] Dijkstra implémenté avec Min-Heap (file de priorité)
- [ ] Reconstitution du chemin optimal fonctionnelle
- [ ] Endpoint REST `/api/v1/routing/emergency-path` opérationnel
- [ ] Sortie JSON : coût total, séquence des points de passage, temps de calcul
- [ ] Analyse de complexité formalisée : O((|V| + |E|) log |V|)
- [ ] Version naïve implémentée : O(|V|²)
- [ ] Benchmark comparatif réalisé
- [ ] Tests unitaires passants (cas normaux + cas limites)
- [ ] Code source commenté et mis en page proprement (police à chasse fixe)
- [ ] PDF unique généré (< 5 Mo) avec page de garde, code, tests, note d'analyse
- [ ] PDF déposé sur Pronote par les deux étudiants du binôme avant le 05/11/2026

---

> **Sources :** `QUEENBEE_CDC_COMMUN_M1.docx` et `Sujet_Examen_Algorithmique_QueenBee.pdf`  
> *Dernière mise à jour : 30/10/2026*