"""Data schema and synthetic dataset helpers for CircleMatch."""

import json
import re
from .claude import add_user_message, chat


def _extract_json_text(response):
    if not response:
        return response

    response = response.strip()

    # Strip markdown code fences if present.
    fence_match = re.search(r"```(?:json)?\n(.*?)\n```", response, re.S)
    if fence_match:
        response = fence_match.group(1).strip()

    # Find the first JSON object or array start.
    start_pos = None
    for index, ch in enumerate(response):
        if ch in "[{":
            start_pos = index
            break
    if start_pos is None:
        return response

    opening = response[start_pos]
    closing = "]" if opening == "[" else "}"

    depth = 0
    in_string = False
    escape = False
    for index in range(start_pos, len(response)):
        ch = response[index]
        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue

        if ch == opening:
            depth += 1
        elif ch == closing:
            depth -= 1
            if depth == 0:
                return response[start_pos : index + 1].strip()

    # Fallback: return the entire trimmed response if we couldn't extract a complete structure.
    return response


def _normalize_dataset_parsed(parsed, batch_id):
    if isinstance(parsed, list):
        return parsed

    if isinstance(parsed, dict):
        # Accept top-level wrappers like {"users": [...]} or {"data": [...]}.
        if "users" in parsed and isinstance(parsed["users"], list):
            return parsed["users"]
        if "data" in parsed and isinstance(parsed["data"], list):
            return parsed["data"]

        # Accept a single-key object whose value is the list we want.
        if len(parsed) == 1:
            value = next(iter(parsed.values()))
            if isinstance(value, list):
                return value

    raise ValueError(f"Batch {batch_id} expected JSON array, got {type(parsed).__name__}")


def _validate_dataset_response(response, n_users, batch_id):
    response_text = _extract_json_text(response)
    try:
        parsed = json.loads(response_text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Batch {batch_id} response is not valid JSON: {exc}\nResponse:\n{response}"
        ) from exc

    parsed = _normalize_dataset_parsed(parsed, batch_id)

    if len(parsed) != n_users:
        raise ValueError(
            f"Batch {batch_id} expected {n_users} users, but got {len(parsed)}"
        )

    for index, item in enumerate(parsed, start=1):
        if not isinstance(item, dict):
            raise ValueError(
                f"Batch {batch_id} item {index} is not an object: {type(item).__name__}"
            )
        if "user_id" not in item or not isinstance(item["user_id"], str):
            raise ValueError(f"Batch {batch_id} item {index} missing valid user_id")

        answers = item.get("answers")
        alternate_answers = item.get("onboarding_responses")
        if answers is None and alternate_answers is not None:
            answers = alternate_answers
            item["answers"] = answers
            item.pop("onboarding_responses", None)

        if not isinstance(answers, dict):
            raise ValueError(
                f"Batch {batch_id} item {index} missing valid answers object"
            )

    return parsed


def generate_dataset(n_users=25, batch_id=1):
    """Generate a synthetic dataset of user answers to onboarding questions."""
    prompt = f"""
Generate a synthetic dataset of {n_users} users answering onboarding questions for a small-group matching system called CircleMatch.

Return valid JSON only.

Each user should feel realistic and different. Do not make everyone emotionally polished or self-aware.

Generate users across these patterns:
- newcomers to the city
- busy professionals
- introverts
- extroverts
- recently single people
- people seeking activity friends
- people seeking deeper emotional connection
- people who want low-pressure social plans
- people who want consistent weekly community
- people who are shy at first
- people who prefer structured plans
- people who are spontaneous
- people with limited availability
- people with broad availability

Include natural variation:
- some answers should be short
- some should be detailed
- some should be casual
- some should be slightly vague
- some should contain mixed needs, e.g. “I want deeper friendship but I’m also busy”
- some should mention constraints like location, work schedule, social anxiety, being new to Toronto, or preferring small groups

Do NOT generate harmful, extreme, or crisis-level content.
Do NOT make the answers sound like they were written by the same person.
    Keep each answer concise and natural, roughly 1-3 sentences per question.

    Return an array of objects with:
    - user_id: string, format "batch-{batch_id}-user-001"
    - answers: object mapping each exact question to the user's free-text answer
    Use the exact key name "answers" for the question responses object.
1. What kind of connection are you looking for right now?
2. What has been missing socially in your life lately?
3. What kind of group would genuinely feel good to you?
4. What pace of connection feels comfortable to you?
5. In a new group, what helps you feel comfortable?
6. What role do you naturally play in a group when you feel at ease?
7. What kinds of activities do you actually enjoy doing with other people?
8. What times / days are generally easiest for you to meet?
"""
    messages = []
    add_user_message(messages, prompt)
    response = chat(
        messages,
        system="You generate realistic synthetic user research data. Return valid JSON only."
    )
    return _validate_dataset_response(response, n_users, batch_id)
