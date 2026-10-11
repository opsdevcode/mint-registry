#!/usr/bin/env python3
"""Public /integrations fetch contract. No network."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.json"
RECORDS = ROOT / "records" / "v0.json"
DIRECTORY = ROOT / "docs" / "directory.md"
INDEX_SCHEMA = ROOT / "schemas" / "mint.registry-index.v0.json"
RECORDS_SCHEMA = ROOT / "schemas" / "mint.catalog-records.v0.json"
PAGES = ROOT / "opsdevcode-release.json"


class DirectoryFetchTests(unittest.TestCase):
    def test_index_is_anonymous_github_release_contract(self) -> None:
        index = json.loads(INDEX.read_text(encoding="utf-8"))
        self.assertEqual(index["schema"], "mint.registry-index/v0")
        self.assertIs(index["hostedService"], False)
        self.assertEqual(index["canonical"], "github-release")
        self.assertEqual(
            index["fetch"]["releaseDownload"],
            "https://github.com/opsdevcode/mint-registry/releases/download/{tag}/",
        )
        self.assertEqual(
            index["fetch"]["raw"],
            "https://raw.githubusercontent.com/opsdevcode/mint-registry/{tag}/",
        )
        identities = {item["identity"] for item in index["entries"]}
        self.assertIn("local.sandbox.ensure_marker", identities)
        self.assertIn("repo.github.plan", identities)

    def test_index_entries_match_verified_records(self) -> None:
        index = json.loads(INDEX.read_text(encoding="utf-8"))
        records = json.loads(RECORDS.read_text(encoding="utf-8"))
        by_id = {item["identity"]: item for item in records["integrations"]}
        for entry in index["entries"]:
            record = by_id[entry["identity"]]
            self.assertEqual(entry["artifactDigest"], record["artifactDigest"])
            self.assertEqual(entry["manifestDigest"], record["manifestDigest"])
            self.assertEqual(entry["commit"], record["release"]["commit"])
            self.assertEqual(entry["tag"], record["release"]["tag"])
            self.assertEqual(entry["origin"], "github")

    def test_schemas_and_directory_doc_exist(self) -> None:
        for path in (INDEX_SCHEMA, RECORDS_SCHEMA, DIRECTORY):
            self.assertTrue(path.is_file(), path)
        text = DIRECTORY.read_text(encoding="utf-8")
        self.assertIn("/integrations", text)
        self.assertIn("v0.2.0-alpha.0", text)
        self.assertIn("does not rewrite that homepage", text)
        self.assertNotIn("mint apply", text.lower())

    def test_pages_role_stays_none(self) -> None:
        contract = json.loads(PAGES.read_text(encoding="utf-8"))
        self.assertEqual(contract["downstream"]["pages"]["role"], "none")
        self.assertFalse((ROOT / "Dockerfile").exists())


if __name__ == "__main__":
    unittest.main()
