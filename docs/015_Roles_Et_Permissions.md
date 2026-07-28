# Rôles et permissions — module conditionnel

À conserver lorsqu’il existe plusieurs catégories d’utilisateurs, agents, services ou administrateurs.

## Rôles

| Rôle | Responsabilité | Données visibles | Actions autorisées | Actions interdites |
| --- | --- | --- | --- | --- |
| {{ROLE}} | {{ROLE_RESPONSIBILITY}} | {{VISIBLE_DATA}} | {{ALLOWED_ACTIONS}} | {{FORBIDDEN_ACTIONS}} |

## Matrice d’autorisation

| Capacité | {{ROLE_A}} | {{ROLE_B}} | Condition | Journalisation |
| --- | --- | --- | --- | --- |
| {{CAPABILITY}} | autorisé | interdit | {{AUTH_CONDITION}} | {{AUTH_LOGGING}} |

## Principes

- refus par défaut ;
- moindre privilège ;
- séparation authentification/autorisation ;
- permissions évaluées côté source de vérité, pas seulement dans l’interface ;
- délégation, expiration et révocation explicites ;
- actions d’agents limitées par capacité et autorisation, jamais par simple recommandation.

