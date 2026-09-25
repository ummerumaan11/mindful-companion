"""
Crisis detection: a simple, deliberately conservative keyword matcher.

This is NOT a clinical risk assessment tool. It exists as a hard safety net:
if any of these phrases appear, the app stops its normal conversational flow
entirely and shows crisis resources instead. It is intentionally biased
toward false positives (better to show resources unnecessarily than to miss
a real signal).
"""
import re

# Deliberately common, plain-language phrases a real user in crisis might type.
# This list is intentionally NOT exhaustive or clever — that's a feature, not
# a bug, for a portfolio project. A production system would use a properly
# validated classifier, not a keyword list.
CRISIS_PATTERNS = [
    r"\bkill myself\b",
    r"\bend my life\b",
    r"\bwant to die\b",
    r"\bwant to be dead\b",
    r"\bsuicid\w*\b",
    r"\bself[\s-]?harm\w*\b",
    r"\bhurt(ing)? myself\b",
    r"\bcut(ting)? myself\b",
    r"\bno reason to live\b",
    r"\bbetter off dead\b",
    r"\bcan'?t go on\b",
    r"\bdon'?t want to (be here|exist|live)\b",
]

_COMPILED = [re.compile(p, re.IGNORECASE) for p in CRISIS_PATTERNS]


def is_crisis_message(text: str) -> bool:
    if not text:
        return False
    return any(pattern.search(text) for pattern in _COMPILED)


CRISIS_RESPONSE = """
I'm really glad you told me. I'm not able to provide the support you need right now,
but please reach out to someone who can — you don't have to go through this alone.

**If you're in immediate danger, please call emergency services: 112 (India).**

If you'd like, you can also reach out to a trusted friend, family member, or doctor right now.
"""
