# Brief de bootstrap

Ce document court peut remplir plusieurs rôles au démarrage. Séparez ensuite les sujets dans les documents spécialisés seulement lorsque leur profondeur le justifie.

## Intention

- **Problème observé :** {{BOOTSTRAP_PROBLEM}}
- **Résultat recherché :** {{BOOTSTRAP_OUTCOME}}
- **Personne ou système concerné :** {{BOOTSTRAP_ACTOR}}

## Principes

- {{BOOTSTRAP_PRINCIPLE}}

## Périmètre

- **Inclus dans la première tranche :** {{BOOTSTRAP_INCLUDED}}
- **Explicitement exclu :** {{BOOTSTRAP_EXCLUDED}}

## Premier cas d’usage

- **Scénario :** {{BOOTSTRAP_USE_CASE}}
- **Critère d’acceptation observable :** {{BOOTSTRAP_ACCEPTANCE}}

## État de la première tranche de code

Tant qu’aucun essai n’a commencé :

- **Régime :** aucune tranche active ;
- **Frontière de liberté :** aucune ;
- **Critère de passage :** première inconnue bornée.

Si une exploration commence avant l’activation de `PROJECT_STATE.md`, mettre à
jour ces trois lignes. Ce brief remplit alors temporairement le rôle
`current-state`.

## Cible finale connue

{{BOOTSTRAP_FINAL_TARGET_OR_UNKNOWN}}

Cette cible est une intention. Elle n’active ni release, ni distribution, ni exploitation.
