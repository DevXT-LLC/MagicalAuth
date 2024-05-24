# uvicorn Server:app --port 12437 --workers 4
# streamlit run UI.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoints import Auth
from Globals import getenv
import logging
import os

app = FastAPI(
    title=getenv("APP_NAME"),
    description="A magical authentication system.",
    version="0.0.1",
    docs_url="/",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logging.basicConfig(
    level=getenv("LOGLEVEL"),
    format="%(asctime)s | %(levelname)s | %(message)s",
)

app.include_router(Auth.router)
