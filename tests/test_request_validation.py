import pytest
from pydantic import ValidationError

from conftest import load_plugin_module


def test_instructions_max_length_rejected():
    mod = load_plugin_module()
    with pytest.raises(ValidationError):
        mod.OrganizeRequest(instructions="x" * 8001)


def test_instructions_empty_rejected():
    mod = load_plugin_module()
    with pytest.raises(ValidationError):
        mod.OrganizeRequest(instructions="")
