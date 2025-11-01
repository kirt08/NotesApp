from fastapi import FastAPI, Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session

from database import engine, Base
from models import UserBase, User, NoteBase, Note
from schemas import Users, Notes

from utils import hash

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

@app.post("/create_user")
async def create_user(user : UserBase, db : Session = Depends(get_db)) -> dict:
    if db.query(Users).filter(Users.login == user.login).first():
        raise HTTPException(status_code=409, detail="Login already exists")
    
    new_user =  Users(login = user.login, password = hash(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"data": "successfully created"}

@app.post("/login_user")
async def login_user(user : UserBase, db : Session = Depends(get_db)) -> dict:
    saved_user = db.query(Users).filter(Users.login == user.login).first()
    if hash(user.password) == saved_user.password:
        return {"data": "True"}
    else:
        return {"data": "False"}
    
@app.post("/create_note")
async def create_note(note : NoteBase, db : Session = Depends(get_db)) -> dict:
    user = db.query(Users).filter(Users.login == note.author_name).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    temp_author_id = db.query(Users).filter(Users.login == note.author_name).first()

    if db.query(Notes).filter(Notes.author_id == temp_author_id.id).first():
        raise HTTPException(status_code=409, detail="You can have only one note")
    
    new_note = Notes(title = note.title, text = note.text, author_id = temp_author_id.id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return {"data": "successfully created"}

        
@app.get("/show_note/{author_name}")
async def show_note_by_author_name(author_name : str, db : Session = Depends(get_db)) -> List:
    temp_user = db.query(Users).filter(Users.login == author_name).first()
    if not temp_user:
        raise HTTPException(status_code=404)
    return [{"title": note.title, "text": note.text} for note in temp_user.notes]

