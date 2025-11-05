from fastapi import APIRouter, Depends, HTTPException
from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
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
    
    new_user =  Users(login = user.login, password = to_hash(user.password), hash_previous_commit = None)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"data": "successfully created"}

@router.post("/login")
async def login_user(user : UserBase, db : AsyncSession = Depends(get_db)) -> Dict:
    result = await db.execute(select(Users).filter(Users.login == user.login))
    saved_user = result.scalars().first()

    if not saved_user:
        return {"data": f"User: {user.login} was not found"}

    if to_hash(user.password) == saved_user.password:
        return {"data": "True"}
    else:
        return {"data": "False"}
    
@router.delete("/delete_user")
async def delete_user(user: UserBase, db : AsyncSession = Depends(get_db)) -> Dict:
    result = await db.execute(
        select(Users)
        .options(selectinload(Users.notes))
        .filter(Users.login == user.login)
    )
    temp_user = result.scalars().first()

    if not temp_user:
        return {"data": f"User {user.login} was not found"}
    
    if to_hash(user.password) != temp_user.password:
        return {"data": "Incorrect password"}

    for note in temp_user.notes:  
        await db.delete(note)

    await db.delete(temp_user)
    await db.commit()

    return {"data": f"User {temp_user.login} was successfully deleted"}

@router.delete("/delete_note")
async def delete_note(user : UserBase, db : AsyncSession = Depends(get_db)) -> Dict:
    result = await db.execute(
        select(Users)
        .options(selectinload(Users.notes))
        .filter(Users.login == user.login)
    )
    temp_user = result.scalars().first()

    if not temp_user:
        return {"data": f"User {user.login} was not found"}
    
    if to_hash(user.password) != temp_user.password:
        return {"data": "Incorrect password"}
    
    for note in temp_user.notes:  
        await db.delete(note)
    await db.commit()
    
    return {"data": f"Note of {user.login} was successfully deleted"}