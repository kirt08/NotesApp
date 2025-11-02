from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models import UserBase, User
from database_schemas import Users
from utils import to_hash

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/create")
async def create_user(user : UserBase, db : AsyncSession = Depends(get_db)) -> dict:
    if (await db.execute(
        select(Users).filter(Users.login == user.login))
    ).scalars().first():
        raise HTTPException(status_code=409, detail="Login already exists")
    
    new_user =  Users(login = user.login, password = to_hash(user.password))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"data": "successfully created"}

@router.post("/login")
async def login_user(user : UserBase, db : AsyncSession = Depends(get_db)) -> dict:
    result = await db.execute(select(Users).filter(Users.login == user.login))
    saved_user = result.scalars().first()

    if to_hash(user.password) == saved_user.password:
        return {"data": "True"}
    else:
        return {"data": "False"}