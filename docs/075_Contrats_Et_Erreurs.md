# Contrats, erreurs et compatibilité

## Contrats internes et externes

| ID | Producteur | Consommateur | Format/version | Validation | Compatibilité |
| --- | --- | --- | --- | --- | --- |
| CT-001 | {{CONTRACT_PRODUCER}} | {{CONTRACT_CONSUMER}} | {{CONTRACT_FORMAT}} | {{CONTRACT_VALIDATION}} | {{CONTRACT_COMPATIBILITY}} |

## Modèle d’erreur

Une erreur importante précise :

- catégorie stable ;
- cause technique conservée sans être exposée inutilement ;
- message utilisateur compréhensible ;
- caractère récupérable ou non ;
- action recommandée ;
- identifiant de corrélation lorsque pertinent ;
- données qu’il est interdit d’inscrire dans les journaux.

| Code | Situation | Message utilisateur | Récupération | Journalisation |
| --- | --- | --- | --- | --- |
| {{ERROR_CODE}} | {{ERROR_SITUATION}} | {{USER_ERROR_MESSAGE}} | {{ERROR_RECOVERY}} | {{ERROR_LOGGING}} |

## Versionnement

Définir la compatibilité des API, formats de fichiers, schémas de données, configurations et sauvegardes. Une rupture exige migration, preuve, sauvegarde préalable et stratégie de retour arrière.

## Idempotence et répétition

Les opérations susceptibles d’être relancées après une interruption indiquent si elles sont idempotentes, reprenables ou compensables.

