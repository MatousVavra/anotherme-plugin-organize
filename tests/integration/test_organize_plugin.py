"""Organize plugin integration tests (moved from the AnotherMe host repo,
tests/test_plugins/test_remaining_plugins.py)."""
import os
from pathlib import Path
from unittest.mock import patch

import pytest


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def client(make_client):
    return make_client()


# ===========================================================================
# Organize plugin
# ===========================================================================

def test_organize_plugin_listed(client):
    names = {p["name"] for p in client.get("/plugins").json()}
    assert "organize" in names


def test_organize_returns_suggestions(client):
    with patch("src.llm.organize", return_value="Suggestion: organize files by date."):
        resp = client.post("/plugins/organize", json={"instructions": "organize my vault"})
    assert resp.status_code == 200
    data = resp.json()
    assert "suggestions" in data
    assert "organize files by date" in data["suggestions"]
