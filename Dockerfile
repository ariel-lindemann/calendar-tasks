FROM python:3.13.1-slim

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt && \
    python3 -m pip install "fastapi[standard]"

COPY app/ .
CMD ["fastapi", "run", "calendar-tasks.py", "--port", "8000"]
