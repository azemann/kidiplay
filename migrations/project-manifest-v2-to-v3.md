# Migration manuelle de `project.yaml` v2 vers v3

La v1 et la v2 restent valides avec leur contrat historique exact pour le
développement. Elles ne peuvent pas déclarer les champs v3 `delivery`, `role`,
`contract` ou `handoff`, ni prouver les niveaux `release` et suivants. Migrer
explicitement lorsque la séparation des frontières apporte une valeur réelle ;
ne jamais « rétrograder » un manifeste v3 en changeant seulement son numéro.

## 1. Inventorier les pipelines

Pour chaque pipeline existant, identifier sa fonction dominante :

- vérification de commit ou PR : `development` ;
- production et qualification d’une version : `release` ;
- publication, store, promotion ou déploiement : `distribution` ;
- observation, reprise ou retrait : `operation`.

Un pipeline mêlant plusieurs frontières doit être séparé avant la migration.

## 2. Ajouter les portées

```yaml
schema_version: 3
delivery:
  scopes:
    development:
      status: active
      execution: automated
      pipelines: [development-ci]
    release:
      status: deferred
      reason: "Décision de release encore ouverte."
    distribution:
      status: deferred
      reason: "Canal non activé."
    operation:
      status: not-applicable
      reason: "Aucun système exploité."
```

Chaque pipeline doit appartenir à une seule portée.

## 3. Qualifier les artefacts

Une sortie de contrôle devient `verification-output`.

Un objet destiné à être publié ou déployé devient `release-artifact` et reçoit un contrat immuable avec version, révision, digest, provenance, exigences SBOM/signature et opérations de qualification.

S'il traverse plusieurs pipelines, ajouter son `handoff` persistant et
`verify_digest: true`.

## 4. Séparer la distribution

La distribution :

- commence par `verify-artifact` ;
- consomme un `release-artifact` ;
- peut publier, promouvoir ou déployer ;
- ne contient ni `build`, ni `package`, ni `sign` ;
- ne déclare aucune sortie d’artefact.

## 5. Valider

```bash
./scripts/check-project.sh release
./scripts/check-project.sh distribution
```

Ne changez pas `schema_version` tant que chaque pipeline et artefact n’a pas reçu une portée et un rôle confirmés humainement.
