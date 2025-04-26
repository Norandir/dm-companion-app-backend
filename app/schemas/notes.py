from pydantic import BaseModel
from typing import Optional

# For reading a note
class Note(BaseModel):
    id: int
    title: str
    content: Optional[str]
    campaign_id: Optional[int]

    class Config:
        orm_mode = True

# For creating a new note
class NoteCreate(BaseModel):
    title: str
    content: Optional[str] = None
    campaign_id: Optional[int] = None

# For updating a note
class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
