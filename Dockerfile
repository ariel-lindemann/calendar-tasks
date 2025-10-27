FROM python:3.13.5-slim

RUN apt-get update && apt-get install -y curl && apt-get clean
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

COPY uv.lock .
COPY pyproject.toml .
COPY app/ app/
COPY frontend/ frontend/
RUN uv sync

CMD [".venv/bin/fastapi", "run", "app/calendar-tasks.py", "--port", "8000"]
