from dotenv import load_dotenv
from pathlib import Path
import os
 
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

DB_URL = os.getenv("SQLALCHEMY_DATABASE_URL")


import hashlib
def hash(s : str) -> str:
    hashed = hashlib.sha256(s.encode()).hexdigest()
    return hashed