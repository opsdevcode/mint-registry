#!/usr/bin/env python3
"""Validate static mint-registry JSON. No network, no install."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_NAMES = {
    "Dockerfile",
    "docker-compose.yml",
    "credentials.json",
    "secrets.json",
}
SECRET_KEYS = frozenset(
    {"password", "token", "secret", "pat", "api_key", "authorization", "private_key"}
)


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def walk_keys(value: object) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            lowered = str(key).lower()
            if lowered in SECRET_KEYS:
                fail(f"remove secret-shaped field {key}")
            walk_keys(item)
    elif isinstance(value, list):
        for item in value:
            walk_keys(item)


def main() -> int:
    for name in FORBIDDEN_NAMES:
        if (ROOT / name).exists():
            fail(f"remove {name}; mint-registry is static JSON only")
    records_path = ROOT / "records" / "v0.json"
    index_path = ROOT / "index.json"
    records = json.loads(records_path.read_text(encoding="utf-8"))
    index = json.loads(index_path.read_text(encoding="utf-8"))
    walk_keys(records)
    walk_keys(index)
    if records.get("schema") != "mint.catalog-records/v0":
        fail("records/v0.json schema must be mint.catalog-records/v0")
    if index.get("schema") != "mint.registry-index/v0":
        fail("index.json schema must be mint.registry-index/v0")
    if index.get("records") != "records/v0.json":
        fail("index.json records must point at records/v0.json")
    dumped = json.dumps(records) + json.dumps(index)
    if "pypi.org" in dumped.lower() and "not PyPI" not in dumped:
        fail("canonical coordinates must be GitHub Releases, not PyPI")
    if '"latest"' in dumped:
        fail("records must not use a latest alias")
    integrations = records.get("integrations")
    if not isinstance(integrations, list) or len(integrations) < 2:
        fail("records/v0.json needs official local and github integrations")
    identities = {item.get("identity") for item in integrations}
    if "local.sandbox.ensure_marker" not in identities:
        fail("missing local.sandbox.ensure_marker github record")
    if "repo.github.plan" not in identities:
        fail("missing repo.github.plan github record")
    for item in integrations:
        if item.get("origin") != "github":
            fail(f"{item.get('identity')} origin must be github")
        if item.get("executionSupport") == "privileged":
            fail(f"{item.get('identity')} must not be privileged in the registry")
        phases = item.get("phases") or []
        if "execute" in phases:
            fail(f"{item.get('identity')} must not list execute")
        digest = str(item.get("artifactDigest", ""))
        manifest = str(item.get("manifestDigest", ""))
        if not digest.startswith("sha256:") or not manifest.startswith("sha256:"):
            fail(f"{item.get('identity')} needs sha256 digests")
        release = item.get("release") or {}
        commit = str(release.get("commit", ""))
        if len(commit) != 40:
            fail(f"{item.get('identity')} release.commit must be a 40-character SHA")
        tag = str(release.get("tag", ""))
        if tag == "latest":
            fail(f"{item.get('identity')} must not use latest")
    print("mint-registry records ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
