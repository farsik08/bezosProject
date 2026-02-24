from pathlib import Path

from fastapi.testclient import TestClient

from milestones.api import create_app


DATA = Path(__file__).resolve().parents[1] / "data" / "milestones"


def test_health():
    app = create_app(DATA)
    c = TestClient(app)
    r = c.get("/health")
    assert r.status_code == 200
    assert r.json()["ok"] is True


def test_stages_default_excludes_noisy():
    app = create_app(DATA)
    c = TestClient(app)
    r = c.get("/stages")
    assert r.status_code == 200
    stages = r.json()
    assert len(stages) == 10
    assert all(not s["is_noisy"] for s in stages)


def test_stages_include_noisy():
    app = create_app(DATA)
    c = TestClient(app)
    r = c.get("/stages?include_noisy=true")
    assert r.status_code == 200
    stages = r.json()
    assert len(stages) == 13


def test_stage_detail_hides_noisy_by_default():
    app = create_app(DATA)
    c = TestClient(app)
    r = c.get("/stages/noisy_alt_movements")
    # our noisy stage id fallback uses stem; should be hidden
    assert r.status_code == 404


def test_milestones_for_age():
    app = create_app(DATA)
    c = TestClient(app)
    r = c.get("/milestones?age_months=18")
    assert r.status_code == 200
    ms = r.json()
    assert len(ms) > 0
    assert all("stage_id" in m and "text" in m and "domain" in m for m in ms)
