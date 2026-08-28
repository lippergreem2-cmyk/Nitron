"""
NITRON SKILL REGISTRY

Turns learned knowledge into reusable capabilities.

A capability contains:
    - what Nitron learned
    - what Nitron can do with it
    - evidence supporting the capability
    - confidence
"""

import json
import os
import re
from datetime import datetime


SKILLS_FILE = os.path.join(
    os.path.dirname(__file__),
    "skills.json"
)


def _load():
    if not os.path.exists(SKILLS_FILE):
        return {}

    try:
        with open(
            SKILLS_FILE,
            "r",
            encoding="utf-8"
        ) as f:
            data = json.load(f)

        return data if isinstance(data, dict) else {}

    except Exception:
        return {}


def _save(data):
    tmp = SKILLS_FILE + ".tmp"

    with open(
        tmp,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )

    os.replace(
        tmp,
        SKILLS_FILE
    )


def normalize(name):
    name = str(name).strip().lower()
    name = re.sub(r"\s+", " ", name)
    return name


def _words(text):
    return re.findall(
        r"[a-zA-Z0-9_+#.-]+",
        str(text).lower()
    )


def register(
    name,
    description="",
    abilities=None,
    prerequisites=None,
    confidence=0.5,
    evidence=None,
    handlers=None,
    capability_type="knowledge",
    input_schema=None
):
    skills = _load()

    key = normalize(name)

    existing = skills.get(
        key,
        {}
    )

    old_abilities = (
        existing.get("abilities", [])
        if isinstance(existing, dict)
        else []
    )

    old_evidence = (
        existing.get("evidence", [])
        if isinstance(existing, dict)
        else []
    )

    old_handlers = (
        existing.get("handlers", [])
        if isinstance(existing, dict)
        else []
    )

    new_handlers = handlers or []

    skills[key] = {
        "name": str(name).strip(),

        "description": (
            description
            or existing.get(
                "description",
                ""
            )
        ),

        "abilities": sorted(
            set(
                old_abilities
                + (abilities or [])
            )
        ),

        "prerequisites": sorted(
            set(
                (
                    existing.get(
                        "prerequisites",
                        []
                    )
                    if isinstance(existing, dict)
                    else []
                )
                + (prerequisites or [])
            )
        ),

        "confidence": max(
            0.0,
            min(
                1.0,
                float(confidence)
            )
        ),

        "evidence": list(
            dict.fromkeys(
                old_evidence
                + (evidence or [])
            )
        ),

        "handlers": list(
            dict.fromkeys(
                old_handlers
                + new_handlers
            )
        ),

        "capability_type": (
            str(
                capability_type
                or existing.get(
                    "capability_type",
                    "knowledge"
                )
            ).strip()
        ),

        "input_schema": (
            input_schema
            if isinstance(input_schema, dict)
            else existing.get(
                "input_schema",
                {}
            )
        ),

        "learned_at": (
            existing.get(
                "learned_at"
            )
            if isinstance(existing, dict)
            and existing.get("learned_at")
            else datetime.utcnow().isoformat()
        ),

        "updated_at":
            datetime.utcnow().isoformat()
    }

    _save(skills)

    return skills[key]


def learn_skill(
    name,
    description="",
    abilities=None,
    evidence=None,
    handlers=None,
    capability_type="knowledge",
    input_schema=None
):
    """
    Register a skill as learned.

    Repeated successful learning increases confidence.
    """

    skills = _load()

    key = normalize(name)

    old = skills.get(key)

    if old:
        confidence = min(
            1.0,
            float(
                old.get(
                    "confidence",
                    0.5
                )
            ) + 0.10
        )
    else:
        confidence = 0.60

    return register(
        name=name,
        description=description,
        abilities=abilities,
        confidence=confidence,
        evidence=evidence,
        handlers=handlers,
        capability_type=capability_type,
        input_schema=input_schema
    )


def has_skill(
    name,
    minimum_confidence=0.5
):
    skill = get_skill(name)

    if not skill:
        return False

    return (
        float(
            skill.get(
                "confidence",
                0
            )
        )
        >= minimum_confidence
    )


