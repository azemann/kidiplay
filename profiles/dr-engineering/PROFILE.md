# Profil d’ingénierie DR

Ce profil n’intègre pas DR au noyau générique. Il relie des briques indépendantes et interopérables : DR, Ω, Atlas, Forge A, Forge B et DR-Dev.

## Règles de séparation

- DR fournit la grammaire et les opérateurs ;
- Ω définit le système, ses frontières, son intention et sa cohérence ;
- Atlas cartographie structure, flux, pilotes et tâches ;
- Forge A construit ;
- Forge B examine la construction et ses écarts ;
- DR-Dev observe le dépôt et retourne un rapport structuré ; il ne construit pas à la place de Forge A ;
- aucune métaphore DR ne devient une preuve scientifique sans protocole du domaine.

## Ordre de travail proposé

`contexte → Ω-intent → carte Atlas → plan Forge A → construction → observation DR-Dev → revue Forge B → correction`

## Documents du profil

- `CANON_REFERENCE.md` ;
- `OMEGA_INTENT.md` ;
- `ATLAS_MAP.md` ;
- `ATLAS_FLOWS.md` ;
- `FORGE_A_PLAN.md` ;
- `FORGE_B_REVIEW.md` ;
- `DR_DEV_REPORT.md` ;
- `LAYERS_C0_C9.md` ;
- `OPERATORS.md`.

