# Système de design

## Source canonique

Les valeurs visuelles de référence sont déclarées dans `design/tokens.css`. Les implémentations propres à une plateforme doivent traduire ces rôles sans en changer silencieusement le sens.

## Hiérarchie des tokens

1. **primitifs** : couleurs, dimensions et durées brutes ;
2. **sémantiques** : fond, surface, texte, accent, danger ;
3. **composants** : bouton principal, panneau, champ, badge ;
4. **exceptions de projet** : rares, documentées et locales.

## Composants fondamentaux

- `AppShell` : cadre principal et zones sûres ;
- `TopBar` / `SideBar` / `BottomNav` : navigation selon l’espace ;
- `Panel` et `Card` : regroupement hiérarchique ;
- `Button` : primaire, secondaire, discret, danger ;
- `IconButton` : cible 48 px et libellé accessible ;
- `Field`, `Select`, `Switch`, `Slider` : contrôles cohérents ;
- `Badge` / `StatusChip` : état court, jamais seule source d’information ;
- `Dialog`, `Drawer`, `BottomSheet` : profondeur adaptée au viewport ;
- `Toast` : confirmation non bloquante ;
- `EmptyState`, `ErrorState`, `Skeleton` : états structurels ;
- `DiagnosticPanel` : détails techniques révélés sur demande.

## États de composant

Chaque composant interactif pertinent définit : repos, survol, focus, actif, sélectionné, désactivé, chargement, succès et erreur.

## Grille et espacement

- grille fondée sur 4 px ;
- rythme courant : 8, 12, 16, 24, 32 et 48 px ;
- largeur de lecture bornée ;
- espace plus grand entre groupes qu’entre éléments d’un même groupe ;
- aucune valeur ponctuelle sans justification lorsqu’un token convient.

## Adaptation par plateforme

- **web/PWA :** pointeur, clavier, tactile, redimensionnement et installation ;
- **Android :** zones sûres, clavier logiciel, bouton retour et changement de posture ;
- **Linux/bureau :** densité maîtrisée, menus contextuels et raccourcis ;
- **Windows/macOS :** conventions natives préservées par les adaptateurs d’interface.

## Documentation d’un composant

Chaque composant partagé précise : intention, anatomie, variantes, états, comportement responsive, clavier, accessibilité et exemples à éviter.

