# Architecture

## Contexte

{{ARCHITECTURE_CONTEXT}}

## Vue logique

Décrire les responsabilités avant les technologies.

| Composant | Responsabilité | Entrées | Sorties | Dépendances autorisées |
| --- | --- | --- | --- | --- |
| {{COMPONENT}} | {{RESPONSIBILITY}} | {{COMPONENT_INPUTS}} | {{COMPONENT_OUTPUTS}} | {{DEPENDENCIES}} |

La présentation dépend du modèle d’application par des contrats explicites. Elle traduit les états métier en états d’interface, mais ne devient pas la source de vérité des règles.

## Sources de vérité

| Information | Source canonique | Lecteurs | Écrivains |
| --- | --- | --- | --- |
| {{INFORMATION}} | {{SOURCE}} | {{READERS}} | {{WRITERS}} |

## Frontières externes

{{EXTERNAL_SYSTEMS}}

## Flux critique

{{CRITICAL_FLOW}}

## Première tranche verticale

Décrire le plus petit parcours complet qui traverse modèle, logique, stockage éventuel et interface, et qui apporte une valeur vérifiable. Cette tranche inclut son état de chargement, son erreur principale et sa validation responsive.

## Risques architecturaux

- {{ARCH_RISK}}
