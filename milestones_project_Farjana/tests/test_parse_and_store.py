from pathlib import Path

from milestones.parse import parse_stage_from_filename, load_stages_and_milestones
from milestones.store import MilestoneStore


DATA = Path(__file__).resolve().parents[1] / "data" / "milestones"


def test_stage_filename_parsing():
    p = DATA / "06_early_toddlerhood_12-18_months.txt"
    s = parse_stage_from_filename(p)
    assert s.stage_id == "06"
    assert s.min_months == 12
    assert s.max_months == 18
    assert s.is_noisy is False


def test_load_counts_and_noisy_detection():
    stages, milestones = load_stages_and_milestones(DATA)
    assert len(stages) == 13
    noisy = [s for s in stages if s.is_noisy]
    assert len(noisy) == 3
    # ensure each stage produced at least one milestone sentence
    by_stage = {}
    for m in milestones:
        by_stage.setdefault(m.stage_id, 0)
        by_stage[m.stage_id] += 1
    assert all(by_stage[s.stage_id] > 0 for s in stages)


def test_store_default_excludes_noisy_milestones():
    store = MilestoneStore(DATA)
    # noisy stages should return empty milestones unless included
    noisy_ids = [s.stage_id for s in store.stages if s.is_noisy]
    assert noisy_ids
    for sid in noisy_ids:
        assert store.milestones_for_stage(sid) == []
        assert len(store.milestones_for_stage(sid, include_noisy=True)) > 0


def test_store_query_by_age():
    store = MilestoneStore(DATA)
    # 13 months should match 12-18
    stages = store.stages_for_age(13)
    assert any(s.stage_id == "06" for s in stages)
    ms = store.milestones_for_age(13)
    assert len(ms) > 0
