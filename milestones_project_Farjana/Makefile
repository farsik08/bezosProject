PY=python

.PHONY: install test run docker-build docker-run

install:
	$(PY) -m pip install -e ".[dev]"

test:
	pytest

run:
	uvicorn milestones.api:app --reload

docker-build:
	docker build -t milestones:latest .

docker-run:
	docker run --rm -p 8000:8000 milestones:latest
