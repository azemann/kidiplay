# Design

## Contenu

- `tokens.css` : fondations visuelles web de référence ;
- futurs logos, icônes ou illustrations : uniquement avec leur source et leur licence ;
- captures de référence : dans un sous-dossier versionné si elles servent de preuve.

## Règle

Les rôles sémantiques sont stables ; les valeurs de marque peuvent évoluer par décision. Une adaptation Android, desktop ou native doit préserver les rôles, la hiérarchie et les exigences d’accessibilité, même lorsque le format des tokens change.

`tokens.css` est la source canonique pour une interface web. Une plateforme non web crée un adaptateur de tokens documenté ; elle ne transforme pas ce fichier en format universel implicite. Si le projet adopte un thème clair, il met également à jour `color-scheme` et valide séparément ses contrastes.
