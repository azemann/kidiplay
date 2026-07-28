# Historique

## 1.7.0 — 2026-07-27

### Boucle de développement à liberté graduée

- consolidation de `exploration → construction → intégration → stabilisation` comme régimes réentrants de la tranche active ;
- séparation explicite entre régime de travail, niveau d’adoption, portée de livraison et phase d’opération ;
- liberté d’essai autorisée et bornée en exploration : variantes, mocks, valeurs temporaires et dépendances d’essai isolées ;
- critères de transition fondés sur des preuves, sans transformer la boucle en chaîne rigide ;
- exigences des agents et des tests rendues proportionnelles au régime courant ;
- le rôle `current-state`, mappé par défaut vers `PROJECT_STATE.md`, devient la source de vérité du régime, de la frontière expérimentale, des raccourcis temporaires et du critère de passage ;
- clarification de la frontière finale : la stabilisation reste dans `development`, la release produit et qualifie l’artefact, la distribution le consomme sans reconstruction ;
- aucune migration de manifeste : schémas, niveaux et portées v1.6 restent compatibles.

## 1.6.0 — 2026-07-24

### Adoption progressive et frontières de livraison

- ajout d’un point d’entrée `START_HERE.md` et de deux parcours explicites pour projet neuf ou dépôt existant ;
- ajout de `project.adoption.yaml`, de son schéma et de rôles documentaires mappables vers les chemins déjà présents ;
- niveaux cumulatifs `bootstrap`, `discovery`, `development`, `release`, `distribution` et `operation` ;
- obligations calculées depuis le niveau, les profils et les préoccupations, avec statuts déclarables `active`, `deferred` et `not-applicable` ;
- diagnostic initial en lecture seule, sans installation ni exécution du code observé ;
- validation locale et CI unifiées derrière `scripts/check-project.sh`, sans contrôle silencieusement ignoré ;
- manifeste logiciel v3 séparant les portées `development`, `release`, `distribution` et `operation` des phases universelles ;
- contrats `verification-output` et `release-artifact`, avec interdiction de reconstruire dans la distribution ;
- validation sémantique renforcée : commandes, DAG, phases, producteurs, consommateurs, secrets, rollback, portées et qualification ;
- frontières rendues exécutoires : vocabulaire `uses → phase`, qualifications antérieures à `create-release`, handoff persistant, environnements et approbations ;
- définitions v1/v2 historiques isolées de la v3 afin d’empêcher toute rétrogradation contournant les règles ;
- CI contextuelle : auto-contrôle complet du dépôt modèle et validation du niveau courant dans tout projet instancié ;
- suite adversariale de 40 tests couvrant aussi les chemins de contournement et la non-mutation du diagnostic ;
- exemples bootstrap, compatibilité v2, adoption existante et livraison segmentée ;
- guide principal entièrement recomposé autour du parcours utilisateur ;
- compatibilité maintenue pour les manifestes technologiques v1 et de livraison v2.

## 1.5.0 — 2026-07-21

### Cycle universel de livraison logicielle

- formalisation du cycle `verify → produce → deliver → operate` comme graphe d'opérations optionnelles ;
- distinction canonique entre opération, pipeline, orchestrateur, politique, artefact, release, environnement et déploiement ;
- extension de `project.yaml` aux pipelines, artefacts qualifiés, environnements, promotions, preuves, secrets référencés et stratégies de rollback ;
- ajout de `docs/042_Cycle_Livraison_Universel.md` et de l'ADR-0003 ;
- ajout d'un profil GitHub Actions et d'un exemple de livraison web de bout en bout ;
- contrôles automatiques du schéma, des YAML et des références dangereuses aux secrets ;
- maintien d'une frontière nette : le template décrit et vérifie, il ne génère pas encore des pipelines multi-fournisseurs.

## 1.4.0 — 2026-07-21

### Registre technologique déclaratif

- ajout d'un manifeste `project.yaml` pour décrire explicitement composants, langages, runtimes, outils, cibles, commandes et artefacts ;
- séparation canonique entre langage, compilateur/interpréteur, runtime, gestionnaire de dépendances, outil de build, framework, plateforme et environnement de développement ;
- ajout de `docs/041_Registre_Technologique.md` et d'un schéma JSON du manifeste ;
- profils technologiques extensibles et premiers exemples pour TypeScript/Node.js, Rust/Cargo et Python/CPython ;
- règles de détection fondées sur des indices, avec provenance, confiance, ambiguïtés et priorité donnée à la déclaration humaine ;
- prise en charge conceptuelle des dépôts multi-composants sans imposer de moteur de commandes ni de cycle de vie artificiel ;
- contrôle structurel du manifeste, du schéma et du registre dans le dépôt modèle.

## 1.3.0 — 2026-07-19

### Couverture exhaustive et profils

- mémoire opératoire `PROJECT_STATE.md` et rétrospective ;
- sources, preuves, risques, données et schémas ;
- rôles, permissions, flux, événements, boucles, échelles et carte système ;
- métriques et garde-fous ;
- modèle de menace, runbooks, reprise, distribution et fin de support ;
- registre et pipeline des assets ;
- dossiers conditionnels `schemas`, `migrations`, `fixtures`, `examples`, `benchmarks` ;
- profils software, Android, Linux service, Web/PWA, jeu et recherche/simulation ;
- profil DR maintenant DR, Ω, Atlas, Forge A/B et DR-Dev indépendants ;
- contrôle automatique étendu aux nouvelles sources de vérité obligatoires.

## 1.2.0 — 2026-07-19

### Audit et corrections

- exigences fonctionnelles et qualités mesurables ;
- contrats, erreurs, compatibilité et idempotence ;
- cycle de vie complet de l’application et séparation cycle/santé/opération ;
- registre d’audit et de dettes ;
- sécurité renforcée, frontières de confiance et chaîne de dépendances ;
- contenu, tonalité, actions sensibles et cible WCAG 2.2 AA ;
- contrôle automatique de structure, variables résiduelles et secrets potentiels ;
- workflow CI minimal ;
- placeholders techniques rendus non ambigus ;
- suppression de la version dupliquée dans le README.

## 1.1.0 — 2026-07-19

### Ajouté

- intention et architecture de l’expérience utilisateur ;
- charte graphique sombre professionnelle par défaut ;
- distinction entre fondations communes, signature de gamme et identité du projet ;
- système de design et composants fondamentaux ;
- tokens CSS primitifs et sémantiques ;
- règles responsive pour téléphone, Fold, tablette et bureau ;
- accessibilité : cible 48 px, clavier, focus, contraste, zoom et mouvement réduit ;
- états d’interface obligatoires ;
- protocole de validation visuelle.

## 1.0.0 — 2026-07-18

- première version du template générique d’ingénierie de projet.
