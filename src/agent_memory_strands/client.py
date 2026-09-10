"""Construction of the Agent Memory client used by the tools.

The Agent Memory client lives in the ``surrealdb`` package, v3 alpha or later
(``pip install "surrealdb[memory]>=3.0.0b8"``).
It is imported lazily so that importing ``agent_memory_strands`` never requires a
configured environment, and so a missing dependency produces a clear message
rather than an import error at package load time.
"""

from __future__ import annotations

import os
from typing import Any

# Environment variables read by build_client when an argument is not supplied.
ENV_CONTEXT = "AGENT_MEMORY_CONTEXT"
ENV_ENDPOINT = "AGENT_MEMORY_ENDPOINT"
ENV_API_KEY = "AGENT_MEMORY_API_KEY"


def build_client(
    *,
    context: str | None = None,
    endpoint: str | None = None,
    api_key: str | None = None,
    timeout: float = 30.0,
    max_retries: int = 3,
) -> Any:
    """Build a synchronous Agent Memory client from arguments or the environment.

    Any argument left as ``None`` falls back to its environment variable:
    ``AGENT_MEMORY_CONTEXT``, ``AGENT_MEMORY_ENDPOINT`` and ``AGENT_MEMORY_API_KEY``.

    Args:
        context: Agent Memory context id, for example ``"acme-prod"``.
        endpoint: Agent Memory host URL, for example ``"https://api.agent-memory.example"``.
        api_key: Bearer token used to authenticate requests.
        timeout: Per-request timeout in seconds.
        max_retries: Retry attempts for idempotent operations.

    Returns:
        A ``surrealdb.Agent Memory`` instance.

    Raises:
        ImportError: If the ``surrealdb`` package is not installed.
        ValueError: If context, endpoint or api_key cannot be resolved.
    """
    context = context or os.getenv(ENV_CONTEXT)
    endpoint = endpoint or os.getenv(ENV_ENDPOINT)
    api_key = api_key or os.getenv(ENV_API_KEY)

    missing = [
        name
        for name, value in (
            (ENV_CONTEXT, context),
            (ENV_ENDPOINT, endpoint),
            (ENV_API_KEY, api_key),
        )
        if not value
    ]
    if missing:
        raise ValueError(
            "Agent Memory client configuration is incomplete. Provide it as arguments "
            "to build_client / agent_memory_tools, or set these environment variables: "
            + ", ".join(missing)
        )

    try:
        from surrealdb.memory import Memory
    except ImportError as exc:  # pragma: no cover - exercised only without surrealdb
        raise ImportError(
            "The 'surrealdb' package is required for the Agent Memory client. "
            "The Agent Memory client ships as an extra; install it with: "
            'pip install "surrealdb[memory]>=3.0.0b8"'
        ) from exc

    return Memory(
        context=context,
        endpoint=endpoint,
        api_key=api_key,
        timeout=timeout,
        max_retries=max_retries,
    )
