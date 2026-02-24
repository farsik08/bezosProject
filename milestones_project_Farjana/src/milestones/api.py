from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from .store import MilestoneStore


class StageOut(BaseModel):
    stage_id: str
    title: str
    min_months: int
    max_months: int
    filename: str
    is_noisy: bool


class MilestoneOut(BaseModel):
    stage_id: str
    text: str
    domain: str


def create_app(data_dir: Optional[Path] = None) -> FastAPI:
    data_dir = Path(data_dir) if data_dir else Path(__file__).resolve().parents[2] / "data" / "milestones"
    store = MilestoneStore(data_dir)

    app = FastAPI(title="Milestones API", version="0.1.0")

    @app.get("/health")
    def health():
        return {"ok": True}

    @app.get("/stages", response_model=List[StageOut])
    def list_stages(include_noisy: bool = Query(False)):
        stages = [s for s in store.stages if include_noisy or not s.is_noisy]
        return stages

    @app.get("/stages/{stage_id}")
    def stage_detail(stage_id: str, include_noisy: bool = Query(False)):
        stage = store.get_stage(stage_id)
        if not stage:
            raise HTTPException(status_code=404, detail="stage not found")
        if stage.is_noisy and not include_noisy:
            raise HTTPException(status_code=404, detail="stage not found")
        return {
            "stage": StageOut(**stage.__dict__),
            "milestones": [MilestoneOut(**m.__dict__) for m in store.milestones_for_stage(stage_id, include_noisy=True)],
        }

    @app.get("/milestones", response_model=List[MilestoneOut])
    def milestones(age_months: int = Query(..., ge=0, le=60), include_noisy: bool = Query(False)):
        ms = store.milestones_for_age(age_months, include_noisy=include_noisy)
        return [MilestoneOut(**m.__dict__) for m in ms]

    return app


app = create_app()
