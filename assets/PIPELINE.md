# Pipeline des assets — module conditionnel

## Étapes

`intention → source → nettoyage → découpage → normalisation → intégration → validation → export`

## Contrat d’entrée

{{ASSET_INPUT_CONTRACT}}

## Transformations

| Étape | Outil | Entrée | Sortie | Paramètres | Reproductible ? |
| --- | --- | --- | --- | --- | --- |
| {{ASSET_STEP}} | {{ASSET_TOOL}} | {{ASSET_INPUT}} | {{ASSET_OUTPUT}} | {{ASSET_PARAMETERS}} | {{ASSET_REPRODUCIBLE}} |

## Contrat de sortie

{{ASSET_OUTPUT_CONTRACT}}

## Validation

- lisibilité à la taille d’utilisation ;
- fond et transparence corrects ;
- dimensions, nommage et compression conformes ;
- absence de texte inaccessible ou de marque indésirable ;
- variantes cohérentes ;
- source, licence et procédure enregistrées.

