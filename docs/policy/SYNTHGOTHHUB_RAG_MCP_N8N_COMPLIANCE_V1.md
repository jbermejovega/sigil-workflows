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

## QuasarPi render/livecode package

A reusable package for `QUASARPI_PLURAL_TYPED_QUNOS_MIMBREPI_LAURELPI_RENDER_LIVECODE_RESOURCE_V1` is admissible only when it remains inactive and review-bounded by default.

```yaml
quasarpi_package:
  source_authority: jbermejovega/sigilbook
  required:
    - inactive_workflow_export
    - schema_version
    - provenance_fixture
    - plural_section_fixture
    - failure_fixture
    - no_credentials_fixture
    - stable_diffusion_plan_only_assertion
    - sonic_pi_source_only_assertion
    - no_repository_mutation_assertion
    - replay_metadata
  forbidden:
    - implicit_model_download
    - automatic_image_generation
    - automatic_audio_execution
    - hidden_external_call
    - direct_default_branch_write
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

Promotion is rejected when a workflow hides credentials, discards error states, mutates a repository without an explicit branch/PR boundary, omits provenance, collapses QUNOS plurality, or reports an exported plan as executed output.

## Cross-repository authority

- `sigilbook` is the typed knowledge and policy authority.
- `sigiln8n` executes optional n8n orchestration.
- `sigil-workflows` stores reusable workflow packages.
- `SIGIL-QuoQuantum-LLM` consumes the typed model/tool boundary.
- `stable-diffusion` is an optional visual render adapter, not authority.
- `sonic-pi` is an optional livecode adapter, not authority.

No repository silently overwrites another repository's source history, attribution, license, or default branch.

## Seal

```text
Workflow definitions are versioned.
Fixtures witness behavior.
Render and livecode adapters remain gated.
Failures remain first-class.
Replay metadata reconstructs execution.
PR review authorizes mutation.
PIORNALEGO ES CANON.
```
