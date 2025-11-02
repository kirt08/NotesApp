from fastapi import FastAPI

from sqlalchemy.orm import Session

from routers.users import router as users_router
from routers.notes import router as notes_router

from database import init_db

app = FastAPI()
app.include_router(users_router)
app.include_router(notes_router)

init_db()




