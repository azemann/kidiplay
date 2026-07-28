# Plan de sauvegarde et de reprise — module conditionnel

## Objectifs

- **RPO — perte de données maximale acceptable :** {{RPO}}
- **RTO — durée maximale de rétablissement :** {{RTO}}
- **Mode dégradé acceptable :** {{ACCEPTABLE_DEGRADED_MODE}}

## Inventaire de reprise

| Élément | Sauvegardé ? | Emplacement | Chiffrement | Rétention | Responsable |
| --- | --- | --- | --- | --- | --- |
| {{RECOVERY_ITEM}} | {{IS_BACKED_UP}} | {{BACKUP_LOCATION}} | {{BACKUP_ENCRYPTION}} | {{BACKUP_RETENTION}} | {{BACKUP_OWNER}} |

## Ordre de restauration

1. {{RESTORE_STEP_1}}
2. {{RESTORE_STEP_2}}
3. {{RESTORE_STEP_3}}

## Validation

| Test | Fréquence | Dernier résultat | Preuve | Prochaine date |
| --- | --- | --- | --- | --- |
| {{RECOVERY_TEST}} | {{RECOVERY_FREQUENCY}} | {{RECOVERY_RESULT}} | {{RECOVERY_EVIDENCE}} | {{NEXT_RECOVERY_TEST}} |

## Scénarios

- panne locale ;
- perte ou corruption de données ;
- mise à jour défectueuse ;
- compromission ;
- indisponibilité d’un fournisseur ;
- perte de l’appareil principal.

