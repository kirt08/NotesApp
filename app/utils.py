from dotenv import load_dotenv
from pathlib import Path
import os
import hashlib
 
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

DB_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

def to_hash(s : str) -> str:
    hashed = hashlib.sha256(s.encode()).hexdigest()
    return hashed