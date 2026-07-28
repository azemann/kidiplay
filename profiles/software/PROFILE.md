# Profil logiciel

## À décider

- application, bibliothèque, CLI ou service ;
- plateformes et versions supportées ;
- modèle de données et formats publics ;
- fonctionnement local, distant ou hybride ;
- installation, configuration et mise à jour ;
- stratégie d’erreur et de journalisation ;
- tests, distribution et fin de support.

## Invariants proposés

- domaine indépendant de l’interface et des fournisseurs ;
- sources de vérité uniques ;
- export sans enfermement ;
- opérations sensibles explicites ;
- dépendances justifiées et remplaçables ;
- reprise après interruption définie pour les écritures importantes.

## Exigences progressives

- `bootstrap` : manifeste technologique minimal et cible principale ;
- `development` : architecture, choix et registre technologiques, qualité et contrats ;
- `release` : seulement si un artefact versionné doit être qualifié ;
- `distribution` : seulement si une publication, un store ou un déploiement existe ;
- `operation` : seulement pour une application installée, un service ou des données persistantes.

Les rôles exacts sont calculés depuis `project.adoption.yaml`. Ce profil n’impose pas à lui seul données, interface, sécurité avancée ou exploitation.

À l’intérieur de `development`, la tranche active suit selon le besoin :

```text
exploration ⇄ construction ⇄ intégration ⇄ stabilisation
```

Ce sont des régimes de liberté et de preuve, non des niveaux ou des phases de
pipeline. Leur état est conservé dans le document mappé au rôle
`current-state` ; `PROJECT_STATE.md` devient le chemin par défaut à partir de
la construction.
