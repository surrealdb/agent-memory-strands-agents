"""Quickstart: give a Strands agent memory backed by Agent Memory.

The agent stores a fact in one turn and recalls it in the next.

Prerequisites:
    pip install "agent-memory-strands-agents[bedrock]"

    export AGENT_MEMORY_ENDPOINT="https://api.agent-memory.example"
    export AGENT_MEMORY_API_KEY="your-bearer-token"
    export AGENT_MEMORY_CONTEXT="acme-prod"

Amazon Bedrock is the default Strands model provider, so also configure AWS
credentials (for example with the AWS CLI) before running this.

Run:
    python examples/quickstart.py
"""

from strands import Agent

from agent_memory_strands import agent_memory_tools


def main() -> None:
    agent = Agent(tools=agent_memory_tools())

    agent("Remember that we signed a contract with Meditech Solutions for 1.2M GBP.")

    answer = agent("What is the value of the Meditech Solutions contract?")
    print(answer)


if __name__ == "__main__":
    main()