def get_skill(name):
    return _load().get(
        normalize(name)
    )


def list_skills():
    return list(
        _load().values()
    )


def find_for_task(task):
    """
    Find learned capabilities relevant to a task.

    Matching is intentionally strict:
    - Exact capability names are strongest.
    - Multi-word capabilities require meaningful word overlap.
    - Description/ability text does not create a match by itself.
    - Broad capabilities such as "Python" cannot beat a more
      appropriate exact capability merely because Python appears
      somewhere in the request.
    """

    task_text = str(task).lower().strip()
    task_words = set(_words(task_text))

    matches = []

    for skill in _load().values():

        if not isinstance(skill, dict):
            continue

        name = str(skill.get("name", "")).strip()
        if not name:
            continue

        name_lower = name.lower()
        name_words = set(_words(name_lower))

        if not name_words:
            continue

        confidence = float(
            skill.get("confidence", 0)
        )

        score = 0

        # --------------------------------------------------
        # EXACT CAPABILITY NAME
        # --------------------------------------------------

        if name_lower in task_text:
            score += 1000

        # --------------------------------------------------
        # WORD MATCHING
        # --------------------------------------------------

        overlap = task_words & name_words

        if not overlap:
            # Do NOT match a skill merely because one of its
            # description/ability words happens to occur in
            # the user's request.
            continue

        # A single-word skill such as "Python" requires the
        # actual word "python" in the request.
        if len(name_words) == 1:
            score += 500

        # Multi-word skills require meaningful overlap.
        else:
            overlap_ratio = (
                len(overlap) / len(name_words)
            )

            # Require at least half of the capability name
            # to appear in the request.
            if overlap_ratio < 0.5:
                continue

            score += len(overlap) * 300

            # Strong bonus for matching the whole capability.
            if overlap_ratio == 1.0:
                score += 700

        # --------------------------------------------------
        # CAPABILITY TYPE PRIORITY
        # --------------------------------------------------
        # When the request is clearly programming-related,
        # prefer a learned programming capability over generic
        # knowledge entries such as "Python" or "Python program".

        capability_type = str(
            skill.get("capability_type", "")
        ).strip().lower()

        programming_words = {
            "programming",
            "program",
            "code",
            "coding",
            "software",
            "script",
            "project",
            "build",
            "debug",
            "test",
            "analyze",
            "write",
            "create",
        }

        if (
            capability_type == "programming"
            and task_words & programming_words
        ):
            score += 900

        # --------------------------------------------------
        # CONFIDENCE
        # --------------------------------------------------

        score += int(100 * confidence)

        matches.append(
            (
                score,
                skill
            )
        )

    # --------------------------------------------------
    # CAPABILITY TYPE PRIORITY
    # --------------------------------------------------
    # When a learned executable capability matches the task,
    # prefer it over broad knowledge skills such as "Python".
    #
    # This prevents:
    #   "build a Python project"
    #   "analyze Python code"
    #   "write a Python program"
    #
    # from being routed to generic knowledge instead of the
    # learned programming capability.

    programming_matches = [
        item
        for item in matches
        if str(
            item[1].get(
                "capability_type",
                ""
            )
        ).strip().lower() == "programming"
    ]

    if programming_matches:
        matches = programming_matches

    matches.sort(
        key=lambda item: (
            item[0],
            float(
                item[1].get(
                    "confidence",
                    0
                )
            )
        ),
        reverse=True
    )

    return [
        skill
        for _, skill in matches
    ]

def best_for_task(task):
    matches = find_for_task(
        task
    )

    return (
        matches[0]
        if matches
        else None
    )


def capability_report():

    skills = list_skills()

    return {
        "total_skills":
            len(skills),

        "skills":
            skills,

        "average_confidence": (
            sum(
                float(
                    s.get(
                        "confidence",
                        0
                    )
                )
                for s in skills
            )
            / len(skills)
            if skills
            else 0
        )
    }


if __name__ == "__main__":

    print(
        json.dumps(
            capability_report(),
            indent=2,
            ensure_ascii=False
        )
    )
