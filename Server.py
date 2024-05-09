from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoints import Auth
import logging
import os

app = FastAPI(
    title="MagicalAuth",
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
    level=os.environ.get("LOGLEVEL", "INFO"),
    format="%(asctime)s | %(levelname)s | %(message)s",
)

app.include_router(Auth.router)
