# SIGIL PACAWEB Starter Workflow

`pages/sigil-pacaweb.yml` is a public GitHub Actions starter workflow for
repositories that publish a SIGIL/PACA-generated static web surface with GitHub
Pages.

## Expected Project Shapes

The starter workflow accepts one of three explicit project shapes:

```text
scripts/pacaweb_build.sh
pacaweb/index.html
public/index.html
```

If `scripts/pacaweb_build.sh` exists, the workflow calls it with:

```bash
bash scripts/pacaweb_build.sh "$PWD" "$PWD/build/pacaweb-deploy"
```

If no build script exists, it copies `pacaweb/` or `public/` only when that
directory already contains `index.html`. It fails fast when no publishable
surface is present.

## Generated Artifact

The workflow uploads:

```text
build/pacaweb-deploy
```

Required output:

```text
build/pacaweb-deploy/index.html
```

Optional output:

```text
build/pacaweb-deploy/deploy-manifest.json
```

When a deploy manifest is present, the workflow validates it with
`python -m json.tool` before uploading the Pages artifact.

## Public Sharing Contract

This workflow is intended for developer reuse. It keeps the deploy surface
explicit and avoids publishing a generated placeholder when a repository has not
declared a PACAWEB source.

```text
source must be explicit
artifact must contain index.html
deploy-manifest.json must parse when present
Pages URL is authority only after workflow success
```

## Repository Setup

After adding this workflow to a repository, enable:

```text
Settings -> Pages -> Build and deployment -> Source: GitHub Actions
```

Then run the workflow manually or push to the default branch.
