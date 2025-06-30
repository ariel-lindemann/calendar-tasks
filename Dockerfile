FROM python:3.13.5-slim

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt && \
    python3 -m pip install "fastapi[standard]"

COPY app/ app/
COPY frontend/ frontend/
CMD ["fastapi", "run", "app/calendar-tasks.py", "--port", "8000"]
