import os
from dotenv import load_dotenv

load_dotenv()


def getenv(var_name: str):
    default_values = {
        "MODE": "production",
        "DATABASE_TYPE": "sqlite",
        "ALLOWLIST": "*",
        "ENCRYPTION_SECRET": "n0ne",
        "APP_NAME": "Magical Auth",
        "AUTH_PROVIDER": "magicalauth",
        "MAGIC_LINK_URL": "https://localhost:8507/",
        "LOG_LEVEL": "INFO",
        "LOG_FORMAT": "%(asctime)s | %(levelname)s | %(message)s",
        "UVICORN_WORKERS": 1,
        "DATABASE_NAME": (
            "./test" if os.getenv("DATABASE_TYPE", "sqlite") == "sqlite" else "postgres"
        ),
        "DATABASE_USER": "postgres",
        "DATABASE_PASSWORD": "postgres",
        "DATABASE_HOST": "notesdb",
        "DATABASE_PORT": "5432",
        "SELECTED_EHR": "None",
    }
    default_value = default_values[var_name] if var_name in default_values else None
    return os.getenv(var_name, default_value)
