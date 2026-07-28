# Assets KidiPlay

Ce dossier sépare les références artistiques des ressources candidates ou
validées pour l’application. La présence d’un fichier ne prouve pas encore son
intégration dans le rendu.

## Structure cible

```text
assets/
├── brand/
│   ├── logo-kidiplay.png
│   └── icon-app.png
├── reference/
│   ├── style-board/
│   └── mascot/
├── mascot/
│   └── kiwi/
├── icons/
│   ├── navigation/
│   └── actions/
├── games/
│   └── memory/
├── backgrounds/
├── ui/
│   ├── frames/
│   ├── buttons/
│   ├── cards/
│   └── stickers/
├── audio/
│   └── voice/
│       └── fr/
└── prompts/
```

Les SVG ne font pas partie du contrat actuel : l’intégration cible utilise des
ressources raster décodées et rendues par Skia.

## État de la première vague

| Famille | État |
| --- | --- |
| Concepts Kiwi avec fond | référence, conservée dans `reference/mascot/` |
| Kiwi repos, joie, guide et dessin | candidats PNG RGBA dans `mascot/kiwi/` |
| Icônes Jouer, Dessiner et Galerie | candidats PNG RGBA dans `icons/navigation/` |
| Chien, chat, ours, lapin et dos de carte | candidats PNG RGBA dans `games/memory/` |
| Atelier-jardin horizontal et vertical | candidats PNG opaques dans `backgrounds/` |
| Premier accueil paysage | référence dans `reference/screens/` |
| Cadres et grandes surfaces tactiles | à construire avec Compose/Skia |
| Voix française de Kiwi | texte et enregistrement à produire séparément |

## Pipeline de production

1. Générer une planche de direction artistique.
2. Valider le style général avant tout découpage.
3. Générer ensuite une famille à la fois depuis l’ancre stylistique.
4. Détourer et exporter chaque asset individuellement en PNG RGBA.
5. Vérifier la lisibilité à petite taille.
6. Vérifier l’alpha, les dimensions et les bords.
7. Charger l’asset dans le rendu Skia à sa taille d’usage.
8. Nommer et classer l’asset.
9. Enregistrer le prompt source dans `assets/prompts/`.

## Nommage

Utiliser des noms anglais stables, en minuscules, avec des tirets et une version :

```text
kiwi-idle-v01.png
icon-drawing-v01.png
animal-dog-front-v01.png
background-garden-landscape-v01.webp
```

## Formats

| Asset | Cible de travail | Fond |
| --- | --- | --- |
| Mascotte | 2048 × 2048 PNG RGBA | transparent |
| Icône de menu | 1024 × 1024 PNG RGBA | transparent |
| Animal Memory | 1024 × 1024 PNG RGBA | transparent |
| Carte et cadre | 1024 × 1024 PNG RGBA | transparent |
| Décor horizontal | 1920 × 1080 PNG ou WebP | plein |
| Décor vertical | 1080 × 1920 PNG ou WebP | plein |
| Logo et icône d’application | PNG RGBA aux tailles Android requises | transparent |

Les quatre premiers candidats Kiwi mesurent 1254 × 1254. Ils sont suffisants
pour l’exploration et le prototype, mais restent sous la cible de travail
2048 × 2048 ; ils ne doivent donc pas être présentés comme le pack final.

Les icônes et éléments du Memory mesurent également 1254 × 1254. Les décors
mesurent 1672 × 941 et 941 × 1672 : leur ratio est adapté à l’exploration, mais
ils restent sous les cibles 1920 × 1080 et 1080 × 1920.

## Validation

Un asset est accepté lorsqu’il respecte `docs/012_Charte_Graphique.md`, possède
un canal alpha contrôlé lorsque requis, reste lisible à sa taille réelle, ne
contient aucun texte généré et a été chargé dans le rendu cible.
