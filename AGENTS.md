# Instructions pour les agents

## Mission

Intervenir sur ce projet sans perdre son intention, son vocabulaire ni ses invariants.

## Avant de modifier

1. Lire `project.adoption.yaml`, le document mappé au rôle `current-state`, `README.md`, les rôles actifs, les profils et les décisions concernées. Le chemin par défaut du présent opérationnel est `PROJECT_STATE.md`.
2. Identifier dans ce rôle la tranche active et son régime :
   `exploration`, `construction`, `intégration`, `stabilisation` ou aucune tranche active.
3. Examiner l’état réel du projet et les changements déjà présents ; ne pas confondre capacité prévue, expérimentale, intégrée et fonctionnelle.
4. Identifier la source de vérité, la frontière de liberté et les invariants touchés.
5. Rechercher un concept existant avant d’introduire un terme ou une abstraction.
6. Distinguer clairement constat, hypothèse, proposition et décision.
7. Vérifier sources, risques, données, flux et échelles lorsque la tâche les affecte.
8. En intégration ou stabilisation, vérifier `docs/095_Registre_Audit.md` et ne pas déclarer terminé un point encore ouvert dans le périmètre touché.
9. Pour un projet logiciel, lire `project.yaml` et vérifier qu'il correspond aux manifestes, lockfiles, scripts, commandes et cibles réellement présents. En exploration, ne compléter que les éléments touchés et ne pas remplir artificiellement les inconnues.
10. Si la livraison est touchée, distinguer opération universelle, politique, orchestrateur, artefact, environnement et cible ; ne jamais écrire une valeur de secret dans le manifeste.
11. Pour une adoption `existing` encore au niveau `discovery`, rester en lecture seule tant que le diagnostic n’a pas été validé. Après validation, un travail borné peut commencer ; le niveau `development` doit être validé avant de déclarer l’intégration terminée.

Si aucun régime n’est déclaré, le préciser avant d’agir. Ne jamais supposer
silencieusement qu’un prototype est en stabilisation.

## Invariants permanents

- préserver les changements sans rapport avec la tâche ;
- ne jamais écrire un secret, jeton ou donnée réelle sensible dans le dépôt, les tests, captures ou journaux ;
- ne jamais détruire silencieusement une donnée, un historique ou une voie de retour ;
- identifier clairement ce qui est expérimental ;
- ne pas présenter une capacité temporaire comme intégrée, stable ou terminée ;
- empêcher un prototype d’entrer silencieusement dans une release ou une distribution ;
- ne pas modifier silencieusement le sens d’un concept ;
- ne pas déclarer dans le document mappé au rôle `current-state` une capacité sans preuve proportionnée ;
- signaler les contradictions au lieu d’en choisir arbitrairement une version ;
- ne pas confondre langage, compilateur/interpréteur, runtime, gestionnaire de dépendances, outil de build, framework et plateforme ;
- ne jamais déduire silencieusement une commande depuis une simple convention technologique ;
- ne jamais confondre publication d'un artefact, création d'une release et déploiement dans un environnement ;
- ne jamais reconstruire un artefact dans la portée `distribution`.

## Exigences selon le régime

| Régime | Liberté et obligation |
| --- | --- |
| `exploration` | Essayer plusieurs pistes, mocks, données fictives, valeurs temporaires et prototypes jetables dans une frontière visible. Conserver l’observation et décider explicitement quoi jeter ou retenir. ADR, couverture exhaustive et documentation finale peuvent attendre. |
| `construction` | Matérialiser la piste retenue par une petite tranche observable. Relier le comportement principal à un critère d’acceptation, ajouter les contrôles ciblés et consigner les raccourcis temporaires. |
| `intégration` | Raccorder aux vrais contrats, données, erreurs, permissions, composants et sources de vérité. Retirer ou isoler les mocks, justifier les dépendances et traiter compatibilité, migration et retour arrière lorsqu’ils sont affectés. |
| `stabilisation` | Geler le périmètre fonctionnel, corriger, simplifier et exécuter les validations proportionnées au risque. Fermer ou expliciter les dettes, actualiser l’état, l’audit et la documentation. |

