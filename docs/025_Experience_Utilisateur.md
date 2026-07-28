# Expérience utilisateur

## Question centrale

À quelle question immédiate l’écran principal doit-il répondre ?

> {{CENTRAL_USER_QUESTION}}

## Promesse d’expérience

{{EXPERIENCE_PROMISE}}

## Principes UX

- montrer d’abord ce dont l’utilisateur a besoin pour décider ;
- révéler la complexité technique progressivement ;
- donner un retour immédiat après chaque action ;
- rendre les erreurs compréhensibles et réparables ;
- conserver la maîtrise des données et des actions sensibles ;
- ne jamais dépendre uniquement d’une couleur pour transmettre un état ;
- préserver les fonctions essentielles sans souris et sur petit écran.

## Architecture de l’information

| Espace | Question utilisateur | Contenu principal | Action principale |
| --- | --- | --- | --- |
| {{SPACE}} | {{USER_QUESTION}} | {{CONTENT}} | {{PRIMARY_ACTION}} |

## Parcours principal

1. {{JOURNEY_ENTRY}}
2. {{UNDERSTANDING}}
3. {{USER_ACTION}}
4. {{FEEDBACK}}
5. {{RECOVERY_OR_CONTINUATION}}

## États obligatoires

Pour chaque écran ou bloc alimenté par des données, définir :

- initial ;
- chargement ou attente ;
- vide ;
- succès ;
- erreur récupérable ;
- indisponible ;
- dégradé ;
- hors ligne, lorsque pertinent.

## Responsive

Le projet ne conçoit pas « une version mobile réduite », mais une hiérarchie adaptée à chaque espace disponible.

- **téléphone compact :** une colonne, action principale immédiatement accessible ;
- **téléphone pliable :** continuité lors du changement de posture et largeur ;
- **tablette :** panneaux complémentaires sans étirer inutilement le contenu ;
- **bureau :** densité accrue, raccourcis clavier et vues simultanées utiles ;
- **grands écrans :** largeur de lecture bornée et espaces latéraux exploités avec intention.

## Accessibilité

- taille tactile minimale : 48 × 48 px ;
- focus clavier visible ;
- ordre de navigation logique ;
- contraste suffisant ;
- libellé accessible pour chaque icône interactive ;
- zoom utilisateur conservé ;
- support de `prefers-reduced-motion` ;
- textes compréhensibles sans jargon interne.

### Cible

Pour une interface web, viser WCAG 2.2 niveau AA. Pour une plateforme native, appliquer les recommandations d’accessibilité équivalentes de la plateforme et documenter les exceptions.

## Contenu et tonalité

- commencer par la situation et l’action utiles, puis proposer le détail technique ;
- employer les mots du glossaire dans le produit, avec des libellés compréhensibles par l’utilisateur ;
- nommer précisément les conséquences d’une action destructive ;
- préférer « Réessayer », « Reconfigurer » ou « Restaurer » à une erreur sans issue ;
- ne pas utiliser une formulation rassurante lorsque l’état réel est inconnu.

## Actions sensibles

Une confirmation décrit l’objet, la conséquence, la réversibilité et l’étape suivante. Les actions irréversibles ne sont jamais placées ou stylées comme une action ordinaire.
