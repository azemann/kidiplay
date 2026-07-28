# Contribuer

## Flux recommandé

1. Relier le changement à un besoin ou problème précis.
2. Déclarer le régime de la tranche : exploration, construction, intégration ou stabilisation.
3. Vérifier le vocabulaire et les décisions existantes.
4. Explorer seulement si une inconnue le justifie, puis conserver le verdict.
5. Construire la plus petite tranche observable.
6. L’intégrer aux frontières réelles.
7. La stabiliser proportionnellement au risque.

Une petite correction peut condenser plusieurs régimes. Elle doit néanmoins
satisfaire leurs critères de sortie avant d’être présentée comme stable.

## Une contribution doit préciser

- intention ;
- régime courant et critère de passage ;
- périmètre inclus et exclu ;
- frontière expérimentale et raccourcis temporaires, s’ils existent ;
- concepts et sources de vérité touchés ;
- risques et compatibilité ;
- méthode de validation ;
- migration ou retour arrière si nécessaire.

Une contribution exploratoire peut rester en brouillon et différer ADR,
documentation finale ou couverture exhaustive. Elle ne doit jamais laisser
croire que son prototype est intégré.

## Convention de commit proposée

`type(zone): description concise`

Types suggérés : `feat`, `fix`, `docs`, `refactor`, `test`, `build`, `chore`.
