FROM python:3.10.14-slim

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt && \
    python3 -m pip install "fastapi[standard]"

COPY calendar-tasks.py .
CMD ["fastapi", "run", "calendar-tasks.py", "--port", "8000"]
