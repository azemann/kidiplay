# Choix techniques

Les technologies sont choisies après la vision, le périmètre et le modèle métier.

## Contraintes de choix

- plateformes cibles : {{TARGET_PLATFORMS}} ;
- fonctionnement hors ligne : {{OFFLINE_REQUIREMENT}} ;
- volumétrie : {{EXPECTED_SCALE}} ;
- compétences disponibles : {{AVAILABLE_SKILLS}} ;
- durée de vie visée : {{EXPECTED_LIFETIME}}.

## Chaîne technologique retenue

Ne pas confondre les catégories. Décrire la chaîne réelle, par composant si le dépôt est multi-stack :

```text
source → compilateur/interpréteur → runtime → dépendances → build → framework éventuel → artefact → plateforme d'exécution
```

Le détail calculable appartient à `project.yaml`. Le présent document explique les raisons, alternatives et risques des choix.

| Domaine | Choix | Raisons | Alternatives | Risques |
| --- | --- | --- | --- | --- |
| Langage(s) | {{LANGUAGE}} | {{LANGUAGE_REASON}} | {{LANGUAGE_ALTERNATIVES}} | {{LANGUAGE_RISKS}} |
| Compilateur/interpréteur | {{COMPILER_OR_INTERPRETER}} | {{COMPILER_REASON}} | {{COMPILER_ALTERNATIVES}} | {{COMPILER_RISKS}} |
| Runtime | {{RUNTIME}} | {{RUNTIME_REASON}} | {{RUNTIME_ALTERNATIVES}} | {{RUNTIME_RISKS}} |
| Gestion des dépendances | {{DEPENDENCY_TOOL}} | {{DEPENDENCY_REASON}} | {{DEPENDENCY_ALTERNATIVES}} | {{DEPENDENCY_RISKS}} |
| Build et tâches | {{BUILD_TOOL}} | {{BUILD_REASON}} | {{BUILD_ALTERNATIVES}} | {{BUILD_RISKS}} |
| Frameworks/bibliothèques structurantes | {{FRAMEWORKS}} | {{FRAMEWORK_REASON}} | {{FRAMEWORK_ALTERNATIVES}} | {{FRAMEWORK_RISKS}} |
| Interface | {{UI_STACK}} | {{UI_REASON}} | {{UI_ALTERNATIVES}} | {{UI_RISKS}} |
| Données | {{DATA_STACK}} | {{DATA_REASON}} | {{DATA_ALTERNATIVES}} | {{DATA_RISKS}} |
| Tests | {{TEST_STACK}} | {{TEST_REASON}} | {{TEST_ALTERNATIVES}} | {{TEST_RISKS}} |
| Interface/design system | {{DESIGN_STACK}} | {{DESIGN_REASON}} | {{DESIGN_ALTERNATIVES}} | {{DESIGN_RISKS}} |

## Dépendances

Chaque dépendance importante doit préciser son utilité, sa licence, son coût de remplacement et sa politique de mise à jour.

Une bibliothèque de composants ne remplace ni la charte, ni les tokens sémantiques, ni la validation visuelle.

## Portabilité et sortie

Préciser comment exporter les données, remplacer une dépendance critique, reconstruire le projet et quitter un fournisseur sans perdre la source de vérité.

## Versions supportées

{{SUPPORTED_VERSIONS}}

## Commandes et artefacts réels

Documenter les commandes propres au dépôt (`install`, `develop`, `test`, `lint`, `format`, `build`, `package`) et les artefacts obtenus. Une opération non applicable utilise `status: not-applicable` avec sa raison. Ne pas inventer une commande universelle qui masquerait les subtilités de la stack.

Dans `project.yaml`, employer les statuts canoniques `defined`, `unresolved`, `not-applicable` et `disabled`. Seul `defined` autorise l’exécution.

Séparer :

- build de contrôle pour le développement ;
- build et package reproductibles pour la release ;
- publication ou déploiement de l’artefact déjà qualifié.

Une cible finale peut être connue alors que ses comptes, clés, stores et environnements restent différés.
