# Profils de livraison

Ces profils traduisent des capacités universelles vers des orchestrateurs, formats, registres, mécanismes de signature, cibles de déploiement et systèmes d'observabilité.

Un profil indique ses capacités, limites, modèle de permissions, syntaxe de référence des secrets et sources officielles. Il ne devient jamais la source de vérité de l'intention du projet.

Un orchestrateur peut servir plusieurs portées, mais chaque pipeline v3 appartient à une seule portée. La traduction doit préserver l’artefact entre release et distribution.

Un passage entre pipelines déclare un `handoff` persistant et vérifie son
digest. Une exécution manuelle conserve un graphe explicite avec
`orchestrator: manual` et une procédure ; elle ne peut pas être une portée vide.

Sous-familles prévues : `orchestrators/`, `artifact-formats/`, `registries/`, `signing/`, `deployment-targets/`, `observability/`. La v1.6 n’ajoute que les références éprouvées par ses exemples.
