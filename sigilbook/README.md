# SIGIL Public Workflow Sharing

This directory contains the SIGILBOOK-linked public sharing contract for
`jbermejovega/sigil-workflows`.

## QQUAPP Exact Chain

```text
jbermejovega/sigilbook
-> rulezero public workflow law
-> jbermejovega/sigil-workflows
-> developer repository
-> pull request review surface
-> KQC public sharing witness
```

## Use In A Developer Repository

1. Add the starter workflow `automation/sigil-kqc-public-sharing.yml` through the
   GitHub Actions workflow template UI or copy it into `.github/workflows/`.
2. Add a public manifest at `.sigil/workflows/public-sharing.json`.
3. Keep the manifest aligned with `qquapp_public_workflow_sharing_v1.json`.
4. Open a pull request so maintainers can review before merge.

The KQC rule rejects force transport, identity transport, secret transport,
direct upstream mutation, branch topology as authority, private payloads, and
unreviewed workflow installation.

## Local Check

```bash
python sigilbook/validate_qquapp_public_workflow_sharing.py sigilbook/qquapp_public_workflow_sharing_v1.json
```
