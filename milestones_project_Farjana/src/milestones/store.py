from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Dict, List, Optional

from .models import Milestone, Stage
from .parse import load_stages_and_milestones


class MilestoneStore:
    """Loads milestone text files and provides query helpers."""

    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        stages, milestones = load_stages_and_milestones(self.data_dir)
        self._stages: Dict[str, Stage] = {s.stage_id: s for s in stages}
        self._milestones_by_stage: Dict[str, List[Milestone]] = {}
        for m in milestones:
            self._milestones_by_stage.setdefault(m.stage_id, []).append(m)

    @property
    def stages(self) -> List[Stage]:
        return sorted(self._stages.values(), key=lambda s: (s.min_months, s.max_months, s.stage_id))

    def get_stage(self, stage_id: str) -> Optional[Stage]:
        return self._stages.get(stage_id)

    def milestones_for_stage(self, stage_id: str, include_noisy: bool = False) -> List[Milestone]:
        stage = self.get_stage(stage_id)
        if not stage:
            return []
        if stage.is_noisy and not include_noisy:
            return []
        return list(self._milestones_by_stage.get(stage_id, []))

    def stages_for_age(self, age_months: int, include_noisy: bool = False) -> List[Stage]:
        res: List[Stage] = []
        for s in self.stages:
            if not include_noisy and s.is_noisy:
                continue
            if s.min_months <= age_months <= s.max_months:
                res.append(s)
        return res

    def milestones_for_age(self, age_months: int, include_noisy: bool = False) -> List[Milestone]:
        ms: List[Milestone] = []
        for s in self.stages_for_age(age_months, include_noisy=include_noisy):
            ms.extend(self.milestones_for_stage(s.stage_id, include_noisy=include_noisy))
        return ms

    def to_dict(self) -> dict:
        return {
            "stages": [asdict(s) for s in self.stages],
            "milestones": {
                sid: [asdict(m) for m in self.milestones_for_stage(sid, include_noisy=True)]
                for sid in self._stages.keys()
            },
        }
