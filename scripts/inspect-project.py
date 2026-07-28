#!/usr/bin/env python3
"""Inventorie un dépôt existant sans écrire ni exécuter son code."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


SKIPPED_DIRECTORIES = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "target",
    "dist",
    "build",
    ".venv",
    "venv",
    "__pycache__",
}

MANIFEST_NAMES = {
    "project.yaml",
    "project.adoption.yaml",
    "package.json",
    "Cargo.toml",
    "pyproject.toml",
    "requirements.txt",
    "go.mod",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "settings.gradle",
    "settings.gradle.kts",
    "Package.swift",
    "pubspec.yaml",
    "CMakeLists.txt",
    "Makefile",
    "Dockerfile",
}

LOCKFILE_NAMES = {
    "package-lock.json",
    "npm-shrinkwrap.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "bun.lock",
    "bun.lockb",
    "Cargo.lock",
    "uv.lock",
    "poetry.lock",
    "Pipfile.lock",
    "go.sum",
    "gradle.lockfile",
}

TEMPLATE_COLLISIONS = {
    "README.md",
    "AGENTS.md",
    "VERSION",
    "CHANGELOG.md",
    "PROJECT_STATE.md",
    "SECURITY.md",
    ".github/workflows",
}

TECHNOLOGY_MARKERS = {
    "TypeScript": {"tsconfig.json"},
    "Node.js": {"package.json"},
    "Rust": {"Cargo.toml"},
    "Python": {"pyproject.toml", "requirements.txt"},
    "Go": {"go.mod"},
    "Java/JVM": {"pom.xml", "build.gradle", "build.gradle.kts"},
    "Android/Gradle": {"settings.gradle", "settings.gradle.kts", "AndroidManifest.xml"},
    "Swift": {"Package.swift"},
    "Flutter/Dart": {"pubspec.yaml"},
    "C/C++": {"CMakeLists.txt"},
    "Docker/OCI": {"Dockerfile", "compose.yaml", "docker-compose.yml"},
}


def iter_files(root: Path, max_files: int) -> list[Path]:
    files: list[Path] = []
    for directory, names, filenames in os.walk(root):
        names[:] = sorted(name for name in names if name not in SKIPPED_DIRECTORIES)
        for filename in sorted(filenames):
            path = Path(directory) / filename
            if path.is_symlink() or not path.is_file():
                continue
            files.append(path)
            if len(files) >= max_files:
                return files
    return files


def fingerprint(path: Path) -> tuple[int, int, str | None]:
    stat = path.stat()
    digest = None
    if stat.st_size <= 10 * 1024 * 1024:
        hasher = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                hasher.update(chunk)
        digest = hasher.hexdigest()
    return stat.st_size, stat.st_mtime_ns, digest


def snapshot(paths: list[Path], root: Path) -> dict[str, tuple[int, int, str | None]]:
    result = {
        str(path.relative_to(root)): fingerprint(path)
        for path in paths
        if path.exists()
    }
    for git_path in (root / ".git" / "HEAD", root / ".git" / "index"):
        if git_path.is_file():
            result[str(git_path.relative_to(root))] = fingerprint(git_path)
    return result


def relative(paths: list[Path], root: Path) -> list[str]:
    return [str(path.relative_to(root)) for path in paths]


def read_package_scripts(path: Path) -> dict[str, dict[str, str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return {}
    scripts = data.get("scripts")
    if not isinstance(scripts, dict):
        return {}
    return {
        str(path): {
            str(name): str(command)
            for name, command in sorted(scripts.items())
        }
    }


def git_observation(root: Path) -> dict[str, Any]:
    if not (root / ".git").exists():
        return {"present": False, "status": "absent"}
    try:
        process = subprocess.run(
            [
                "git",
                "--no-optional-locks",
                "-C",
                str(root),
                "status",
                "--short",
                "--branch",
                "--untracked-files=normal",
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
            env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as error:
        return {
            "present": True,
            "status": "ambiguous",
            "reason": f"état Git non lu : {error}",
        }
    lines = process.stdout.splitlines()
    return {
        "present": True,
        "status": "confirmed" if process.returncode == 0 else "ambiguous",
        "branch": lines[0] if lines else None,
        "changes": lines[1:] if process.returncode == 0 else [],
        "error": process.stderr.strip() or None,
    }


def inspect(root: Path, max_files: int) -> tuple[dict[str, Any], list[str]]:
    files = iter_files(root, max_files)
    before = snapshot(files, root)
    names = {path.name for path in files}

    manifests = [path for path in files if path.name in MANIFEST_NAMES]
    lockfiles = [path for path in files if path.name in LOCKFILE_NAMES]
    workflows = [
        path
        for path in files
        if ".github/workflows" in path.as_posix()
        or path.name in {".gitlab-ci.yml", "Jenkinsfile", "azure-pipelines.yml"}
    ]
    tests = [
        path
        for path in files
        if "test" in path.name.lower()
        or any(part.lower() in {"test", "tests", "spec", "specs"} for part in path.parts)
    ]
    documentation = [
        path
        for path in files
        if path.suffix.lower() in {".md", ".rst", ".adoc"}
    ]

    package_scripts: dict[str, dict[str, str]] = {}
    for package in (path for path in manifests if path.name == "package.json"):
        for key, value in read_package_scripts(package).items():
            package_scripts[str(Path(key).relative_to(root))] = value

    probable = []
    for technology, markers in TECHNOLOGY_MARKERS.items():
        evidence = sorted(names.intersection(markers))
        if evidence:
            probable.append({"technology": technology, "evidence": evidence})

    js_lockfiles = sorted(
        path.name
        for path in lockfiles
        if path.name
        in {
            "package-lock.json",
            "npm-shrinkwrap.json",
            "pnpm-lock.yaml",
            "yarn.lock",
            "bun.lock",
            "bun.lockb",
        }
    )
    ambiguous = []
    if len(set(js_lockfiles)) > 1:
        ambiguous.append(
            {
                "subject": "gestionnaire de dépendances JavaScript",
                "evidence": js_lockfiles,
                "reason": "plusieurs familles de lockfiles sont présentes",
            }
        )

    contradictions = []
    for package in (path for path in manifests if path.name == "package.json"):
        try:
            data = json.loads(package.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            continue
        declared = data.get("packageManager")
        if not isinstance(declared, str):
            continue
        manager = declared.split("@", 1)[0]
        expected = {
            "npm": {"package-lock.json", "npm-shrinkwrap.json"},
            "pnpm": {"pnpm-lock.yaml"},
            "yarn": {"yarn.lock"},
            "bun": {"bun.lock", "bun.lockb"},
        }.get(manager, set())
        nearby = {path.name for path in lockfiles if path.parent == package.parent}
        if expected and nearby and not expected.intersection(nearby):
            contradictions.append(
                {
                    "subject": str(package.relative_to(root)),
                    "declared": declared,
                    "observed_lockfiles": sorted(nearby),
                }
            )

    collision_paths = []
    for collision in TEMPLATE_COLLISIONS:
        candidate = root / collision
        if candidate.exists():
            collision_paths.append(collision)

    absent = []
    if not manifests:
        absent.append("aucun manifeste technologique reconnu")
    if not lockfiles:
        absent.append("aucun lockfile reconnu")
    if not workflows:
        absent.append("aucun workflow CI/CD reconnu")
    if not tests:
        absent.append("aucun fichier de test reconnu par le diagnostic")
    if not documentation:
        absent.append("aucune documentation textuelle reconnue")

    report: dict[str, Any] = {
        "root": str(root),
        "read_only": True,
        "files_observed": len(files),
        "truncated": len(files) >= max_files,
        "confirmed": {
            "manifests": relative(manifests, root),
            "lockfiles": relative(lockfiles, root),
            "workflows": relative(workflows, root),
            "tests_sample": relative(tests[:50], root),
            "documentation_sample": relative(documentation[:50], root),
            "declared_package_scripts": package_scripts,
            "git": git_observation(root),
        },
        "probable": probable,
        "ambiguous": ambiguous,
        "contradictory": contradictions,
        "absent": absent,
        "template_collisions": sorted(collision_paths),
        "commands_executed_from_project": [],
        "next_action": (
            "Consigner et faire valider ce diagnostic avant toute copie, "
            "installation, migration ou modification."
        ),
    }

    after_files = iter_files(root, max_files)
    after = snapshot(after_files, root)
    changed = sorted(path for path in set(before) | set(after) if before.get(path) != after.get(path))
    return report, changed


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Diagnostic initial en lecture seule",
        "",
        f"- Racine : `{report['root']}`",
        f"- Fichiers observés : {report['files_observed']}",
        f"- Inventaire tronqué : {'oui' if report['truncated'] else 'non'}",
        "- Script du projet exécuté : aucun",
        "",
        "## Confirmé",
        "",
    ]
    confirmed = report["confirmed"]
    for label in (
        "manifests",
        "lockfiles",
        "workflows",
        "tests_sample",
        "documentation_sample",
    ):
        values = confirmed[label]
        lines.append(f"- {label} : {', '.join(f'`{value}`' for value in values) if values else 'aucun'}")
    package_scripts = confirmed["declared_package_scripts"]
    if package_scripts:
        lines.append("- Scripts déclarés :")
        for manifest, scripts in package_scripts.items():
            for name, command in scripts.items():
                lines.append(f"  - `{manifest}` — `{name}` : `{command}`")
    else:
        lines.append("- Scripts déclarés : aucun")
    git = confirmed["git"]
    lines.append(f"- Git : {git.get('status')}")
    if git.get("branch"):
        lines.append(f"- Référence : `{git['branch']}`")
    if git.get("changes"):
        lines.append(f"- Changements locaux observés : {len(git['changes'])}")
    lines.extend(["", "## Probable", ""])
    if report["probable"]:
        for item in report["probable"]:
            evidence = ", ".join(f"`{value}`" for value in item["evidence"])
            lines.append(f"- {item['technology']} — indices : {evidence}")
    else:
        lines.append("- Aucun environnement déduit.")
    lines.extend(["", "## Ambigu", ""])
    if report["ambiguous"]:
        for item in report["ambiguous"]:
            lines.append(f"- {item['subject']} : {item['reason']} ({', '.join(item['evidence'])})")
    else:
        lines.append("- Aucune ambiguïté automatique détectée.")
    lines.extend(["", "## Contradictoire", ""])
    if report["contradictory"]:
        for item in report["contradictory"]:
            lines.append(
                f"- `{item['subject']}` déclare `{item['declared']}`, "
                f"lockfiles observés : {', '.join(item['observed_lockfiles'])}"
            )
    else:
        lines.append("- Aucune contradiction automatique détectée.")
    lines.extend(["", "## Absent ou non observé", ""])
    lines.extend(f"- {item}" for item in report["absent"])
    if not report["absent"]:
        lines.append("- Aucun manque générique signalé.")
    lines.extend(["", "## Collisions à traiter sans écrasement", ""])
    if report["template_collisions"]:
        lines.extend(f"- `{item}`" for item in report["template_collisions"])
    else:
        lines.append("- Aucune collision canonique.")
    lines.extend(["", "## Prochaine action", "", report["next_action"]])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="dépôt à observer")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--max-files", type=int, default=50_000)
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        parser.error(f"répertoire introuvable : {root}")
    if args.max_files < 1:
        parser.error("--max-files doit être positif")

    try:
        report, changed = inspect(root, args.max_files)
    except (OSError, UnicodeError) as error:
        print(f"DIAGNOSTIC IMPOSSIBLE : {error}", file=sys.stderr)
        return 2

    if changed:
        print(
            "GARANTIE LECTURE SEULE VIOLÉE : changement observé dans "
            + ", ".join(changed),
            file=sys.stderr,
        )
        return 2

    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
