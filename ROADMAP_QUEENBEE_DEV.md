# ROADMAP - PROJET QUEENBEE
## Spécialité : DÉVELOPPEMENT (DevOps)

> **Projet fil rouge INGETIS-ITIS - Master 1 - Janvier à Mai 2027**  
> **Plateforme Intelligente de Gestion Apicole Solidaire Multi-Sites (Afrique)**  
> **Durée :** 5 mois (16 semaines) | **Méthodologie :** Sprints de 2 semaines

---

## 🛠️ STACK TECHNIQUE - DÉVELOPPEMENT (DevOps)

| Domaine | Technologie | Usage |
|---------|-------------|-------|
| Conteneurisation | Docker | Conteneurisation de l'ensemble des services applicatifs |
| Orchestration edge | K3s (ou Docker Compose) | Orchestration sur sites edge |
| CI/CD | GitHub Actions ou GitLab CI | Intégration et déploiement continus |
| Infrastructure as Code | Ansible (recommandé) ou Terraform | Provisioning et gestion d'infrastructure |
| Monitoring | Prometheus + Grafana | Supervision et dashboards d'exploitation |
| Messaging (sync différée) | MQTT ou RabbitMQ | Synchronisation site ↔ central en connectivité limitée |
| API technique minimale | Node.js/Express ou Python/FastAPI | Développement des APIs métier |
| Automatisation de workflows | n8n | Intégrations API, notifications, synchronisation |
| DevSecOps | Snyk | Scan de dépendances et conteneurs, intégré à la CI/CD |
| Versionning | Git / GitHub | Gestion du code source |
| Documentation | Markdown / Notion / Confluence | README, DCT, schémas |

---

## 🗓️ JALONS DU PROJET (16 semaines)

| Jalon | Semaines | Livrables DevOps |
|-------|----------|------------------|
| Kick-off | S1 | Équipe constituée, backlog initial |
| Sprint 0 | S2-3 | Architecture applicative, environnement, DCT v1 |
| Sprint 1-2 | S4-7 | API core, conteneurs Docker, pipeline CI/CD build/test |
| Sprint 3-4 | S8-11 | APIs complètes, déploiement CI/CD, n8n, dashboard d'exploitation |
| Sprint 5 | S12-14 | Intégration, tests, optimisation, documentation déploiement |
| Soutenance | S15-16 | Présentation finale, démo fonctionnelle |

---

## 📅 ROADMAP DÉTAILLÉE PAR TÂCHE - DÉVELOPPEMENT

---

### PHASE 1 : S1 - KICK-OFF & CADRAGE
**Objectif :** Constitution de l'équipe DevOps, définition du backlog initial, environnement de travail

- [ ] T1.1 - Constitution de l'équipe Développement (DevOps)
- [ ] T1.2 - Réunion de kick-off et présentation du projet QueenBee
- [ ] T1.3 - Création du dépôt Git/GitHub et organisation des branches (main, develop, feature/)
- [ ] T1.4 - Installation des outils de collaboration (Slack/Discord, Jira/Trello, Miro/Draw.io)
- [ ] T1.5 - Réception et configuration des accès : VDOM FortiGate, compte SIEM scopé, VM cloud (Oracle Cloud)
- [ ] T1.6 - Rédaction du backlog initial et priorisation des user stories côté DevOps
- [ ] T1.7 - Définition des rôles et responsabilités dans l'équipe DevOps

**Livrables :** Équipe constituée, backlog initial DevOps, dépôt Git créé, accès infrastructure configurés

---

### PHASE 2 : S2-S3 - SPRINT 0 (ARCHITECTURE & CADRAGE)
**Objectif :** Architecture applicative multi-sites, environnement de développement, spécifications détaillées

