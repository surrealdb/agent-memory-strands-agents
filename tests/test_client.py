"""Tests for build_client configuration resolution.

These avoid importing the real surrealdb client by monkeypatching the lazy
import inside build_client, so they run without the surrealdb package.
"""

from __future__ import annotations

import sys
import types

import pytest

from agent_memory_strands import build_client
from agent_memory_strands.client import ENV_API_KEY, ENV_CONTEXT, ENV_ENDPOINT


@pytest.fixture
def fake_surrealdb(monkeypatch):
    """Install a fake 'surrealdb.memory' exposing a recording Memory class.

    The client is imported as ``from surrealdb.memory import Memory``, so the
    stub has to be a submodule and be registered in ``sys.modules`` under its
    dotted name - a bare attribute on a fake ``surrealdb`` is not importable.
    """
    captured = {}

    class Memory:
        def __init__(self, **kwargs):
            captured.update(kwargs)

    memory_module = types.ModuleType("surrealdb.memory")
    memory_module.Memory = Memory

    package = types.ModuleType("surrealdb")
    package.memory = memory_module

    monkeypatch.setitem(sys.modules, "surrealdb", package)
    monkeypatch.setitem(sys.modules, "surrealdb.memory", memory_module)
    return captured


def _clear_env(monkeypatch):
    for name in (ENV_CONTEXT, ENV_ENDPOINT, ENV_API_KEY):
        monkeypatch.delenv(name, raising=False)


def test_build_from_arguments(monkeypatch, fake_surrealdb):
    _clear_env(monkeypatch)
    build_client(context="acme", endpoint="https://api.example", api_key="secret")
    assert fake_surrealdb["context"] == "acme"
    assert fake_surrealdb["endpoint"] == "https://api.example"
    assert fake_surrealdb["api_key"] == "secret"
    assert fake_surrealdb["timeout"] == 30.0
    assert fake_surrealdb["max_retries"] == 3


def test_build_from_environment(monkeypatch, fake_surrealdb):
    monkeypatch.setenv(ENV_CONTEXT, "env-context")
    monkeypatch.setenv(ENV_ENDPOINT, "https://env.example")
    monkeypatch.setenv(ENV_API_KEY, "env-key")
    build_client()
    assert fake_surrealdb["context"] == "env-context"
    assert fake_surrealdb["endpoint"] == "https://env.example"
    assert fake_surrealdb["api_key"] == "env-key"


def test_arguments_take_precedence_over_environment(monkeypatch, fake_surrealdb):
    monkeypatch.setenv(ENV_CONTEXT, "env-context")
    monkeypatch.setenv(ENV_ENDPOINT, "https://env.example")
    monkeypatch.setenv(ENV_API_KEY, "env-key")
    build_client(context="explicit")
    assert fake_surrealdb["context"] == "explicit"
    assert fake_surrealdb["endpoint"] == "https://env.example"


def test_missing_config_raises_listing_all_gaps(monkeypatch):
    _clear_env(monkeypatch)
    with pytest.raises(ValueError) as exc:
        build_client()
    message = str(exc.value)
    assert ENV_CONTEXT in message
    assert ENV_ENDPOINT in message
    assert ENV_API_KEY in message
