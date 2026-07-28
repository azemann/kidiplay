#!/usr/bin/env python3
"""Tests de non-régression du validateur v1.7."""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MODULE_PATH = ROOT / "scripts" / "validate-manifest.py"
SPEC = importlib.util.spec_from_file_location("project_template_validator", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("impossible de charger le validateur")
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


def yaml_data(path: Path) -> dict:
    return VALIDATOR.load_yaml(path, ROOT)


class ManifestCompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.project_schema = json.loads(
            (ROOT / "schemas/project.schema.json").read_text(encoding="utf-8")
        )

    def validate(self, name: str) -> dict:
        path = ROOT / "examples" / name
        data = yaml_data(path)
        VALIDATOR.schema_validate(path, data, self.project_schema, ROOT)
        VALIDATOR.validate_project_semantics(path, data, ROOT)
        return data

    def test_v1_remains_valid(self) -> None:
        self.validate("project.multi-stack.yaml")

    def test_v2_remains_valid(self) -> None:
        project = self.validate("project.v2-compat.yaml")
        self.assertEqual(
            VALIDATOR.validate_requested_scope(project, "development"),
            [],
        )
        self.assertTrue(VALIDATOR.validate_requested_scope(project, "release"))

    def test_v3_bootstrap_is_valid(self) -> None:
        project = self.validate("project.bootstrap.yaml")
        self.assertEqual(
            VALIDATOR.validate_requested_scope(project, "development"),
            [],
        )
        self.assertTrue(VALIDATOR.validate_requested_scope(project, "release"))

    def test_v3_split_delivery_is_valid(self) -> None:
        project = self.validate("project.delivery.yaml")
        self.assertEqual(
            VALIDATOR.validate_requested_scope(project, "distribution"),
            [],
        )

    def test_development_allows_unresolved_commands(self) -> None:
        project = self.validate("project.bootstrap.yaml")
        commands = project["components"]["main"]["commands"]
        self.assertEqual(commands["test"]["status"], "unresolved")
        self.assertEqual(commands["build"]["status"], "unresolved")

    def test_development_allows_experimental_verification_output(self) -> None:
        path = ROOT / "examples/project.bootstrap.yaml"
        data = copy.deepcopy(yaml_data(path))
        data["delivery"]["scopes"]["development"]["pipelines"] = [
            "development-spike"
        ]
        data["pipelines"]["development-spike"] = {
            "orchestrator": "manual",
            "operations": {
                "probe-idea": {
                    "phase": "produce",
                    "uses": "x-spike",
                    "component": "main",
                    "command": {
                        "status": "defined",
                        "argv": ["python3", "-c", "print('spike observation')"],
                    },
                    "outputs": ["spike-observation"],
                }
            },
        }
        data["artifacts"]["spike-observation"] = {
            "role": "verification-output",
            "type": "experiment-observation",
            "path": "experiments/spike-observation.json",
            "produced_by": "probe-idea",
            "retention_days": 3,
        }
        data["components"]["main"]["artifacts"].append("spike-observation")
        VALIDATOR.schema_validate(path, data, self.project_schema, ROOT)
        VALIDATOR.validate_project_semantics(path, data, ROOT)

    def test_control_build_remains_valid_in_development(self) -> None:
        project = self.validate("project.delivery.yaml")
        development_pipelines = project["delivery"]["scopes"]["development"][
            "pipelines"
        ]
        self.assertIn("development-ci", development_pipelines)
        operation = project["pipelines"]["development-ci"]["operations"][
            "build-preview"
        ]
        self.assertEqual(operation["uses"], "build")
        preview = project["artifacts"]["web-preview"]
        self.assertEqual(preview["role"], "verification-output")
        self.assertEqual(preview["produced_by"], "build-preview")

    def assert_semantic_failure(
        self,
        mutation,
        expected: str | None = None,
        require_schema_valid: bool = False,
    ) -> None:
        path = ROOT / "examples/project.delivery.yaml"
        data = copy.deepcopy(yaml_data(path))
        mutation(data)
        if require_schema_valid:
            VALIDATOR.schema_validate(path, data, self.project_schema, ROOT)
        if expected is None:
            context = self.assertRaises(VALIDATOR.ValidationProblem)
        else:
            context = self.assertRaisesRegex(
                VALIDATOR.ValidationProblem,
                expected,
            )
        with context:
            VALIDATOR.validate_project_semantics(path, data, ROOT)

    def assert_schema_failure(self, mutation) -> None:
        path = ROOT / "examples/project.delivery.yaml"
        data = copy.deepcopy(yaml_data(path))
        mutation(data)
        with self.assertRaises(VALIDATOR.ValidationProblem):
            VALIDATOR.schema_validate(path, data, self.project_schema, ROOT)

    def test_distribution_cannot_rebuild(self) -> None:
        def mutate(data):
            operation = data["pipelines"]["distribution"]["operations"][
                "verify-web-release"
            ]
            operation["phase"] = "produce"
            operation["uses"] = "build"

        self.assert_semantic_failure(mutate)

    def test_release_artifact_must_be_immutable(self) -> None:
        self.assert_semantic_failure(
            lambda data: data["artifacts"]["web-release"]["contract"].update(
                {"immutable": False}
            )
        )

    def test_distribution_rejects_verification_output(self) -> None:
        self.assert_semantic_failure(
            lambda data: data["artifacts"]["web-release"].update(
                {"role": "verification-output"}
            )
        )

    def test_producer_must_declare_output(self) -> None:
        def mutate(data):
            data["pipelines"]["release"]["operations"]["package-web"]["outputs"] = []

        self.assert_semantic_failure(mutate)

    def test_distribution_must_verify_release_artifact(self) -> None:
        def mutate(data):
            data["pipelines"]["distribution"]["operations"]["publish-web"]["needs"] = []

        self.assert_semantic_failure(mutate)

    def test_pipeline_has_only_one_scope(self) -> None:
        def mutate(data):
            data["delivery"]["scopes"]["operation"] = {
                "status": "active",
                "execution": "automated",
                "pipelines": ["distribution"],
            }

        self.assert_semantic_failure(mutate)

    def test_v2_rejects_v3_delivery_fields(self) -> None:
        self.assert_schema_failure(
            lambda data: data.update({"schema_version": 2})
        )

    def test_legacy_v2_keeps_relaxed_v15_contract(self) -> None:
        path = ROOT / "examples/project.v2-compat.yaml"
        data = copy.deepcopy(yaml_data(path))
        component = next(iter(data["components"].values()))
        component["languages"] = {"primary": "rust"}
        component["toolchain"] = {"build": "cargo"}
        component["commands"]["test"]["status"] = "historical-status"
        data["evidence"] = {}
        VALIDATOR.schema_validate(path, data, self.project_schema, ROOT)
        VALIDATOR.validate_project_semantics(path, data, ROOT)

    def test_deploy_cannot_masquerade_as_development_verification(self) -> None:
        def mutate(data):
            operation = data["pipelines"]["development-ci"]["operations"]["test-dev"]
            operation.update(
                {
                    "phase": "verify",
                    "uses": "deploy",
                    "inputs": ["web-release"],
                    "environment": "production",
                }
            )

        self.assert_semantic_failure(mutate)

    def test_build_cannot_masquerade_as_operation(self) -> None:
        def mutate(data):
            data["pipelines"]["maintenance"] = {
                "orchestrator": "github-actions",
                "operations": {
                    "bad-operation": {"phase": "operate", "uses": "build"}
                },
            }
            data["delivery"]["scopes"]["operation"] = {
                "status": "active",
                "execution": "automated",
                "pipelines": ["maintenance"],
            }

        self.assert_semantic_failure(mutate)

    def test_release_artifact_requires_build_or_package_producer(self) -> None:
        def mutate(data):
            operation = data["pipelines"]["release"]["operations"]["package-web"]
            operation.update({"phase": "verify", "uses": "test"})

        self.assert_semantic_failure(mutate)

    def test_release_requires_create_release(self) -> None:
        def mutate(data):
            del data["pipelines"]["release"]["operations"]["create-web-release"]

        self.assert_semantic_failure(mutate)

    def test_create_release_follows_all_qualifications(self) -> None:
        def mutate(data):
            operation = data["pipelines"]["release"]["operations"][
                "create-web-release"
            ]
            operation["needs"] = ["package-web"]

        self.assert_semantic_failure(mutate)

    def test_qualification_must_belong_to_release(self) -> None:
        def mutate(data):
            data["artifacts"]["web-release"]["contract"]["qualified_by"].append(
                "rollback-production"
            )

        self.assert_semantic_failure(mutate)

    def test_arbitrary_operation_cannot_qualify_release(self) -> None:
        def mutate(data):
            data["artifacts"]["web-release"]["contract"]["qualified_by"].append(
                "build-release"
            )

        self.assert_semantic_failure(mutate)

    def test_distribution_active_requires_release(self) -> None:
        def mutate(data):
            data["delivery"]["scopes"]["release"] = {
                "status": "not-applicable",
                "reason": "aucune release",
            }

        self.assert_semantic_failure(mutate)

    def test_manual_distribution_cannot_be_empty(self) -> None:
        def mutate(data):
            data["delivery"]["scopes"]["distribution"] = {
                "status": "active",
                "execution": "manual",
                "pipelines": [],
                "intent": {
                    "targets": [
                        {"kind": "hosting", "platform": "web"}
                    ]
                },
            }

        self.assert_semantic_failure(mutate)

    def test_deploy_requires_environment(self) -> None:
        def mutate(data):
            del data["pipelines"]["distribution"]["operations"][
                "deploy-production"
            ]["environment"]

        self.assert_semantic_failure(mutate)

    def test_approval_requires_positive_minimum(self) -> None:
        def mutate(data):
            data["environments"]["production"]["approvals"]["minimum"] = 0

        self.assert_semantic_failure(mutate)

    def test_signed_promotion_requires_signed_contract(self) -> None:
        def mutate(data):
            data["environments"]["production"]["promotion"][
                "require_signed_artifacts"
            ] = True

        self.assert_semantic_failure(mutate)

    def test_artifact_output_has_exactly_one_declared_producer(self) -> None:
        def mutate(data):
            data["pipelines"]["release"]["operations"]["build-release"][
                "outputs"
            ] = ["web-release"]

        self.assert_semantic_failure(mutate)

    def test_distribution_requires_persistent_handoff(self) -> None:
        def mutate(data):
            del data["artifacts"]["web-release"]["handoff"]

        self.assert_semantic_failure(mutate)

    def test_development_cannot_produce_release_artifact(self) -> None:
        def mutate(data):
            data["artifacts"]["web-preview"].update(
                {
                    "role": "release-artifact",
                    "contract": {
                        "immutable": True,
                        "version_source": "project.version",
                        "revision_source": "vcs.commit",
                        "digest_algorithm": "sha256",
                        "provenance": "optional",
                        "sbom": "optional",
                        "signature": "optional",
                        "qualified_by": [],
                    },
                }
            )

        self.assert_semantic_failure(
            mutate,
            expected="doit être produit en release",
            require_schema_valid=True,
        )

    def test_experimental_operation_cannot_enter_distribution(self) -> None:
        def mutate(data):
            operation = data["pipelines"]["distribution"]["operations"][
                "verify-web-release"
            ]
            operation.update({"phase": "verify", "uses": "x-spike"})

        self.assert_semantic_failure(
            mutate,
            expected="extension opaque interdite dans distribution",
            require_schema_valid=True,
        )

    def test_development_cannot_create_release(self) -> None:
        def mutate(data):
            operation = data["pipelines"]["development-ci"]["operations"][
                "build-preview"
            ]
            operation.update(
                {
                    "phase": "deliver",
                    "uses": "create-release",
                    "inputs": ["web-release"],
                }
            )

        self.assert_semantic_failure(
            mutate,
            expected="opération create-release interdite dans development",
            require_schema_valid=True,
        )

    def test_development_cannot_publish_or_deploy(self) -> None:
        for forbidden in ("publish", "deploy"):
            with self.subTest(uses=forbidden):
                def mutate(data, operation_name=forbidden):
                    operation = data["pipelines"]["development-ci"]["operations"][
                        "build-preview"
                    ]
                    operation.update(
                        {
                            "phase": "deliver",
                            "uses": operation_name,
                            "inputs": ["web-release"],
                        }
                    )
                    if operation_name == "deploy":
                        operation["environment"] = "production"

                self.assert_semantic_failure(
                    mutate,
                    expected=f"opération {forbidden} interdite dans development",
                    require_schema_valid=True,
                )

    def test_regime_names_are_not_machine_axes(self) -> None:
        regimes = {
            "exploration",
            "construction",
            "intégration",
            "stabilisation",
        }
        machine_terms = (
            set(VALIDATOR.LEVELS)
            | set(VALIDATOR.PHASE_INDEX)
            | set(VALIDATOR.SCOPE_OPERATIONS)
            | set(VALIDATOR.CANONICAL_PHASES)
            | set(VALIDATOR.CANONICAL_PHASES.values())
        )
        for operations in VALIDATOR.SCOPE_OPERATIONS.values():
            machine_terms.update(operations)
        self.assertTrue(regimes.isdisjoint(machine_terms))

        schema_enums: set[str] = set()

        def collect_enums(node) -> None:
            if isinstance(node, dict):
                values = node.get("enum", [])
                schema_enums.update(
                    value for value in values if isinstance(value, str)
                )
                for value in node.values():
                    collect_enums(value)
            elif isinstance(node, list):
                for value in node:
                    collect_enums(value)

        collect_enums(self.project_schema)
        self.assertTrue(regimes.isdisjoint(schema_enums))


class AdoptionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.adoption = {
            "schema_version": 1,
            "template_version": "1.7.0",
            "adoption": {
                "origin": "new",
                "current_level": "bootstrap",
                "initialized_at": None,
            },
            "profiles": {"active": []},
            "concerns": {},
            "documents": {},
        }
        required = VALIDATOR.compute_required_roles(
            self.adoption,
            "bootstrap",
            None,
        )
        for role in required:
            path = self.root / VALIDATOR.ROLE_RULES[role].path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"{role}\n", encoding="utf-8")
            self.adoption["documents"][role] = {
                "path": str(path.relative_to(self.root)),
                "status": "active",
            }

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def evaluate(self) -> dict:
        return VALIDATOR.evaluate_adoption(
            self.root,
            self.adoption,
            "bootstrap",
            None,
        )

    def test_minimal_bootstrap_succeeds(self) -> None:
        self.assertEqual(self.evaluate()["errors"], [])

    def test_active_missing_document_fails(self) -> None:
        identity = self.root / self.adoption["documents"]["identity"]["path"]
        identity.unlink()
        self.assertTrue(self.evaluate()["errors"])

    def test_placeholder_in_active_document_fails(self) -> None:
        identity = self.root / self.adoption["documents"]["identity"]["path"]
        identity.write_text("{{PROJECT_NAME}}\n", encoding="utf-8")
        self.assertTrue(self.evaluate()["errors"])

    def test_core_role_cannot_be_not_applicable(self) -> None:
        self.adoption["documents"]["vision"] = {
            "status": "not-applicable",
            "reason": "test invalide",
        }
        self.assertTrue(self.evaluate()["errors"])

    def test_deferred_deadline_blocks(self) -> None:
        self.adoption["documents"]["custom-report"] = {
            "status": "deferred",
            "until": "bootstrap",
            "reason": "test",
        }
        self.assertTrue(self.evaluate()["errors"])

    def test_software_development_requires_technology_manifest_role(self) -> None:
        self.adoption["profiles"]["active"] = ["software"]
        required = VALIDATOR.compute_required_roles(
            self.adoption,
            "development",
            yaml_data(ROOT / "examples/project.bootstrap.yaml"),
        )
        self.assertIn("technology-registry", required)

    def test_existing_example_maps_every_discovery_role(self) -> None:
        adoption = yaml_data(ROOT / "examples/adoption.existing.yaml")
        project = yaml_data(ROOT / "examples/project.bootstrap.yaml")
        required = VALIDATOR.compute_required_roles(adoption, "discovery", project)
        self.assertEqual(set(required) - set(adoption["documents"]), set())

    def test_unknown_concern_is_rejected(self) -> None:
        self.adoption["concerns"]["sensitve-data"] = {"status": "active"}
        self.assertTrue(self.evaluate()["errors"])

    def test_empty_active_document_is_rejected(self) -> None:
        identity = self.root / self.adoption["documents"]["identity"]["path"]
        identity.write_text("", encoding="utf-8")
        self.assertTrue(self.evaluate()["errors"])

    def test_existing_cannot_start_at_bootstrap(self) -> None:
        self.adoption["adoption"]["origin"] = "existing"
        self.assertTrue(self.evaluate()["errors"])

    def test_incompatible_template_major_is_rejected(self) -> None:
        self.adoption["template_version"] = "999.0.0"
        self.assertTrue(self.evaluate()["errors"])

    def test_template_version_1_6_adoption_remains_valid(self) -> None:
        self.adoption["template_version"] = "1.6.0"
        self.assertEqual(self.evaluate()["errors"], [])

    def test_secret_finding_is_part_of_validation_report(self) -> None:
        secret_file = self.root / "settings.txt"
        secret_file.write_text(
            "api" + "_key = " + "definitely-real\n",
            encoding="utf-8",
        )
        findings = VALIDATOR.scan_potential_secrets(self.root)
        self.assertTrue(findings)


