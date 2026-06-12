"""robots.txt AI bot access checks."""

from __future__ import annotations

from pitchmind_site.types import CheckResult

AI_BOTS = ["GPTBot", "ClaudeBot", "PerplexityBot", "anthropic-ai", "Google-Extended"]


def _parse_robots(content: str) -> dict[str, list[str]]:
    """Return user-agent -> list of disallow paths."""
    agents: dict[str, list[str]] = {}
    current: str | None = None
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.lower().startswith("user-agent:"):
            current = line.split(":", 1)[1].strip()
            agents.setdefault(current, [])
        elif line.lower().startswith("disallow:") and current:
            path = line.split(":", 1)[1].strip()
            agents[current].append(path)
    return agents


def _bot_allowed(agents: dict[str, list[str]], bot: str) -> bool:
    disallows = agents.get(bot, [])
    if "*" in agents:
        disallows = disallows + agents["*"]
    if not disallows:
        return True
    return not any(d == "/" or d == "/*" for d in disallows)


def check_robots(content: str, *, fetched_ok: bool) -> CheckResult:
    if not fetched_ok:
        return CheckResult(
            check_type="robots",
            severity="partial",
            score=50,
            message="robots.txt not found — bots may crawl by default",
            recommendation="Add robots.txt explicitly allowing AI bots you want indexed.",
        )

    agents = _parse_robots(content)
    blocked = [bot for bot in AI_BOTS if not _bot_allowed(agents, bot)]
    allowed_count = len(AI_BOTS) - len(blocked)

    if allowed_count == len(AI_BOTS):
        return CheckResult(
            check_type="robots",
            severity="pass",
            score=100,
            message="robots.txt allows major AI crawlers",
            recommendation=None,
        )
    if allowed_count > 0:
        return CheckResult(
            check_type="robots",
            severity="partial",
            score=50,
            message=f"Some AI bots blocked: {', '.join(blocked)}",
            recommendation="Allow GPTBot, ClaudeBot, and PerplexityBot unless you intentionally block them.",
        )
    return CheckResult(
        check_type="robots",
        severity="fail",
        score=0,
        message=f"AI crawlers blocked: {', '.join(blocked)}",
        recommendation="Remove Disallow: / for AI bots in robots.txt to improve GEO visibility.",
    )


def is_pitchmind_blocked(content: str) -> bool:
    agents = _parse_robots(content)
    return not _bot_allowed(agents, "PitchMindBot") and not _bot_allowed(agents, "*")
