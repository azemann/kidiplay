# Procédures d’exploitation — module conditionnel

Une procédure doit rester accessible même lorsque le système principal est indisponible.

## Modèle de procédure

### RUN-001 — {{RUNBOOK_TITLE}}

- **Symptômes :** {{RUNBOOK_SYMPTOMS}}
- **Impact :** {{RUNBOOK_IMPACT}}
- **Préconditions :** {{RUNBOOK_PRECONDITIONS}}
- **Permissions nécessaires :** {{RUNBOOK_PERMISSIONS}}

#### 1. Vérifications sans mutation

{{READ_ONLY_CHECKS}}

#### 2. Diagnostic

{{DIAGNOSTIC_STEPS}}

#### 3. Réparation autorisée

{{REPAIR_STEPS}}

#### 4. Retour arrière

{{ROLLBACK_STEPS}}

#### 5. Validation finale

{{FINAL_VALIDATION}}

#### 6. Escalade

{{ESCALATION}}

## Procédures minimales à envisager

- service impossible à démarrer ;
- configuration invalide ;
- dépendance externe indisponible ;
- mise à jour ou migration interrompue ;
- disque plein ou stockage inaccessible ;
- sauvegarde ou restauration échouée ;
- perte de connexion ;
- désinstallation incomplète ;
- suspicion de compromission.

