FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip

COPY pyproject.toml /app/pyproject.toml
COPY src /app/src
COPY data /app/data
COPY README.md /app/README.md

RUN pip install --no-cache-dir -e .

EXPOSE 8000

CMD ["uvicorn", "milestones.api:app", "--host", "0.0.0.0", "--port", "8000"]
