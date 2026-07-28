# Schémas

Conserver ici les contrats exécutables ou formels : JSON Schema, SQL, OpenAPI, formats de configuration, événements ou fichiers d’échange.

Chaque schéma précise version, propriétaire, producteurs, consommateurs, compatibilité et procédure de migration. Les exemples ne remplacent pas la validation.

- `project.schema.json` : technologie et livraison logicielle, versions 1 à 3 ;
- `project-adoption.schema.json` : entrée, niveau, profils, préoccupations et rôles documentaires.

Le premier décrit le logiciel. Le second décrit l’adoption de la méthode. Aucun
ne remplace le document mappé au rôle `current-state`.

Le régime de la tranche active — exploration, construction, intégration ou
stabilisation — est volontairement absent des schémas. Il est réentrant, peut
différer entre plusieurs branches et relève du présent opérationnel consigné
dans le document mappé au rôle `current-state`. `PROJECT_STATE.md` devient le
chemin par défaut à partir de la construction.

Les versions 1 et 2 conservent leurs définitions historiques séparées pour le
développement. Les champs v3 y sont interdits. Le niveau `release` et les
niveaux suivants exigent une migration explicite vers la v3.

Les schémas valident la forme. `scripts/validate-manifest.py` ajoute les invariants sémantiques : références, DAG, portées, artefacts, obligations progressives et chemins documentaires.
