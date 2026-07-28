# Guide d’utilisation du template

Ce guide est la référence complète. Pour commencer, ouvrez d’abord `START_HERE.md`.

## 1. Choisir la porte d’entrée

Le choix est temporaire :

- `new` : partir de l’intention, du périmètre et d’une première tranche ;
- `existing` : partir des preuves du dépôt, diagnostiquer sans modifier, puis adopter progressivement.

Les deux parcours convergent à `development`.

Ne créez pas deux variantes du template. Ne copiez pas tout le dépôt dans un projet existant.

## 2. Comprendre les deux manifestes

### `project.adoption.yaml`

Il décrit l’usage de la méthode :

- origine d’adoption ;
- niveau courant ;
- profils actifs ;
- préoccupations transversales ;
- rôles documentaires et chemins réels.

### `project.yaml`

Pour un logiciel, il décrit la réalité technologique et la livraison :

- composants ;
- langages et chaîne d’outils ;
- commandes ;
- artefacts ;
- pipelines ;
- environnements et références de secrets ;
- portées développement, release, distribution et exploitation.

Ne placez pas l’état présent dans ces manifestes : il appartient au document
mappé au rôle `current-state`, par défaut `PROJECT_STATE.md`, notamment le
régime de la tranche active.

## 3. Avancer par niveaux

| Niveau | Preuve demandée | N’exige pas encore |
| --- | --- | --- |
| `bootstrap` | intention, périmètre, première tranche et raccordement | CI/CD, store, production |
| `discovery` | projet suffisamment observé et contradictions visibles | choix définitifs |
| `development` | tranche développable, testable et reprenable | artefact final |
| `release` | artefact versionné, immuable et qualifié | publication ou déploiement |
| `distribution` | même artefact publiable ou déployable | exploitation permanente |
| `operation` | santé, maintenance, reprise et retrait | aucune couche fictive |

Les validations sont cumulatives, mais les profils et préoccupations rendent certaines exigences conditionnelles.

Le régime de développement est un autre concept. Il répond à « quelle liberté
possède la tranche active ? » et prend les valeurs `exploration`,
`construction`, `intégration` ou `stabilisation`. Il n’est ni un niveau
d’adoption, ni une portée, ni une phase machine.

## 4. Parcours d’un projet neuf

Suivre `guides/NEW_PROJECT.md`.

Au niveau `bootstrap`, compléter seulement :

1. identité et résultat recherché ;
2. vision courte ;
3. principes invariants ;
4. périmètre ;
5. une exigence vérifiable ;
6. un cas d’usage ;
7. état présent et première tranche.

Pour un logiciel, activer `software`, remplir le minimum réel de `project.yaml` et laisser une commande inconnue à `unresolved` avec une raison.

Release, distribution et exploitation restent normalement différées.
Une exploration bornée peut commencer sans inventer une architecture
définitive. Sa question, sa frontière et son résultat sont consignés dans
`PROJECT_STATE.md` dès que celui-ci devient la mémoire active.

## 5. Parcours d’un projet existant

Suivre `guides/EXISTING_PROJECT.md`.

Le bon ordre est :

```text
observer
→ inventorier
→ distinguer faits et inférences
→ relever collisions et contradictions
→ faire valider le diagnostic
→ mapper les rôles existants
→ adopter le minimum
```

Le diagnostic ne modifie rien :

```bash
python3 scripts/inspect-project.py /chemin/du/projet
```

N’écrasez jamais silencieusement `README.md`, `AGENTS.md`, `VERSION`, `CHANGELOG.md`, un workflow, un manifeste ou un lockfile.

Après validation humaine du diagnostic, une exploration isolée peut réduire une
inconnue avant l’adoption complète. Ici, « intégration » est réservée au
raccordement d’une tranche de code au socle réel ; l’installation du template
est appelée adoption de la méthode.

## 6. Mapper les rôles documentaires

Les règles exigent un rôle, non un chemin fixe :

```yaml
documents:
  architecture:
    path: docs/system/overview.md
    status: active
```

Les seuls statuts déclarables sont :

- `active` : applicable maintenant, chemin existant, aucun placeholder ;
- `deferred` : applicable plus tard, avec `until` et `reason` ;
- `not-applicable` : réellement sans objet, avec `reason`.

`required` est calculé par le validateur. Un projet ne peut pas se dispenser lui-même d’un invariant.

Un modèle dormant peut rester dans une copie complète du template : ses placeholders ne bloquent pas. Un projet existant ne doit copier que les fichiers retenus par son plan d’adoption.

## 7. Activer profils et préoccupations

Les profils disponibles sont documentés dans `profiles/README.md`. Leur activation machine se fait uniquement dans `project.adoption.yaml`.

Les préoccupations couvrent les dimensions transversales :

- interface utilisateur ;
- données persistantes ou sensibles ;
- réseau et authentification ;
- multi-utilisateur ;
- service en arrière-plan ;
- assets ;
- livraison automatisée.

N’activez pas une préoccupation « au cas où ». Activez-la lorsqu’elle existe ou lorsque la tranche courante la rend nécessaire.

## 8. Décrire la technologie

Pour un logiciel, `project.yaml` est confronté aux manifestes, lockfiles, scripts et cibles réels.

