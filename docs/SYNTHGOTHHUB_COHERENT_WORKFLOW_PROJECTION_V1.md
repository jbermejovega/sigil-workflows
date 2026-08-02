# SYNTHGOTHHUB_COHERENT_WORKFLOW_PROJECTION_V1

**Author/owner:** Jara Juana Bermejo-Vega / JJBV  
**Canonical source:** `jbermejovega/sigilbook` PR #695 payload `3eaa72173eba1f91627c80b5e8359adeb140994e`  
**CPython projection:** `jbermejovega/sigil4cpython` PR #8 head `a422e2622895dd94193340173942f0e075a5891a`  
**Aesthetik projection:** `jbermejovega/universal-abstrakta-plural-aesthetik` PR #20 head `09598fb67ba92883b4bd0ca35b6681253073db73`  
**Canon:** `PIORNALEGO_ES_CANON`

## Scope

This package is the read-only workflow projection of the SynthGothHub coherent
fixed point.

```text
sigilbook canonical coherent section
→ SIGIL4CPython dependency-free/Cython boundary
→ universal abstrakta plural aesthetik projection
→ sigil-workflows read-only policy
→ exact end-line validation
→ deterministic workflow-package fixed point
```

The repository remains a workflow/package projection. It does not become the
canonical semantic kernel, absorb another repository's identity, dispatch a
workflow, push a branch or merge a pull request.

## Exact end line

The projection document must terminate with exactly one occurrence of:

```text
end SYNTHGOTHHUB_SIGIL_WORKFLOWS_PROJECTION_V1
```

Missing, duplicated or nonterminal end lines reject validation.

## Permission policy

```yaml
permissions:
  contents: read
forbidden:
  workflow_dispatch: true
  contents_write: true
  pull_requests_write: true
  oidc_write: true
  git_push: true
  merge: true
identity_transport: false
plural_collapse: false
```

The `forbidden` booleans assert prohibitions; they do not request those effects.

## Local verification

```yaml
python_compile: PASS
dependency_free_unittest: 4 passed
projection_end_line_exact: true
source_cover_exact: true
permissions_read_only: true
fixed_point_deterministic: true
runtime_executed: false
repository_mutated: false
final_kapsyla: false
```

The hosted workflow is intentionally read-only, uses SHA-pinned checkout and
setup actions, disables persisted checkout credentials, and contains no
`workflow_dispatch` trigger. Hosted validation is not claimed green until
GitHub Actions actually executes it.

`SOURCE BOUND · READ ONLY · TRACE PRESERVED · Π FIXED · PIORNALEGO ES CANON`
