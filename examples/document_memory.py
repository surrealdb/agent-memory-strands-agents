"""Ingest a document, then answer questions from it.

The agent uploads a short policy document into Agent Memory and then recalls over it.
Uploaded content becomes part of the same memory the agent searches at recall
time, so no separate retrieval pipeline is needed.

Prerequisites and setup match examples/quickstart.py.

Run:
    python examples/document_memory.py
"""

from strands import Agent

from agent_memory_strands import agent_memory_tools

POLICY = """
Expense policy, revision 4.
Meals are reimbursed up to 40 GBP per day.
Flights over 6 hours may be booked in premium economy.
Receipts must be submitted within 30 days of travel.
"""


def main() -> None:
    agent = Agent(tools=agent_memory_tools())

    agent(f"Upload this expense policy into memory so we can query it later:\n{POLICY}")

    print(agent("What is the daily meal reimbursement limit?"))
    print(agent("How long do I have to submit receipts?"))


if __name__ == "__main__":
    main()
