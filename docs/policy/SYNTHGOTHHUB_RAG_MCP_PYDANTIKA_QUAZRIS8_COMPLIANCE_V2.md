# SYNTHGOTHHUB RAG · MCP · PYDANTIKA · QUAZRIS8 Compliance Policy V2

Status: `ACTIVE_TYPED_WORKFLOW_POLICY`  
Supersedes: `SYNTHGOTHHUB_RAG_MCP_N8N_COMPLIANCE_V1`  
Canon: `PIORNALEGO_ES_CANON`

## Scope

This repository now stores canonical PYDANTIKA models, QUAZRIS8 gate definitions, fixtures, replay traces, and adapters. n8n exports are legacy migration inputs only.

## Canonical workflow package

```yaml
workflow_package:
  required:
    - pydantika_model
    - schema_version
    - discriminated_action_types
    - quazris8_gate_manifest
    - fixture_inputs
    - expected_outputs
    - failure_fixtures
    - provenance_contract
    - replay_metadata
    - credential_reference_policy
    - rollback_or_disable_path
```

## QUAZRIS8 promotion chain

```text
Q1_PROBE
-> Q2_DECLARE
-> Q3_TYPE
-> Q4_BOUND
-> Q5_EXECUTE
-> Q6_TRACE
-> Q7_VERIFY
-> Q8_CLOSE
```

No gate may be skipped. A failure is emitted as a typed obstruction preserving the original input, gate, validation errors, and provenance.

## Legacy n8n import

```yaml
legacy_n8n:
  canonical: false
  allowed:
    - parse_export
    - convert_to_pydantika_actions
    - preserve_graph_dependencies
    - preserve_failure_edges
    - emit_migration_trace
  rejected:
    - direct_execution_as_canonical_workflow
    - embedded_credentials
    - silent_node_coercion
    - workflow_success_as_certificate
```

## Cross-repository authority

- `sigilbook`: policy and typed knowledge authority.
- `sigil-workflows`: canonical PYDANTIKA/QUAZRIS8 model and fixture registry.
- `sigiln8n`: legacy migration surface.
- `SIGIL-QuoQuantum-LLM`: model and MCP consumer boundary.

## Seal

```text
PYDANTIKA types.
QUAZRIS8 gates.
Fixtures witness behavior.
Failures remain first-class.
Replay reconstructs execution.
n8n remains migration-only.
```
