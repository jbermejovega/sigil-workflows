"""Validate the read-only SynthGothHub workflow-package projection."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any

PROJECTION_ID = "SYNTHGOTHHUB_SIGIL_WORKFLOWS_PROJECTION_V1"
EXPECTED_END_LINE = f"end {PROJECTION_ID}"
SIGILBOOK_PR = 695
SIGILBOOK_PAYLOAD_HEAD = "5f5d0f0b776d34077a22e897d8ec68cab6637d42"
SIGIL4CPYTHON_PR = 8
SIGIL4CPYTHON_HEAD = "99ddaa7d273f2f6c87affc985a1a721776344f50"
AESTHETIK_PR = 20
AESTHETIK_HEAD = "ce4588f8108fc451279b6efb0e522a0798fa7a69"
PI_REF = "PI:SYNTHGOTHHUB:COHERENT_SHEAF:CYTHON:V1"


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def validate_document(document: str) -> tuple[str, ...]:
    errors: list[str] = []
    lines = document.rstrip("\n").splitlines()
    if not lines or lines[-1] != EXPECTED_END_LINE:
        errors.append("EXACT_END_LINE_MISSING")
    if document.count(EXPECTED_END_LINE) != 1:
        errors.append("END_LINE_NOT_UNIQUE")
    required = {
        f"projection {PROJECTION_ID}",
        "author Jara Juana Bermejo-Vega / JJBV",
        f"source sigilbook#{SIGILBOOK_PR}@{SIGILBOOK_PAYLOAD_HEAD}",
        "target jbermejovega/sigil-workflows",
        f"pi {PI_REF}",
        "invariant READ_ONLY",
        "invariant NO_WORKFLOW_DISPATCH",
        "invariant NO_IDENTITY_TRANSPORT",
        "invariant NO_PLURAL_COLLAPSE",
        "invariant TRACE_PRESERVED",
    }
    errors.extend(f"MISSING_LINE:{line}" for line in sorted(required - set(lines)))
    return tuple(errors)


def validate_policy(policy: dict[str, Any]) -> tuple[str, ...]:
    errors: list[str] = []
    expected_sources = {
        "sigilbook": {"pull_request": SIGILBOOK_PR, "head": SIGILBOOK_PAYLOAD_HEAD},
        "sigil4cpython": {"pull_request": SIGIL4CPYTHON_PR, "head": SIGIL4CPYTHON_HEAD},
        "aesthetik": {"pull_request": AESTHETIK_PR, "head": AESTHETIK_HEAD},
    }
    if policy.get("sources") != expected_sources:
        errors.append("SOURCE_COVER_DRIFT")
    if policy.get("permissions") != {"contents": "read"}:
        errors.append("PERMISSIONS_NOT_READ_ONLY")
    forbidden = policy.get("forbidden", {})
    for key in (
        "workflow_dispatch",
        "contents_write",
        "pull_requests_write",
        "oidc_write",
        "git_push",
        "merge",
    ):
        if forbidden.get(key) is not True:
            errors.append(f"FORBIDDEN_EFFECT_NOT_DECLARED:{key}")
    if policy.get("identity_transport") is not False:
        errors.append("IDENTITY_TRANSPORT")
    if policy.get("plural_collapse") is not False:
        errors.append("PLURAL_COLLAPSE")
    return tuple(errors)


def fixed_point(document: str, policy: dict[str, Any]) -> str:
    return sha256(
        canonical_json({"document": document, "policy": policy, "pi_ref": PI_REF}).encode(
            "utf-8"
        )
    ).hexdigest()


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    document = (root / "projections" / f"{PROJECTION_ID}.sigil").read_text(
        encoding="utf-8"
    )
    policy = json.loads(
        (root / "policies" / "synthgothhub-coherent-fixed-point-v1.json").read_text(
            encoding="utf-8"
        )
    )
    errors = (*validate_document(document), *validate_policy(policy))
    result = {
        "projection_id": PROJECTION_ID,
        "state": "ADMIT" if not errors else "REJECT",
        "errors": errors,
        "fixed_point_sha256": fixed_point(document, policy),
        "runtime_executed": False,
        "repository_mutated": False,
        "final_kapsyla": False,
    }
    print(canonical_json(result))
    return 0 if not errors else 3


if __name__ == "__main__":
    raise SystemExit(main())