- [ ] T2.1 - Conception de l'architecture applicative multi-sites (microservices ou monolithe modulaire)
- [ ] T2.2 - Définition des conteneurs Docker pour tous les services (Dockerfile, docker-compose)
- [ ] T2.3 - Installation et configuration de K3s (ou Docker Compose) sur sites edge
- [ ] T2.4 - Conception du pipeline CI/CD (GitHub Actions ou GitLab CI)
- [ ] T2.5 - Choix et configuration du stack technique API (Node.js/Express ou Python/FastAPI)
- [ ] T2.6 - Rédaction du Document de Cadrage Technique (DCT) - version 1 (30-35 pages)
- [ ] T2.7 - Définition des interfaces API principales (authentification, ruches, inspections, récoltes, alertes, analytics)
- [ ] T2.8 - Modèle de données initial pour les services backend

**Livrables Sprint 0 :** Architecture validée, environnement configuré, DCT v1, spécifications d'API

---

### PHASE 3 : S4-S7 - SPRINTS 1-2 (FONDATIONS & MODULES CORE)
**Objectif :** Développement des fonctionnalités de base, mise en place de l'infrastructure DevOps

- [ ] T3.1 - Développement de l'API d'authentification (inscription, login, refresh token, profil, JWT, RBAC)
- [ ] T3.2 - Développement de l'API CRUD ruches (création, consultation, historique des mesures, statut)
- [ ] T3.3 - Conteneurisation de tous les services applicatifs (Docker images versionnées)
- [ ] T3.4 - Pipeline CI/CD : build et test automatisés (lint, unit tests, build d'images)
- [ ] T3.5 - Intégration de Snyk dans la CI/CD (scan dépendances et conteneurs)
- [ ] T3.6 - Scripts IaC (Ansible/Terraform) pour provisioning d'un site pilote
- [ ] T3.7 - Déploiement de l'environnement de démonstration sur VM cloud (Oracle Cloud)

**Livrables Sprint 1-2 :** API core fonctionnelle, conteneurs Docker, pipeline CI/CD, IaC initial, environnement de démo

---

| Jalon | Semaines | Livrables DevOps |
|-------|----------|------------------|
| Kick-off | S1 | Équipe constituée, backlog initial |
| Sprint 0 | S2-3 | Architecture applicative, environnement, DCT v1 |
| Sprint 1-2 | S4-7 | API core, conteneurs Docker, pipeline CI/CD build/test |
| Sprint 3-4 | S8-11 | APIs complètes, déploiement CI/CD, n8n, dashboard d'exploitation |
| Sprint 5 | S12-14 | Intégration, tests, optimisation, documentation déploiement |
| Soutenance | S15-16 | Présentation finale, démo fonctionnelle |

---

### PHASE 4 : S8-S11 - SPRINTS 3-4 (FONCTIONNALITÉS AVANCÉES)
**Objectif :** APIs complètes, déploiement automatisé, synchronisation hors-ligne, automatisation n8n

- [ ] T4.1 - Développement de l'API inspections (création, consultation, synchronisation différée)
- [ ] T4.2 - Développement de l'API récoltes (déclaration, validation, écart vs prédiction)
- [ ] T4.3 - Développement de l'API alertes (génération, consultation, traitement)
- [ ] T4.4 - Développement de l'API analytics (KPIs multi-sites, génération de rapports)
- [ ] T4.5 - Pipeline CI/CD : déploiement automatisé avec porte de sécurité Snyk
- [ ] T4.6 - Dashboard d'exploitation (déploiements, synchronisations, incidents) avec Prometheus + Grafana
- [ ] T4.7 - Mécanisme de synchronisation différée site ↔ central (MQTT, files de synchronisation)
- [ ] T4.8 - Workflows n8n : intégration API, notifications, synchronisation
- [ ] T4.9 - Application mobile hors-ligne (apicultrices et coordinateurs) - frontend
- [ ] T4.10 - Documentation de déploiement multi-sites

**Livrables Sprint 3-4 :** APIs complètes, déploiement CI/CD opérationnel, n8n workflows, dashboard d'exploitation, application mobile, documentation déploiement

---

### PHASE 5 : S12-S14 - SPRINT 5 (INTÉGRATION, TESTS, POLISH)
**Objectif :** Intégration, tests complets, correction des bugs, préparation soutenance

- [ ] T5.1 - Tests d'intégration bout en bout (API, déploiement, synchronisation)
- [ ] T5.2 - Optimisation des pipelines CI/CD (performance, fiabilité, temps de build)
- [ ] T5.3 - Correction des bugs de déploiement et de conteneurisation
- [ ] T5.4 - Finalisation du dashboard d'exploitation
- [ ] T5.5 - Documentation de déploiement multi-sites finale
- [ ] T5.6 - Correction des bugs critiques identifiés
- [ ] T5.7 - Démonstration d'intégration finale
- [ ] T5.8 - Préparation de la présentation finale (20-25 slides)
- [ ] T5.9 - Répétition de la soutenance

**Livrables Sprint 5 :** Système intégré et testé, documentation complète, environnement de démo opérationnel, support de présentation

---

### PHASE 6 : S15-S16 - SOUTENANCE
**Objectif :** Présentation finale devant le jury, démonstration, réponses aux questions

- [ ] T6.1 - Soutenance finale (présentation 20-25 slides + démo live)
- [ ] T6.2 - Réponses aux questions du jury
- [ ] T6.3 - Remise des livrables finaux (code, documentation, démos)
- [ ] T6.4 - Clôture du projet et rétrospective finale

**Livrables finaux :** Présentation soutenance, démo fonctionnelle, tous les livrables DevOps

---

## 📦 LIVRABLES SPÉCIFIQUES - DÉVELOPPEMENT (DevOps)

| Livrable | Description | Format |
|----------|-------------|--------|
| Code source | Repository GitHub complet avec branches et tags | GitHub |
| Pipelines CI/CD | Pipeline fonctionnel (build, test, déploiement) avec porte de sécurité Snyk | GitHub Actions / GitLab CI |
| DCT | Document de Cadrage Technique (30-35 pages) | DOCX / PDF |
| Scripts IaC | Scripts Infrastructure as Code documentés | Ansible / Terraform |
| Workflows n8n | Au moins un workflow n8n fonctionnel (intégration API ou notification) | Fichiers exportés n8n |
| Environnement de démo | Environnement fonctionnel déployé sur VM cloud | URL / Accès |
| README | Guide d'installation et d'utilisation | Markdown |

---

## 🔄 RITUELS DE SYNCHRONISATION

| Fréquence | Jour | Objectif |
|-----------|------|----------|
| Planning hebdo, points bloquants | Lundi | Alignement de la semaine DevOps |
| Démo intégration, rétrospective | Vendredi | Avancement des APIs, CI/CD, déploiement |
| Daily standups | Quotidien | 15 min, points bloquants |
| Sprint planning et rétrospective | Début/fin de sprint | Planification et amélioration continue |

---

## 🎯 CRITÈRES D'ÉVALUATION SPÉCIFIQUES - DÉVELOPPEMENT

- [ ] Pipeline CI/CD opérationnel de bout en bout
- [ ] Conteneurisation cohérente et documentée (Docker)
- [ ] IaC reproductible (Ansible ou Terraform)
- [ ] Monitoring d'exploitation fonctionnel (Prometheus + Grafana)
- [ ] Scan de sécurité Snyk intégré à la CI/CD
- [ ] Mécanisme de synchronisation différée site ↔ central fonctionnel
- [ ] Au moins un workflow n8n exporté et fonctionnel

---

## ⚠️ RISQUES ET MITIGATIONS - DÉVELOPPEMENT

| Risque | Impact | Mitigation |
|--------|--------|------------|
| Connectivité intermittente | Élevé | Edge computing (K3s léger), MQTT, synchronisation différée |
| Échec de déploiement en production | Moyen | Pipeline CI/CD avec tests automatisés, rollback rapide |
| Vulnérabilités dans les dépendances | Élevé | Scan Snyk systématique dans la CI/CD, mise à jour régulière |

---

> **Note :** Ce roadmap concerne uniquement la spécialité **Développement (DevOps)**.  
> **Sources :** `QUEENBEE_CDC_COMMUN_M1.docx` et `Sujet_Examen_Algorithmique_QueenBee.pdf`.  
> *Dernière mise à jour : 30/10/2026*