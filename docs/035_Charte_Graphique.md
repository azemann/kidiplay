# Charte graphique

## Intention

Créer une interface professionnelle, lisible, calme et immédiatement compréhensible, avec une profondeur visuelle maîtrisée. La technologie reste en arrière-plan ; l’état et l’action utile dominent.

## Signature visuelle par défaut

- fond sombre proche du bleu nuit, jamais noir plat généralisé ;
- surfaces bleu-gris superposées ;
- cartes légèrement translucides lorsque le contexte le justifie ;
- bordures claires fines et ombres douces ;
- texte principal blanc cassé, texte secondaire atténué ;
- accents peu nombreux et sémantiques ;
- gradients et lueurs réservés aux points d’attention ;
- coins arrondis cohérents, sans transformer chaque élément en pilule.

Cette signature est un défaut de gamme, pas une obligation de marque. Les fondations d’accessibilité et de cohérence restent obligatoires même si l’identité visuelle change.

## Identité du projet

- **Caractère :** {{BRAND_CHARACTER}}
- **Tonalité :** {{BRAND_TONE}}
- **Couleur ou accent distinctif :** {{BRAND_ACCENT}}
- **Densité :** {{INTERFACE_DENSITY}}
- **Principe de différenciation :** {{VISUAL_DIFFERENTIATOR}}

## Couleurs

Les valeurs canoniques vivent dans `design/tokens.css`.

| Rôle | Usage |
| --- | --- |
| fond | toile générale et ambiance |
| surface | panneaux, cartes et navigation |
| texte | hiérarchie primaire, secondaire, discrète |
| accent | action ou information dominante |
| succès | état confirmé ou sain |
| avertissement | attention sans échec |
| danger | erreur, arrêt ou action destructive |

La couleur ne constitue jamais l’unique indicateur : ajouter texte, forme, icône ou position.

## Typographie

- pile système : `system-ui`, `-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, `sans-serif` ;
- titres forts avec espacement légèrement resserré ;
- grands titres fluides via `clamp()` ;
- corps lisible, sans taille inférieure à 16 px par défaut ;
- micro-libellés en capitales uniquement pour de courtes catégories ;
- nombres et états importants alignés et immédiatement comparables.

## Iconographie

- SVG interne ou bibliothèque SVG homogène ;
- trait, taille optique et angles cohérents ;
- aucune icône seule sans nom accessible ;
- pas d’emoji comme composant fonctionnel ;
- pictogrammes décoratifs explicitement ignorés par les technologies d’assistance.

## Images et illustrations

{{IMAGE_DIRECTION}}

Les visuels générés ou importés doivent être lisibles à leur taille réelle, sans texte intégré lorsque celui-ci doit rester accessible ou traduisible.

## Mouvement

- durée courte : 160 ms ;
- durée standard : 200 ms ;
- durée ample maximale courante : 220 ms ;
- animer principalement opacité et transformation ;
- ne jamais retarder une action pour montrer une animation ;
- réduire ou supprimer les mouvements non indispensables lorsque demandé par le système.

## À éviter

- néons sur chaque élément ;
- glassmorphism qui réduit le contraste ;
- ombres et rayons différents sans logique ;
- textes gris trop faibles ;
- animations permanentes ;
- interfaces techniques exposant directement noms de fichiers, services ou adaptateurs sans nécessité utilisateur.

## Contrastes et thèmes

Le thème sombre fourni doit être mesuré, pas supposé accessible. Si un thème clair est livré, il possède ses propres tokens sémantiques et subit la même validation. Le système ne doit pas inverser mécaniquement les couleurs.
