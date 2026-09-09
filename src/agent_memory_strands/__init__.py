"""AgentMemory agent memory as tools for the Strands Agents SDK.

Give a Strands agent persistent memory backed by AgentMemory:

    from strands import Agent
    from agent_memory_strands import agent_memory_tools

    agent = Agent(tools=agent_memory_tools())
    agent("Remember that our launch date is 2026-09-01.")
    print(agent("When do we launch?"))
"""

from __future__ import annotations

from .client import build_client
from .tools import TOOL_NAMES, agent_memory_tools

__all__ = ["agent_memory_tools", "build_client", "TOOL_NAMES", "__version__"]

__version__ = "0.1.0"
