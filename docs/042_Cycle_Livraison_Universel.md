# Cycle universel de livraison logicielle

## Décision

Le registre technologique décrit **avec quoi** un projet est construit. Le cycle de livraison décrit **ce qui arrive** aux sources, preuves, artefacts, releases et systèmes en service. Un pipeline automatise seulement une partie de ce cycle ; GitHub Actions, GitLab CI, Jenkins ou Unity Build Automation n'en sont que des orchestrateurs.

Le modèle est un graphe déclaratif, jamais une liste rigide d'étapes obligatoires.

## Ontologie minimale

| Objet | Définition | Ne pas confondre avec |
| --- | --- | --- |
| opération | action universelle ayant entrées, sorties et résultat | commande propre à un outil |
| pipeline | graphe d'opérations déclaré, manuel ou automatisé | fournisseur CI/CD |
| orchestrateur | système exécutant un pipeline | cycle de vie lui-même |
| politique | règle qui autorise, bloque ou qualifie | commande d'exécution |
| preuve | résultat vérifiable : rapport, checksum, SBOM, attestation | simple journal |
| artefact | sortie immuable et identifiée d'une production | dossier temporaire mutable |
| release | ensemble versionné d'artefacts et de métadonnées | publication ou déploiement |
| registre | destination de publication d'un artefact | environnement d'exécution |
| environnement | contexte nommé avec règles et configuration | plateforme cible |
| déploiement | matérialisation d'une release dans un environnement | téléchargement/publication |
| promotion | autorisation de faire avancer la même release | reconstruction de cette release |

## Phases et opérations canoniques

Les identifiants suivants sont stables. Un projet n'active que ce qui lui est applicable.

| Phase | Opérations |
| --- | --- |
| `verify` | `resolve-dependencies`, `format-check`, `lint`, `type-check`, `test`, `quality`, `security-scan`, `license-check`, `verify-artifact` |
| `produce` | `build`, `package`, `checksum`, `generate-sbom`, `attest`, `sign` |
| `deliver` | `create-release`, `publish`, `promote`, `deploy`, `verify-deployment` |
| `operate` | `monitor`, `backup`, `restore`, `update`, `rollback`, `retire` |

Le validateur impose le couple `uses → phase` et les opérations admises par
portée. Une extension locale utilise le préfixe `x-`; elle reste interdite aux
frontières sensibles `distribution` et `operation` tant que le noyau ne connaît
pas sa sémantique.

Définitions qui ferment les ambiguïtés :

- `build` transforme des sources en sorties exécutables ou distribuables ;
- `package` assemble une sortie dans un format de distribution ;
- `create-release` fige une version, ses artefacts et ses preuves ;
- `publish` rend un artefact disponible dans un registre ou canal ;
- `deploy` installe ou active une release dans un environnement ;
- `promote` fait avancer **la même release immuable** après satisfaction d'une politique.

## Portées v3 : un axe orthogonal

La phase décrit ce que fait une opération. La portée décrit à quelle frontière elle appartient.

| Portée | Phases admises | Résultat |
| --- | --- | --- |
| `development` | `verify`, éventuellement `produce:build` | code et build de contrôle |
| `release` | `verify`, `produce`, `deliver:create-release` | artefact immuable et qualifié |
| `distribution` | `verify:verify-artifact`, `deliver`, rollback explicite | artefact publié ou déployé |
| `operation` | `operate` | système observé et maintenu |

Un pipeline v3 appartient à une seule portée. Les portées ont les statuts `active`, `deferred`, `unresolved` ou `not-applicable`.

À l’intérieur de `development`, la tranche active peut être en exploration,
construction, intégration ou stabilisation. Ces régimes règlent la liberté de
travail ; ils ne sont ni des phases du graphe, ni des sous-portées machine.
« Construction » désigne ici la matérialisation progressive du comportement,
pas nécessairement l’opération canonique `build`.

La stabilisation peut produire un build de contrôle ou un
`verification-output`. Elle ne produit, ne package, ne signe et ne crée aucun
`release-artifact`. Cette responsabilité commence dans la portée `release`.
Voir `044_Boucle_Developpement.md`.

Une portée différée n’exige ni pipeline, ni environnement, ni secret. `distribution.intent` peut néanmoins déclarer tôt une cible finale si elle influence l’architecture.

Une portée `release` ou `distribution` active possède toujours un graphe
d'opérations. En mode manuel, son orchestrateur est `manual` et le pipeline
référence une procédure contrôlée. « Manuel » dispense d'un fournisseur CI/CD,
jamais du contrat ni des preuves.

## Graphe d'opérations

