from pydantic import BaseModel, Field
from typing import Annotated, Optional

class UserBase(BaseModel):
    login : Annotated[str, Field(..., min_length=1, max_length=64)]
    password : Annotated[str, Field(..., min_length=1, max_length=64)]

class User(UserBase):
    id : Annotated[int, Field(...)]
    hash_previous_commit : Annotated[Optional[str], Field(...)]

    class Config:
        from_attributes = True


class NoteBase(BaseModel):
    title : Annotated[str, Field(..., min_length=4)]
    text : str
    author_name : str

class NoteUpdate(BaseModel):
    title : Annotated[str, Field(..., min_length=4)]
    text : str
    
class Note(NoteBase):
    id : Annotated[int, Field(...)]

    class Config:
        from_attributes = True