# ADR-0006 — Liberté graduée dans la boucle de développement

- **Statut :** accepté
- **Date :** 2026-07-27
- **Décideurs :** mainteneur du template

## Contexte

La v1.6 sépare correctement développement, release, distribution et
exploitation, mais traite encore `development` comme un bloc unique. Des règles
adaptées à l’intégration ou à la stabilisation s’appliquent alors trop tôt et
figent l’architecture avant que le code ait réduit les inconnues.

## Décision

La tranche active évolue entre quatre régimes réentrants : `exploration`,
`construction`, `intégration` et `stabilisation`.

Ces régimes ne deviennent ni niveaux d’adoption, ni portées de livraison, ni
phases machine. Leur source de vérité est le document mappé au rôle
`current-state`, dont `PROJECT_STATE.md` est le chemin normal à partir de la
construction ; `AGENTS.md` adapte la liberté, la documentation et les preuves
au régime courant.

Des invariants permanents protègent secrets, données, travail existant,
réversibilité et honnêteté de l’état déclaré. Le passage vers un régime plus
strict exige une preuve explicite. La stabilisation reste dans `development` et
ne produit pas de `release-artifact`.

## Conséquences

- l’exploration peut commencer sans architecture prématurément figée ;
- les prototypes jetables et les hypothèses invalidées deviennent des résultats
  légitimes ;
- les exigences augmentent à mesure que le travail rejoint le socle stable ;
- un retour vers un régime antérieur est normal ;
- les manifestes et schémas v1.6 restent compatibles ;
- la release et la distribution conservent leurs frontières strictes.

## Alternatives rejetées

- quatre nouveaux niveaux d’adoption : confondrait maturité de la méthode et
  travail d’une tranche ;
- quatre nouvelles portées ou phases : dupliquerait les axes déjà canoniques ;
- mêmes exigences dans tous les régimes : bloque l’exploration ou banalise la
  stabilisation ;
- liberté sans frontière : permettrait au code expérimental d’entrer
  silencieusement dans le produit.
