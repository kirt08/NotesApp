from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from database import get_db
from models import UserBase, User
from database_schemas import Users
from utils import to_hash

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/create")
async def create_user(user : UserBase, db : Session = Depends(get_db)) -> dict:
    if db.query(Users).filter(Users.login == user.login).first():
        raise HTTPException(status_code=409, detail="Login already exists")
    
    new_user =  Users(login = user.login, password = to_hash(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"data": "successfully created"}

@router.post("/login")
async def login_user(user : UserBase, db : Session = Depends(get_db)) -> dict:
    saved_user = db.query(Users).filter(Users.login == user.login).first()
    if to_hash(user.password) == saved_user.password:
        return {"data": "True"}
    else:
        return {"data": "False"}