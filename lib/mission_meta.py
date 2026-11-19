from __future__ import annotations

from typing import Any


def _meta(data: Any) -> dict:
    if not isinstance(data, dict):
        return {}
    meta = data.get("meta")
    return meta if isinstance(meta, dict) else {}


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def lab_badges(lab: Any) -> list[str]:
    if not isinstance(lab, dict):
        return []
    badges = []
    for key, label in (("tier", "TIER"), ("family", "FAMILY"),
                       ("difficulty", "LEVEL")):
        value = lab.get(key)
        if isinstance(value, str) and value.strip():
            badges.append(f"{label}:{value.strip()}")
    env = lab.get("environment")
    if isinstance(env, dict):
        for key, label in (("name", "ENV"), ("boundary", "BOUNDARY"),
                           ("privilege", "PRIV"), ("network", "NET")):
            value = env.get(key)
            if isinstance(value, str) and value.strip():
                badges.append(f"{label}:{value.strip()}")
    return badges


def format_lab_badges(lab: Any) -> str | None:
    badges = lab_badges(lab)
    return " · ".join(badges) if badges else None


def chapter_badges(data: Any) -> list[str]:
    meta = _meta(data)
    badges = []
    for key, label in (("track", "TRACK"), ("phase", "PHASE")):
        value = meta.get(key)
        if isinstance(value, str) and value.strip():
            badges.append(f"{label}:{value.strip()}")
    return badges


def format_chapter_badges(data: Any) -> str | None:
    badges = chapter_badges(data)
    return " · ".join(badges) if badges else None


def tinker_preview(lab: Any, workspace_dir: Any = None) -> str:
    if not isinstance(lab, dict):
        return "Tinker experiment: no lab metadata available."
    lines = ["Tinker experiment:"]
    commands = lab.get("commands")
    cmd = commands.get("tinker", "") if isinstance(commands, dict) else ""
    lines.append(f"  command: {cmd.strip() or '(none declared)'}")
    if workspace_dir is not None:
        lines.append(f"  cwd: {workspace_dir}")
    env = lab.get("environment")
    if isinstance(env, dict):
        timeout = env.get("timeout_s")
        if isinstance(timeout, (int, float)):
            lines.append(f"  timeout_s: {timeout}")
    badges = format_lab_badges(lab)
    if badges:
        lines.append(f"  context: {badges}")
    expected = lab.get("expected_observation")
    if isinstance(expected, str) and expected.strip():
        lines.append(f"  expected: {expected.strip()}")
    artifacts = _string_list(lab.get("artifacts"))
    if artifacts:
        lines.append(f"  artifacts: {', '.join(artifacts)}")
    return "\n".join(lines)


def interleaved_label(check: Any) -> str | None:
    if not isinstance(check, dict):
        return None
    source = check.get("from_chapter")
    if not isinstance(source, str) or not source.strip():
        return None
    block = check.get("from_block")
    if isinstance(block, str) and block.strip():
        return f"Review from {source}/{block}"
    return f"Review from {source}"


def _as_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def suggest_next(chapters: list[dict]) -> dict | None:
    candidates = []
    for chapter in chapters:
        if not isinstance(chapter, dict) or not chapter.get("has_pack"):
            continue
        if str(chapter.get("status", "")).lower() == "mastered":
            continue
        candidates.append(chapter)
    if not candidates:
        return None
    for chapter in candidates:
        if _as_int(chapter.get("due")) > 0:
            return chapter
    return candidates[0]
