# Charte graphique KidiPlay

## 1. Intention visuelle

KidiPlay doit ressembler à un petit monde-jouet chaleureux : papier, crayons, peinture, autocollants, peluches et nature. L’interface doit être joyeuse sans devenir bruyante, infantilisante ou surchargée.

Mots-clés : doux, tactile, arrondi, lisible, chaleureux, rassurant, créatif, vivant.

## 2. Direction artistique

- Illustration jeunesse 2D.
- Formes simples et arrondies.
- Contours épais mais souples.
- Ombres courtes et diffuses.
- Texture légère de papier, craie ou gouache.
- Expressions positives et immédiatement lisibles.
- Peu de détails à petite taille.
- Aucun photoréalisme.
- Pas de 3D brillante ni d’effet plastique agressif.

## 3. Palette fondatrice

| Rôle | Nom | Couleur |
|---|---|---|
| Fond principal | Crème papier | `#FFF9E8` |
| Accent principal | Soleil | `#FFD54F` |
| Action chaude | Orange doux | `#FFB74D` |
| Action calme | Bleu ciel | `#81D4FA` |
| Nature / validation | Vert feuille | `#AED581` |
| Création / douceur | Rose poudré | `#F8BBD0` |
| Accent secondaire | Violet lavande | `#B39DDB` |
| Texte principal | Brun encre | `#4B3B2A` |
| Surface claire | Blanc chaud | `#FFFDF7` |
| Erreur douce | Corail | `#FF8A80` |

Règle : une surface principale claire, une couleur d’action dominante et deux accents maximum par écran.

## 4. Typographie

Famille recommandée pour les titres : `Fredoka` ou `Baloo 2`.
Famille recommandée pour le texte et les indications adultes : `Nunito`.

Principes :

- lettres rondes et très lisibles ;
- tailles généreuses ;
- phrases courtes ;
- pas de texte tout en capitales hors micro-libellé ;
- le sens ne doit jamais dépendre uniquement du texte.

## 5. Formes et composants

### Boutons

- grands ;
- rayon très arrondi ;
- contour ou ombre légère ;
- pictogramme central important ;
- rebond bref à l’appui ;
- état pressé visible ;
- zone tactile supérieure à la forme apparente.

### Cartes

- coins arrondis ;
- fond clair ;
- illustration centrale ;
- ombre discrète ;
- peu d’informations simultanées.

### Icônes

Toutes les icônes doivent partager :

- le même poids de contour ;
- la même perspective frontale ou légèrement trois-quarts ;
- une palette limitée ;
- une silhouette reconnaissable sans texte ;
- un fond transparent pour l’intégration ;
- un export raster PNG avec canal alpha, sans dépendance à un SVG.

## 6. Mascotte

Kiwi est la mascotte officielle de KidiPlay. C’est un petit oiseau turquoise,
rond et rassurant, avec un visage crème en forme de cœur, de grands yeux bruns,
des joues rose pâle, un bec et des pattes orange, et une salopette jaune portant
une étoile orange.

Les invariants de Kiwi sont conservés entre toutes les poses : proportions du
visage et du corps, trois plumes arrondies sur la tête, palette, salopette,
étoile centrale et expression rassurante. Un accessoire n’apparaît que lorsque
la pose le nécessite.

Expressions minimales à produire :

1. repos / accueil ;
2. joie / célébration ;
3. guide / explication ;
4. dessin ;
5. encouragement après une difficulté ;
6. petite erreur sans tristesse.

Les concepts historiques restent dans `assets/reference/mascot/`. Les candidats
destinés à l’application vivent dans `assets/mascot/kiwi/` et ne deviennent
stables qu’après validation à leur taille réelle et chargement par le rendu
Skia.

## 7. Animation

- Entrées douces : fondu + légère montée.
- Boutons : compression puis rebond.
- Réussite : étoile, confettis légers ou halo.
- Erreur : petit mouvement latéral, jamais agressif.
- Durée courte : l’animation ne doit pas ralentir l’enfant.
- Pas de clignotement rapide.

## 8. Son

Le son accompagne mais ne commande jamais l’expérience.

Familles : clic doux, glissement, trait de crayon, gomme, validation, réussite, page, étoile.

Prévoir un contrôle adulte permettant de couper tous les sons.

## 9. Accessibilité et sécurité visuelle

- contraste suffisant entre texte et fond ;
- information doublée par forme, icône ou animation ;
- pas de zones interactives minuscules ;
- pas de publicité déguisée ;
- pas de mécanique visuelle anxiogène ;
- pas de punition graphique forte ;
- interface utilisable au doigt sur tablette et téléphone.

## 10. Règle de cohérence

Aucun asset ne rejoint l’application avant validation des points suivants : silhouette lisible, style cohérent, palette compatible, fond correctement détouré, taille d’usage connue et nom de fichier stable.
