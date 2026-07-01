from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping


EXPECTED_CHAIN_OBJECTS = (
    "0",
    "jbermejovega/sigilbook",
    "rulezero_public_workflow_law",
    "jbermejovega/sigil-workflows",
    "developer_repository",
    "pull_request_review_surface",
    "kqc_public_sharing_witness",
    "0",
)
EXPECTED_CHAIN_MAPS = (
    "include_rulezero",
    "normalize_public_workflow",
    "publish_template",
    "propose_to_developer",
    "review_pull_request",
    "certify_kqc",
)
REQUIRED_KQC_TRUE = (
    "public_trace_only",
    "pull_request_only",
    "maintainer_review_required",
    "no_force_move_transport",
    "no_identity_transport",
    "no_secret_transport",
    "no_direct_upstream_mutation",
    "no_branch_topology_as_authority",
    "sigilbook_chain_declared",
    "qquapp_exact_chain_declared",
    "developer_can_review_before_merge",
)
FORBIDDEN_PAYLOAD_TOKENS = (
    "password",
    "private_key",
    "ghp_",
    "github_pat_",
    "secret=",
    "token=",
    "reset --hard",
    "push --force",
)
EXPECTED_COMPU2526_RULE = {
    "id": "COMPU2526_ASSIGNMENT_REVIEW_INVARIANT_V1",
    "workflow_template": "ci/compu2526-review.yml",
    "metadata_template": "ci/properties/compu2526-review.properties.json",
    "public_sharing_admissible": True,
    "pull_request_review_required": True,
}
EXPECTED_COMPU2526_PERMISSIONS = {"contents": "read"}
EXPECTED_COMPU2526_REQUIRED_ACTIONS = (
    "actions/checkout@v4",
    "actions/setup-python@v5",
)
EXPECTED_COMPU2526_REVIEW_GATES = (
    "repository_manifest_report",
    "python_syntax_py_compile",
    "c_syntax_fsyntax_only",
    "cpp_syntax_fsyntax_only",
    "notebook_json_parse",
    "large_notebook_warning",
    "manual_science_review_trace",
)
EXPECTED_COMPU2526_MANUAL_TERMS = (
    "parameters and random seeds logged",
    "units and rescaling documented",
    "conserved quantities checked",
    "generated data and media provenance clear",
)
EXPECTED_COMPU2526_FORBIDDEN_DEFAULTS = (
    "pytest",
    "make check",
    "make distcheck",
    "jupyter nbconvert --execute",
)


def load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def require_sequence(
    issues: list[str],
    actual: object,
    expected: tuple[str, ...],
    label: str,
) -> None:
    actual_values = tuple(actual or ())
    for value in expected:
        if value not in actual_values:
            issues.append(f"{label} missing {value}")


def validate_compu2526_rule(manifest: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    rules = manifest.get("kqc_workflow_invariant_rules", ())
    if not isinstance(rules, list):
        return ["kqc_workflow_invariant_rules must be a list"]

    rule = next(
        (item for item in rules if isinstance(item, Mapping) and item.get("id") == EXPECTED_COMPU2526_RULE["id"]),
        None,
    )
    if rule is None:
        return ["COMPU2526_ASSIGNMENT_REVIEW_INVARIANT_V1 rule is required"]

    for key, expected in EXPECTED_COMPU2526_RULE.items():
        if rule.get(key) != expected:
            issues.append(f"COMPU2526 rule {key} must be {expected!r}")

    if dict(rule.get("least_privilege_permissions", {})) != EXPECTED_COMPU2526_PERMISSIONS:
        issues.append("COMPU2526 rule least_privilege_permissions must be contents: read")

    require_sequence(issues, rule.get("required_actions"), EXPECTED_COMPU2526_REQUIRED_ACTIONS, "COMPU2526 required_actions")
    require_sequence(issues, rule.get("required_review_gates"), EXPECTED_COMPU2526_REVIEW_GATES, "COMPU2526 required_review_gates")
    require_sequence(issues, rule.get("required_manual_review_terms"), EXPECTED_COMPU2526_MANUAL_TERMS, "COMPU2526 required_manual_review_terms")
    require_sequence(
        issues,
        rule.get("forbidden_default_operations"),
        EXPECTED_COMPU2526_FORBIDDEN_DEFAULTS,
        "COMPU2526 forbidden_default_operations",
    )

    return issues


def validate_manifest(manifest: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []

    if manifest.get("capsule_type") != "QQUAPP_PUBLIC_WORKFLOW_SHARING_V1":
        issues.append("capsule_type must be QQUAPP_PUBLIC_WORKFLOW_SHARING_V1")
    if manifest.get("canonical_repository") != "jbermejovega/sigilbook":
        issues.append("canonical_repository must be jbermejovega/sigilbook")
    if manifest.get("public_workflow_repository") != "jbermejovega/sigil-workflows":
        issues.append("public_workflow_repository must be jbermejovega/sigil-workflows")
    if manifest.get("sharing_mode") != "pull_request_to_other_developers":
        issues.append("sharing_mode must be pull_request_to_other_developers")
    if manifest.get("public_trace_only") is not True:
        issues.append("public_trace_only must be true")
    if manifest.get("private_payload_embedded") is not False:
        issues.append("private_payload_embedded must be false")

    chain = dict(manifest.get("qquapp_exact_chain", {}))
    if chain.get("id") != "SIGILBOOK_SIGIL_WORKFLOWS_PUBLIC_SHARING_EXACT":
        issues.append("qquapp_exact_chain id mismatch")
    if tuple(chain.get("objects", ())) != EXPECTED_CHAIN_OBJECTS:
        issues.append("qquapp_exact_chain objects mismatch")
    if tuple(chain.get("maps", ())) != EXPECTED_CHAIN_MAPS:
        issues.append("qquapp_exact_chain maps mismatch")
    if chain.get("exact") is not True:
        issues.append("qquapp_exact_chain exact must be true")

    kqc = dict(manifest.get("kqc_public_sharing_rule", {}))
    for key in REQUIRED_KQC_TRUE:
        if kqc.get(key) is not True:
            issues.append(f"kqc_public_sharing_rule {key} must be true")
    if kqc.get("private_payload_embedded") is not False:
        issues.append("kqc_public_sharing_rule private_payload_embedded must be false")

    issues.extend(validate_compu2526_rule(manifest))

    allowed_operations = tuple(manifest.get("allowed_operations", ()))
    if "certify_workflow_invariant" not in allowed_operations:
        issues.append("allowed_operations must include certify_workflow_invariant")

    rejected_operations = tuple(manifest.get("rejected_operations", ()))
    if "expensive_simulation_as_default_review_gate" not in rejected_operations:
        issues.append("rejected_operations must include expensive_simulation_as_default_review_gate")

    encoded = json.dumps(manifest, sort_keys=True).lower()
    forbidden_payload_tokens = {item.lower() for item in manifest.get("forbidden_payload_tokens", ())}
    for token in FORBIDDEN_PAYLOAD_TOKENS:
        if token in encoded and token not in forbidden_payload_tokens:
            issues.append(f"manifest contains forbidden token outside forbidden_payload_tokens: {token}")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SIGIL QQUAPP public workflow sharing KQC manifest.")
    parser.add_argument("manifest", nargs="?", default="sigilbook/qquapp_public_workflow_sharing_v1.json")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    manifest = load_manifest(manifest_path)
    issues = validate_manifest(manifest)
    report = {"ok": not issues, "issues": issues, "manifest": str(manifest_path)}
    print(json.dumps(report, indent=2, sort_keys=True))

    if issues:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
