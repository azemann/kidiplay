# Modèle de menace — module conditionnel

À conserver pour tout système exposé à un réseau, manipulant des comptes, exécutant des actions privilégiées ou conservant des données sensibles.

## Actifs à protéger

| Actif | Valeur | Propriétaire | Conséquence d’une perte/altération |
| --- | --- | --- | --- |
| {{ASSET}} | {{ASSET_VALUE}} | {{ASSET_OWNER}} | {{ASSET_IMPACT}} |

## Acteurs et capacités

| Acteur | Accès initial | Capacité supposée | Objectif possible | Confiance |
| --- | --- | --- | --- | --- |
| {{THREAT_ACTOR}} | {{INITIAL_ACCESS}} | {{ACTOR_CAPABILITY}} | {{ACTOR_GOAL}} | {{TRUST_LEVEL}} |

## Scénarios

| ID | Scénario | Précondition | Détection | Prévention | Réponse | Risque résiduel |
| --- | --- | --- | --- | --- | --- | --- |
| TM-001 | {{THREAT_SCENARIO}} | {{THREAT_PRECONDITION}} | {{THREAT_DETECTION}} | {{THREAT_CONTROL}} | {{THREAT_RESPONSE}} | {{RESIDUAL_RISK}} |

## Surfaces d’attaque à examiner

- authentification et récupération de compte ;
- autorisation et élévation de privilège ;
- entrées, fichiers et importations ;
- API, réseau local et accès distant ;
- mises à jour et dépendances ;
- sauvegardes et journaux ;
- installation, service système et désinstallation ;
- agents et outils capables d’agir.

