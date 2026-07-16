"""Shared defaults for the ingestion and query pipelines."""
from dotenv import load_dotenv

load_dotenv()

DEFAULT_DOCS_DIR = "./data"
DEFAULT_DB_PATH = "./chroma_db"
DEFAULT_COLLECTION = "documents"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

MODEL = "gpt-5-mini"
