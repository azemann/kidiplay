# Distribution et versions

Les termes `package`, `release`, `publish`, `promote` et `deploy` suivent les définitions canoniques de `042_Cycle_Livraison_Universel.md`.

La release fabrique et qualifie. La distribution consomme. Le digest de l’artefact distribué doit être celui de l’artefact qualifié ; aucune reconstruction silencieuse n’est admise entre les deux.

## Versionnement

{{VERSIONING_POLICY}}

## Canaux

| Canal | Public | Stabilité attendue | Données admises | Mise à jour |
| --- | --- | --- | --- | --- |
| bêta | {{BETA_AUDIENCE}} | testable | {{BETA_DATA_POLICY}} | {{BETA_UPDATE_POLICY}} |
| stable | {{STABLE_AUDIENCE}} | production | {{STABLE_DATA_POLICY}} | {{STABLE_UPDATE_POLICY}} |

Une prévisualisation ou un prototype de développement est un
`verification-output`, pas un canal de distribution.

## Artefacts

| Plateforme | Format | Produit et qualifié par la release | Signature | Vérification | Publication |
| --- | --- | --- | --- | --- | --- |
| {{RELEASE_PLATFORM}} | {{ARTIFACT_FORMAT}} | {{BUILD_PROCEDURE}} | {{SIGNING_POLICY}} | {{ARTIFACT_VERIFICATION}} | {{PUBLISH_TARGET}} |

Dans un manifeste v3, la distribution accepte seulement un `release-artifact`
dont le contrat est immuable et lié à la version ainsi qu’à la révision source.
Si l’artefact traverse deux pipelines, son `handoff` persistant et la
vérification du digest sont obligatoires.

## Checklist de publication

- [ ] version et changelog cohérents ;
- [ ] tests et audit réussis ;
- [ ] artefact reproductible ou provenance enregistrée ;
- [ ] licences et assets vérifiés ;
- [ ] migrations et sauvegarde testées ;
- [ ] mise à jour depuis la version supportée testée ;
- [ ] retour arrière défini ;
- [ ] notes utilisateur rédigées ;
- [ ] canal et public confirmés.

## Fin de support

Définir préavis, export, migration, durée de maintien, archivage et suppression des données.
