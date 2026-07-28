# Parcours d’un projet neuf

## Résultat du parcours

Le niveau `bootstrap` est atteint lorsque l’intention est compréhensible, le périmètre est borné, une première tranche est vérifiable et la méthode sait quoi demander ensuite.

Il ne prouve ni qu’une release est prête, ni que le produit peut être distribué.

## 1. Initialiser l’adoption

Dans `project.adoption.yaml` :

- conserver `adoption.origin: new` ;
- conserver `adoption.current_level: bootstrap` ;
- activer les profils réellement applicables ;
- mapper les rôles actifs vers les documents choisis ;
- ne pas activer artificiellement les préoccupations futures.

Un document existant peut remplir un rôle depuis n’importe quel chemin. Le chemin proposé par le template n’est qu’un défaut.

## 2. Définir le minimum utile

Compléter uniquement `docs/007_Brief_Bootstrap.md` et l’identité. Au bootstrap,
le brief remplit aussi temporairement le rôle d'état présent afin d'éviter de
dupliquer les mêmes informations. Il peut remplir plusieurs rôles :

- l’identité et le résultat recherché ;
- la vision courte ;
- les principes réellement invariants ;
- le périmètre inclus et exclu ;
- une exigence vérifiable ;
- un premier cas d’usage ;
- l’état présent et la prochaine tranche.

Pour un projet logiciel, activer le profil `software`. Les choix technologiques
déjà confirmés peuvent être consignés dans `project.yaml`; ce registre devient
obligatoire à `development`, pas pour formuler l’intention. Une commande encore
inconnue reste `unresolved` avec sa raison.

## 3. Séparer les frontières

Dans un manifeste logiciel v3, les quatre portées existent indépendamment :

| Portée | État initial conseillé | Objet |
| --- | --- | --- |
| `development` | `active` | coder, tester, corriger, build de contrôle |
| `release` | `deferred` | produire et qualifier un artefact immuable |
| `distribution` | `deferred` | publier, déployer ou envoyer vers un store |
| `operation` | `deferred` | observer, maintenir, reprendre et retirer |

La cible de distribution peut être déclarée comme intention sans créer de pipeline, d’environnement ou de secret.

## 4. Valider le bootstrap

Installer une fois les dépendances du validateur :

```bash
python3 -m pip install --requirement scripts/requirements-validation.txt
```

Puis lancer :

```bash
./scripts/check-project.sh bootstrap
```

Le contrôle porte sur les rôles actifs et exigibles maintenant. Les modèles différés peuvent encore contenir des variables `{{...}}`.

## 5. Entrer dans la boucle de développement

Une exploration bornée peut commencer dès qu’une inconnue et une première
tranche sont formulées. Il n’est pas nécessaire d’inventer d’abord une
architecture définitive.

```text
exploration ⇄ construction ⇄ intégration ⇄ stabilisation
```

| Régime | Travail attendu | Sortie |
| --- | --- | --- |
| exploration | essayer, comparer, jeter ou retenir | piste retenue pour construction ou abandon documenté |
| construction | matérialiser le comportement principal | la tranche est observable et possède un contrôle ciblé |
| intégration | raccorder aux contrats et composants réels | les raccourcis sont traités et les frontières fonctionnent |
| stabilisation | réduire les risques sans étendre le périmètre | les contrôles pertinents sont verts |

Lorsque la piste retenue entre en construction, mapper `current-state` vers
`PROJECT_STATE.md`. Y déclarer le régime, la frontière expérimentale, les
raccourcis temporaires et le critère de passage. Le brief reste la décision
initiale ; `PROJECT_STATE.md` devient la mémoire opérationnelle vivante.

Le niveau d’adoption `development` n’est pas un permis préalable pour chaque
essai. Il doit toutefois être validé au plus tard avant de déclarer
l’intégration terminée. À ce moment :

- le cas d’usage possède un critère d’acceptation ;
- l’architecture minimale réellement retenue est comprise ;
- les commandes applicables sont définies ou explicitement non résolues ;
- la stratégie de test est proportionnée au risque ;
- `PROJECT_STATE.md` décrit la réalité et non l’ambition.

Mettre `adoption.current_level: development`, puis lancer :

```bash
./scripts/check-project.sh development
```

Le canon complet des régimes et transitions est
`docs/044_Boucle_Developpement.md`.

## 6. Activer plus tard release et distribution

N’activer `release` qu’au moment de produire un objet versionné et qualifié. N’activer `distribution` que lorsqu’un canal réel, un store, un registre ou un environnement est choisi.

La distribution consomme l’artefact de release. Elle ne reconstruit jamais silencieusement le projet.
