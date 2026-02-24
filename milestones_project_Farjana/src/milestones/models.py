from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Domain = Literal["gross_motor", "fine_motor", "language", "social_emotional", "cognitive", "sleep", "other"]


@dataclass(frozen=True)
class Stage:
    """A developmental stage sourced from a single text file."""

    stage_id: str
    title: str
    min_months: int
    max_months: int
    filename: str
    is_noisy: bool


@dataclass(frozen=True)
class Milestone:
    """A single extracted milestone sentence."""

    stage_id: str
    text: str
    domain: Domain
