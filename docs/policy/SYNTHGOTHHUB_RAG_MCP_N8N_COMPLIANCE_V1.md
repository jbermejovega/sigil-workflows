# SYNTHGOTHHUB RAG · MCP · n8n Compliance Policy V1

Status: `ACTIVE_WORKFLOW_POLICY`  
Canon: `PIORNALEGO_ES_CANON`

## Scope

This repository stores reusable workflow definitions and validation assets for the SYNTHGOTHHUB RAG/MCP/n8n stack.

## Required package for each workflow

```yaml
workflow_package:
  required:
    - workflow_export
    - schema_version
    - fixture_inputs
    - expected_outputs
    - failure_fixture
    - provenance_contract
    - replay_metadata
    - credential_policy
    - rollback_or_disable_path
```

## Promotion gates

```text
draft
-> schema_valid
-> fixture_tested
-> failure_tested
-> replayable
-> reviewed
-> production_candidate
```

Promotion is rejected when a workflow hides credentials, discards error states, mutates a repository without an explicit branch/PR boundary, or omits provenance.

## Cross-repository authority

- `sigilbook` is the typed knowledge and policy authority.
- `sigiln8n` executes n8n orchestration.
- `sigil-workflows` stores reusable workflow packages.
- `SIGIL-QuoQuantum-LLM` consumes the typed model/tool boundary.

No repository silently overwrites another repository's source history or license.

## Seal

```text
Workflow definitions are versioned.
Fixtures witness behavior.
Failures remain first-class.
Replay metadata reconstructs execution.
PR review authorizes mutation.
```
