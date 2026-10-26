FROM python:3.12-slim

WORKDIR /app
RUN pip install --no-cache-dir uv
COPY pyproject.toml requirements.txt ./
RUN uv sync --no-dev
COPY src ./src
COPY scripts ./scripts
ENV PATH="/app/.venv/bin:$PATH" PYTHONPATH="/app/src"
CMD ["python", "scripts/train.py"]
