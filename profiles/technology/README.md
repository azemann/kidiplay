# Profils technologiques

Ces fichiers décrivent des technologies de manière déclarative. Ils ne sont ni activés comme les profils de projet, ni copiés intégralement dans chaque dépôt.

## Structure d'une fiche

- `id` et `kind` stables ;
- rôles ou capacités réelles ;
- compatibilités ;
- indices de détection avec leur force ;
- manifestes, lockfiles et fichiers de version ;
- commandes conventionnelles sous forme `argv` ;
- artefacts usuels ;
- lien vers la documentation officielle.

Une fiche ne doit pas prétendre qu'une convention est la commande réelle d'un projet. Les scripts et remplacements explicites du dépôt restent prioritaires.

## Premières références

- `languages/` : TypeScript, Rust, Python ;
- `runtimes/` : Node.js, CPython, natif ;
- `tools/` : pnpm, Cargo, uv.

Ajouter les autres écosystèmes lorsqu'un projet réel les exige et qu'une source officielle permet de vérifier la fiche.

Les technologies répondent à « avec quoi ? ». Les profils de `../delivery/` répondent à « comment les opérations sont-elles orchestrées et livrées ? ».
