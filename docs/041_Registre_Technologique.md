# Registre technologique déclaratif

## Rôle

Le registre décrit **avec quoi** un projet logiciel est réalisé. Il complète la méthode d'ingénierie sans devenir un moteur autonome, un lanceur universel ni une liste codée en dur de tous les langages.

`project.yaml` est la déclaration propre au projet. `profiles/technology/` fournit des références extensibles. `schemas/project.schema.json` définit la forme minimale vérifiable.

Versions du manifeste :

- v1 : registre technologique initial ;
- v2 : graphe de livraison non segmenté ;
- v3 : portées développement, release, distribution et exploitation, avec contrat d’artefact.

Les versions v1 et v2 restent acceptées. Le passage en v3 n’est jamais automatique.

## Taxonomie canonique

| Élément | Question à laquelle il répond | Exemples |
| --- | --- | --- |
| langage | Dans quelle notation écrit-on la source ? | TypeScript, Rust, Python |
| compilateur/interpréteur | Qu'est-ce qui transforme ou évalue la source ? | `tsc`, `rustc`, CPython |
| runtime | Dans quel environnement s'exécute le programme ? | navigateur, Node.js, JVM, natif |
| gestionnaire de dépendances | Comment résoudre et verrouiller les dépendances ? | pnpm, Cargo, uv |
| outil de build | Comment produire et orchestrer les artefacts ? | Vite, Cargo, CMake |
| framework/bibliothèque | Quelle structure applicative est fournie ? | React, Axum, FastAPI |
| plateforme cible | Où le résultat fonctionne-t-il ? | Linux, Android, navigateur |
| conteneurisation | Comment isoler et distribuer l'environnement ? | Docker, OCI |
| intégration continue | Où les validations automatisées s'exécutent-elles ? | GitHub Actions |
| IDE | Où l'humain édite-il le projet ? | VS Code, Android Studio |

Une technologie peut fournir plusieurs **capacités**. Cargo reste principalement un outil de chaîne Rust mais peut résoudre les dépendances, construire, tester, lancer et publier. La catégorie facilite la compréhension ; les capacités décrivent les fonctions réelles.

## Chaîne à documenter

```text
source
→ compilation ou interprétation
→ runtime
→ résolution des dépendances
→ build ou transformation technique
→ artefact
→ lancement
→ processus ou interface observable
```

Toutes les étapes ne s'appliquent pas à tous les projets. Une bibliothèque n'a pas nécessairement de processus `running`; un script interprété n'a pas forcément de build; un firmware peut être flashé plutôt que lancé.

Cette chaîne technique ne décrit pas le régime de développement
`construction`, qui désigne la matérialisation progressive d’une tranche.

## Dépôts multi-composants

Chaque composant possède sa racine, sa chaîne et ses cibles. Un dépôt Tauri peut ainsi déclarer un frontend TypeScript/React/Vite et un hôte Rust/Cargo sans forcer une fausse « stack principale » unique.

## Commandes

Les commandes sont stockées sous forme d'arguments structurés :

```yaml
commands:
  test:
    status: defined
    argv: [cargo, test, --workspace]
```

Valeurs de `status` :

- `defined` : commande explicitement vérifiée ;
- `unresolved` : opération pertinente mais commande encore inconnue ;
- `not-applicable` : opération sans sens pour ce composant, avec `reason` ;
- `disabled` : commande volontairement désactivée, avec `reason`.

Une chaîne shell n'est utilisée que si elle est réellement nécessaire et doit alors être signalée comme telle. Aucun outil ne doit improviser silencieusement une commande.

`defined` exige un tableau `argv` non vide. Les trois autres statuts exigent une raison.

## Détection et preuve

La détection recueille des indices, elle ne crée pas une vérité :

- `package.json` indique un écosystème JavaScript, pas à lui seul TypeScript, React ou npm ;
- `tsconfig.json` renforce fortement l'hypothèse TypeScript ;
- un lockfile désigne généralement le gestionnaire effectivement choisi ;
- scripts, dépendances, fichiers de configuration et arborescence précisent framework, tests, build et cible ;
- un monorepo doit être analysé par racine de composant.

Tout résultat détecté doit conserver sa provenance et un état : `confirmed`, `probable`, `ambiguous`, `contradictory` ou `absent`. Une déclaration humaine explicite est prioritaire, mais toute contradiction avec le dépôt réel est signalée.

## Extension progressive

Le modèle accepte de nouveaux profils sans modifier son noyau. Une nouvelle technologie doit fournir : identifiant stable, catégorie principale, capacités, indices, fichiers manifestes et lockfiles, contraintes de version, commandes conventionnelles documentées et sources officielles.

Le registre initial couvre seulement les chaînes réellement utilisées dans nos projets. L'exhaustivité porte sur le **modèle des relations**, pas sur une accumulation prématurée de centaines de fiches.
