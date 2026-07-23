# n8n → PYDANTIKA → QUAZRIS8 Migration Glue V1

Canonical workflow packages are PYDANTIKA models plus QUAZRIS8 gate manifests.

Legacy n8n exports may be imported only as migration fixtures. Conversion must preserve node order, dependency edges, failure branches, credential references, side-effect classes, provenance, and replay metadata.

```text
n8n export
-> migration fixture
-> PYDANTIKA model
-> QUAZRIS8 gate manifest
-> typed workflow package
```
