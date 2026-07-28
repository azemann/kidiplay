#!/usr/bin/env python3
"""Valide l'adoption progressive et les manifestes technologiques du projet."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

try:
    import jsonschema
    import yaml
except ModuleNotFoundError as error:
    print(
        "DÉPENDANCE DE VALIDATION MANQUANTE : "
        f"{error.name}\n"
        "Installer avec : python3 -m pip install --requirement "
        "scripts/requirements-validation.txt",
        file=sys.stderr,
    )
    raise SystemExit(2)


LEVELS = (
    "bootstrap",
    "discovery",
    "development",
    "release",
    "distribution",
    "operation",
)
LEVEL_INDEX = {level: index for index, level in enumerate(LEVELS)}
PHASE_INDEX = {
    "verify": 0,
    "produce": 1,
    "deliver": 2,
    "operate": 3,
}
PLACEHOLDER = re.compile(r"\{\{[A-Z0-9_][A-Z0-9_]*\}\}")
SECRET_ASSIGNMENT = re.compile(
    r"(api[_-]?key|token|password|secret)\s*[:=]\s*[^<{\s][^\s]*",
    re.IGNORECASE,
)
SUPPORTED_TEMPLATE_MAJOR = 1

CANONICAL_PHASES = {
    "resolve-dependencies": "verify",
    "format-check": "verify",
    "lint": "verify",
    "type-check": "verify",
    "test": "verify",
    "quality": "verify",
    "security-scan": "verify",
    "license-check": "verify",
    "verify-artifact": "verify",
    "build": "produce",
    "package": "produce",
    "checksum": "produce",
    "generate-sbom": "produce",
    "attest": "produce",
    "sign": "produce",
    "create-release": "deliver",
    "publish": "deliver",
    "promote": "deliver",
    "deploy": "deliver",
    "verify-deployment": "deliver",
    "monitor": "operate",
    "backup": "operate",
    "restore": "operate",
    "update": "operate",
    "rollback": "operate",
    "retire": "operate",
}
SCOPE_OPERATIONS = {
    "development": {
        "resolve-dependencies",
        "format-check",
        "lint",
        "type-check",
        "test",
        "quality",
        "security-scan",
        "license-check",
        "build",
    },
    "release": {
        "resolve-dependencies",
        "format-check",
        "lint",
        "type-check",
        "test",
        "quality",
        "security-scan",
        "license-check",
        "build",
        "package",
        "checksum",
        "generate-sbom",
        "attest",
        "sign",
        "create-release",
    },
    "distribution": {
        "verify-artifact",
        "publish",
        "promote",
        "deploy",
        "verify-deployment",
        "rollback",
    },
    "operation": {
        "monitor",
        "backup",
        "restore",
        "update",
        "rollback",
        "retire",
    },
}
QUALIFICATION_OPERATIONS = {
    "resolve-dependencies",
    "format-check",
    "lint",
    "type-check",
    "test",
    "quality",
    "security-scan",
    "license-check",
    "checksum",
    "generate-sbom",
    "attest",
    "sign",
}


@dataclass(frozen=True)
class RoleRule:
    path: str
    level: str
    core: bool = False
    origins: tuple[str, ...] = ()


ROLE_RULES: dict[str, RoleRule] = {
    "identity": RoleRule("README.md", "bootstrap", core=True),
    "agent-rules": RoleRule("AGENTS.md", "bootstrap", origins=("new",)),
    "current-state": RoleRule("PROJECT_STATE.md", "bootstrap", origins=("new",)),
    "vision": RoleRule("docs/000_Vision.md", "bootstrap", origins=("new",)),
    "principles": RoleRule("docs/002_Principes.md", "bootstrap", origins=("new",)),
    "scope": RoleRule("docs/003_Perimetre.md", "bootstrap", origins=("new",)),
    "requirements": RoleRule("docs/005_Exigences.md", "bootstrap", origins=("new",)),
    "use-cases": RoleRule("docs/010_Cas_Usage.md", "bootstrap", origins=("new",)),
    "initial-diagnostic": RoleRule(
        "docs/006_Diagnostic_Initial.md", "discovery", core=True, origins=("existing",)
    ),
    "sources": RoleRule("docs/004_Sources_Et_Preuve.md", "discovery"),
    "risks": RoleRule("docs/008_Registre_Risques.md", "discovery"),
    "open-questions": RoleRule("docs/099_Questions_Ouvertes.md", "discovery"),
    "glossary": RoleRule("docs/001_Glossaire.md", "development"),
    "domain-model": RoleRule("docs/020_Modele_Metier.md", "development"),
    "quality-tests": RoleRule("docs/060_Qualite_Et_Tests.md", "development"),
    "contracts-errors": RoleRule("docs/075_Contrats_Et_Erreurs.md", "development"),
    "audit": RoleRule("docs/095_Registre_Audit.md", "development"),
    "retrospective": RoleRule("RETROSPECTIVE.md", "development"),
    "architecture": RoleRule("docs/030_Architecture.md", "development"),
    "technology-decisions": RoleRule("docs/040_Choix_Techniques.md", "development"),
    "technology-registry": RoleRule("project.yaml", "development"),
    "roles-permissions": RoleRule("docs/015_Roles_Et_Permissions.md", "development"),
    "flows-loops": RoleRule("docs/021_Flux_Evenements_Et_Boucles.md", "development"),
    "scales-boundaries": RoleRule("docs/022_Echelles_Et_Frontieres.md", "development"),
    "system-map": RoleRule("docs/023_Carte_Du_Systeme.md", "development"),
    "user-experience": RoleRule("docs/025_Experience_Utilisateur.md", "development"),
    "visual-charter": RoleRule("docs/035_Charte_Graphique.md", "development"),
    "design-system": RoleRule("docs/036_Systeme_Design.md", "development"),
    "data-schemas": RoleRule("docs/045_Donnees_Et_Schemas.md", "development"),
    "metrics": RoleRule("docs/052_Metriques_Et_Garde_Fous.md", "development"),
    "visual-validation": RoleRule("docs/065_Validation_Visuelle.md", "development"),
    "security": RoleRule("docs/070_Securite_Et_Donnees.md", "development"),
    "threat-model": RoleRule("docs/072_Modele_De_Menace.md", "distribution"),
    "assets": RoleRule("assets/ASSETS.md", "development"),
    "asset-pipeline": RoleRule("assets/PIPELINE.md", "development"),
    "delivery-cycle": RoleRule("docs/042_Cycle_Livraison_Universel.md", "release"),
    "distribution-releases": RoleRule("docs/085_Distribution_Et_Releases.md", "release"),
    "changelog": RoleRule("CHANGELOG.md", "release"),
    "exploitation": RoleRule("docs/080_Exploitation.md", "distribution"),
    "application-lifecycle": RoleRule("docs/081_Cycle_De_Vie.md", "operation"),
    "runbooks": RoleRule("docs/083_Runbooks.md", "operation"),
    "recovery": RoleRule("docs/084_Plan_De_Reprise.md", "operation"),
}

PROFILE_REQUIREMENTS: dict[str, dict[str, set[str]]] = {
    "software": {
        "development": {
            "agent-rules",
            "architecture",
            "current-state",
            "quality-tests",
            "technology-decisions",
            "technology-registry",
        }
    },
    "android": {
        "development": {
            "architecture",
            "technology-registry",
            "user-experience",
            "visual-charter",
            "design-system",
            "visual-validation",
        },
        "release": {"distribution-releases"},
        "operation": {"application-lifecycle"},
    },
    "linux-service": {
        "development": {"architecture", "technology-registry"},
        "distribution": {"exploitation"},
        "operation": {"application-lifecycle", "runbooks"},
    },
    "web-pwa": {
        "development": {
            "user-experience",
            "visual-charter",
            "design-system",
            "visual-validation",
        },
        "release": {"distribution-releases"},
    },
    "game": {
        "development": {
            "user-experience",
            "visual-charter",
            "visual-validation",
            "assets",
            "asset-pipeline",
            "flows-loops",
        }
    },
    "research-simulation": {
        "discovery": {"sources", "risks", "open-questions"},
        "development": {"data-schemas", "metrics", "flows-loops"},
    },
    "dr-engineering": {},
}

CONCERN_REQUIREMENTS: dict[str, dict[str, set[str]]] = {
    "user-interface": {
        "development": {
            "user-experience",
            "visual-charter",
            "design-system",
            "visual-validation",
        }
    },
    "persistent-data": {
        "development": {"data-schemas"},
        "operation": {"recovery"},
    },
    "sensitive-data": {
        "development": {"security"},
        "distribution": {"threat-model"},
    },
    "network-access": {
        "development": {"security"},
        "distribution": {"threat-model"},
    },
    "authentication": {
        "development": {"security", "roles-permissions"},
        "distribution": {"threat-model"},
    },
    "multi-user": {
        "development": {"roles-permissions"},
    },
    "background-service": {
        "development": {"flows-loops", "scales-boundaries", "system-map"},
        "distribution": {"exploitation"},
        "operation": {"application-lifecycle", "runbooks"},
    },
    "assets": {
        "development": {"assets", "asset-pipeline"},
    },
    "automated-delivery": {
        "release": {"distribution-releases"},
        "distribution": {"exploitation"},
    },
}

SCOPE_REQUIREMENTS = {
    "release": {"distribution-releases", "changelog"},
    "distribution": {"distribution-releases"},
    "operation": {"exploitation", "application-lifecycle"},
}

TEMPLATE_FILES = {
    "START_HERE.md",
    "TEMPLATE_GUIDE.md",
    "VERSION",
    "guides/NEW_PROJECT.md",
    "guides/EXISTING_PROJECT.md",
    "project.adoption.yaml",
    "project.yaml",
    "schemas/project-adoption.schema.json",
    "schemas/project.schema.json",
    "scripts/check-project.sh",
    "scripts/validate-manifest.py",
    "scripts/inspect-project.py",
    "scripts/test-validation.py",
    "scripts/requirements-validation.txt",
    "docs/043_Adoption_Progressive.md",
    "docs/044_Boucle_Developpement.md",
    "docs/041_Registre_Technologique.md",
    "docs/042_Cycle_Livraison_Universel.md",
    "docs/007_Brief_Bootstrap.md",
    "docs/090_Decisions/ADR-0004-adoption-progressive.md",
    "docs/090_Decisions/ADR-0005-frontieres-livraison.md",
    "docs/090_Decisions/ADR-0006-boucle-developpement.md",
    "examples/project.bootstrap.yaml",
    "examples/project.delivery.yaml",
    "examples/project.multi-stack.yaml",
    "examples/project.v2-compat.yaml",
    "examples/adoption.existing.yaml",
    "migrations/project-manifest-v2-to-v3.md",
    ".github/workflows/project-check.yml",
    *{rule.path for rule in ROLE_RULES.values()},
}


class ValidationProblem(ValueError):
    """Erreur sémantique associée à un manifeste."""


def display_path(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def semantic_fail(path: Path, root: Path, message: str) -> None:
    raise ValidationProblem(f"{display_path(path, root)}: {message}")


def load_yaml(path: Path, root: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValidationProblem(f"{display_path(path, root)}: fichier manquant") from None
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise ValidationProblem(f"{display_path(path, root)}: YAML invalide : {error}") from error
    if not isinstance(data, dict):
        raise ValidationProblem(f"{display_path(path, root)}: objet YAML racine attendu")
    return data


def load_json(path: Path, root: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValidationProblem(f"{display_path(path, root)}: fichier manquant") from None
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValidationProblem(f"{display_path(path, root)}: JSON invalide : {error}") from error
    if not isinstance(data, dict):
        raise ValidationProblem(f"{display_path(path, root)}: objet JSON racine attendu")
    return data


def schema_validate(
    path: Path,
    data: dict[str, Any],
    schema: dict[str, Any],
    root: Path,
) -> None:
    validator = jsonschema.Draft202012Validator(
        schema,
        format_checker=jsonschema.FormatChecker(),
    )
    errors = sorted(validator.iter_errors(data), key=lambda item: list(item.absolute_path))
    if not errors:
        return
    error = errors[0]
    location = ".".join(str(part) for part in error.absolute_path) or "<racine>"
    semantic_fail(path, root, f"schéma invalide à {location}: {error.message}")


def transitive_dependencies(
    operation_id: str,
    operations: dict[str, Any],
) -> set[str]:
    found: set[str] = set()
    pending = list(operations.get(operation_id, {}).get("needs", []))
    while pending:
        dependency = pending.pop()
        if dependency in found:
            continue
        found.add(dependency)
        pending.extend(operations.get(dependency, {}).get("needs", []))
    return found


def validate_project_semantics(path: Path, data: dict[str, Any], root: Path) -> None:
    schema_version = data.get("schema_version", 1)
    components = set(data.get("components", {}))
    artifacts = set(data.get("artifacts", {}))
    environments = set(data.get("environments", {}))
    secrets = set(data.get("secrets", {}))

    for component_id, component in data.get("components", {}).items():
        for artifact in component.get("artifacts", []):
            if schema_version >= 2 and artifact not in artifacts:
                semantic_fail(path, root, f"composant {component_id}: artefact inconnu {artifact}")

    all_operations: dict[str, tuple[str, dict[str, Any]]] = {}
    for pipeline_id, pipeline in data.get("pipelines", {}).items():
        operations = pipeline.get("operations", {})
        for operation_id, operation in operations.items():
            if operation_id in all_operations:
                semantic_fail(path, root, f"identifiant d'opération dupliqué {operation_id}")
            all_operations[operation_id] = (pipeline_id, operation)

        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(operation_id: str) -> None:
            if operation_id in visiting:
                semantic_fail(
                    path,
                    root,
                    f"cycle détecté dans {pipeline_id} autour de {operation_id}",
                )
            if operation_id in visited:
                return
            if operation_id not in operations:
                semantic_fail(path, root, f"{pipeline_id}: dépendance inconnue {operation_id}")
            visiting.add(operation_id)
            for dependency in operations[operation_id].get("needs", []):
                visit(dependency)
                dependency_phase = operations[dependency]["phase"]
                current_phase = operations[operation_id]["phase"]
                if (
                    schema_version >= 3
                    and PHASE_INDEX[dependency_phase] > PHASE_INDEX[current_phase]
                ):
                    semantic_fail(
                        path,
                        root,
                        f"{operation_id}: dépendance de phase inversée vers {dependency}",
                    )
            visiting.remove(operation_id)
            visited.add(operation_id)

        for operation_id in operations:
            visit(operation_id)

        for operation_id, operation in operations.items():
            component = operation.get("component")
            if component and component not in components:
                semantic_fail(path, root, f"{operation_id}: composant inconnu {component}")
            environment = operation.get("environment")
            if environment and environment not in environments:
                semantic_fail(path, root, f"{operation_id}: environnement inconnu {environment}")
            for field, known in (
                ("inputs", artifacts),
                ("outputs", artifacts),
                ("secrets", secrets),
            ):
                for reference in operation.get(field, []):
                    if reference not in known:
                        semantic_fail(
                            path,
                            root,
                            f"{operation_id}: référence {field} inconnue {reference}",
                        )

            failure = operation.get("failure", {})
            if (
                schema_version >= 3
                and failure.get("mode") == "retry"
                and not operation.get("idempotent")
            ):
                semantic_fail(
                    path,
                    root,
                    f"{operation_id}: retry exige idempotent: true",
                )
            if schema_version >= 3 and failure.get("mode") == "rollback":
                rollback = failure.get("rollback_operation")
                if not rollback:
                    semantic_fail(
                        path,
                        root,
                        f"{operation_id}: rollback_operation requis",
                    )

    for artifact_id, artifact in data.get("artifacts", {}).items():
        producer = artifact["produced_by"]
        if producer not in all_operations:
            semantic_fail(path, root, f"artefact {artifact_id}: producteur inconnu {producer}")
        producer_operation = all_operations[producer][1]
        if (
            schema_version >= 3
            and artifact_id not in producer_operation.get("outputs", [])
        ):
            semantic_fail(
                path,
                root,
                f"artefact {artifact_id}: le producteur {producer} ne le déclare pas en sortie",
            )

    if schema_version >= 3:
        for operation_id, (pipeline_id, operation) in all_operations.items():
            operations = data["pipelines"][pipeline_id]["operations"]
            ancestors = transitive_dependencies(operation_id, operations)
            for artifact_id in operation.get("inputs", []):
                producer = data["artifacts"][artifact_id]["produced_by"]
                producer_pipeline = all_operations[producer][0]
                if producer_pipeline == pipeline_id and producer not in ancestors:
                    semantic_fail(
                        path,
                        root,
                        f"{operation_id}: consomme {artifact_id} sans dépendre de {producer}",
                    )

    for secret_id, secret in data.get("secrets", {}).items():
        declared_consumers = set(secret["required_by"])
        actual_consumers = {
            operation_id
            for operation_id, (_, operation) in all_operations.items()
            if secret_id in operation.get("secrets", [])
        }
        unknown = declared_consumers - set(all_operations)
        if unknown:
            semantic_fail(
                path,
                root,
                f"secret {secret_id}: opérations inconnues {sorted(unknown)}",
            )
        if schema_version >= 3 and declared_consumers != actual_consumers:
            semantic_fail(
                path,
                root,
                f"secret {secret_id}: required_by et consommateurs réels divergent",
            )

    for environment_id, environment in data.get("environments", {}).items():
        promotion = environment.get("promotion", {})
        for operation in promotion.get("require_operations", []):
            if operation not in all_operations:
                semantic_fail(
                    path,
                    root,
                    f"environnement {environment_id}: opération requise inconnue {operation}",
                )
        rollback = environment.get("deployment", {}).get("rollback_operation")
        if rollback:
            if rollback not in all_operations:
                semantic_fail(
                    path,
                    root,
                    f"environnement {environment_id}: rollback inconnu {rollback}",
                )
            rollback_operation = all_operations[rollback][1]
            if schema_version >= 3 and rollback_operation.get("uses") != "rollback":
                semantic_fail(
                    path,
                    root,
                    f"environnement {environment_id}: {rollback} n'utilise pas rollback",
                )
            if (
                schema_version >= 3
                and rollback_operation.get("environment") != environment_id
            ):
                semantic_fail(
                    path,
                    root,
                    f"environnement {environment_id}: rollback dans un autre environnement",
                )

    if schema_version >= 3:
        for operation_id, (_, operation) in all_operations.items():
            failure = operation.get("failure", {})
            rollback = failure.get("rollback_operation")
            if rollback:
                if rollback not in all_operations:
                    semantic_fail(path, root, f"{operation_id}: rollback inconnu {rollback}")
                rollback_operation = all_operations[rollback][1]
                if rollback_operation.get("uses") != "rollback":
                    semantic_fail(path, root, f"{operation_id}: {rollback} n'est pas un rollback")
                if rollback_operation.get("environment") != operation.get("environment"):
                    semantic_fail(
                        path,
                        root,
                        f"{operation_id}: rollback dans un environnement différent",
                    )

    if schema_version >= 3:
        validate_v3_delivery(path, data, root, all_operations)


def validate_v3_delivery(
    path: Path,
    data: dict[str, Any],
    root: Path,
    all_operations: dict[str, tuple[str, dict[str, Any]]],
) -> None:
    pipelines = data.get("pipelines", {})
    scopes = data["delivery"]["scopes"]
    pipeline_scope: dict[str, str] = {}

    for scope_name, scope in scopes.items():
        status = scope["status"]
        assigned = scope.get("pipelines", [])
        execution = scope.get("execution")
        if status != "active" and assigned:
            semantic_fail(
                path,
                root,
                f"portée {scope_name}: pipelines interdits avec le statut {status}",
            )
        if (
            status == "active"
            and scope_name in {"release", "distribution"}
            and not assigned
        ):
            semantic_fail(
                path,
                root,
                f"portée {scope_name}: un graphe d'opérations est requis, "
                "y compris pour une exécution manuelle",
            )
        if status == "active" and execution in {"automated", "hybrid"} and not assigned:
            semantic_fail(path, root, f"portée {scope_name}: pipeline automatisé requis")
        for pipeline_id in assigned:
            if pipeline_id not in pipelines:
                semantic_fail(
                    path,
                    root,
                    f"portée {scope_name}: pipeline inconnu {pipeline_id}",
                )
            if pipeline_id in pipeline_scope:
                semantic_fail(
                    path,
                    root,
                    f"pipeline {pipeline_id}: affecté à plusieurs portées",
                )
            pipeline_scope[pipeline_id] = scope_name

    unassigned = set(pipelines) - set(pipeline_scope)
    if unassigned:
        semantic_fail(path, root, f"pipelines sans portée : {sorted(unassigned)}")

    for pipeline_id, pipeline in pipelines.items():
        scope_name = pipeline_scope[pipeline_id]
        scope_execution = scopes[scope_name].get("execution")
        if scope_execution == "manual":
            if pipeline["orchestrator"] != "manual":
                semantic_fail(
                    path,
                    root,
                    f"pipeline {pipeline_id}: orchestrator manual requis par la portée",
                )
            if scope_name in {"release", "distribution"} and not pipeline.get(
                "procedure"
            ):
                semantic_fail(
                    path,
                    root,
                    f"pipeline {pipeline_id}: procédure manuelle explicite requise",
                )
            if pipeline.get("procedure"):
                procedure_path = safe_project_path(root, pipeline["procedure"])
                if not procedure_path.is_file():
                    semantic_fail(
                        path,
                        root,
                        f"pipeline {pipeline_id}: procédure introuvable "
                        f"{pipeline['procedure']}",
                    )
        for operation_id, operation in pipeline["operations"].items():
            phase = operation["phase"]
            uses = operation["uses"]
            canonical_phase = CANONICAL_PHASES.get(uses)
            if canonical_phase and phase != canonical_phase:
                semantic_fail(
                    path,
                    root,
                    f"{operation_id}: {uses} appartient à la phase {canonical_phase}, "
                    f"pas {phase}",
                )
            if canonical_phase and uses not in SCOPE_OPERATIONS[scope_name]:
                semantic_fail(
                    path,
                    root,
                    f"{operation_id}: opération {uses} interdite dans {scope_name}",
                )
            if canonical_phase is None:
                if not uses.startswith("x-"):
                    semantic_fail(
                        path,
                        root,
                        f"{operation_id}: opération non canonique {uses}; "
                        "préfixer une extension explicite par x-",
                    )
                if scope_name in {"distribution", "operation"}:
                    semantic_fail(
                        path,
                        root,
                        f"{operation_id}: extension opaque interdite dans {scope_name}",
                    )
                if phase not in {"verify", "produce"}:
                    semantic_fail(
                        path,
                        root,
                        f"{operation_id}: extension admise uniquement en verify/produce",
                    )
            if scope_name == "distribution" and operation.get("outputs"):
                semantic_fail(
                    path,
                    root,
                    f"{operation_id}: une distribution ne produit pas d'artefact",
                )
            if uses in {"deploy", "promote", "verify-deployment", "rollback"}:
                if not operation.get("environment"):
                    semantic_fail(
                        path,
                        root,
                        f"{operation_id}: environnement requis pour {uses}",
                    )

            for artifact_id in operation.get("outputs", []):
                if data["artifacts"][artifact_id]["produced_by"] != operation_id:
                    semantic_fail(
                        path,
                        root,
                        f"{operation_id}: sortie {artifact_id} attribuée à un autre producteur",
                    )

    artifacts = data.get("artifacts", {})
    release_artifacts: dict[str, dict[str, Any]] = {}
    for artifact_id, artifact in artifacts.items():
        role = artifact.get("role")
        if role not in {"verification-output", "release-artifact"}:
            semantic_fail(path, root, f"artefact {artifact_id}: rôle v3 requis")
        producer = artifact["produced_by"]
        producer_pipeline = all_operations[producer][0]
        producer_scope = pipeline_scope[producer_pipeline]
        contract = artifact.get("contract")

        if role == "verification-output":
            if producer_scope not in {"development", "release"}:
                semantic_fail(
                    path,
                    root,
                    f"artefact {artifact_id}: sortie de vérification produite par {producer_scope}",
                )
            if contract:
                semantic_fail(
                    path,
                    root,
                    f"artefact {artifact_id}: contrat de release interdit pour une sortie de contrôle",
                )
            continue

        release_artifacts[artifact_id] = artifact
        if producer_scope != "release":
            semantic_fail(
                path,
                root,
                f"artefact {artifact_id}: un release-artifact doit être produit en release",
            )
        producer_operation = all_operations[producer][1]
        if producer_operation["uses"] not in {"build", "package"}:
            semantic_fail(
                path,
                root,
                f"artefact {artifact_id}: producteur build ou package requis",
            )
        if not contract:
            semantic_fail(path, root, f"artefact {artifact_id}: contrat de release requis")
        if not contract.get("immutable"):
            semantic_fail(path, root, f"artefact {artifact_id}: immutable: true requis")

        qualified_by = contract.get("qualified_by", [])
        for operation_id in qualified_by:
            if operation_id not in all_operations:
                semantic_fail(
                    path,
                    root,
                    f"artefact {artifact_id}: qualification inconnue {operation_id}",
                )
            qualification_pipeline, qualification = all_operations[operation_id]
            if pipeline_scope[qualification_pipeline] != "release":
                semantic_fail(
                    path,
                    root,
                    f"artefact {artifact_id}: qualification {operation_id} hors release",
                )
            if qualification["uses"] not in QUALIFICATION_OPERATIONS:
                semantic_fail(
                    path,
                    root,
                    f"artefact {artifact_id}: {operation_id} n'est pas une qualification",
                )
        operations_using_artifact: dict[str, list[str]] = defaultdict(list)
        for operation_id, (_, operation) in all_operations.items():
            if artifact_id in operation.get("inputs", []):
                operations_using_artifact[operation["uses"]].append(operation_id)

        required_operations = {"checksum": "digest"}
        if contract.get("provenance") == "required":
            required_operations["attest"] = "provenance"
        if contract.get("sbom") == "required":
            required_operations["generate-sbom"] = "SBOM"
        if contract.get("signature") == "required":
            required_operations["sign"] = "signature"
        for uses, label in required_operations.items():
            matching_operations = set(operations_using_artifact.get(uses, []))
            if not matching_operations:
                semantic_fail(
                    path,
                    root,
                    f"artefact {artifact_id}: opération {uses} requise pour {label}",
                )
            if not matching_operations.intersection(qualified_by):
                semantic_fail(
                    path,
                    root,
                    f"artefact {artifact_id}: {uses} doit figurer dans qualified_by",
                )

        release_creations = [
            operation_id
            for operation_id in operations_using_artifact.get("create-release", [])
            if pipeline_scope[all_operations[operation_id][0]] == "release"
        ]
        if not release_creations:
            semantic_fail(
                path,
                root,
                f"artefact {artifact_id}: aucune opération create-release ne le consomme",
            )
        for release_operation_id in release_creations:
            release_pipeline_id = all_operations[release_operation_id][0]
            release_operations = pipelines[release_pipeline_id]["operations"]
            ancestors = transitive_dependencies(
                release_operation_id,
                release_operations,
            )
            missing_qualifications = set(qualified_by) - ancestors
            if missing_qualifications:
                semantic_fail(
                    path,
                    root,
                    f"{release_operation_id}: qualifications non antérieures "
                    f"{sorted(missing_qualifications)}",
                )

    release_scope = scopes["release"]
    distribution_scope = scopes["distribution"]
    if release_scope["status"] == "active" and not release_artifacts:
        semantic_fail(path, root, "portée release: aucun release-artifact déclaré")
    if distribution_scope["status"] == "active":
        if release_scope["status"] != "active":
            semantic_fail(
                path,
                root,
                "portée distribution: une portée release active est requise",
            )
        if not distribution_scope.get("intent", {}).get("targets"):
            semantic_fail(
                path,
                root,
                "portée distribution: au moins une cible explicite est requise",
            )

    distribution_actions = 0
    distributed_artifacts: set[str] = set()
    for operation_id, (pipeline_id, operation) in all_operations.items():
        scope_name = pipeline_scope[pipeline_id]
        if operation["uses"] in {"create-release", "publish", "promote", "deploy"}:
            inputs = operation.get("inputs", [])
            if not inputs:
                semantic_fail(
                    path,
                    root,
                    f"{operation_id}: au moins un release-artifact en entrée est requis",
                )
            for artifact_id in inputs:
                if artifacts[artifact_id].get("role") != "release-artifact":
                    semantic_fail(
                        path,
                        root,
                        f"{operation_id}: {artifact_id} n'est pas un release-artifact",
                    )
        if scope_name == "distribution":
            for artifact_id in operation.get("inputs", []):
                if artifacts[artifact_id].get("role") != "release-artifact":
                    semantic_fail(
                        path,
                        root,
                        f"{operation_id}: la distribution consomme {artifact_id}, non qualifié",
                    )
            if operation["uses"] in {"publish", "promote", "deploy"}:
                distribution_actions += 1
                pipeline_operations = data["pipelines"][pipeline_id]["operations"]
                ancestors = transitive_dependencies(operation_id, pipeline_operations)
                for artifact_id in operation.get("inputs", []):
                    distributed_artifacts.add(artifact_id)
                    verified = any(
                        pipeline_operations[ancestor]["uses"] == "verify-artifact"
                        and artifact_id
                        in pipeline_operations[ancestor].get("inputs", [])
                        for ancestor in ancestors
                    )
                    if not verified:
                        semantic_fail(
                            path,
                            root,
                            f"{operation_id}: {artifact_id} n'est pas vérifié "
                            "dans la portée distribution",
                        )
                    handoff = artifacts[artifact_id].get("handoff")
                    if not handoff or not handoff.get("verify_digest"):
                        semantic_fail(
                            path,
                            root,
                            f"{operation_id}: {artifact_id} ne déclare pas de handoff "
                            "persistant avec vérification du digest",
                        )

    if distribution_scope["status"] == "active":
        if distribution_actions == 0:
            semantic_fail(
                path,
                root,
                "portée distribution: aucune action publish, promote ou deploy",
            )
        if not distributed_artifacts:
            semantic_fail(
                path,
                root,
                "portée distribution: aucun release-artifact consommé",
            )

    for environment_id, environment in data.get("environments", {}).items():
        approvals = environment.get("approvals", {})
        if approvals.get("required") and approvals.get("minimum", 0) < 1:
            semantic_fail(
                path,
                root,
                f"environnement {environment_id}: minimum >= 1 requis avec approbation",
            )
        promotion = environment.get("promotion", {})
        required_operations = set(promotion.get("require_operations", []))
        environment_consumers = [
            operation
            for _, operation in all_operations.values()
            if operation.get("environment") == environment_id
            and operation["uses"] in {"promote", "deploy", "verify-deployment"}
        ]
        for operation in environment_consumers:
            for artifact_id in operation.get("inputs", []):
                artifact = artifacts[artifact_id]
                if artifact.get("role") != "release-artifact":
                    continue
                qualified_by = set(artifact["contract"]["qualified_by"])
                missing = required_operations - qualified_by
                if missing:
                    semantic_fail(
                        path,
                        root,
                        f"environnement {environment_id}: politiques non satisfaites "
                        f"pour {artifact_id}: {sorted(missing)}",
                    )
                if (
                    promotion.get("require_signed_artifacts")
                    and artifact["contract"]["signature"] != "required"
                ):
                    semantic_fail(
                        path,
                        root,
                        f"environnement {environment_id}: {artifact_id} "
                        "doit exiger une signature",
                    )


def add_requirements(
    required: dict[str, set[str]],
    mapping: dict[str, set[str]],
    requested_level: str,
    provenance: str,
) -> None:
    requested_index = LEVEL_INDEX[requested_level]
    for level, roles in mapping.items():
        if LEVEL_INDEX[level] <= requested_index:
            for role in roles:
                required[role].add(f"{provenance}@{level}")


def project_scope_status(project: dict[str, Any] | None, scope: str) -> str | None:
    if not project or project.get("schema_version", 1) < 3:
        return None
    return project["delivery"]["scopes"][scope]["status"]


def compute_required_roles(
    adoption: dict[str, Any],
    level: str,
    project: dict[str, Any] | None,
) -> dict[str, set[str]]:
    origin = adoption["adoption"]["origin"]
    requested_index = LEVEL_INDEX[level]
    required: dict[str, set[str]] = defaultdict(set)

    for role, rule in ROLE_RULES.items():
        if LEVEL_INDEX[rule.level] > requested_index:
            continue
        if rule.origins and origin not in rule.origins:
            continue
        if rule.core or (rule.origins and origin in rule.origins):
            required[role].add(f"core@{rule.level}")

    if origin == "existing" and requested_index >= LEVEL_INDEX["development"]:
        for role in (
            "agent-rules",
            "current-state",
            "vision",
            "principles",
            "scope",
            "requirements",
            "use-cases",
        ):
            required[role].add("core-existing@development")

    for profile in adoption.get("profiles", {}).get("active", []):
        add_requirements(
            required,
            PROFILE_REQUIREMENTS.get(profile, {}),
            level,
            profile,
        )

    for concern, declaration in adoption.get("concerns", {}).items():
        if declaration.get("status") == "active":
            add_requirements(
                required,
                CONCERN_REQUIREMENTS.get(concern, {}),
                level,
                concern,
            )

    for scope in ("release", "distribution", "operation"):
        if (
            requested_index >= LEVEL_INDEX[scope]
            and project_scope_status(project, scope) == "active"
        ):
            for role in SCOPE_REQUIREMENTS[scope]:
                required[role].add(f"scope-{scope}@{scope}")

    return required


def safe_project_path(root: Path, declared_path: str) -> Path:
    path = (root / declared_path).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        raise ValidationProblem(
            f"project.adoption.yaml: chemin hors du projet : {declared_path}"
        ) from None
    return path


def find_placeholders(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []
    return sorted(set(PLACEHOLDER.findall(text)))


def validate_adoption_metadata(
    adoption: dict[str, Any],
    level: str,
) -> list[str]:
    errors: list[str] = []
    version = adoption.get("template_version", "")
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", version)
    if not match:
        errors.append("template_version: version sémantique x.y.z attendue")
    elif int(match.group(1)) != SUPPORTED_TEMPLATE_MAJOR:
        errors.append(
            f"template_version {version}: incompatible avec le validateur "
            f"de génération majeure {SUPPORTED_TEMPLATE_MAJOR}"
        )

    origin = adoption["adoption"]["origin"]
    if origin == "existing" and level == "bootstrap":
        errors.append(
            "origine existing: commencer à discovery par un diagnostic en lecture seule"
        )
    if origin == "new" and level == "discovery":
        errors.append(
            "origine new: passer de bootstrap à development ; "
            "discovery est la porte d'entrée d'un projet existant"
        )
    return errors


def scan_potential_secrets(root: Path) -> list[str]:
    excluded_directories = {
        ".git",
        ".hg",
        ".svn",
        ".venv",
        "venv",
        "node_modules",
        "__pycache__",
    }
    findings: list[str] = []
    for directory, names, filenames in os.walk(root):
        names[:] = [
            name for name in names if name not in excluded_directories
        ]
        for filename in filenames:
            if filename == ".env.example":
                continue
            path = Path(directory) / filename
            if path.is_symlink() or not path.is_file():
                continue
            try:
                if path.stat().st_size > 2 * 1024 * 1024:
                    continue
                lines = path.read_text(encoding="utf-8").splitlines()
            except (OSError, UnicodeError):
                continue
            for line_number, line in enumerate(lines, start=1):
                if SECRET_ASSIGNMENT.search(line):
                    findings.append(
                        f"secret potentiel : "
                        f"{display_path(path, root)}:{line_number}"
                    )
                    if len(findings) >= 20:
                        return findings
    return findings


def evaluate_adoption(
    root: Path,
    adoption: dict[str, Any],
    level: str,
    project: dict[str, Any] | None,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    documents = adoption.get("documents", {})
    required = compute_required_roles(adoption, level, project)
    requested_index = LEVEL_INDEX[level]
    origin = adoption["adoption"]["origin"]
    errors.extend(validate_adoption_metadata(adoption, level))
    active_paths: dict[str, list[str]] = defaultdict(list)
    for role, declaration in documents.items():
        if declaration["status"] == "active":
            active_paths[declaration["path"]].append(role)

    for profile in adoption.get("profiles", {}).get("active", []):
        profile_path = root / "profiles" / profile / "PROFILE.md"
        if not profile_path.is_file():
            errors.append(
                f"profil {profile}: descripteur manquant "
                f"{display_path(profile_path, root)}"
            )
        if profile not in PROFILE_REQUIREMENTS:
            warnings.append(
                f"profil personnalisé {profile}: aucune exigence machine centrale"
            )

    for concern, declaration in adoption.get("concerns", {}).items():
        if concern not in CONCERN_REQUIREMENTS:
            errors.append(
                f"préoccupation inconnue {concern}: corriger l'identifiant ou "
                "enregistrer ses règles dans le validateur"
            )
        if declaration["status"] == "deferred":
            until = declaration["until"]
            if LEVEL_INDEX[until] <= requested_index:
                errors.append(
                    f"préoccupation {concern}: échéance {until} atteinte ; "
                    "l'activer ou la déclarer non applicable"
                )

    for role, declaration in documents.items():
        if role not in ROLE_RULES:
            warnings.append(f"rôle documentaire personnalisé : {role}")
        status = declaration["status"]
        if status == "deferred" and LEVEL_INDEX[declaration["until"]] <= requested_index:
            errors.append(
                f"rôle {role}: différé jusqu'à {declaration['until']}, "
                "échéance désormais atteinte"
            )
        if status == "not-applicable" and role in required:
            sources = ", ".join(sorted(required[role]))
            errors.append(
                f"rôle {role}: obligatoire ({sources}), ne peut pas être non applicable"
            )
        if status != "active":
            continue

    for declared_path, roles in sorted(active_paths.items()):
        path = safe_project_path(root, declared_path)
        if not path.is_file():
            errors.append(
                f"document actif manquant {declared_path} "
                f"(rôles {', '.join(sorted(roles))})"
            )
            continue
        try:
            if not path.read_text(encoding="utf-8").strip():
                errors.append(
                    f"document actif vide {declared_path} "
                    f"(rôles {', '.join(sorted(roles))})"
                )
                continue
        except UnicodeDecodeError:
            pass
        placeholders = find_placeholders(path)
        if placeholders:
            errors.append(
                f"variables non remplacées dans {declared_path} "
                f"(rôles {', '.join(sorted(roles))}; "
                f"exemples : {', '.join(placeholders[:5])})"
            )

    for role, sources in sorted(required.items()):
        declaration = documents.get(role)
        rule = ROLE_RULES[role]
        if declaration is None:
            errors.append(
                f"rôle {role}: requis par {', '.join(sorted(sources))}; "
                f"mapper un document, par défaut {rule.path}"
            )
        elif declaration["status"] != "active":
            errors.append(
                f"rôle {role}: requis par {', '.join(sorted(sources))}, "
                f"statut actuel {declaration['status']}"
            )

    if origin == "existing" and requested_index >= LEVEL_INDEX["discovery"]:
        if "initial-diagnostic" not in required:
            errors.append("invariant interne : diagnostic initial non calculé")

    return {
        "required_roles": {
            role: sorted(sources) for role, sources in sorted(required.items())
        },
        "deferred_documents": sorted(
            role
            for role, declaration in documents.items()
            if declaration["status"] == "deferred"
        ),
        "warnings": warnings,
        "errors": errors,
    }


def validate_requested_scope(
    project: dict[str, Any] | None,
    level: str,
) -> list[str]:
    if not project:
        return []
    requested_index = LEVEL_INDEX[level]
    errors: list[str] = []
    if project.get("schema_version", 1) < 3:
        if requested_index >= LEVEL_INDEX["release"]:
            return [
                "les manifestes v1/v2 restent valides au niveau development, "
                "mais ne peuvent pas prouver les frontières release/distribution ; "
                "migrer explicitement vers la v3"
            ]
        return []
    scopes = project["delivery"]["scopes"]

    for scope in ("development", "release", "distribution", "operation"):
        if requested_index < LEVEL_INDEX[scope]:
            continue
        status = scopes[scope]["status"]
        if scope == "development" and status != "active":
            errors.append(
                f"portée development: le niveau {level} exige status: active, "
                f"statut actuel {status}"
            )
            continue
        if status in {"deferred", "unresolved"}:
            errors.append(
                f"portée {scope}: le niveau {level} exige une décision active "
                f"ou not-applicable, statut actuel {status}"
            )

    if requested_index >= LEVEL_INDEX["release"] and scopes["release"]["status"] == "active":
        release_artifacts = [
            artifact
            for artifact in project.get("artifacts", {}).values()
            if artifact.get("role") == "release-artifact"
        ]
        if not release_artifacts:
            errors.append("niveau release: aucun release-artifact déclaré")

    if (
        requested_index >= LEVEL_INDEX["distribution"]
        and scopes["distribution"]["status"] == "active"
        and scopes["distribution"].get("execution") in {"automated", "hybrid"}
    ):
        distribution_pipelines = scopes["distribution"].get("pipelines", [])
        operations = [
            operation
            for pipeline_id in distribution_pipelines
            for operation in project["pipelines"][pipeline_id]["operations"].values()
        ]
        if not any(
            operation["uses"] in {"publish", "promote", "deploy"}
            for operation in operations
        ):
            errors.append(
                "niveau distribution: aucune opération publish, promote ou deploy"
            )
    return errors


def require_template_files(root: Path) -> list[str]:
    return [
        f"fichier de template manquant : {path}"
        for path in sorted(TEMPLATE_FILES)
        if not (root / path).is_file()
    ]


def validate_template(
    root: Path,
    project_schema: dict[str, Any],
    adoption_schema: dict[str, Any],
) -> dict[str, Any]:
    errors = require_template_files(root)
    warnings: list[str] = []

    adoption_path = root / "project.adoption.yaml"
    adoption = load_yaml(adoption_path, root)
    schema_validate(adoption_path, adoption, adoption_schema, root)

    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if adoption.get("template_version") != version:
        errors.append(
            "project.adoption.yaml: template_version doit correspondre exactement à VERSION"
        )

    project_paths = [
        root / "project.yaml",
        *sorted((root / "examples").glob("project.*.yaml")),
    ]
    for path in project_paths:
        data = load_yaml(path, root)
        schema_validate(path, data, project_schema, root)
        validate_project_semantics(path, data, root)

    for path in sorted((root / "examples").glob("adoption.*.yaml")):
        data = load_yaml(path, root)
        schema_validate(path, data, adoption_schema, root)

    for path in sorted(root.rglob("*.yaml")):
        load_yaml(path, root)
    for path in sorted(root.rglob("*.json")):
        load_json(path, root)

    return {
        "required_roles": {},
        "deferred_documents": [],
        "warnings": warnings,
        "errors": errors,
    }


def render_text(report: dict[str, Any]) -> str:
    status = "READY" if not report["errors"] else "BLOCKED"
    lines = [
        f"NIVEAU {report['level']} — {status}",
        f"Origine : {report['origin']}",
        f"Rôles obligatoires : {len(report['required_roles'])}",
        f"Documents différés déclarés : {len(report['deferred_documents'])}",
        f"Avertissements : {len(report['warnings'])}",
        f"Erreurs : {len(report['errors'])}",
    ]
    if report["warnings"]:
        lines.extend(["", "AVERTISSEMENTS"])
        lines.extend(f"- {warning}" for warning in report["warnings"])
    if report["errors"]:
        lines.extend(["", "BLOCAGES"])
        lines.extend(f"- {error}" for error in report["errors"])
    lines.extend(["", "PROCHAINE ACTION", report["next_action"]])
    return "\n".join(lines) + "\n"


def determine_next_action(report: dict[str, Any]) -> str:
    if report["errors"]:
        return report["errors"][0]
    level = report["level"]
    if level == "operation":
        return "Maintenir les preuves, l'état présent et les procédures de reprise."
    next_level = LEVELS[LEVEL_INDEX[level] + 1]
    return (
        f"Le niveau {level} est satisfait. N'activer {next_level} "
        "que lorsqu'il correspond à une réalité du projet."
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "level",
        nargs="?",
        choices=LEVELS,
        help="niveau à vérifier ; sinon lit project.adoption.yaml",
    )
    parser.add_argument("--root", default=".", help="racine du projet")
    parser.add_argument("--template", action="store_true", help="auto-contrôle du template")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        print(f"RACINE INVALIDE : {root}", file=sys.stderr)
        return 2

    template_mode = args.template or os.environ.get("TEMPLATE_MODE") == "1"
    try:
        project_schema = load_json(root / "schemas/project.schema.json", root)
        adoption_schema = load_json(
            root / "schemas/project-adoption.schema.json",
            root,
        )

        if template_mode:
            level = args.level or "operation"
            result = validate_template(root, project_schema, adoption_schema)
            origin = "template"
        else:
            adoption_path = root / "project.adoption.yaml"
            adoption = load_yaml(adoption_path, root)
            schema_validate(adoption_path, adoption, adoption_schema, root)
            level = args.level or adoption["adoption"]["current_level"]
            origin = adoption["adoption"]["origin"]

            active_profiles = set(adoption.get("profiles", {}).get("active", []))
            project: dict[str, Any] | None = None
            project_path = root / "project.yaml"
            if "software" in active_profiles or project_path.is_file():
                project = load_yaml(project_path, root)
                schema_validate(project_path, project, project_schema, root)
                validate_project_semantics(project_path, project, root)

            result = evaluate_adoption(root, adoption, level, project)
            result["errors"].extend(validate_requested_scope(project, level))

        result["errors"].extend(scan_potential_secrets(root))
        report = {
            "status": "ready" if not result["errors"] else "blocked",
            "level": level,
            "origin": origin,
            **result,
        }
        report["next_action"] = determine_next_action(report)
    except (ValidationProblem, jsonschema.ValidationError) as error:
        report = {
            "status": "blocked",
            "level": args.level or "unknown",
            "origin": "template" if template_mode else "unknown",
            "required_roles": {},
            "deferred_documents": [],
            "warnings": [],
            "errors": [str(error)],
        }
        report["next_action"] = determine_next_action(report)

    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_text(report), end="")
    return 0 if report["status"] == "ready" else 1


if __name__ == "__main__":
    raise SystemExit(main())
