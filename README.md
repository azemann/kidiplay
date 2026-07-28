# {{PROJECT_NAME}}

> {{ONE_SENTENCE_PURPOSE}}

La version du dépôt modèle est déclarée dans `VERSION`. Une adoption enregistre la version utilisée dans `project.adoption.yaml`; elle n’écrase pas le versionnement déjà présent d’un projet existant.

## Première utilisation

Ouvrir `START_HERE.md`, puis choisir :

- projet neuf : `guides/NEW_PROJECT.md` ;
- projet existant : `guides/EXISTING_PROJECT.md`.

Le choix est enregistré dans `project.adoption.yaml`. Les deux parcours
convergent à `development` comme niveau d’adoption ; une exploration bornée peut
commencer plus tôt.

## Sources de vérité

- adoption de la méthode : `project.adoption.yaml` ;
- présent opérationnel : rôle `current-state`, mappé par défaut vers `PROJECT_STATE.md` ;
- boucle de développement : `docs/044_Boucle_Developpement.md` ;
- technologie et livraison logicielle : `project.yaml` ;
- vision, périmètre et exigences : rôles mappés dans le manifeste d’adoption ;
- décisions structurantes : `docs/090_Decisions/` ;
- futur : `docs/050_Roadmap.md` ;
- versions publiées : `CHANGELOG.md` ;
- apprentissage : `RETROSPECTIVE.md`.

Un projet existant peut mapper un rôle vers un autre chemin. La numérotation de `docs/` n’est pas imposée.

## Validation

```bash
python3 -m pip install --requirement scripts/requirements-validation.txt
./scripts/check-project.sh
```

Le contrôle sans argument lit le niveau courant. Il vérifie uniquement ce qui est actif ou requis à ce niveau et indique la prochaine action.

```bash
./scripts/check-project.sh development
./scripts/check-project.sh --current --format json
```

Le workflow fourni auto-valide le dépôt modèle uniquement dans
`azemann/project-template`. Dans tout dépôt copié ou adopté, il exécute
`--current` : une CI verte ne peut donc pas contourner le niveau réellement
déclaré.

## Frontières logicielles

Pour un logiciel :

- `development` fait respirer la tranche entre exploration, construction, intégration et stabilisation ;
- `release` produit un artefact immuable et qualifié ;
- `distribution` publie ou déploie ce même artefact ;
- `operation` observe, maintient, reprend et retire le système.

> Libre pour explorer, cohérent pour construire, rigoureux pour intégrer,
> strict pour stabiliser.

La CI de développement n’oblige pas à configurer la distribution.
