# Données et schémas

## Inventaire canonique

| Donnée/agrégat | Identité stable | Source de vérité | Création | Mutation | Suppression | Sensibilité |
| --- | --- | --- | --- | --- | --- | --- |
| {{DATA_ENTITY}} | {{STABLE_IDENTITY}} | {{DATA_SOURCE_OF_TRUTH}} | {{DATA_CREATION}} | {{DATA_MUTATION}} | {{DATA_DELETION}} | {{DATA_CLASSIFICATION}} |

## Distinctions métier

Documenter ici les concepts techniquement proches mais non interchangeables, par exemple identité/emplacement, direct/enregistrement, source/donnée dérivée ou fichier/ressource.

| Concept A | Concept B | Différence opératoire | Risque de confusion |
| --- | --- | --- | --- |
| {{DATA_CONCEPT_A}} | {{DATA_CONCEPT_B}} | {{OPERATIONAL_DIFFERENCE}} | {{CONFUSION_RISK}} |

## Schémas et versions

| Schéma | Format | Version actuelle | Compatibilité lecture | Compatibilité écriture | Emplacement |
| --- | --- | --- | --- | --- | --- |
| {{SCHEMA_NAME}} | {{SCHEMA_FORMAT}} | {{SCHEMA_VERSION}} | {{READ_COMPATIBILITY}} | {{WRITE_COMPATIBILITY}} | {{SCHEMA_LOCATION}} |

## Import, export et portabilité

- formats ouverts disponibles ;
- validation avant import ;
- rapport des éléments rejetés ;
- export complet sans dépendance au fournisseur ;
- conservation des identifiants lorsque nécessaire ;
- politique de données dérivées et recalculables.

## Migrations

Chaque migration précise préconditions, sauvegarde, transformation, validation, idempotence, reprise après interruption et retour arrière.