Chaque opération déclare : `id`, `uses`, phase, dépendances `needs`, commande ou adaptateur, entrées, sorties, conditions, timeout, reprise et politique d'échec. `needs` forme un graphe orienté acyclique. Les branches indépendantes peuvent s'exécuter en parallèle ; une dépendance interdit l'exécution avant succès de ses prédécesseurs.

Une condition ne doit pas contenir de code arbitraire portable. Elle utilise des faits déclarés tels que l'événement, la branche, le tag, l'environnement ou le statut d'une opération.

États de résultat : `pending`, `running`, `succeeded`, `failed`, `skipped`, `cancelled`, `blocked`. Politiques d'échec : `stop`, `continue`, `retry`, `rollback`. Une reprise déclare un nombre maximal, un délai et les erreurs éligibles ; elle n'est sûre que pour une opération idempotente.

## Artefacts et preuves

Un artefact déclaré possède au minimum un identifiant, un type, un chemin ou une référence, le producteur et une politique de rétention.

La v3 distingue :

- `verification-output` : sortie de CI, aperçu ou diagnostic, jamais distribuable ;
- `release-artifact` : sortie immuable, versionnée, liée à une révision et qualifiée.

Le contrat d’un `release-artifact` déclare source de version, source de révision, digest, provenance, SBOM, signature et opérations de qualification. `required`, `optional` et `not-applicable` expriment une exigence de contrat, non un résultat d’exécution.

Un artefact promu n'est pas reconstruit entre staging et production. Le digest relie exactement ce qui a été testé, signé, publié et déployé.

Lorsqu'un pipeline de distribution consomme un artefact produit dans un autre
pipeline, `handoff` déclare le support persistant utilisé (`release-asset`,
registre, artefact d'orchestrateur, store ou stockage objet) et impose la
vérification du digest après transfert.

`publish`, `promote` et `deploy` consomment uniquement un `release-artifact`. La portée `distribution` interdit `build`, `package`, `sign` et toute nouvelle sortie d’artefact.

## Environnements et promotion

Un environnement déclare son type (`development`, `test`, `staging`, `production` ou nom métier), ses cibles, protections, approbations, variables non sensibles, références de secrets, stratégie de déploiement et rollback.

Les règles de promotion peuvent exiger : opérations réussies, branche ou tag autorisé, approbation humaine, signature valide, seuil qualité, fenêtre temporelle ou absence d'incident. La configuration organisationnelle peut renforcer ces règles sans que le projet puisse les affaiblir.

## Secrets et frontières de responsabilité

`project.yaml` ne contient jamais une valeur secrète. Il ne contient qu'une référence opaque :

```yaml
secrets:
  registry-token:
    provider: github-actions
    reference: REGISTRY_TOKEN
    required_by: [publish-web]
```

Le projet déclare le besoin ; l'organisation définit la politique ; l'orchestrateur résout la référence au dernier moment ; la commande ne journalise pas la valeur.

## Échecs, reprise et rollback

Le rollback est une opération explicite, conditionnelle et testée. Il précise le déclencheur, la cible précédente, les données compatibles, les migrations réversibles ou compensatoires, le responsable et la preuve de succès. Si le retour arrière est impossible, la stratégie de reprise en avant doit être documentée.

Un échec de monitoring n'équivaut pas automatiquement à un échec de déploiement. Le système distingue état désiré, état observé, santé et résultat de l'opération.

## Portabilité et adaptateurs

Le manifeste universel n'utilise pas la syntaxe `${{ ... }}` de GitHub, les stages GitLab ou un Jenkinsfile. Un profil d'orchestrateur documente la traduction et ses pertes éventuelles. La portabilité signifie que l'intention et les contrats survivent au changement d'orchestrateur, pas que chaque fonctionnalité fournisseur possède un équivalent parfait.

Ordre de résolution d'une opération : remplacement explicite du projet, commande du composant, script natif vérifié, profil de framework, capacité de l'outil, puis diagnostic `unresolved`. Aucune commande n'est improvisée silencieusement.

## Périmètre de la v1.7

La v1.5 a fourni le graphe universel. La v1.6 ajoute les portées, les statuts différables et le contrat d’artefact de release.

La v1.7 ajoute la liberté graduée à l’intérieur du développement sans modifier
le graphe, les phases, les portées ou les schémas.

Elle ne fournit ni moteur `./project`, ni générateur multi-fournisseurs, ni catalogue exhaustif. La migration v2 vers v3 reste une décision humaine : un outil ne peut pas déduire fiablement si un pipeline relève du développement, de la release, de la distribution ou de l’exploitation.
