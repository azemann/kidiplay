# Profil Linux et service

## Portabilité

- distributions et architectures supportées ;
- session utilisateur ou service système ;
- emplacements XDG pour configuration, données, cache et journaux ;
- Wayland/X11 lorsque l’interface ou la capture l’exige ;
- paquet, archive, AppImage ou installation locale ;
- permissions et groupes nécessaires.

## Cycle de vie

- adaptateur `systemd` séparé du domaine ;
- install, configure, start, stop, restart et status ;
- doctor sans mutation ;
- repair avec plan ;
- logs expurgés ;
- update, backup, restore et uninstall ;
- suppression du programme séparée de celle des données.

## Preuves minimales

- installation sur environnement propre ;
- démarrage après reboot lorsque attendu ;
- panne explicable ;
- mise à jour et retour arrière ;
- désinstallation sans résidu non annoncé ;
- fonctionnement dégradé documenté.

