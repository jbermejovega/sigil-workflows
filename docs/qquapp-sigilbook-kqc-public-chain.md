# QQUAPP SIGILBOOK KQC Public Workflow Chain

## Purpose

`sigil-workflows` is the public workflow sharing surface for developers. `sigilbook` remains the canonical source for the PACATERMINAL, SIGILAPI, RuleZero, QQUAPP, and QUASARPI chain.

This package adds a preview starter workflow that downstream repositories can copy from GitHub Actions starter workflows without importing private authority, secrets, or write-token behavior.

## Exact Chain

```yaml
QQUAPP_SIGILBOOK_KQC_PUBLIC_CHAIN_V1:
  canonical_source:
    repo: jbermejovega/sigilbook
    pull_request: 44
    branch: codex/global-plural-mcp-workflow
    workflow: .github/workflows/mcp-django-uap-workflow.yml
  public_surface:
    repo: jbermejovega/sigil-workflows
    starter_workflow: automation/qquapp-sigilbook-kqc-chain.yml
    metadata: automation/properties/qquapp-sigilbook-kqc-chain.properties.json
  chain:
    - PACATERMINAL_MCP_DJANGO_UAP_WORKFLOW_V1
    - SIGILAPI_TYPESCRIPT_QQUAPP_PRESHEAF_INJECTION_V1
    - RULEZERO_CONTEXTUAL_GLUE_QQUAPP_QUASARPI_V1
    - QQUAPP_SIGILBOOK_KQC_PUBLIC_CHAIN_V1
```

## KQC Safety Rule

Public sharing is admissible only when the workflow keeps the canonical `sigilbook` chain visible and stays inside a read-only, replay-safe boundary.

The starter workflow enforces these safety conditions:

- `pull_request_target` is rejected.
- Secrets are not required.
- Token permissions are `contents: read`.
- Marketplace actions are not required for startup.
- Force-move transport patterns such as force push or hard reset are rejected.
- The chain witness is written to the GitHub Actions step summary.

This makes the public PR review surface safe for other developers: they can inspect the declared QQUAPP/SIGILBOOK chain and KQC policy without receiving privileged repository authority.

## Developer Use

In a downstream repository, create a new workflow from the GitHub Actions starter workflow catalog and choose `QQUAPP SIGILBOOK KQC Chain` while it is in preview review. The workflow can also be copied manually from `automation/qquapp-sigilbook-kqc-chain.yml`.

The default canonical chain is:

```text
https://github.com/jbermejovega/sigilbook/pull/44
```

When maintainers decide the template is ready for broad public visibility, remove the `preview` label from `automation/properties/qquapp-sigilbook-kqc-chain.properties.json` in a follow-up PR.