Une décision structurante reçoit une ADR lorsqu’elle est retenue pour le socle,
pas pour chaque variante exploratoire. Une dépendance d’essai peut rester isolée
pendant l’exploration ; elle doit être justifiée ou retirée avant la fin de
l’intégration.

## Règles du socle stable

Les exigences suivantes deviennent obligatoires pour ce qui rejoint le socle
stable. Une exploration peut y déroger temporairement à l’intérieur de sa
frontière déclarée, sans enfreindre les invariants permanents.

- préférer une modification petite, cohérente et vérifiable ;
- ne pas déplacer la logique métier dans l’interface ;
- ne pas introduire une couleur, une taille, un rayon, une ombre ou une durée arbitraire lorsqu’un token existe ;
- couvrir les états vide, chargement, erreur, succès, indisponible et dégradé lorsqu’ils sont possibles ;
- préserver une cible tactile minimale de 48 px et un focus clavier visible ;
- employer des icônes SVG cohérentes plutôt que des emojis comme éléments d’interface ;
- respecter `prefers-reduced-motion` et ne pas verrouiller le zoom utilisateur ;
- vérifier au minimum téléphone, tablette/fold et bureau pour toute interface responsive ;
- préserver la compatibilité ou fournir migration, sauvegarde et retour arrière ;
- traiter installation, configuration, démarrage, diagnostic, mise à jour, sauvegarde, restauration et suppression comme un cycle explicite lorsque le projet est distribué ;
- mettre à jour le document mappé au rôle `current-state` à chaque transition de régime et à la fin de toute tranche qui change l’état réel du projet ; `PROJECT_STATE.md` devient le chemin par défaut à partir de la construction ;
- alimenter `RETROSPECTIVE.md` à la fin d’un jalon, sans transformer chaque micro-changement en cérémonie ;
- tester proportionnellement au risque ;
- ne pas activer release, distribution ou exploitation uniquement parce que leurs modèles existent ;
- préserver les chemins et sources de vérité existants lorsqu’un rôle documentaire peut y être mappé.

Les vérifications exhaustives d’interface, d’accessibilité, de compatibilité et
de migration s’appliquent avant la fin de l’intégration ou pendant la
stabilisation lorsqu’elles sont pertinentes. Elles ne doivent pas bloquer une
première sonde visuelle isolée en exploration.

## Transitions de régime

- `exploration → construction` : piste retenue et observation conservée ;
- `construction → intégration` : comportement principal observable et contrôle ciblé ;
- `intégration → stabilisation` : raccordement réel, raccourcis traités et contrats cohérents ;
- sortie de `stabilisation` : contrôles pertinents verts, risques explicites et révision source identifiable ; activer `release` seulement si un livrable versionné est applicable.

Un retour vers un régime antérieur est normal lorsqu’une preuve invalide la
solution. Le canon du dépôt modèle est `docs/044_Boucle_Developpement.md` ;
les règles présentes ici restent suffisantes lorsqu’il n’est pas installé dans
un dépôt adopté.

## Validation minimale

En exploration, exécuter au moins la sonde qui peut confirmer ou invalider
l’hypothèse. À chaque transition, appliquer le critère du régime suivant.

Avant de quitter la stabilisation ou avant une livraison, exécuter les commandes
réellement définies dans `project.yaml`, puis `./scripts/check-project.sh`.
Vérifier : comportement demandé, tests pertinents, documentation touchée,
absence de secret, cohérence avec le glossaire, accessibilité, rendu visuel,
migration et retour arrière lorsque pertinents.

Le résumé final doit distinguer : réalisé et vérifié, réalisé mais non vérifié, non réalisé, risques restants et prochaine action.

## Commandes du projet

La source calculable est `project.yaml`. `defined` exige un `argv` vérifié ; `unresolved`, `not-applicable` et `disabled` exigent une raison.

La validation de la méthode est :

```bash
./scripts/check-project.sh
```

Ne jamais exécuter une commande `unresolved` ni tenter d’interpréter une variable `{{...}}`.
