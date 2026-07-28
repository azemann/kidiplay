# Brief de bootstrap

Ce document court peut remplir plusieurs rôles au démarrage. Séparez ensuite les sujets dans les documents spécialisés seulement lorsque leur profondeur le justifie.

## Intention

- **Problème observé :** les expériences numériques destinées aux jeunes
  enfants séparent souvent jeu, apprentissage et création, ou les rendent
  difficiles à utiliser sans lecture et sans accompagnement adulte constant.
- **Résultat recherché :** proposer un univers local, rassurant et immédiatement
  compréhensible où l’enfant peut jouer, dessiner et retrouver ses créations.
- **Personne ou système concerné :** un jeune enfant utilisant un téléphone, une
  tablette ou un appareil pliable Android, avec un adulte responsable des
  réglages.

## Principes

- aucune publicité, aucun achat intégré et aucun compte obligatoire au
  démarrage ;
- fonctionnement local privilégié et opérations adultes séparées de l’espace
  enfant ;
- grandes cibles tactiles, navigation courte et compréhension possible sans
  lecture complexe ;
- progression par petites tranches observables, réversibles et testées sur
  appareil réel ;
- cohérence avec la direction artistique KidiPlay et sa mascotte Kiwi.

## Périmètre

- **Inclus dans la première tranche :** un écran d’accueil Android présentant
  Kiwi et trois accès reconnaissables — Jouer, Dessiner et Galerie — avec des
  assets raster intégrables par Skia.
- **Explicitement exclu :** implémentation complète du Memory, de l’atelier de
  dessin et de la galerie ; compte, synchronisation distante, publicité, achat,
  publication en store et distribution.

## Premier cas d’usage

- **Scénario :** l’enfant ouvre KidiPlay et identifie depuis l’accueil les trois
  activités principales avec l’aide visuelle de Kiwi.
- **Critère d’acceptation observable :** sur le Galaxy Z Fold6 appairé, en mode
  fermé puis ouvert, l’enfant peut toucher chacune des trois zones d’au moins
  48 px ; chaque action fournit un retour visible et atteint un écran
  temporaire identifiable, sans dépendre d’un texte long.

## État de la première tranche de code

- **Régime :** exploration.
- **Inconnue active :** le personnage de référence peut-il devenir une famille
  de sprites cohérents, détourés et suffisamment lisibles pour l’accueil ?
- **Frontière de liberté :** `assets/reference/`, `assets/mascot/kiwi/`,
  `assets/icons/navigation/`, `assets/backgrounds/`, `assets/prompts/`, le
  socle Gradle et `app/`. Ces éléments forment encore une exploration
  réversible : ni le pack visuel ni le prototype Android ne font partie d’un
  socle stable ou d’une release.
- **Observation actuelle :** quatre concepts historiques avec fond, quatre
  poses de Kiwi, trois icônes de navigation, quatre animaux avec dos de carte,
  deux décors adaptatifs et une référence d’accueil existent. Un prototype
  Kotlin/Compose charge les sprites et propose un accueil adaptatif avec trois
  destinations temporaires. Le 28 juillet 2026, les tests unitaires Gradle ont
  réussi et le prototype a été compilé, installé puis lancé sur le Galaxy Z
  Fold6. Le comportement visuel détaillé en modes fermé et ouvert reste à
  vérifier. Les éléments isolés possèdent un canal alpha contrôlé ; les décors
  sont opaques.
- **Critère de passage :** retenir ou corriger les quatre candidats après
  comparaison visuelle, confirmer la lisibilité du pack à la taille d’usage et
  charger au moins un sprite de chaque famille par le futur socle Skia.

## Cible finale connue

Application Android locale pour téléphone, tablette et appareil pliable,
réunissant mini-jeux, création libre et galerie enfantine. Skia est la cible de
rendu raster connue. Kotlin, Compose et Gradle sont utilisés par le prototype
exploratoire ; l’empaquetage de livraison et la distribution ne sont pas encore
confirmés.

Cette cible est une intention. Elle n’active ni release, ni distribution, ni exploitation.
