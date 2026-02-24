from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, List, Tuple

from .models import Domain, Milestone, Stage

_STAGE_RE = re.compile(
    r"^(?P<num>\d{2})_(?P<title>[a-z0-9_]+)_(?P<min>\d+)-(?P<max>\d+)_months\.txt$",
    re.IGNORECASE,
)


def is_noisy_file(path: Path) -> bool:
    name = path.name.lower()
    if name.startswith("noisy_"):
        return True
    # content-based heuristics in case filenames change
    try:
        txt = path.read_text(encoding="utf-8", errors="ignore").lower()
    except Exception:
        return False
    noisy_markers = [
        "some sources",
        "differ substantially",
        "miracle",
        "detox",
        "cure",
        "specialized mobility training",
        "no longer considered",
    ]
    return any(m in txt for m in noisy_markers)


def parse_stage_from_filename(path: Path) -> Stage:
    m = _STAGE_RE.match(path.name)
    if not m:
        # fallback: treat as noisy/unknown stage
        return Stage(
            stage_id=path.stem,
            title=path.stem.replace("_", " "),
            min_months=0,
            max_months=0,
            filename=path.name,
            is_noisy=is_noisy_file(path),
        )
    title = m.group("title").replace("_", " ")
    return Stage(
        stage_id=m.group("num"),
        title=title,
        min_months=int(m.group("min")),
        max_months=int(m.group("max")),
        filename=path.name,
        is_noisy=is_noisy_file(path),
    )


_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def split_sentences(text: str) -> List[str]:
    text = re.sub(r"\s+", " ", text.strip())
    if not text:
        return []
    parts = _SENTENCE_SPLIT_RE.split(text)
    # normalize and drop very short fragments
    out: List[str] = []
    for p in parts:
        p = p.strip()
        if len(p) < 20:
            continue
        out.append(p)
    return out


def classify_domain(sentence: str) -> Domain:
    s = sentence.lower()

    # gross motor
    if any(k in s for k in ["walk", "crawl", "roll", "sit", "stand", "steps", "lift their heads", "mobility"]):
        return "gross_motor"
    # fine motor
    if any(k in s for k in ["grasp", "stack", "blocks", "scribble", "crayons", "spoon", "fine motor", "pincer"]):
        return "fine_motor"
    # language
    if any(k in s for k in ["coo", "babble", "words", "vocabulary", "talk", "requests", "language"]):
        return "language"
    # social / emotional
    if any(k in s for k in ["caregiver", "recognition", "imitation", "pretending", "joy", "frustration", "attention", "social"]):
        return "social_emotional"
    # sleep
    if "sleep" in s or "wake" in s:
        return "sleep"
    # cognitive
    if any(k in s for k in ["focus", "attention", "exploring", "curiosity", "learn", "problem"]):
        return "cognitive"

    return "other"


def extract_milestones(stage: Stage, text: str) -> List[Milestone]:
    sentences = split_sentences(text)
    return [Milestone(stage_id=stage.stage_id, text=sent, domain=classify_domain(sent)) for sent in sentences]


def load_stages_and_milestones(folder: Path) -> Tuple[List[Stage], List[Milestone]]:
    stages: List[Stage] = []
    milestones: List[Milestone] = []

    for path in sorted(folder.glob("*.txt")):
        stage = parse_stage_from_filename(path)
        stages.append(stage)
        text = path.read_text(encoding="utf-8", errors="ignore")
        milestones.extend(extract_milestones(stage, text))

    return stages, milestones