class ReadOnlyInspectionTests(unittest.TestCase):
    def test_inspection_changes_no_file(self) -> None:
        spec = importlib.util.spec_from_file_location(
            "project_template_inspector",
            ROOT / "scripts/inspect-project.py",
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        inspector = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = inspector
        spec.loader.exec_module(inspector)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            package = root / "package.json"
            package.write_text(
                '{"scripts":{"test":"node --test"},"packageManager":"npm@11"}\n',
                encoding="utf-8",
            )
            lockfile = root / "package-lock.json"
            lockfile.write_text("{}\n", encoding="utf-8")
            before = {
                path.name: path.read_bytes()
                for path in (package, lockfile)
            }
            report, changed = inspector.inspect(root, 100)
            after = {
                path.name: path.read_bytes()
                for path in (package, lockfile)
            }
            self.assertEqual(changed, [])
            self.assertEqual(before, after)
            self.assertEqual(report["commands_executed_from_project"], [])
            self.assertEqual(
                report["confirmed"]["declared_package_scripts"]["package.json"],
                {"test": "node --test"},
            )

    def test_inspection_detects_a_created_file(self) -> None:
        spec = importlib.util.spec_from_file_location(
            "project_template_inspector_creation",
            ROOT / "scripts/inspect-project.py",
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        inspector = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = inspector
        spec.loader.exec_module(inspector)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("test\n", encoding="utf-8")

            def creating_git_observation(observed_root):
                (observed_root / "unexpected.txt").write_text(
                    "mutation\n",
                    encoding="utf-8",
                )
                return {"present": False, "status": "absent"}

            inspector.git_observation = creating_git_observation
            _, changed = inspector.inspect(root, 100)
            self.assertIn("unexpected.txt", changed)


if __name__ == "__main__":
    unittest.main(verbosity=2)
