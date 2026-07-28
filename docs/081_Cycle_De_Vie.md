# Cycle de vie de l’application

Ce document traite de l'état d'une application installée ou en service. Le chemin des sources vers une release puis un déploiement relève de `042_Cycle_Livraison_Universel.md`. Les deux cycles se rencontrent au déploiement mais ne doivent pas être fusionnés.

Ce document devient obligatoire dès qu’une application est installée, exécutée comme service, mise à jour ou responsable de données persistantes.

Dans le manifeste v3, il correspond normalement à une portée `operation` active. Une release publiable mais jamais installée comme système n’a pas à inventer ce cycle.

## Responsabilité

Le gestionnaire de cycle de vie orchestre l’installation, la configuration, l’exécution, le diagnostic, la réparation, la mise à jour, la sauvegarde, la restauration et le retrait. Le domaine métier ne connaît ni `systemd`, ni `launchd`, ni le gestionnaire de services Windows.

## Dimensions d’état

Ne pas enfermer toute la réalité dans une seule énumération :

- **cycle de vie :** `Created`, `Installing`, `Installed`, `Configuring`, `Configured`, `Ready`, `Starting`, `Running`, `Updating`, `Stopping`, `Stopped`, `Removing`, `Removed`, `Failed` ;
- **santé :** `Unknown`, `Healthy`, `Degraded`, `Unhealthy` ;
- **opération active :** diagnostic, réparation, sauvegarde, restauration, migration ou mise à jour, avec progression lorsqu’elle est connaissable.

## Transitions

| Source | Action | Intermédiaire | Succès | Échec/récupération |
| --- | --- | --- | --- | --- |
| `Created` | installer | `Installing` | `Installed` | `Failed` puis nettoyage/reprise |
| `Installed` | configurer | `Configuring` | `Configured` | `Failed` puis correction |
| `Configured` | valider | — | `Ready` | santé `Degraded/Unhealthy` |
| `Ready/Stopped` | démarrer | `Starting` | `Running` | `Failed` ou retour `Stopped` |
| `Running` | arrêter | `Stopping` | `Stopped` | `Failed` avec état réel sondé |
| état compatible | mettre à jour | `Updating` | état cible documenté | retour arrière ou `Failed` |
| `Stopped` | supprimer | `Removing` | `Removed` | reprise ou réparation |

## Invariants

- état observé distingué de l’état désiré ;
- transition interdite refusée explicitement ;
- opération longue suivie et interruptible lorsque possible ;
- installation, mise à jour, sauvegarde et restauration idempotentes ou accompagnées d’une compensation ;
- suppression des données séparée de la désinstallation du programme ;
- diagnostic sans mutation, réparation avec plan explicite ;
- adaptateurs système remplaçables derrière un port commun.

## Adaptateurs cibles

| Plateforme | Adaptateur | État |
| --- | --- | --- |
| Linux | `systemd` ou mode utilisateur documenté | {{LINUX_RUNTIME_STATUS}} |
| Windows | Service Control Manager | {{WINDOWS_RUNTIME_STATUS}} |
| macOS | `launchd` | {{MACOS_RUNTIME_STATUS}} |

Le nom du futur gestionnaire générique reste une décision séparée ; le template n’impose ni « DR Runtime » ni « Lifekeeper ».
