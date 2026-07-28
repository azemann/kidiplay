# Exemples — module conditionnel

Les exemples démontrent un parcours minimal supporté avec des données non sensibles. Ils doivent être exécutables ou explicitement marqués comme illustratifs.

Un exemple ne doit pas devenir une seconde implémentation non maintenue du produit.

`project.multi-stack.yaml` illustre la description v1 d'un dépôt Tauri sans confondre frontend navigateur, runtime d'outillage Node.js et hôte natif Rust.

`project.bootstrap.yaml` montre un projet neuf dont le développement est actif tandis que release, distribution et exploitation restent différées.

`project.delivery.yaml` sépare les portées `development`, `release` et `distribution`. La distribution y consomme, via un `handoff` persistant, le même artefact immuable que la release a qualifié, sans reconstruction.

Les régimes exploration, construction, intégration et stabilisation ne sont pas
ajoutés à ces manifestes : ils appartiennent à la tranche active et sont
consignés dans `PROJECT_STATE.md`.

`project.v2-compat.yaml` protège la lecture des manifestes v2 non segmentés.

`adoption.existing.yaml` montre comment un dépôt existant mappe les rôles documentaires vers ses propres chemins sans les renommer.
