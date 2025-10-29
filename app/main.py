from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import logging
logger = logging.getLogger("uvicorn.app.main")
logger.setLevel(logging.INFO)

import app.routes as routes
from app.persistence import init_db
from app.version import get_version

app = FastAPI(
    title = "calendar-tasks",
    version = get_version(),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

app.include_router(routes.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Recurring Appointments Calendar API! Use the /generate-calendar endpoint to generate a calendar file."
    }

init_db()