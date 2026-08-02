import unittest

from scripts.validate_synthgothhub_projection import (
    EXPECTED_END_LINE,
    fixed_point,
    validate_document,
    validate_policy,
)

DOCUMENT = """projection SYNTHGOTHHUB_SIGIL_WORKFLOWS_PROJECTION_V1
author Jara Juana Bermejo-Vega / JJBV
source sigilbook#695@5f5d0f0b776d34077a22e897d8ec68cab6637d42
target jbermejovega/sigil-workflows
section SECTION_SIGIL_WORKFLOWS_PUBLIC
kernel SIGIL_PLURAL_UNIVERSAL_ABSTRAKTA_AESTHETIK_KERNEL_V1
pi PI:SYNTHGOTHHUB:COHERENT_SHEAF:CYTHON:V1
invariant READ_ONLY
invariant NO_WORKFLOW_DISPATCH
invariant NO_IDENTITY_TRANSPORT
invariant NO_PLURAL_COLLAPSE
invariant TRACE_PRESERVED
end SYNTHGOTHHUB_SIGIL_WORKFLOWS_PROJECTION_V1"""

POLICY = {
    "sources": {
        "sigilbook": {
            "pull_request": 695,
            "head": "5f5d0f0b776d34077a22e897d8ec68cab6637d42",
        },
        "sigil4cpython": {
            "pull_request": 8,
            "head": "99ddaa7d273f2f6c87affc985a1a721776344f50",
        },
        "aesthetik": {
            "pull_request": 20,
            "head": "ce4588f8108fc451279b6efb0e522a0798fa7a69",
        },
    },
    "permissions": {"contents": "read"},
    "forbidden": {
        "workflow_dispatch": True,
        "contents_write": True,
        "pull_requests_write": True,
        "oidc_write": True,
        "git_push": True,
        "merge": True,
    },
    "identity_transport": False,
    "plural_collapse": False,
}


class ProjectionTests(unittest.TestCase):
    def test_projection_and_policy_admit(self):
        self.assertEqual(validate_document(DOCUMENT), ())
        self.assertEqual(validate_policy(POLICY), ())
        self.assertEqual(fixed_point(DOCUMENT, POLICY), fixed_point(DOCUMENT, POLICY))

    def test_missing_end_rejects(self):
        self.assertIn(
            "EXACT_END_LINE_MISSING",
            validate_document(DOCUMENT.rsplit("\n", 1)[0]),
        )

    def test_duplicate_end_rejects(self):
        self.assertIn(
            "END_LINE_NOT_UNIQUE",
            validate_document(DOCUMENT + "\n" + EXPECTED_END_LINE),
        )

    def test_write_permission_rejects(self):
        bad = {**POLICY, "permissions": {"contents": "write"}}
        self.assertIn("PERMISSIONS_NOT_READ_ONLY", validate_policy(bad))


if __name__ == "__main__":
    unittest.main()
