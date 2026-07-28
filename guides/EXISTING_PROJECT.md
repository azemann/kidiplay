# Adoption d’un projet existant

## Règle de départ

Le dépôt réel est la première preuve. La méthode doit s’y raccorder sans écraser ses choix, son historique ni ses fichiers de travail.

Ne copiez pas tout le template dans le dépôt.

## 1. Diagnostic strictement en lecture seule

Depuis une copie du template :

```bash
python3 scripts/inspect-project.py /chemin/du/projet
```

Pour une sortie exploitable par un autre outil :

```bash
python3 scripts/inspect-project.py /chemin/du/projet --format json
```

Le diagnostic inventorie :

- arborescence et composants probables ;
- manifestes, lockfiles et configurations ;
- commandes déclarées sans les exécuter ;
- tests, workflows, artefacts et documentation ;
- état Git observable ;
- collisions avec les noms du template ;
- indices confirmés, probables, ambigus, contradictoires ou absents.

Il ne doit jamais installer une dépendance, exécuter un script du projet, modifier un lockfile ou réécrire un workflow.

## 2. Consigner l’état initial

Utiliser `docs/006_Diagnostic_Initial.md` ou mapper le rôle `initial-diagnostic` vers un rapport existant.

Le rapport doit distinguer :

- les faits observés ;
- les déductions à confirmer ;
- les contradictions ;
- les inconnues ;
- les fichiers à préserver ;
- les commandes détectées mais non exécutées ;
- la plus petite adoption proposée.

L’adoption de la méthode commence seulement après validation humaine de ce rapport.

## 3. Adopter la méthode sans collision

Le kit exécutable minimal comprend :

- `project.adoption.yaml` ;
- `schemas/project-adoption.schema.json` et, pour un logiciel, `schemas/project.schema.json` ;
- `scripts/check-project.sh`, `scripts/validate-manifest.py` et `scripts/requirements-validation.txt` ;
- le `PROFILE.md` de chaque profil activé ;
- uniquement les documents réellement mappés comme actifs.

Ajouter `project.yaml` lorsqu'il existe déjà ou lorsque le profil `software` est
activé. `scripts/inspect-project.py` reste un outil externe de diagnostic : il
peut être lancé depuis une copie du template sans être installé dans le projet.

Créer `project.adoption.yaml`, puis déclarer :

```yaml
adoption:
  origin: existing
  current_level: discovery
```

Mappez chaque rôle vers le fichier déjà utilisé par le projet :

```yaml
documents:
  identity:
    path: README.md
    status: active
  architecture:
    path: docs/architecture/system-overview.md
    status: active
```

Ne renommez pas un document uniquement pour satisfaire le template.

Pour chaque collision (`README.md`, `AGENTS.md`, `VERSION`, `CHANGELOG.md`, workflow), choisissez explicitement :

- conserver le fichier tel quel ;
- compléter une section sans supprimer l’existant ;
- créer un nouveau fichier non conflictuel ;
- différer l’adoption avec une raison.

## 4. Cartographier la réalité technologique

Pour un logiciel :

- activer le profil `software` ;
- décrire chaque composant dans `project.yaml` ;
- confronter les déclarations aux manifestes, lockfiles et scripts ;
- conserver `unresolved` lorsqu’une commande ou une relation reste ambiguë ;
- ne jamais choisir silencieusement entre deux indices contradictoires.

Un pipeline existant reste une preuve. Il n’est pas remplacé avant que sa fonction et ses artefacts soient compris.

## 5. Valider la découverte

Installer les dépendances du validateur, puis lancer :

```bash
python3 -m pip install --requirement scripts/requirements-validation.txt
./scripts/check-project.sh discovery
```

Le résultat doit indiquer ce qui bloque et une prochaine action. Aucun document de distribution ou d’exploitation n’est exigé simplement parce qu’il existe dans le template.

## 6. Rejoindre la boucle commune

Après validation humaine du diagnostic, une exploration isolée peut réduire une
inconnue sans attendre que toute l’adoption soit terminée. Elle respecte les
éléments à préserver et ne modifie pas silencieusement un contrat, un workflow,
un manifeste ou un lockfile.

Avant la première modification, mapper le rôle `current-state` vers le
diagnostic validé ou vers un petit document d’état. À partir de la construction,
le chemin recommandé devient `PROJECT_STATE.md`.

```text
exploration ⇄ construction ⇄ intégration ⇄ stabilisation
```

Ici, l’**adoption** désigne le raccordement de la méthode au dépôt.
L’**intégration** désigne le raccordement de la tranche de code au socle réel.

Le projet valide le niveau `development` au plus tard avant de déclarer
l’intégration de la tranche terminée. À ce point :

- la tranche reprise est définie ;
- les commandes et tests utiles sont compris ;
- les contradictions critiques sont résolues ou explicitement bloquantes ;
- l’architecture minimale et le registre technologique correspondent au dépôt ;
- les frontières de préservation sont respectées ;
- les mocks et raccourcis sont retirés, isolés ou acceptés explicitement.

`PROJECT_STATE.md` enregistre le régime de la tranche, sa frontière de liberté
et son critère de passage. À partir de là, l’origine `existing` n’ajoute plus
d’exigence particulière. Release, distribution et exploitation restent
activées séparément selon la réalité.
