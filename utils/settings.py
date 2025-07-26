import os

from urllib.parse import quote

from dotenv import load_dotenv

load_dotenv(override=True)

DOT_HOST = str(os.environ['DOT_HOST'])
DOT_PORT = int(os.environ['DOT_PORT'])

DB_HOST = str(os.environ['DB_HOST'])
DB_PORT = int(os.environ['DB_PORT'])
DB_USER = str(os.environ['DB_USER'])
DB_PASS = quote(os.environ['DB_PASS'])
DB_NAME = str(os.environ['DB_NAME'])

REDIS_HOST = str(os.environ['REDIS_HOST'])
REDIS_PORT = int(os.environ['REDIS_PORT'])
REDIS_PASS = quote(os.environ['REDIS_PASS'])
REDIS_DB = int(os.environ['REDIS_DB'])

DB_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

REGISTRATION_ENABLED = (
    {"true": True, "false": False}
    .get(os.environ['REGISTRATION_ENABLED'])
)

if REGISTRATION_ENABLED is None:
    print(os.environ['REGISTRATION_ENABLED'])
    raise ValueError("REGISTRATION_ENABLED must be either true or false")
