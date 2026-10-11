# Public `/integrations` directory fetch

The language GitHub Pages site owns `/integrations` UI. This repository
does not host a registry service, does not enable GitHub Pages, and
does not rewrite that homepage.

Render the directory from **real verified records** in a GitHub Release
snapshot. Anonymous HTTP. Pin a tag. Never `/releases/latest`, never
`main`, never PyPI, never a marketplace.

## Pin (current public snapshot)

| Field | Value |
| --- | --- |
| Tag | `v0.2.0-alpha.0` |
| Commit | `30d523034560f3fc7ebfdc1ae76f598c5949b93f` |
| Release | https://github.com/opsdevcode/mint-registry/releases/tag/v0.2.0-alpha.0 |
| `index.json` sha256 | `bbf5f62eb87921d005444c3d4d7093e9284a6fc562a62544fdb8f8b63a2fd82e` |
| `records/v0.json` (asset `v0.json`) sha256 | `a039554b3b979ed780fdd7cdd28e5a89b48ca75b4f08e8a3bd3929f6ae3f85a5` |

After a later Release Please snapshot, update the pin to that tag and
re-check `SHA256SUMS`. Do not invent records.

## Anonymous HTTP (canonical)

GitHub Release assets (no auth):

```text
https://github.com/opsdevcode/mint-registry/releases/download/v0.2.0-alpha.0/index.json
https://github.com/opsdevcode/mint-registry/releases/download/v0.2.0-alpha.0/v0.json
https://github.com/opsdevcode/mint-registry/releases/download/v0.2.0-alpha.0/SHA256SUMS
```

`v0.json` on the release is the bytes of `records/v0.json` in the tag.

## Browser CORS (language Pages)

`github.com/releases/download/...` redirects without
`Access-Control-Allow-Origin`. Browser `fetch` from
`https://opsdevcode.github.io/specmint-language/` should use the same
tag on `raw.githubusercontent.com` (CORS `*`), then verify SHA-256
against the pinned `SHA256SUMS`:

```text
https://raw.githubusercontent.com/opsdevcode/mint-registry/v0.2.0-alpha.0/index.json
https://raw.githubusercontent.com/opsdevcode/mint-registry/v0.2.0-alpha.0/records/v0.json
```

Build-time fetch in `specmint-language` CI may use the release-download
URLs instead; those remain canonical.

## Index contract

`index.json` schema `mint.registry-index/v0` (`schemas/mint.registry-index.v0.json`):

- `hostedService` is `false`
- `canonical` is `github-release`
- `fetch.releaseDownload` / `fetch.raw` are `{tag}` templates
- `entries[]` are the official identities (`local.sandbox.ensure_marker`,
  `repo.github.plan`) with release commit, tag, and digests

Records schema: `schemas/mint.catalog-records.v0.json`.

## What the language site must not do

- Rewrite the docs homepage as the directory
- Call a hosted registry API
- Install, pip, or execute on discovery
- Show unverified or unpublished artifacts
