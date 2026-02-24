# Milestones

A small, self-contained project that:

- Loads milestone text files from `data/milestones/`
- Parses each stage (age range) from the filename
- Extracts milestone sentences and classifies them into domains
- Flags clearly *noisy* sources (kept in the dataset, excluded by default)
- Exposes a FastAPI service + a simple CLI

## Run the API

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .

uvicorn milestones.api:app --reload
```

Open:
- `GET /health`
- `GET /stages`
- `GET /stages/{stage_id}`
- `GET /milestones?age_months=12`

## Run the CLI

```bash
python -m milestones list-stages
python -m milestones milestones 18
```

## Tests

```bash
pip install pytest httpx
pytest
```

## Milestones checklist (implemented)

- [x] Load milestone files from `data/milestones/`
- [x] Parse age/stage ranges from filenames (e.g., `12–18 months`)
- [x] Split content into individual milestone items
- [x] Classify each milestone into a domain (gross motor, fine motor, language, social-emotional, cognitive, sleep, other)
- [x] Detect and flag noisy sources (`noisy_*.txt`) and exclude by default (still queryable)
- [x] FastAPI endpoints + CLI
- [x] Automated tests (parser, store behavior, API)

## How I verified correctness

1. **Unit tests:** `pytest` covers:
   - filename/stage parsing
   - sentence extraction and normalization
   - noisy-file filtering behavior
   - API responses and default query behavior
2. **Manual sanity checks:** ran the API locally and queried a few ages (`/milestones?age_months=...`) to confirm:
   - stage selection is correct
   - noisy sources are excluded by default
   - returned items are non-empty and well-formed

## Local dev setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
uvicorn milestones.api:app --reload
```

## Run with Docker

```bash
docker build -t milestones:latest .
docker run --rm -p 8000:8000 milestones:latest
```

## CI

A GitHub Actions workflow is included at `.github/workflows/ci.yml` and runs tests on pushes and pull requests.
