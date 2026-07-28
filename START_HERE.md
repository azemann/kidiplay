# Commencer ici

Un seul template, deux portes d’entrée.

## A — Le projet est neuf

Partez de l’intention, du périmètre et d’une première tranche vérifiable.

1. Ouvrez `guides/NEW_PROJECT.md`.
2. Dans `project.adoption.yaml`, conservez `origin: new`.
3. Activez uniquement les profils réellement utiles.
4. Complétez les documents actifs du niveau `bootstrap`.
5. Lancez :

```bash
./scripts/check-project.sh bootstrap
```

La release, la distribution et l’exploitation peuvent rester différées. Déclarez tôt la cible finale si elle influence le produit, mais ne configurez pas encore de store, de signature ou de production.

## B — Le dépôt contient déjà un projet

Commencez par observer. Ne copiez pas tout le template et n’écrasez aucun fichier existant.

1. Ouvrez `guides/EXISTING_PROJECT.md`.
2. Depuis une copie du template, lancez le diagnostic en lecture seule :

```bash
python3 scripts/inspect-project.py /chemin/du/projet
```

3. Faites valider le diagnostic avant toute adoption ou modification.
4. Mappez les rôles documentaires vers les fichiers déjà présents.
5. Lancez ensuite :

```bash
./scripts/check-project.sh discovery
```

Le diagnostic n’installe rien, n’exécute aucun script du dépôt et ne modifie aucun fichier.

## Convergence

Les deux parcours convergent comme preuve d’adoption :

```text
new      → bootstrap ───────────┐
                                ├→ development validé
existing → discovery ───────────┘
```

Le travail de chaque tranche possède sa propre boucle, qui peut commencer avant
la validation complète du niveau `development` :

```text
exploration ⇄ construction ⇄ intégration ⇄ stabilisation
                                                ├→ tranche close
                                                └→ si applicable : release
```

`new` et `existing` décrivent seulement l’entrée dans la méthode. Ils ne créent pas deux types permanents de projets.

Les quatre régimes appartiennent à la tranche active, pas au projet entier.
L’exploration peut commencer avant que le niveau `development` soit entièrement
validé ; dans un dépôt existant, elle attend la validation humaine du
diagnostic. Elle reste bornée, identifiable et réversible.

Ne remplissez pas tout le dépôt. Le validateur indique ce qui est requis maintenant, ce qui est différé et la prochaine action.
