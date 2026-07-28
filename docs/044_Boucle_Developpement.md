# Boucle de développement

## Décision

La portée `development` possède quatre régimes de travail pour la tranche active :

```text
exploration ⇄ construction ⇄ intégration ⇄ stabilisation
                                                ├→ tranche close
                                                └→ si applicable : release
```

Cette boucle n’est pas une nouvelle série de niveaux d’adoption, de portées de
livraison ou de phases d’opération :

- le **niveau d’adoption** indique ce que la méthode sait déjà du projet ;
- la **portée** sépare développement, release, distribution et exploitation ;
- la **phase** classe une opération en `verify`, `produce`, `deliver` ou `operate` ;
- le **régime** règle la liberté et la preuve attendue pour la tranche en cours.

Le régime appartient à une tranche, pas au projet entier. Les retours sont
normaux, l’exploration est optionnelle et une petite correction peut condenser
plusieurs régimes. Les critères de passage restent applicables.

> Libre pour explorer, cohérent pour construire, rigoureux pour intégrer,
> strict pour stabiliser.

## Invariants permanents

Même en exploration :

- aucun secret ni donnée personnelle réelle n’est introduit ;
- aucune donnée, branche ou modification sans rapport n’est détruite
  silencieusement ;
- l’expérimental est identifiable et ne se présente pas comme intégré ;
- une voie de retour est conservée ;
- les capacités temporaires ne sont pas déclarées terminées ;
- un prototype n’entre pas silencieusement dans le socle stable, une release ou
  une distribution.

Ces invariants protègent le projet sans exiger dès le premier essai la qualité
d’une release.

## Les quatre régimes

| Régime | Question principale | Liberté admise | Preuve attendue |
| --- | --- | --- | --- |
| `exploration` | Quelle piste mérite d’être retenue ? | variantes, prototypes jetables, mocks, données fictives, valeurs temporaires et dépendances d’essai isolées | observation reproductible, piste retenue ou hypothèse invalidée |
| `construction` | La piste retenue peut-elle matérialiser le comportement visé ? | architecture encore modifiable, refactorisations locales et tests ciblés | comportement principal observable et critère d’acceptation relié |
| `intégration` | La tranche fonctionne-t-elle avec le vrai système ? | corrections de raccordement, adaptation des contrats et migrations explicites | frontières réelles raccordées, raccourcis traités, tests d’intégration pertinents |
| `stabilisation` | Peut-on faire confiance à cette révision ? | corrections et simplifications ; pas de nouvelle capacité hors nécessité de fiabilité | régressions, cas limites, sécurité, accessibilité, performance et documentation vérifiés selon le risque |

### Exploration

L’exploration réduit une inconnue. Elle peut commencer au niveau `bootstrap` ou,
pour un dépôt existant, après validation humaine du diagnostic `discovery`.

Elle peut utiliser un dossier d’expérience, une branche, un prototype local ou
une tranche clairement marquée. Une dépendance temporaire ne rejoint pas le
socle sans être réévaluée. Une valeur codée en dur ne contient jamais de secret
ou de donnée réelle sensible.

Une exploration peut se terminer par un abandon. Son résultat utile est alors
la preuve qui évite de répéter l’impasse, non du code à conserver.

### Construction

La construction matérialise une piste retenue. Le code vise désormais le
produit, mais sa forme peut encore changer. Les critères d’acceptation, les
commandes utiles et les tests ciblés deviennent explicites.

Les compromis temporaires restent visibles dans `PROJECT_STATE.md`. Une
démonstration locale ne prouve pas encore que la tranche respecte toutes les
frontières du système.

### Intégration

L’intégration raccorde la tranche au socle stable : contrats, données, erreurs,
permissions, composants, UX réelle et sources de vérité.

Les mocks qui remplacent une frontière réelle sont retirés ou conservés comme
fixtures explicites. Les nouvelles dépendances sont justifiées. Compatibilité,
migration et retour arrière sont traités lorsqu’ils sont affectés. Le niveau
d’adoption `development` doit être validé au plus tard avant de déclarer
l’intégration terminée.

### Stabilisation

La stabilisation gèle le périmètre fonctionnel de la tranche. Elle corrige,
réduit les risques et rassemble les preuves. Un défaut peut ramener la tranche
en construction ou en intégration ; ce retour n’est pas un échec de méthode.

La stabilisation reste dans la portée `development`. Elle peut produire un
build de contrôle ou un `verification-output`, jamais un `release-artifact`.

## Critères de transition

Une transition de régime est une décision explicite fondée sur une preuve :

- `exploration → construction` : une piste est retenue et l’observation qui la
  justifie est conservée ;
- `construction → intégration` : le comportement principal est observable et
  possède au moins un contrôle ciblé ;
- `intégration → stabilisation` : le raccordement réel fonctionne, les
  raccourcis sont retirés, isolés ou acceptés, et les contrats touchés sont
  cohérents ;
- sortie de `stabilisation` : les contrôles pertinents sont verts, les risques
  restants sont explicites et la révision source est identifiable. La tranche
  peut alors être close ou remise à `release` si un livrable versionné est
  applicable.

Le déplacement d’un fichier, un commit ou une impression de finition ne suffit
pas à faire changer une tranche de régime.

## Source de vérité et travail parallèle

Le document mappé au rôle `current-state` enregistre pour la tranche principale :

- le régime courant ;
- l’objectif ou l’inconnue ;
- la frontière de liberté ;
- les raccourcis temporaires ;
- le critère de passage ;
- les preuves disponibles.

Au bootstrap, ce rôle peut encore pointer vers `docs/007_Brief_Bootstrap.md`.
Dans un dépôt existant en découverte, il peut pointer vers le diagnostic validé.
À partir de la construction, `PROJECT_STATE.md` est le chemin par défaut et
devient la mémoire opérationnelle vivante.

Si plusieurs tranches avancent en parallèle, le document décrit la tranche
principale et chaque branche, issue ou pull request déclare son propre régime.
Il ne faut pas inventer un régime global censé résumer tout le dépôt.

## Frontière avec la release

La stabilisation prépare une révision source fiable et ses preuves. La portée
`release` produit ensuite l’artefact versionné, immuable et qualifié. La portée
`distribution` consomme exactement cet artefact.

Ainsi, liberté et rigueur ne s’opposent pas : elles s’appliquent à des moments
et à des frontières différents.

Dans ce document, `construction` n’est pas l’opération technique `build`, et
`intégration` n’est pas l’intégration continue. Une CI peut fournir des preuves
dans chacun des régimes.
