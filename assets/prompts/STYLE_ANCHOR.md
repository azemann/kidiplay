# Ancre stylistique KidiPlay

## Formulation canonique

Direction artistique officielle KidiPlay : illustration jeunesse chaleureuse,
formes très arrondies, texture douce de papier peint et de jouet, contours
propres légèrement irréguliers, volumes moelleux, ombres courtes et diffuses,
palette pastel jaune, orange, bleu ciel, vert tendre et rose, expressions
joyeuses et rassurantes, aucun réalisme photographique, aucun texte.

Pour un asset isolé, ajouter :

> Personnage ou objet unique, entièrement visible, centré avec une marge
> généreuse, sans décor, sans sol, sans reflet et sans ombre portée, destiné à
> un export PNG avec canal alpha.

## Invariants

- conserver les rôles de couleur définis dans `docs/012_Charte_Graphique.md` ;
- limiter les détails qui disparaissent à la taille d’usage ;
- ne jamais générer de texte dans un asset d’interface ;
- produire une famille cohérente plutôt que des éléments isolés sans référence ;
- valider le détourage et le chargement Skia avant de qualifier un asset.
