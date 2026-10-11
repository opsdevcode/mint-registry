# mint-registry

Static community catalog for Mint integrations.

This repository is JSON only. There is no server, database, credential
store, or hosted registry service. Discovery does not install or execute.

Records use `mint.catalog-records/v0`. Official GitHub Release
coordinates for `mint-integration-local` and `mint-integration-github`
include artifact digest, manifest digest, tag, and commit SHA.

```bash
git clone https://github.com/opsdevcode/mint-registry.git
# after the language ADR/cache lands:
mint integrations update --project . --registry ./mint-registry
mint integrations search sandbox --project .
```

`update --registry` copies `records/v0.json` into
`.mint/catalog-records.json`. It does not pip, download, or execute.

Canonical catalog snapshots are GitHub Releases of this repository.
Pin a release tag or commit SHA. There is no `latest` alias, no
`/releases/latest` pin, and no integration PyPI.

Apache-2.0.
