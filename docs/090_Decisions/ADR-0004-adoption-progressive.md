# ADR-0004 — Deux portes d’entrée et une adoption progressive

- **Statut :** accepté
- **Date :** 2026-07-24
- **Décideurs :** mainteneur du template

## Contexte

La v1.5 décrit correctement un projet mûr, mais présente presque toutes ses couches dès le premier usage. Le guide demande de supprimer les documents non applicables tandis que le contrôle exige une liste fixe et scanne les placeholders de tout le dépôt. Cette contradiction rend le bootstrap lourd et l’adoption d’un dépôt existant dangereuse.

## Décision

Le template conserve un seul noyau et introduit deux origines d’adoption, `new` et `existing`, qui convergent à `development`.

Un manifeste séparé, `project.adoption.yaml`, porte le niveau courant, les profils, les préoccupations et la correspondance entre rôles documentaires et chemins réels. L’obligation d’un rôle est calculée ; seuls `active`, `deferred` et `not-applicable` sont déclarables.

Le contrôle devient progressif et cumulatif. Les placeholders ne sont recherchés que dans les documents actifs. Un diagnostic en lecture seule précède toute adoption d’un dépôt existant.

## Conséquences

- un projet neuf peut valider son bootstrap sans préparer la distribution ;
- un projet existant conserve ses chemins et sources de vérité ;
- les exigences apparaissent lorsqu’elles deviennent applicables ;
- le validateur doit expliquer la provenance et la prochaine action ;
- la méthode possède désormais un manifeste supplémentaire, volontairement limité à l’adoption.

## Alternatives rejetées

- deux templates séparés : divergence inévitable après l’entrée ;
- tous les documents obligatoires dès le départ : coût sans rapport avec la maturité ;
- suppression manuelle sans registre : incohérente avec la validation ;
- statut `required` choisi par le projet : permettrait de contourner un invariant ;
- copie automatique dans un dépôt existant : risque d’écrasement et de régression.
