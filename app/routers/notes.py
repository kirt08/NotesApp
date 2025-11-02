from fastapi import APIRouter, HTTPException, Depends
from typing import List

from sqlalchemy.orm import Session

from database import get_db
from models import NoteBase, Note
from database_schemas import Users, Notes


router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/create")
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

        
@router.get("/show/{author_name}")
async def show_note_by_author_name(author_name : str, db : Session = Depends(get_db)) -> List:
    temp_user = db.query(Users).filter(Users.login == author_name).first()
    if not temp_user:
        raise HTTPException(status_code=404)
    return [{"title": note.title, "text": note.text} for note in temp_user.notes]