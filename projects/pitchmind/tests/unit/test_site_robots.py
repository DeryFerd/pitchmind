import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "packages", "site-auditor"))

from pitchmind_site.robots import check_robots

ROBOTS_ALLOW = """
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /
"""

ROBOTS_BLOCK = """
User-agent: *
Disallow: /
"""


def test_robots_allows_ai_bots():
    result = check_robots(ROBOTS_ALLOW, fetched_ok=True)
    assert result.severity == "pass"
    assert result.score == 100


def test_robots_blocks_ai_bots():
    result = check_robots(ROBOTS_BLOCK, fetched_ok=True)
    assert result.severity == "fail"
    assert result.score == 0
