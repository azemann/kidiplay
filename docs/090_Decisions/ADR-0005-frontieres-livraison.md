# ADR-0005 — Séparer développement, release, distribution et exploitation

- **Statut :** accepté
- **Date :** 2026-07-24
- **Décideurs :** mainteneur du template

## Contexte

Le graphe v1.5 distingue les phases `verify`, `produce`, `deliver` et `operate`, mais un pipeline peut encore mélanger contrôle de PR, construction finale, publication et rollback. Un projet neuf ne peut pas exprimer simplement « développement actif, distribution différée, cible connue ».

## Décision

Le manifeste logiciel v3 ajoute quatre portées orthogonales aux phases :

- `development` : vérification et éventuel build de contrôle ;
- `release` : vérification finale, build, package et création de release ;
- `distribution` : vérification de l’artefact, publication, promotion ou déploiement ;
- `operation` : observation, mise à jour, reprise et retrait.

Un pipeline appartient à une seule portée. La distribution consomme uniquement
un `release-artifact` immuable, versionné, lié à une révision et qualifié, reçu
par un handoff persistant dont le digest est vérifié. Elle ne peut ni construire
ni empaqueter.

Une portée peut être `active`, `deferred`, `unresolved` ou `not-applicable`. Une cible future peut être déclarée comme intention sans pipeline, secret ou environnement actif.

## Conséquences

- la CI de développement reste légère et indépendante de la mise en production ;
- l’artefact qualifié matérialise la frontière entre fabrication et distribution ;
- le même artefact est publié, promu et déployé ;
- les manifestes v1 et v2 restent valides pour le développement, mais doivent
  migrer avant de prouver une release ou une distribution ;
- la migration vers v3 exige une décision humaine sur la portée de chaque pipeline.

## Alternatives rejetées

- déduire la portée depuis le nom du pipeline : non fiable ;
- reconstruire pour chaque environnement : rompt la traçabilité ;
- fusionner portée et phase : une release utilise plusieurs phases ;
- exiger la distribution au bootstrap : comptes, clés et environnements prématurés.
