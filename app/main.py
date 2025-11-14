from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from routers.users import router as users_router
from routers.notes import router as notes_router
from routers.devs import router as devs_router
from routers.dolt import router as dolt_router

from database import create_db_and_tables

app = FastAPI()

@app.on_event("startup")
async def on_start():
    print("1")
    await create_db_and_tables()

app.include_router(users_router)
app.include_router(notes_router)
app.include_router(devs_router)
app.include_router(dolt_router)

origins = [
    "http://localhost:5500",  
    "http://127.0.0.1:5500", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       
    allow_credentials=True,      
    allow_methods=["*"],         
    allow_headers=["*"], 
)
