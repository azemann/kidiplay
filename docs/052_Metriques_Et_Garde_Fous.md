# Métriques et garde-fous — module conditionnel

## Résultat principal

| Métrique | Définition | Source | Fenêtre | Segments | Cible | Limites |
| --- | --- | --- | --- | --- | --- | --- |
| {{PRIMARY_METRIC}} | {{METRIC_DEFINITION}} | {{METRIC_SOURCE}} | {{METRIC_WINDOW}} | {{METRIC_SEGMENTS}} | {{METRIC_TARGET}} | {{METRIC_LIMITS}} |

## Pilotes

| Pilote | Relation attendue | Mesure | Action possible |
| --- | --- | --- | --- |
| {{DRIVER_METRIC}} | {{EXPECTED_RELATION}} | {{DRIVER_MEASURE}} | {{DRIVER_ACTION}} |

## Garde-fous

| Garde-fou | Dégradation interdite | Seuil | Réponse |
| --- | --- | --- | --- |
| {{GUARDRAIL}} | {{FORBIDDEN_DEGRADATION}} | {{GUARDRAIL_THRESHOLD}} | {{GUARDRAIL_RESPONSE}} |

## Règles

- ne pas optimiser une métrique isolée au détriment du système ;
- versionner les définitions ;
- distinguer mesure produit, métrique technique et indicateur commercial ;
- documenter biais, données manquantes et changements d’instrumentation.

