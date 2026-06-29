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


def load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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

    encoded = json.dumps(manifest, sort_keys=True).lower()
    for token in FORBIDDEN_PAYLOAD_TOKENS:
        if token in encoded and token not in {item.lower() for item in manifest.get("forbidden_payload_tokens", ())}:
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
