import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "packages", "harness"))

from pitchmind_harness import AgentHarness, BudgetExhausted, CircuitOpen


@pytest.mark.asyncio
async def test_agent_harness_budget_exhausted():
    harness = AgentHarness(budget_usd=0.01)

    async def cheap():
        return "ok"

    await harness.execute(cheap, cost_estimate=0.005)

    with pytest.raises(BudgetExhausted):
        await harness.execute(cheap, cost_estimate=0.01)


@pytest.mark.asyncio
async def test_agent_harness_circuit_breaker():
    harness = AgentHarness(budget_usd=10.0, circuit_failure_threshold=2)

    async def fail():
        raise RuntimeError("boom")

    for _ in range(2):
        with pytest.raises(RuntimeError):
            await harness.execute(fail, cost_estimate=0.0)

    assert harness.circuit_open
    with pytest.raises(CircuitOpen):
        await harness.execute(fail, cost_estimate=0.0)
