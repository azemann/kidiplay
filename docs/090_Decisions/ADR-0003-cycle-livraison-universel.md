# ADR-0003 — Modéliser la livraison comme un graphe universel

- **Statut :** accepté
- **Date :** 2026-07-21
- **Décideurs :** {{DECISION_OWNERS}}

## Contexte

La v1.4 décrit la chaîne technologique mais pas complètement le devenir des sources et artefacts. Réduire le CI/CD à `.github/workflows` lierait le modèle à un fournisseur et confondrait opérations, orchestration et politique.

## Décision

Le template modélise la livraison par un graphe optionnel d'opérations réparties entre `verify`, `produce`, `deliver` et `operate`. Les orchestrateurs sont des adaptateurs. Les artefacts sont identifiés et traçables ; les environnements portent les protections ; les secrets ne sont que référencés ; promotion, reprise et rollback sont explicites.

Le schéma reste déclaratif. Aucun moteur universel ou générateur multi-fournisseurs n'est inclus en v1.5.

## Conséquences

- un même projet peut exprimer sa livraison indépendamment de GitHub, GitLab, Jenkins ou Unity ;
- les différences de fournisseurs restent visibles dans les profils ;
- les projets simples peuvent omettre toute livraison non applicable ;
- la complexité du schéma augmente et exige des exemples et validations ;
- une future exécution devra valider le DAG, l'idempotence, les références et les politiques avant toute mutation.

## Alternatives rejetées

- une chaîne fixe de quinze étapes : non applicable à tous les projets ;
- un workflow GitHub Actions comme source de vérité : dépendance fournisseur ;
- un moteur universel immédiat : abstraction non encore éprouvée ;
- des secrets dans le manifeste : risque de fuite et responsabilité mal placée.
