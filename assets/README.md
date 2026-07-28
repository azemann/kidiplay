# Assets KidiPlay

Ce dossier contient les ressources visuelles et sonores validées pour l’application.

## Structure cible

```text
assets/
├── brand/
│   ├── logo/
│   └── palette/
├── mascots/
│   ├── source/
│   └── exports/
├── icons/
│   ├── navigation/
│   ├── tools/
│   └── games/
├── illustrations/
│   ├── animals/
│   ├── fruits/
│   ├── objects/
│   ├── shapes/
│   └── numbers/
├── backgrounds/
├── stickers/
├── ui/
├── sounds/
├── fonts/
└── prompts/
```

## Première vague d’assets

1. Planche d’identité visuelle KidiPlay.
2. Mascotte principale et six expressions.
3. Icônes : Jouer, Dessiner, Galerie, Retour, Son, Réglages adultes.
4. Huit animaux cohérents pour le Memory.
5. Fond d’accueil léger.
6. Boutons et cartes de référence.

## Pipeline de production

1. Générer une planche de direction artistique.
2. Valider le style général avant tout découpage.
3. Générer ensuite une famille à la fois.
4. Détourer et exporter chaque asset individuellement.
5. Vérifier la lisibilité à petite taille.
6. Nommer et classer l’asset.
7. Enregistrer le prompt source dans `assets/prompts/`.

## Nommage

Utiliser des noms anglais stables, sans espaces :

```text
mascot_welcome_v01.png
icon_draw_v01.png
animal_fox_front_v01.png
background_home_day_v01.webp
sound_success_soft_v01.ogg
```

## Formats

- Sources de travail : PNG haute définition.
- Icônes et personnages : PNG transparent ou SVG après vectorisation.
- Arrière-plans : WebP.
- Sons : OGG + MP3 si nécessaire.
- Toujours conserver une version source non compressée.

## Validation

Un asset est accepté lorsqu’il respecte `docs/012_Charte_Graphique.md`, qu’il reste lisible à sa taille réelle et qu’il ne contient aucun texte généré illisible.