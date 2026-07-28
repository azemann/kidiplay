# Diagnostic initial

Ce document est requis au niveau `discovery` pour l’adoption d’un dépôt existant. Il décrit ce qui a été observé avant toute modification.

## Périmètre observé

{{DISCOVERY_SCOPE}}

## Confirmé

Faits directement soutenus par un fichier, un manifeste, un lockfile, une commande déclarée ou une preuve reproductible.

- {{CONFIRMED_FACT}}

## Probable

Déductions fortement soutenues mais encore à confirmer.

- {{PROBABLE_FACT}}

## Ambigu

Plusieurs interprétations restent compatibles avec les preuves.

- {{AMBIGUOUS_FACT}}

## Contradictoire

Deux sources de vérité ou indices ne racontent pas la même chose.

- {{CONTRADICTION}}

## Absent ou inconnu

- {{MISSING_OR_UNKNOWN}}

## Éléments à préserver

- fichiers et historiques : {{FILES_TO_PRESERVE}}
- changements locaux : {{LOCAL_CHANGES}}
- interfaces et contrats : {{CONTRACTS_TO_PRESERVE}}

## Commandes détectées mais non exécutées

| Rôle | Déclaration observée | Provenance | Confiance |
| --- | --- | --- | --- |
| {{COMMAND_ROLE}} | `{{COMMAND_DECLARATION}}` | {{COMMAND_SOURCE}} | {{COMMAND_CONFIDENCE}} |

## Collisions avec le template

| Chemin | Rôle actuel | Décision proposée |
| --- | --- | --- |
| {{COLLIDING_PATH}} | {{CURRENT_ROLE}} | {{COLLISION_DECISION}} |

## Adoption minimale proposée

- rôles documentaires à mapper : {{DOCUMENT_ROLE_MAPPING}}
- profils à activer : {{PROFILES_TO_ACTIVATE}}
- fichiers strictement nécessaires : {{MINIMAL_NEW_FILES}}
- changements différés : {{DEFERRED_CHANGES}}

## Prochaine action

{{NEXT_DISCOVERY_ACTION}}

Tant que la validation ci-dessous n’est pas accordée, le régime reste
observation en lecture seule. Si une exploration commence ensuite avant
l’adoption complète, ce document peut temporairement remplir le rôle
`current-state` à condition d’y consigner le régime, la frontière de liberté et
le critère de passage.

## Validation humaine

- **Décision :** {{DISCOVERY_APPROVAL}}
- **Responsable :** {{DISCOVERY_APPROVER}}
- **Date :** {{DISCOVERY_APPROVAL_DATE}}