Ne confondez pas :

```text
langage
→ compilateur ou interpréteur
→ runtime
→ gestionnaire de dépendances
→ outil de build
→ framework éventuel
→ artefact
→ plateforme cible
```

Une détection produit un indice à confirmer. Elle ne choisit jamais silencieusement un gestionnaire, une commande ou un framework.

Statuts de commande :

- `defined` : `argv` non vide et vérifié ;
- `unresolved` : pertinent mais encore inconnu, avec raison ;
- `not-applicable` : sans objet, avec raison ;
- `disabled` : volontairement désactivé, avec raison.

## 9. Faire respirer le développement

La portée `development` contient une boucle réentrante :

```text
exploration ⇄ construction ⇄ intégration ⇄ stabilisation
                                                ├→ tranche close
                                                └→ si applicable : release
```

| Régime | Résultat recherché | Résultat du régime |
| --- | --- | --- |
| `exploration` | réduire une inconnue et comparer des pistes | observation conservée et piste retenue ou abandonnée |
| `construction` | matérialiser le comportement principal | tranche observable et contrôle ciblé |
| `intégration` | raccorder aux frontières réelles | contrats cohérents, raccourcis traités et tests de frontière |
| `stabilisation` | rendre la révision fiable | contrôles pertinents verts et risques restants explicites |

L’exploration autorise prototypes jetables, mocks, données fictives, valeurs
temporaires et dépendances d’essai isolées. Les invariants de secret, de
non-destruction, de réversibilité et d’honnêteté restent permanents.

Une petite correction peut condenser plusieurs régimes. Un défaut découvert en
stabilisation peut ramener en construction. La transition dépend d’une preuve,
pas d’un déplacement de fichier ou d’une impression de finition.

La source de vérité est le rôle `current-state`. Au bootstrap, il peut pointer
vers le brief ; à partir de la construction, son chemin par défaut est
`PROJECT_STATE.md`. Le canon complet est `docs/044_Boucle_Developpement.md`.

## 10. Séparer développement, release et distribution

Les phases universelles décrivent l’action :

```text
verify → produce → deliver → operate
```

Les portées décrivent la frontière :

```text
development → release → distribution → operation
```

Ces axes sont orthogonaux. Une release utilise par exemple `verify`, `produce`, puis `deliver:create-release`.

Règle centrale :

> La distribution consomme un `release-artifact` immuable et qualifié. Elle ne build, ne package et ne signe pas une nouvelle copie.

Si la release et la distribution utilisent des pipelines distincts, déclarer
le `handoff` persistant de l’artefact et vérifier son digest. Une portée manuelle
de release ou de distribution conserve un graphe d’opérations avec
`orchestrator: manual` et une procédure explicite.

Une cible future peut être déclarée sous `distribution.intent` tandis que la portée reste `deferred`.

La stabilisation reste dans `development`. Elle prépare une révision source et
ses preuves ; elle ne package, ne signe et ne crée pas la release.

## 11. Lancer la validation

Installer une fois :

```bash
python3 -m pip install --requirement scripts/requirements-validation.txt
```

Puis :

```bash
./scripts/check-project.sh bootstrap
./scripts/check-project.sh discovery
./scripts/check-project.sh development
./scripts/check-project.sh release
./scripts/check-project.sh distribution
./scripts/check-project.sh operation
```

Sans argument, le script lit le niveau courant. Une sortie machine est disponible :

```bash
./scripts/check-project.sh --current --format json
```

Le contrôle local et GitHub Actions passent par la même entrée. Une dépendance de validation absente provoque une erreur explicite ; aucun contrôle n’est ignoré.

## 12. Maintenir les sources de vérité

- `README.md` : identité durable ;
- rôle `current-state` : présent opérationnel et reprise, mappé par défaut vers
  `PROJECT_STATE.md` à partir de la construction ;
- `docs/050_Roadmap.md` : futur envisagé ;
- `CHANGELOG.md` : versions publiées ;
- `RETROSPECTIVE.md` : apprentissage de méthode ;
- ADR : décisions structurantes.

Ne dupliquez pas la même information dans ces fichiers.

À chaque jalon :

1. comparer le résultat à la vision ;
2. actualiser l’état réel ;
3. fermer ou reformuler les questions ;
4. conserver les preuves ;
5. retirer les règles devenues fausses ;
6. décider explicitement si le niveau suivant devient applicable.

## 13. Personnalisation visuelle

- fondations communes : lisibilité, focus, accessibilité, responsive et mouvement réduit ;
- signature du template : défaut remplaçable ;
- identité du projet : couleurs, tonalité, illustration et densité propres.

Un projet sans interface n’active pas les rôles de design. Un projet avec interface conserve les fondations, même s’il remplace entièrement la signature visuelle.

## 14. Retour vers le template

Une amélioration remonte au template lorsqu’elle est générique, répétée ou protège un invariant commun. Une particularité métier reste dans son projet ou son profil.

La v1.7 rend la liberté et la rigueur proportionnelles au régime de la tranche.
Elle ne modifie ni les niveaux d’adoption, ni les portées, ni les phases du
manifeste et n’ajoute aucun moteur universel de commandes.
