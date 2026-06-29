# SIGILBOOK KQC Rule

`ci/sigilbook-kqc-rule.yml` is a public starter workflow for repositories that
want a small, explicit SIGILBOOK KQC gate before sharing workflows with other
developers.

The rule is intentionally minimal and portable. It uses only Python from the
GitHub Actions runner and does not install external dependencies.

## What It Checks

The workflow scans tracked text, manifest, and trace files:

```text
*.md
*.txt
*.yml
*.yaml
*.json
*.jsonl
*.toml
```

It requires the public rule surface to include these markers:

```text
sigilbook
kqc
trace or synk
certificate or proof_gate
no transport or no_transport
```

It also parses tracked JSON and JSONL files. A malformed manifest or trace file
fails the gate.

## Why This Exists

Public workflow sharing needs a small rule that keeps identity and deploy claims
bounded. This starter workflow gives downstream developers a reusable check for
the core SIGILBOOK KQC contract:

```text
no trace => no authority
no certificate => no release
no transport
public sharing requires explicit source and witness
```

## How To Use

Add the starter workflow to a repository through the GitHub Actions new workflow
UI, then add or update documentation/manifests so the repository explicitly
states its KQC markers.

Typical files that can satisfy the rule:

```text
README.md
docs/kqc/SIGILBOOK_KQC_RULE.md
registry/*.yml
synk/*.jsonl
```

The workflow runs on pushes and pull requests to the repository default branch.

## Review Notes

This rule is a guard, not a final certificate. Human review still decides
whether the trace, certificate, and no-transport claims are meaningful for a
specific repository.
