# Profils de projet

Un profil est une extension conditionnelle du template. Il ne devient actif que lorsqu’il est déclaré dans `project.adoption.yaml` et adapté au projet.

## Profils disponibles

- `software` : application ou bibliothèque logicielle générale ;
- `android` : application Android, téléphone, tablette et Fold ;
- `linux-service` : application Linux installée ou exécutée comme service ;
- `web-pwa` : interface web installable, responsive et potentiellement hors ligne ;
- `game` : jeu, moteur, niveaux, assets et boucles de gameplay ;
- `research-simulation` : recherche, données, protocoles et simulation reproductible ;
- `dr-engineering` : usage explicite du canon DR avec Ω, Atlas, Forge A/B et DR-Dev séparés.

Le sous-dossier `technology/` n'est pas un profil de projet supplémentaire : c'est un registre déclaratif de références technologiques utilisable par les profils ci-dessus.

## Activation

1. choisir uniquement les profils nécessaires ;
2. les ajouter à `profiles.active` dans `project.adoption.yaml` ;
3. mapper les rôles que le validateur rend obligatoires ;
4. enregistrer les compromis structurants par ADR ;
5. ne jamais considérer un profil comme une preuve de conformité automatique.

Un profil dormant peut rester dans le dépôt modèle. Dans un projet existant, ne copier que le profil activé et les références réellement nécessaires.

## Composition

Plusieurs profils peuvent être combinés, par exemple :

```text
Flux Explorer Linux = software + linux-service
Application Fold = software + android
Jeu PWA = game + web-pwa
Simulation DR = research-simulation + dr-engineering
```
