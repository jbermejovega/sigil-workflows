# QQUAPP Public Workflow Sharing V1

```yaml
QQUAPP_PUBLIC_WORKFLOW_SHARING_V1:
  status:
    canonical: true
    public_workflow_integration: true
    developer_sharing: true
    pull_request_only: true
    replay_safe: true
    trace_preserved: true
    pi_fixed: true
    no_force_move_transport: true
    no_identity_transport: true
    no_secret_transport: true
    kqc_required: true

  canonical_repository: jbermejovega/sigilbook
  public_workflow_repository: jbermejovega/sigil-workflows
  consumer_surface: other_developer_repositories
  sharing_mode: pull_request_to_other_developers
```

## Rule

`jbermejovega/sigil-workflows` is the public workflow integration and sharing
repository for SIGIL-aligned developer workflows. It distributes workflow
patterns by pull request and review, not by force-moving branches, secrets,
private SIGILBOOK material, or identity-bearing transport.

The repository is linked to `jbermejovega/sigilbook` by QQUAPP exact chain:

```yaml
qquapp_exact_chain:
  id: SIGILBOOK_SIGIL_WORKFLOWS_PUBLIC_SHARING_EXACT
  objects:
    - "0"
    - jbermejovega/sigilbook
    - rulezero_public_workflow_law
    - jbermejovega/sigil-workflows
    - developer_repository
    - pull_request_review_surface
    - kqc_public_sharing_witness
    - "0"
  maps:
    - include_rulezero
    - normalize_public_workflow
    - publish_template
    - propose_to_developer
    - review_pull_request
    - certify_kqc
  exact: true
```

## KQC Safety Rule For Sharing

A shared workflow is admissible only when all of these are true:

```yaml
kqc_public_sharing_rule:
  public_trace_only: true
  private_payload_embedded: false
  pull_request_only: true
  maintainer_review_required: true
  no_force_move_transport: true
  no_identity_transport: true
  no_secret_transport: true
  no_direct_upstream_mutation: true
  no_branch_topology_as_authority: true
  sigilbook_chain_declared: true
  qquapp_exact_chain_declared: true
  developer_can_review_before_merge: true
```

## KQC Workflow Invariant Rule: COMPU2526

`COMPU2526_ASSIGNMENT_REVIEW_INVARIANT_V1` binds the computational physics
assignment review starter workflow to the SigilBook public sharing rule.

```yaml
kqc_workflow_invariant_rules:
  - id: COMPU2526_ASSIGNMENT_REVIEW_INVARIANT_V1
    workflow_template: ci/compu2526-review.yml
    metadata_template: ci/properties/compu2526-review.properties.json
    public_sharing_admissible: true
    pull_request_review_required: true
    least_privilege_permissions:
      contents: read
    required_actions:
      - actions/checkout@v4
      - actions/setup-python@v5
    required_review_gates:
      - repository_manifest_report
      - python_syntax_py_compile
      - c_syntax_fsyntax_only
      - cpp_syntax_fsyntax_only
      - notebook_json_parse
      - large_notebook_warning
      - manual_science_review_trace
    forbidden_default_operations:
      - pytest
      - make check
      - make distcheck
      - jupyter nbconvert --execute
```

The rule preserves review safety: the workflow may smoke-check source and
notebook structure, but it must not turn expensive simulations, notebook
execution, package tests, or Make targets into default public review transport.

Rejected operations:

```yaml
rejected_operations:
  - force_push_as_release
  - reset_hard_as_public_transport
  - secret_or_token_in_manifest
  - hidden_private_sigilbook_rule
  - direct_upstream_mutation
  - identity_transport
  - unreviewed_workflow_installation
  - branch_topology_as_authority
  - expensive_simulation_as_default_review_gate
```

## Developer PR Contract

A PR from this repository to another developer repository should include:

- the workflow file being proposed
- the KQC public sharing manifest or a link to this descriptor
- explicit reviewer control before merge
- no secrets, credentials, tokens, private traces, or hidden authorization rules
- a replay-safe status trace from the workflow check

## Seal

```text
SIGILBOOK defines.
SIGIL-WORKFLOWS shares.
QQUAPP chains.
Developers review.
KQC gates.
No force move transport.
Typed invariants preserve review shape.
```
